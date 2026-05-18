# AI Resume Analyzer API

Plateforme RH d'analyse intelligente de CV : upload PDF, extraction de texte, scoring automatique par rapport à un profil de poste, traitement asynchrone et dashboard recruteur.

## Stack

- Python 3.12, Django 5, Django REST Framework
- JWT avec SimpleJWT
- PostgreSQL 16, Redis, Celery (traitement asynchrone)
- PyPDF2 (extraction texte PDF) + spaCy (couche NLP)
- drf-spectacular pour la documentation Swagger/OpenAPI
- pytest pour les tests
- CI GitHub Actions

## Structure du projet

```
ai_analyser/
├── apps/
│   ├── accounts/   # recruteurs et rôles, inscription, JWT
│   ├── resumes/    # candidats, CV (PDF), profils de poste, analyses asynchrones
│   ├── analytics/  # dashboard RH et scores
│   └── common/     # pagination et gestion d'erreurs API
├── config/         # settings, urls, celery, wsgi/asgi
├── tests/          # tests unitaires (services d'analyse)
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## Installation

Avec Docker Compose (recommandé) :

```bash
cp .env.example .env
docker compose up --build
```

L'API démarre sur `http://localhost:8002` et le worker Celery est lancé automatiquement. La documentation API est disponible sur `http://localhost:8002/api/docs/`.

Sans Docker (développement local) :

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python manage.py migrate
python manage.py runserver
celery -A config worker -l info
```

## Variables d'environnement

Copier `.env.example` vers `.env` puis adapter les valeurs.

| Variable | Description | Défaut |
|---|---|---|
| `DJANGO_SECRET_KEY` | Clé secrète Django | `change-me` |
| `DJANGO_DEBUG` | Mode debug | `true` |
| `DJANGO_ALLOWED_HOSTS` | Hôtes autorisés, séparés par des virgules | `localhost,127.0.0.1` |
| `POSTGRES_DB` | Nom de la base | `resume_ai_db` |
| `POSTGRES_USER` | Utilisateur PostgreSQL | `postgres` |
| `POSTGRES_PASSWORD` | Mot de passe PostgreSQL | `postgres` |
| `POSTGRES_HOST` | Hôte PostgreSQL | `db` |
| `POSTGRES_PORT` | Port PostgreSQL | `5432` |
| `CELERY_BROKER_URL` | Broker Celery (Redis) | `redis://redis:6379/0` |
| `CELERY_RESULT_BACKEND` | Backend de résultats Celery | `redis://redis:6379/1` |

## Endpoints principaux

| Méthode | URL | Description |
|---|---|---|
| POST | `/api/auth/token/` | Obtenir un JWT (access + refresh) |
| POST | `/api/auth/token/refresh/` | Rafraîchir le JWT |
| POST | `/api/accounts/register/` | Inscription recruteur |
| GET/PATCH | `/api/accounts/me/` | Profil du recruteur connecté |
| GET/POST | `/api/resumes/candidates/` | Lister / créer des candidats |
| GET/POST | `/api/resumes/jobs/` | Lister / créer des profils de poste |
| GET/POST | `/api/resumes/resumes/` | Lister / uploader des CV (PDF) |
| POST | `/api/resumes/resumes/{id}/analyze/` | Lancer l'analyse asynchrone d'un CV (Celery) |
| GET | `/api/analytics/dashboard/` | Dashboard recruteur : total d'analyses, score moyen, top candidats |
| GET | `/api/docs/` | Documentation Swagger interactive |
| GET | `/api/schema/` | Schéma OpenAPI |

Les analyses sont traitées de façon asynchrone : le CV passe par les statuts `uploaded` → `processing` → `analyzed` (ou `failed`). Les fichiers médias (CV) sont stockés sous `media/resumes/`.

Toutes les routes (hors register et token) nécessitent un JWT : envoyer le header `Authorization: Bearer <access_token>`.

## Tests

```bash
pytest
```

## Commandes utiles

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
celery -A config worker -l info
```
