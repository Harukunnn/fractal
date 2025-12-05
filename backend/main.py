from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .engine import available_exercises, create_exercises_for_combination, generate_combinations, seed_state
from .models import (
    AnalyticsEvent,
    AuthResponse,
    Combination,
    Exercise,
    LoginPayload,
    Progress,
    RegisterPayload,
    State,
    Unit,
    UnitCreate,
    User,
    UserCreate,
)
from .persistence import load_state, save_state, storage_info

app = FastAPI(title="Fractale Learning MVP", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE = load_state()


def _persist() -> None:
    save_state(STATE)


def _log_event(name: str, user_id: str | None = None, unit_id: str | None = None, exercise_id: str | None = None, metadata: Dict[str, str] | None = None) -> None:
    STATE.analytics.append(
        AnalyticsEvent(
            name=name,
            user_id=user_id,
            unit_id=unit_id,
            exercise_id=exercise_id,
            metadata=metadata or {},
        )
    )
    _persist()


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _create_session(user_id: str) -> str:
    token = str(uuid4())
    STATE.sessions[token] = user_id
    _persist()
    return token


def _check_credentials(email: str, password: str) -> str | None:
    stored = STATE.credentials.get(email)
    if not stored:
        return None
    if stored != _hash_password(password):
        return None
    return STATE.account_index.get(email)


def _init_progress_for_user(user: User) -> None:
    for unit in STATE.units.values():
        key = f"{user.id}:{unit.id}"
        if key not in STATE.progress:
            STATE.progress[key] = Progress(user_id=user.id, unit_id=unit.id)
    _persist()


def _highlight_mismatch(expected: str, provided: str) -> str:
    expected_tokens = expected.split()
    provided_tokens = provided.split()
    highlighted: List[str] = []
    for idx, token in enumerate(expected_tokens):
        provided_token = provided_tokens[idx] if idx < len(provided_tokens) else None
        if provided_token and provided_token.lower() == token.lower():
            highlighted.append(token)
        else:
            highlighted.append(f"[{token}]")
    extra = provided_tokens[len(expected_tokens) :]
    if extra:
        highlighted.append("(extra: " + " ".join(extra) + ")")
    return " ".join(highlighted)


class ExerciseAnswer(BaseModel):
    answer: str


class ExerciseFeedback(BaseModel):
    correct: bool
    expected: str
    user_answer: str
    progress: Progress
    highlight: Optional[str] = None


class FractalNode(BaseModel):
    unit: Unit
    related_combinations: List[Combination]


class SessionSummary(BaseModel):
    user: User
    mastered: int
    weak_units: int
    upcoming_reviews: int
    badges: List[str]


@app.post("/auth/register", response_model=AuthResponse, status_code=201)
def register(payload: RegisterPayload) -> AuthResponse:
    if len(payload.password) < 8:
        raise HTTPException(status_code=400, detail="Mot de passe trop court (min. 8 caractères)")
    if payload.email in STATE.credentials:
        raise HTTPException(status_code=409, detail="Email déjà enregistré")
    user = User(name=payload.name, email=payload.email, last_active=datetime.utcnow())
    STATE.users[user.id] = user
    STATE.credentials[payload.email] = _hash_password(payload.password)
    STATE.account_index[payload.email] = user.id
    _init_progress_for_user(user)
    token = _create_session(user.id)
    _log_event("user_registered", user_id=user.id)
    return AuthResponse(token=token, user=user)


@app.post("/auth/login", response_model=AuthResponse)
def login(payload: LoginPayload) -> AuthResponse:
    user_id = _check_credentials(payload.email, payload.password)
    if not user_id or user_id not in STATE.users:
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    STATE.users[user_id].last_active = datetime.utcnow()
    token = _create_session(user_id)
    _log_event("user_logged_in", user_id=user_id)
    return AuthResponse(token=token, user=STATE.users[user_id])


@app.post("/auth/logout")
def logout(token: str) -> dict:
    if token in STATE.sessions:
        user_id = STATE.sessions.pop(token)
        _log_event("user_logged_out", user_id=user_id)
    return {"message": "Session fermée"}


@app.post("/users", response_model=User)
def create_user(payload: UserCreate) -> User:
    user = User(name=payload.name, email=payload.email, last_active=datetime.utcnow())
    STATE.users[user.id] = user
    _init_progress_for_user(user)
    _log_event("user_created", user_id=user.id)
    return user


@app.get("/units", response_model=List[Unit])
def list_units() -> List[Unit]:
    return list(STATE.units.values())


@app.post("/units", response_model=Unit, status_code=201)
def create_unit(payload: UnitCreate) -> Unit:
    if not payload.tags:
        raise HTTPException(status_code=400, detail="Les UM doivent contenir au moins un tag pour les règles de compatibilité")
    unit = Unit(**payload.model_dump())
    STATE.units[unit.id] = unit
    combos = generate_combinations(STATE, unit)
    for combo in combos:
        create_exercises_for_combination(STATE, combo)
    for user in STATE.users.values():
        key = f"{user.id}:{unit.id}"
        if key not in STATE.progress:
            STATE.progress[key] = Progress(user_id=user.id, unit_id=unit.id)
    _log_event("unit_learned", unit_id=unit.id)
    return unit


@app.get("/combinations", response_model=List[Combination])
def list_combinations() -> List[Combination]:
    return list(STATE.combinations.values())


@app.get("/exercises", response_model=List[Exercise])
def list_exercises(user_id: str | None = None, limit: int = 10) -> List[Exercise]:
    if user_id is None:
        return list(STATE.exercises.values())[:limit]
    if user_id not in STATE.users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return available_exercises(STATE, user_id, limit=limit)


@app.post("/exercises/{exercise_id}/answer", response_model=ExerciseFeedback)
def answer_exercise(exercise_id: str, payload: ExerciseAnswer, user_id: str) -> ExerciseFeedback:
    if exercise_id not in STATE.exercises:
        raise HTTPException(status_code=404, detail="Exercice introuvable")
    exercise = STATE.exercises[exercise_id]
    success = payload.answer.strip().lower() == exercise.answer.strip().lower()
    if user_id not in STATE.users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    combo = STATE.combinations.get(exercise.combination_id or "")
    unit_id = combo.unit_ids[0] if combo else ""
    progress_key = f"{user_id}:{unit_id}"
    progress = STATE.progress.get(progress_key) or Progress(user_id=user_id, unit_id=unit_id)
    previous_status = progress.status
    progress.mark_result(success)
    STATE.progress[progress_key] = progress

    STATE.users[user_id].last_active = datetime.utcnow()
    if success:
        STATE.users[user_id].streak += 1
        _log_event("exercise_completed", user_id=user_id, unit_id=unit_id, exercise_id=exercise_id)
        if progress.status == "mastered" and previous_status != "mastered":
            _log_event("unit_mastered", user_id=user_id, unit_id=unit_id)
    else:
        STATE.users[user_id].streak = max(0, STATE.users[user_id].streak - 1)
        _log_event("exercise_failed", user_id=user_id, unit_id=unit_id, exercise_id=exercise_id)
    highlight = None if success else _highlight_mismatch(exercise.answer, payload.answer)
    _persist()
    return ExerciseFeedback(
        correct=success,
        expected=exercise.answer,
        user_answer=payload.answer,
        progress=progress,
        highlight=highlight,
    )


@app.get("/progress", response_model=List[Progress])
def get_progress(user_id: str) -> List[Progress]:
    if user_id not in STATE.users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return sorted(
        [p for p in STATE.progress.values() if p.user_id == user_id],
        key=lambda p: p.next_review_at,
    )


def _badges_for_user(user_id: str) -> List[str]:
    badges: List[str] = []
    progress_items = [p for p in STATE.progress.values() if p.user_id == user_id]
    mastered = sum(1 for p in progress_items if p.status == "mastered")
    weak = sum(1 for p in progress_items if p.status == "weak")
    streak = STATE.users[user_id].streak

    if mastered >= 3:
        badges.append("Fractal Builder")
    if streak >= 3:
        badges.append(f"Streak {streak} 🔥")
    if weak == 0 and progress_items:
        badges.append("No Weak Links")
    return badges


@app.get("/session/{user_id}", response_model=SessionSummary)
def session_summary(user_id: str) -> SessionSummary:
    if user_id not in STATE.users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    progress_items = [p for p in STATE.progress.values() if p.user_id == user_id]
    mastered = sum(1 for p in progress_items if p.status == "mastered")
    weak_units = sum(1 for p in progress_items if p.status == "weak")
    upcoming_reviews = sum(1 for p in progress_items if p.status == "review")
    badges = _badges_for_user(user_id)
    _log_event("session_completed", user_id=user_id)
    return SessionSummary(
        user=STATE.users[user_id],
        mastered=mastered,
        weak_units=weak_units,
        upcoming_reviews=upcoming_reviews,
        badges=badges,
    )


@app.get("/analytics", response_model=List[AnalyticsEvent])
def list_events(limit: int = 50) -> List[AnalyticsEvent]:
    return sorted(STATE.analytics, key=lambda e: e.created_at, reverse=True)[:limit]


@app.get("/fractal-map", response_model=List[FractalNode])
def fractal_map() -> List[FractalNode]:
    result: List[FractalNode] = []
    for unit in STATE.units.values():
        combos = [combo for combo in STATE.combinations.values() if unit.id in combo.unit_ids]
        result.append(FractalNode(unit=unit, related_combinations=combos))
    return result


@app.get("/exercises/next", response_model=Exercise)
def next_exercise(user_id: str, limit: int = 5) -> Exercise:
    if user_id not in STATE.users:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    exercises = available_exercises(STATE, user_id, limit=limit)
    if not exercises:
        raise HTTPException(status_code=404, detail="Aucun exercice disponible")
    choice = exercises[0]
    _log_event("exercise_started", user_id=user_id, exercise_id=choice.id)
    return choice


@app.post("/demo/bootstrap", response_model=AuthResponse)
def bootstrap_demo() -> AuthResponse:
    """Crée un compte éphémère et pré-remplit le moteur pour démarrer en 10 secondes."""

    created = seed_state(STATE) if not STATE.units else {"units": [], "combinations": [], "exercises": []}
    if STATE.users:
        # Réutiliser le premier compte existant comme compte demo si présent
        user = next(iter(STATE.users.values()))
    else:
        user = User(name="Explorer", email=f"demo+{uuid4().hex[:6]}@fractale.app", last_active=datetime.utcnow())
        STATE.users[user.id] = user
        STATE.credentials[user.email] = _hash_password("fractale123")
        STATE.account_index[user.email] = user.id

    _init_progress_for_user(user)
    for unit_id in created.get("units", []):
        key = f"{user.id}:{unit_id}"
        STATE.progress[key] = Progress(user_id=user.id, unit_id=unit_id)

    token = _create_session(user.id)
    _log_event("seed_loaded", metadata={"units": str(len(created.get("units", [])))})
    _log_event("user_logged_in", user_id=user.id)
    return AuthResponse(token=token, user=user)


@app.post("/seed")
def seed() -> dict:
    created = seed_state(STATE)
    for user in STATE.users.values():
        for unit_id in created.get("units", []):
            key = f"{user.id}:{unit_id}"
            STATE.progress[key] = Progress(user_id=user.id, unit_id=unit_id)
    _log_event("seed_loaded", metadata={"units": str(len(created.get("units", [])))})
    _persist()
    return {"message": "Données d'exemple créées", **created}


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "units": len(STATE.units),
        "exercises": len(STATE.exercises),
        "combinations": len(STATE.combinations),
        "analytics": len(STATE.analytics),
    }


def _apply_loaded_state(new_state: State) -> None:
    STATE.users = new_state.users
    STATE.units = new_state.units
    STATE.combinations = new_state.combinations
    STATE.exercises = new_state.exercises
    STATE.progress = new_state.progress
    STATE.analytics = new_state.analytics
    STATE.credentials = new_state.credentials
    STATE.sessions = new_state.sessions
    STATE.account_index = new_state.account_index


def _state_counts() -> Dict[str, int]:
    return {
        "users": len(STATE.users),
        "units": len(STATE.units),
        "combinations": len(STATE.combinations),
        "exercises": len(STATE.exercises),
        "progress": len(STATE.progress),
        "sessions": len(STATE.sessions),
    }


@app.post("/storage/save")
def save_storage() -> dict:
    info = save_state(STATE)
    return {"message": "Sauvegarde effectuée", **info, "counts": _state_counts()}


@app.post("/storage/load")
def load_storage() -> dict:
    new_state = load_state()
    _apply_loaded_state(new_state)
    _persist()
    return {"message": "Données rechargées", **storage_info(), "counts": _state_counts()}


@app.get("/storage/info")
def storage_status() -> dict:
    return {**storage_info(), "counts": _state_counts()}
