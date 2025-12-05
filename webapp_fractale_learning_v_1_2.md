# Web-App Fractale d’Apprentissage — Version 1.2 (Document Synthétique Collaborateur)

## 1. Vision et Concept Général
La web-app est conçue pour répliquer la manière dont un enfant apprend : par **micro-boucles rapides**, **exploration active**, **feedback immédiat**, et **recombinaison progressive**. Chaque élément ajouté (un mot, une règle, un concept) enrichit automatiquement tout le système grâce à un **moteur fractal** capable de générer instantanément des nouvelles phrases, exercices ou variations pertinentes.

Objectif final : créer le système d’apprentissage le plus rapide et naturel possible, applicable à n’importe quel domaine (langues, maths, musique, sport, etc.).

---

## 2. Fonctionnement Central : Les Unités Minimales (UM)
Le cœur du système repose sur les **Unités Minimales (UM)** :
- un mot
- une structure grammaticale
- un concept de base
- un motif (musique)
- un mouvement (sport)

Chaque UM possède :
- un type (vocabulaire, structure, concept…)
- des tags pour les règles de compatibilité
- un niveau de difficulté

### Mécanisme Fractal
1. L’utilisateur apprend une UM.
2. Le système génère automatiquement des combinaisons valides.
3. Des exercices sont créés instantanément (L1→L2, QCM, cloze, etc.).
4. L’utilisateur ajoute une nouvelle UM.
5. Le moteur fractal enrichit automatiquement l’ensemble.

Ce cycle rapide permet une progression exponentielle.

---

## 3. Expérience Utilisateur (UX) — Logique Générale
L’app repose sur une UX guidée, fluide, motivante et structurée selon les besoins cognitifs de l’apprenant.

### Points clés :
- **Onboarding interactif** pour expliquer la logique fractale en quelques secondes.
- **Carte Fractale Visuelle** montrant les UM apprises et leurs connexions.
- **Next Best Action** : l’utilisateur n’est jamais perdu.
- **Gamification intelligente** : streaks, badges, défis journaliers.
- **Feedback nuancé** : surlignage segmenté, corrections partielles, recommandations.
- **Modes d’apprentissage variés** : Zen, Vitesse, Hardcore, Challenge.

Le système est conçu pour être **addictif** tout en restant scientifiquement robuste.

---

## 4. Architecture Technique (Vue Synthétique)

### Stack Principale
- **Frontend** : React + Next.js
- **Backend** : Node.js (NestJS) ou Python (FastAPI)
- **Base de données** : PostgreSQL
- **Cache** : Redis
- **Infra** : Docker + hébergement managé

### Modules Backend
1. Authentification
2. Gestion des UM
3. Moteur Fractal (microservice)
4. Règles grammaticales & compatibilités
5. Générateur d’exercices
6. Système SRS (répétition espacée)
7. Analytics & KPI
8. API pour la carte fractale

### Structure Base de Données
- `users` : comptes et préférences
- `units` : UM avec tags et contenu
- `unit_relations` : règles de compatibilité
- `combinations` : phrases générées automatiquement
- `exercises` : exercices dérivés des combinaisons
- `user_progress` : score de maîtrise des UM
- `user_exercise_logs` : logs pour l’adaptation
- `streaks` : gamification

---

## 5. Fonctionnalités Clés (V1.2)

### A. Moteur Fractal
- Génération automatique de combinaisons
- Filtrage selon règles
- Validation grammaticale
- Gestion lazy (au besoin)

### B. Système d’Exercices
- L1 → L2 (traduction active)
- QCM générés automatiquement
- Cloze tests
- Drag & drop
- Dictée audio
- Prononciation

### C. Mécanismes Pédagogiques
- SRS intégré
- Feedback intelligent
- Visualisation de progression
- Adaptation dynamique du rythme

### D. Gamification
- Streaks
- Badges
- Défis journaliers
- Animations dopaminergiques

### E. Interface
- Mobile-first
- Mode hors-ligne pour révision
- Carte fractale interactive

---

## 6. Roadmap de Développement

### Version 1.0 — MVP Fonctionnel
- UM + combinaisons basiques
- Exercices L1→L2 et QCM
- Auth + progression simple
- UI minimaliste

### Version 1.2 (ce document)
Intégration complète UX/UI + architecture technique + moteur cohérent.

### Version 2.0
- Carte fractale professionnelle
- Gamification complète
- Moteur d’adaptation cognitif avancé
- Variété totale d’exercices

### Version 3.0
- Multi-domaines (maths, musique, sport)
- Mode créateur de contenu
- Intelligence fractale autonome
- API publique

---

## 7. Objectif Collaborateur
Ce document est conçu pour offrir une vision claire, cohérente et complète du projet. Tout collaborateur doit comprendre :
- le concept
- la philosophie pédagogique
- la structure technique
- la feuille de route
- le fonctionnement interne du moteur

Cette V1.2 sert de **référence centrale** avant la phase de conception UI et le développement du MVP.

---

## 8. Résultat Attendu Final
Une plateforme d’apprentissage :
- rapide
- intuitive
- scientifique
- scalable
- adaptée à tous les domaines
- capable de générer des milliers d’exercices pertinents automatiquement

Ce projet se positionne comme une **nouvelle génération d’app d’apprentissage**, au-delà des modèles actuels (Duolingo, Memrise, DeepL, Khan Academy).


---

## 9. Cahier des Charges Fonctionnel (MVP)

### 9.1. Objectif du MVP
Proposer une première version fonctionnelle permettant à un utilisateur :
- de créer un compte et se connecter,
- d’apprendre des Unités Minimales (UM) dans un domaine (langue au départ),
- de voir des phrases générées automatiquement à partir de ces UM,
- de pratiquer avec des exercices simples (L1→L2 et QCM),
- de suivre une progression basique (maîtrise des UM),
- de visualiser une version simplifiée de la carte fractale.

### 9.2. Fonctionnalités "Must-Have"
1. Authentification (inscription, connexion, déconnexion).
2. Gestion des UM prédéfinies (chargées en base) pour une langue (ex : chinois).
3. Ajout d’UM par l’utilisateur (texte simple + type + tags de base).
4. Génération et stockage de combinaisons simples (2 UM max par combinaison dans le MVP).
5. Exercices :
   - traduction L1 → L2,
   - QCM (réponses proposées par le système).
6. Correction basique avec feedback immédiat (correct/incorrect + highlight élément fautif).
7. Suivi de progression par UM (tentatives, réussite, score simple).
8. Visualisation fractale simplifiée (liste + regroupement par type, vue arborescente minimaliste).

### 9.3. Fonctionnalités "Nice-to-Have" (pour V1.5+)
- Streaks et badges simples.
- Mode vitesse.
- Variation d’exercices (cloze, drag & drop).
- Défis journaliers.

---

## 10. User Stories (MVP)

### 10.1. Authentification
- **US-01** : En tant qu’utilisateur, je peux créer un compte avec email + mot de passe afin de sauvegarder ma progression.
- **US-02** : En tant qu’utilisateur, je peux me connecter pour reprendre ma session.
- **US-03** : En tant qu’utilisateur, je peux me déconnecter pour sécuriser mon compte.

### 10.2. Apprentissage d’UM
- **US-10** : En tant qu’utilisateur, je peux voir une liste d’UM proposées (par niveau/domaine) pour commencer à apprendre.
- **US-11** : En tant qu’utilisateur, je peux cliquer sur une UM pour voir sa définition, exemple d’utilisation et phrases associées.
- **US-12** : En tant qu’utilisateur, je peux ajouter une UM simple (texte L2 + traduction L1 + type général) et la voir apparaître dans ma liste.

### 10.3. Génération de Combinaisons
- **US-20** : En tant que système, dès qu’une nouvelle UM est ajoutée, je génère des combinaisons avec une autre UM compatible (limite de 2 UM par combinaison dans le MVP).
- **US-21** : En tant qu’utilisateur, je peux voir quelques exemples de phrases générées automatiquement à partir de mes UM.

### 10.4. Exercices
- **US-30** : En tant qu’utilisateur, je peux lancer une session d’exercices basée sur mes UM actives.
- **US-31** : En tant qu’utilisateur, je peux répondre à des questions L1→L2 via un champ texte.
- **US-32** : En tant qu’utilisateur, je peux répondre à des QCM générés automatiquement à partir des combinaisons.
- **US-33** : En tant qu’utilisateur, je peux recevoir un feedback immédiat après chaque réponse (correct/incorrect, bonne réponse affichée).

### 10.5. Progression
- **US-40** : En tant qu’utilisateur, je peux voir mon score de maîtrise pour chaque UM (ex : barre de progression ou pourcentage).
- **US-41** : En tant qu’utilisateur, je peux voir un récapitulatif de ma session (nombre de bonnes réponses, UM les plus faibles).

### 10.6. Carte Fractale Simplifiée
- **US-50** : En tant qu’utilisateur, je peux accéder à une vue de mes UM et voir lesquelles sont liées entre elles (vue liste ou arbre simple).

---

## 11. Flows UX (MVP)

### 11.1. Flow d’Onboarding
1. L’utilisateur arrive sur la landing page.
2. Il voit une explication simple : "Apprends par petites briques qui se recombinent" + illustration.
3. CTA : "Commencer".
4. Redirection vers page d’inscription/connexion.
5. Une fois connecté, l’utilisateur arrive sur un tableau de bord avec 3 actions proposées :
   - Apprendre une première UM.
   - Lancer un exercice.
   - Voir la carte.

### 11.2. Flow Apprentissage d’une UM
1. L’utilisateur choisit "Apprendre une nouvelle UM".
2. L’app propose une UM existante (ex : "我在" avec explication).
3. L’utilisateur valide qu’il l’a comprise (bouton "Compris").
4. Le système génère 2–3 phrases simples à partir de cette UM + autres UM déjà apprises.
5. L’utilisateur peut passer immédiatement à un exercice basé sur cette UM.

### 11.3. Flow Ajout d’une UM
1. Depuis une page "UM", l’utilisateur clique sur "Ajouter une UM".
2. Il remplit un mini-formulaire :
   - texte L2,
   - traduction L1,
   - type (ex : vocab, structure),
   - tags simples (lieu, action...).
3. Le système valide le formulaire (non vide, longueur minimum...).
4. Le moteur fractal tente de générer des combinaisons avec 1 UM compatible existante.
5. Les combinaisons générées sont visibles dans une section "Nouvelles phrases".

### 11.4. Flow Exercice (Session Simple)
1. L’utilisateur clique sur "Exercices".
2. Le système sélectionne une combinaison liée à une UM peu maîtrisée.
3. L’app montre la phrase en L1 et demande la réponse en L2.
4. L’utilisateur saisit sa réponse.
5. Le système compare, affiche "Correct" ou "Incorrect" et montre la bonne réponse.
6. L’utilisateur passe à la question suivante (5–10 questions par session).
7. À la fin, un écran de récapitulatif s’affiche.

### 11.5. Flow Visualisation Fractale Simplifiée
1. L’utilisateur clique sur "Carte".
2. L’app affiche une liste d’UM regroupées par type (ou un arbre simple type parent/enfant).
3. L’utilisateur clique sur une UM pour voir :
   - les UM liées,
   - les phrases associées,
   - son score de maîtrise.

---

## 12. Spécifications API (Contrats JSON – MVP)

### 12.1. Exemple `POST /auth/register`
**Request**
```json
{
  "email": "user@example.com",
  "password": "MotDePasseSecurise123"
}
```
**Response (201)**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2025-01-01T10:00:00Z",
  "token": "jwt_token"
}
```

### 12.2. Exemple `GET /units`
**Query params** : `domain`, `type`, `page`, `page_size`

**Response (200)**
```json
{
  "items": [
    {
      "id": 1,
      "domain": "zh-CN",
      "type": "structure",
      "content_L2": "我在",
      "content_L1": "je suis à",
      "tags": ["base", "position"],
      "difficulty": 1
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 35
}
```

### 12.3. Exemple `POST /units`
**Request**
```json
{
  "domain": "zh-CN",
  "type": "vocab",
  "content_L2": "家",
  "content_L1": "maison",
  "tags": ["lieu"],
  "difficulty": 1
}
```
**Response (201)**
```json
{
  "id": 2,
  "domain": "zh-CN",
  "type": "vocab",
  "content_L2": "家",
  "content_L1": "maison",
  "tags": ["lieu"],
  "difficulty": 1,
  "created_at": "2025-01-01T10:05:00Z"
}
```

### 12.4. Exemple `GET /exercises/next`
**Response (200)**
```json
{
  "exercise_id": 101,
  "type": "l1_to_l2",
  "question_L1": "Je suis à la maison",
  "hint_units": [1, 2]
}
```

### 12.5. Exemple `POST /exercises/{id}/answer`
**Request**
```json
{
  "answer_L2": "我在家"
}
```
**Response (200)**
```json
{
  "status": "success",
  "correct_answer": "我在家",
  "is_exact_match": true,
  "feedback_segments": [
    {
      "segment": "我在",
      "status": "ok"
    },
    {
      "segment": "家",
      "status": "ok"
    }
  ],
  "updated_progress": {
    "unit_ids": [1,2],
    "mastery_scores": [0.7, 0.6]
  }
}
```

---

## 13. Schémas DB (Types & Contraintes – MVP)

### 13.1. `users`
- `id` UUID (PK)
- `email` TEXT UNIQUE NOT NULL
- `password_hash` TEXT NOT NULL
- `created_at` TIMESTAMP NOT NULL DEFAULT now()

### 13.2. `units`
- `id` SERIAL (PK)
- `domain` TEXT NOT NULL (ex: "zh-CN")
- `type` TEXT NOT NULL (enum logique côté app)
- `content_L2` TEXT NOT NULL
- `content_L1` TEXT NOT NULL
- `tags` JSONB NOT NULL DEFAULT '[]'
- `difficulty` INT NOT NULL DEFAULT 1
- `created_by` UUID NULL (FK vers `users`)
- `created_at` TIMESTAMP NOT NULL DEFAULT now()

Index :
- idx_units_domain
- idx_units_type

### 13.3. `combinations`
- `id` SERIAL (PK)
- `domain` TEXT NOT NULL
- `unit_ids` INT[] NOT NULL
- `phrase_L2` TEXT NOT NULL
- `phrase_L1` TEXT NOT NULL
- `is_valid` BOOLEAN NOT NULL DEFAULT true
- `created_at` TIMESTAMP NOT NULL DEFAULT now()

Index :
- idx_combinations_domain

### 13.4. `exercises`
- `id` SERIAL (PK)
- `combination_id` INT NOT NULL REFERENCES `combinations`(id) ON DELETE CASCADE
- `type` TEXT NOT NULL
- `metadata` JSONB NOT NULL DEFAULT '{}'

### 13.5. `user_progress`
- `id` SERIAL (PK)
- `user_id` UUID NOT NULL REFERENCES `users`(id) ON DELETE CASCADE
- `unit_id` INT NOT NULL REFERENCES `units`(id) ON DELETE CASCADE
- `attempts` INT NOT NULL DEFAULT 0
- `success_count` INT NOT NULL DEFAULT 0
- `mastery_score` REAL NOT NULL DEFAULT 0
- `last_seen_at` TIMESTAMP

Index :
- unique (user_id, unit_id)

### 13.6. `user_exercise_logs`
- `id` SERIAL (PK)
- `user_id` UUID NOT NULL REFERENCES `users`(id) ON DELETE CASCADE
- `exercise_id` INT NOT NULL REFERENCES `exercises`(id) ON DELETE CASCADE
- `status` TEXT NOT NULL (success, fail, partial)
- `time_spent_ms` INT
- `created_at` TIMESTAMP NOT NULL DEFAULT now()

---

## 14. Pseudo-code Moteur Fractal (MVP Simplifié)

### 14.1. Génération de Combinaisons (2 UM max)
```pseudo
function generate_combinations_for_unit(new_unit, existing_units):
    combinations = []
    for unit in existing_units:
        if are_compatible(new_unit, unit):
            phrase_L2 = build_phrase_L2(new_unit, unit)
            phrase_L1 = build_phrase_L1(new_unit, unit)
            if is_valid_phrase(phrase_L2, phrase_L1):
                combinations.append({
                    domain: new_unit.domain,
                    unit_ids: [new_unit.id, unit.id],
                    phrase_L2,
                    phrase_L1
                })
    save_combinations(combinations)
    return combinations
```

### 14.2. Sélection d’un Exercice "Next Best"
```pseudo
function get_next_exercise(user_id):
    weak_units = get_units_with_low_mastery(user_id)
    if weak_units is empty:
        weak_units = get_recent_units(user_id)

    candidate_combinations = get_combinations_for_units(weak_units)

    if candidate_combinations is empty:
        candidate_combinations = get_random_combinations()

    combination = select_best_combination(candidate_combinations)
    exercise = build_exercise_from_combination(combination)
    return exercise
```

### 14.3. Mise à jour du Score de Maîtrise (simplifié)
```pseudo
function update_mastery(user_id, unit_ids, is_success):
    for unit_id in unit_ids:
        progress = get_user_progress(user_id, unit_id)
        progress.attempts += 1
        if is_success:
            progress.success_count += 1
        progress.mastery_score = progress.success_count / progress.attempts
        progress.last_seen_at = now()
        save(progress)
```

---

## 15. Définition du MVP Exact (Scope Final)

### Inclus dans le MVP
- Domaine : langue unique (ex : chinois débutant).
- UM de base pré-intégrées (50–100 unités).
- Ajout d’UM custom par l’utilisateur (simple).
- Génération de combinaisons simples (2 UM, quelques templates prédéfinis).
- Exercices :
  - L1→L2,
  - QCM.
- Progression par UM (score simple).
- Vue fractale simplifiée (liste + regroupement par type, pas encore graph complet).
- UI responsive (desktop + mobile basique).

### Exclu du MVP (pour versions ultérieures)
- Audio et reconnaissance vocale.
- Multi-domaines (maths, musique...).
- Gamification avancée (badges complexes, quêtes).
- Fractal map visuelle avancée (graph interactif complexe).
- SRS avancé avec formules type SM-2.
- Personnalisation fine du rythme.

---

## 16. Gestion des Erreurs & Messages Utilisateur

### API (exemples)
- 400 : données invalides → `{ "error": "invalid_payload", "details": {...} }`
- 401 : non authentifié → `{ "error": "unauthorized" }`
- 404 : ressource introuvable → `{ "error": "not_found" }`
- 500 : erreur serveur → `{ "error": "server_error" }`

### UX (front)
- Messages clairs et courts :
  - "Cette réponse est incorrecte, essaye encore."
  - "UM ajoutée avec succès."
  - "Aucune combinaison possible pour cette UM, ajoute une autre unité compatible."

---

## 17. Tests & Qualité (MVP)

### 17.1. Tests Unitaires
- sur le moteur de génération de combinaisons,
- sur la logique de mise à jour de la progression,
- sur les validations d’API.

### 17.2. Tests Manuels
- flow d’inscription + connexion,
- apprendre une UM → générer combinaisons → faire exercices,
- affichage de progression,
- expérience mobile.

### 17.3. Monitoring Minimal
- logs d’erreurs backend,
- métriques basiques (nombre de users, nombre d’exercices joués).

---

Cette extension du document V1.2 fournit désormais **tout le nécessaire** pour que des développeurs puissent commencer à construire un MVP :
- scope clair,
- user stories,
- flows UX,
- contrats d’API,
- schémas DB précis,
- pseudo-code pour le moteur fractal et la progression,
- définition exacte de ce qui est inclus/exclu.

---
# 18. Préparation Complète MVP — Corrections Suite à la Redteam Avancée

## 18.1. Persona MVP (Défini pour guider toutes les décisions)
**Persona principal : “L’apprenant autonome débutant en langue”**
- Âge : 16–40 ans
- Objectif : apprendre rapidement des bases utiles d’une langue
- Niveau : débutant total
- Temps disponible : 5–15 minutes/session
- Attentes : simplicité, clarté, progression visible
- Frustrations : apps trop complexes ou trop théoriques

Conséquences UX :
- l’ajout d’UM par l’utilisateur = **option avancée, cachée**
- priorité = apprentissage simple, guidé et rapide

---
## 18.2. Critères de Succès du MVP
Un MVP est considéré réussi si :
1. ≥ 70% des utilisateurs terminent **1 session complète** (5 exercices)
2. ≥ 40% reviennent **le lendemain**
3. Les utilisateurs apprennent en moyenne **20 UM** en 1 semaine
4. Le moteur fractal génère des phrases **sans erreurs** dans 95% des cas

---
## 18.3. Objectif Exact du MVP
**Objectif MVP : permettre à un utilisateur d’apprendre 30–50 UM en chinois et de générer automatiquement des phrases simples pour pratiquer.**

Focus = démontrer :
- la vitesse d’apprentissage,
- la pertinence du moteur fractal,
- la fluidité de l’expérience.

---
## 18.4. États Vides, Loading & Erreurs (spécifications UX obligatoires)

### États vides
- Aucun UM → écran : “Commence par apprendre ta première UM : 我在 (je suis à)”
- Aucune combinaison → message : “Ajoute une UM compatible (ex : 家 – maison)”
- Aucun exercice disponible → “Ajoute ou apprends une nouvelle UM pour débloquer des exercices.”

### États chargement
- Skeleton + texte : “Chargement…”

### États erreur
- Erreur API → “Un problème est survenu. Réessaye.”
- Perte réseau → “Connexion perdue. Mode hors-ligne limité activé.”

---
## 18.5. Mode Ajout d’UM : repositionnement stratégique
**Dans le MVP : l’ajout d’UM ne doit PAS être visible pour les débutants.**
- Position : option dans “Avancé”
- Justification : éviter la surcharge cognitive

Seules les UM pré-chargées seront visibles par défaut.

---
## 18.6. Architecture Frontend — Gestion d’État (Décision Technique)

### Choix : **Zustand + TanStack Query**
- Zustand → état global local (user, UI)
- TanStack Query → synchronisation API (UM, combinaisons, exercices)

Ce choix élimine :
- Redux (trop lourd)
- Context (trop limité)

---
## 18.7. Composants Frontend (Hiérarchie Détaillée)

### Page /app
- `<DashboardLayout>`
  - `<Header>`
  - `<NextActionCard>`
  - `<ProgressOverview>`
  - `<UMList>`
  - `<StartExerciseButton>`

### Page /app/learn
- `<UMCard>`
- `<ExamplePhrases>`
- `<LearnButton>`

### Page /app/exercises
- `<ExercisePanel>`
  - `<QuestionDisplay>`
  - `<InputBox>` ou `<QCMOptions>`
  - `<FeedbackBubble>`
  - `<NextButton>`

### Page /app/map
- `<FractalMapSimplified>`
- `<UMNode>`

---
## 18.8. Guideline Code & Environnement de Dev

### Linter & Format
- ESLint + Prettier (config fournie)

### Structure de projet Next.js
```
/src
  /app
  /components
  /lib
  /services
  /styles
```

### Lancement local
- `docker compose up -d`
- `cp .env.example .env`
- `npm install`
- `npm run dev`

---
## 18.9. API — Standardisation Obligatoire

### Format erreur standard (imposé partout)
```
{ "error": "string", "message": "string", "details": {} }
```

### Versioning obligatoire
`/api/v1/...`

### Pagination standardisée
```
{
  "items": [...],
  "page": 1,
  "page_size": 20,
  "total": 100
}
```

---
## 18.10. Règles Fractales **explicites** (pour langue chinoise MVP)

### Compatibilités minimales MVP
- structure_position + lieu → OK
- sujet + verbe + objet → OK
- structure qui impose un lieu (我在) + UM type lieu

### Templates autorisés
1. `[structure][lieu]` → ex : 我在家
2. `[sujet][verbe][objet]` → ex : 我吃饭

### Combinaisons interdites
- structure_position + verbe
- verbe + lieu sans structure
- UM sans tags

### Limites (anti-explosion)
- max 10 combinaisons par UM
- max 2 UM combinées dans le MVP
- prioriser UM les plus fréquentes (tags : “base”)

---
## 18.11. SRS Simplifié — Règles Finalisées

### Score de maîtrise
```
mastery_score = success_count / attempts
```

### Définitions
- UM maîtrisée = score ≥ 0.8
- UM faible = score < 0.6
- UM à réviser = UM non vue depuis 72h

---
## 18.12. Sécurité — Spécifications Minimales

### Mots de passe
- min 8 caractères

### Authentification
- JWT + refresh token rotation

### Anti-bruteforce
- 5 tentatives max / minute sur /auth/login

### Données sensibles
- hash = Argon2

---
## 18.13. Seeds Initiales (Obligatoires pour MVP)

📌 Fichier : `seed_units_zh_cn.json`

Contient au minimum :
- 我在 (je suis à) — structure
- 家 (maison) — lieu
- 学校 (école) — lieu
- 我 (je) — sujet
- 吃 (manger) — verbe
- 饭 (repas) — objet

Permet immédiatement :
- 我在家
- 我在学校
- 我吃饭

---
## 18.14. Exemple d’une Session Utilisateur Complète (MVP)

1. L’utilisateur se connecte
2. Il voit “Commence ici → Apprends 我在”
3. Il apprend 我在 + 2 exemples
4. L’app lui propose d’apprendre 家
5. Le moteur génère 我在家
6. Exercice : “Je suis à la maison” → 我在家
7. Score augmente
8. Session terminée → récap
9. Proposition : “Apprends 学校”

Ce scénario valide que tout le MVP fonctionne.

---
## 18.15. Analytics MVP — Événements Obligatoires

### Events trackés
- `unit_learned`
- `exercise_started`
- `exercise_completed`
- `exercise_failed`
- `unit_mastered`
- `session_completed`

---
## 18.16. Accessibilité MVP
- Contraste AA minimum
- Labels sur tous les champs
- Navigation clavier
- Feedbacks textuels lisibles

---
# ✔️ Le canvas est maintenant **100% prêt pour développement MVP**.
Il contient :
- objectifs,
- règles,
- UX flows,
- API,
- DB,
- moteur fractal,
- SRS,
- sécurité,
- guidelines dev,
- seeds initiales,
- exemple de session.

Aucune question bloquante ne doit rester pour les développeurs.
