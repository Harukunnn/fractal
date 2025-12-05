# Fractale Learning — MVP

Ce dépôt contient un prototype minimal aligné avec la vision décrite dans `webapp_fractale_learning_v_1_2.md`. Il fournit :

- Une API FastAPI pour gérer les **Unités Minimales (UM)**, générer des combinaisons, créer des exercices et suivre une progression simple.
- Un front-end statique léger pour tester rapidement l'expérience : création d'utilisateur, ajout d'UM et résolution d'exercices.

## Structure

- `backend/` — API FastAPI, moteur fractal simplifié et modèles Pydantic.
- `frontend/` — mini-application multi-pages (landing, tableau de bord, UM, progression, compte) qui consomme l'API.
- `webapp_fractale_learning_v_1_2.md` — document source décrivant la vision complète.
- `backend/data/state.json` — sauvegarde locale persistante (créée automatiquement) contenant utilisateurs, UM, sessions et progr
essions.

## Démarrage rapide

1. Installez les dépendances backend :

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Lancez l'API :

   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Ouvrez le front-end :

   - Depuis un navigateur local, servez `frontend/index.html` (ex. `python -m http.server 3000`).
   - Allez sur `http://localhost:3000` : un compte démo est auto-créé, les seeds sont chargées et une première question est disponible en un clic.

## Fonctionnalités incluses

- Authentification légère en mémoire (inscription / connexion / déconnexion) pour lier la progression à un compte, avec mot de passe min. 8 caractères, **sauvegardée automatiquement sur disque**.
- Ajout d'UM avec type, difficulté, tags obligatoires (compatibilités) et langues source/cible.
- Génération automatique de combinaisons suivant les règles MVP (structure_position+lieu, sujet+verbe+objet) et quatre types d'exercices (traduction, QCM, cloze, drag & drop).
- Feedback enrichi avec mise en évidence des mots attendus en cas d'erreur.
- Visualisation basique de la carte fractale (UM + combinaisons liées) et suivi de progression enrichi (maîtrise, score, statut, prochaine révision, badges/streak).
- Semis rapide d'unités minimales génériques (fr → en) embarquées dans le backend, sans fichier spécifique par matière.
- Gamification légère : streak, badges dynamiques et événements analytics traçables (unit_learned, exercise_started/completed/failed, unit_mastered, session_completed, seed_loaded).
- Mode démo immédiat : `/demo/bootstrap` crée un compte temporaire, charge les seeds et retourne un token prêt à l'emploi.
- Sauvegarde locale auto (JSON) : chaque modification est écrite dans `backend/data/state.json`, rechargée au démarrage. Endpoints utilitaires `/storage/save`, `/storage/load`, `/storage/info`.

### Endpoints utiles

- `POST /users` : créer un utilisateur in-memory et initialiser le suivi de progression pour les UM existantes.
- `POST /units` / `GET /units` : ajouter ou lister les UM.
- `GET /exercises?user_id=...` : récupérer des exercices prêts pour l'utilisateur (filtrés par révisions dues).
- `GET /exercises/next?user_id=...` : proposer la "next best question" et tracer `exercise_started`.
- `POST /exercises/{id}/answer?user_id=...` : corriger une réponse et retourner un feedback détaillé + progression.
- `GET /progress?user_id=...` : suivre la maîtrise par UM (tentatives, réussites, précision, prochaine revue).
- `GET /fractal-map` : carte fractale simplifiée (UM + combinaisons).
- `GET /session/{user_id}` : récapitulatif instantané (mastered, weak, révisions en attente, badges).
- `GET /analytics` : événements traçables (unit_learned, exercise_completed/failed, session_completed, seed_loaded).
- `POST /seed` : charge les unités embarquées et génère automatiquement combinaisons + exercices.
- `POST /demo/bootstrap` : compte démo + token + seed en un appel.
- `POST /auth/register` / `POST /auth/login` / `POST /auth/logout` : inscription rapide avec email/mot de passe, session en mémoire.

### Compatibilités et limites

- Combinaisons autorisées : `structure_position + lieu`, `sujet + verbe + objet` (langue cible identique).
- Combinaisons interdites : structure_position + verbe, verbe + lieu sans structure, UM sans tags.
- Anti-explosion : 10 combinaisons max par UM et 3 UM max par combinaison.

## Notes

Ce MVP privilégie la simplicité (stockage en mémoire) afin d'explorer rapidement le moteur fractal et l'enchaînement des micro-boucles d'apprentissage. Il peut servir de base à une implémentation plus robuste (base PostgreSQL, SRS avancé, authentification complète, etc.).
