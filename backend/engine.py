from __future__ import annotations

import random
from datetime import datetime
from typing import Dict, Iterable, List, Tuple

from .models import Combination, Exercise, ExerciseOption, State, Unit


COMPATIBLE_TEMPLATES: Tuple[str, ...] = (
    "structure_position+lieu",
    "sujet+verbe+objet",
)


DEFAULT_SEED_UNITS: Tuple[Dict[str, object], ...] = (
    {
        "phrase": "je suis à",
        "translation": "I am at",
        "unit_type": "structure_position",
        "difficulty": 1,
        "language_from": "fr",
        "language_to": "en",
        "tags": ["structure_position"],
    },
    {
        "phrase": "maison",
        "translation": "home",
        "unit_type": "lieu",
        "difficulty": 1,
        "language_from": "fr",
        "language_to": "en",
        "tags": ["lieu"],
    },
    {
        "phrase": "je",
        "translation": "I",
        "unit_type": "sujet",
        "difficulty": 1,
        "language_from": "fr",
        "language_to": "en",
        "tags": ["sujet"],
    },
    {
        "phrase": "mange",
        "translation": "eat",
        "unit_type": "verbe",
        "difficulty": 1,
        "language_from": "fr",
        "language_to": "en",
        "tags": ["verbe"],
    },
    {
        "phrase": "du riz",
        "translation": "rice",
        "unit_type": "objet",
        "difficulty": 1,
        "language_from": "fr",
        "language_to": "en",
        "tags": ["objet"],
    },
)


def _has_tag(unit: Unit, tag: str) -> bool:
    return tag in (unit.tags or []) or unit.unit_type == tag


def _combine_text(parts: Iterable[str]) -> str:
    return " ".join(piece.strip() for piece in parts if piece).strip()


def _combine_translation(parts: Iterable[str]) -> str:
    translations = [p.strip() for p in parts if p]
    return " ".join(translations)


def _respect_limits(state: State, unit_ids: List[str]) -> bool:
    """Limit combinatorial explosion: max 10 combos per UM."""

    for uid in unit_ids:
        current = sum(1 for combo in state.combinations.values() if uid in combo.unit_ids)
        if current >= 10:
            return False
    return True


def _structure_plus_place(state: State, primary: Unit, partner: Unit) -> Combination | None:
    text = _combine_text([primary.phrase, partner.phrase])
    translation = _combine_translation([primary.translation, partner.translation]) or None
    combo = Combination(text=text, translation=translation, unit_ids=[primary.id, partner.id])
    if _respect_limits(state, combo.unit_ids):
        state.combinations[combo.id] = combo
        return combo
    return None


def _subject_verb_object(state: State, sujet: Unit, verbe: Unit, objet: Unit) -> Combination | None:
    text = _combine_text([sujet.phrase, verbe.phrase, objet.phrase])
    translation = _combine_translation([sujet.translation, verbe.translation, objet.translation]) or None
    combo = Combination(text=text, translation=translation, unit_ids=[sujet.id, verbe.id, objet.id])
    if _respect_limits(state, combo.unit_ids):
        state.combinations[combo.id] = combo
        return combo
    return None


def generate_combinations(state: State, new_unit: Unit) -> List[Combination]:
    combinations: List[Combination] = []
    if not new_unit.tags:
        return combinations

    units = [u for u in state.units.values() if u.language_to == new_unit.language_to and u.tags]

    # Template 1: structure_position + lieu
    if _has_tag(new_unit, "structure_position"):
        for lieu in [u for u in units if _has_tag(u, "lieu")]:
            if _has_tag(lieu, "verbe"):
                continue
            combo = _structure_plus_place(state, new_unit, lieu)
            if combo:
                combinations.append(combo)
    if _has_tag(new_unit, "lieu"):
        for structure in [u for u in units if _has_tag(u, "structure_position")]:
            combo = _structure_plus_place(state, structure, new_unit)
            if combo:
                combinations.append(combo)

    # Template 2: sujet + verbe + objet
    if any(_has_tag(new_unit, tag) for tag in ("sujet", "verbe", "objet")):
        sujets = [u for u in units if _has_tag(u, "sujet")]
        verbes = [u for u in units if _has_tag(u, "verbe")]
        objets = [u for u in units if _has_tag(u, "objet")]
        for sujet in sujets:
            for verbe in verbes:
                for objet in objets:
                    if not (new_unit.id in {sujet.id, verbe.id, objet.id}):
                        continue
                    combo = _subject_verb_object(state, sujet, verbe, objet)
                    if combo:
                        combinations.append(combo)

    return combinations


def _build_multiple_choice_options(state: State, correct_answer: str) -> List[ExerciseOption]:
    distractors = [c.translation or c.text for c in state.combinations.values() if (c.translation or c.text) != correct_answer]
    random.shuffle(distractors)
    options = [ExerciseOption(label="Bonne réponse", value=correct_answer)]
    for distractor in distractors[:3]:
        options.append(ExerciseOption(label="Alternative", value=distractor))
    random.shuffle(options)
    return options


def create_exercises_for_combination(state: State, combination: Combination) -> List[Exercise]:
    exercises: List[Exercise] = []
    prompt = f"Traduisez: {combination.text}"
    answer = combination.translation or combination.text
    translation_exercise = Exercise(type="translation", prompt=prompt, answer=answer, combination_id=combination.id)
    state.exercises[translation_exercise.id] = translation_exercise
    exercises.append(translation_exercise)

    mc_prompt = f"Choisissez la bonne traduction pour: {combination.text}"
    options = _build_multiple_choice_options(state, answer)
    mc_exercise = Exercise(
        type="multiple_choice",
        prompt=mc_prompt,
        answer=answer,
        options=options,
        combination_id=combination.id,
    )
    state.exercises[mc_exercise.id] = mc_exercise
    exercises.append(mc_exercise)

    cloze_source = combination.translation or combination.text
    words = cloze_source.split()
    if len(words) > 1:
        missing_index = random.randrange(len(words))
        answer_word = words[missing_index]
        words[missing_index] = "_____"
        cloze_prompt = "Complétez : " + " ".join(words)
        cloze_exercise = Exercise(
            type="cloze",
            prompt=cloze_prompt,
            answer=answer_word,
            combination_id=combination.id,
        )
        state.exercises[cloze_exercise.id] = cloze_exercise
        exercises.append(cloze_exercise)

    # Drag & drop (ordre des mots)
    tokens = (combination.translation or combination.text).split()
    if len(tokens) > 1:
        shuffled = tokens[:]
        random.shuffle(shuffled)
        drag_prompt = "Réordonnez les mots : " + " | ".join(shuffled)
        drag_exercise = Exercise(
            type="drag_drop",
            prompt=drag_prompt,
            answer=" ".join(tokens),
            options=[ExerciseOption(label="mot", value=token) for token in shuffled],
            combination_id=combination.id,
        )
        state.exercises[drag_exercise.id] = drag_exercise
        exercises.append(drag_exercise)
    return exercises


def available_exercises(state: State, user_id: str, limit: int = 10) -> List[Exercise]:
    now = datetime.utcnow()
    ready_exercises: List[Exercise] = []

    for exercise in state.exercises.values():
        combo = state.combinations.get(exercise.combination_id or "")
        if not combo:
            continue
        unit_id = combo.unit_ids[0]
        progress_key = f"{user_id}:{unit_id}"
        progress = state.progress.get(progress_key)
        if not progress or progress.next_review_at <= now:
            ready_exercises.append(exercise)

    if not ready_exercises:
        ready_exercises = list(state.exercises.values())

    # Return exercises with deterministic order to avoid UI jumps
    return sorted(ready_exercises, key=lambda ex: ex.prompt)[:limit]


def seed_state(state: State, seed_units: Iterable[Dict[str, object]] | None = None) -> Dict[str, List[str]]:
    units_source = list(seed_units) if seed_units is not None else list(DEFAULT_SEED_UNITS)
    created_units: List[str] = []
    created_combinations: List[str] = []
    created_exercises: List[str] = []

    for raw_unit in units_source:
        unit = Unit(**raw_unit)
        state.units[unit.id] = unit
        created_units.append(unit.id)
        combos = generate_combinations(state, unit)
        created_combinations.extend([combo.id for combo in combos])
        for combo in combos:
            exercises = create_exercises_for_combination(state, combo)
            created_exercises.extend([exercise.id for exercise in exercises])
    return {
        "units": created_units,
        "combinations": created_combinations,
        "exercises": created_exercises,
    }
