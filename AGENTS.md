# AGENTS.md — longitudinal-edc

Longitudinal EDC (Electronic Data Capture): a Django web platform for hospitals to manage clinical studies — enroll patients, schedule visits with time windows, capture form data, and export datasets.

## Quick start

```bash
docker compose up --build          # start all services (db, redis, web, worker)
docker compose run --rm web python manage.py <command>   # one-off mgmt commands
docker compose exec web python manage.py <command>       # exec against running container
```

Open http://localhost:8000. Admin at `/admin/` (credentials: `Aditya` / `Aditya123`).

## Running all commands inside Docker

**Every** management command must run via `docker compose run --rm web` or `docker compose exec web`. There is no local virtualenv — all code runs inside the `web` container.

```bash
docker compose run --rm web python manage.py makemigrations
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
docker compose run --rm web python manage.py test apps/studies apps/participants apps/forms apps/audit apps/exports
```

To get a shell inside a running container:
```bash
docker compose exec web bash
docker compose exec db bash          # then `psql -h db -U appuser -d appdb`
```

## Project structure

```
config/               # Django project config (settings, urls, celery, wsgi, asgi)
apps/
  studies/            # Studies CRUD, dashboard, VisitType model, participant enrollment
  participants/       # Participant & Visit models, auto-scheduling, VisitDeviation
  forms/              # Dynamic form templates (JSON schema) + form responses
  audit/              # AuditLog, signals wired to Study/Participant/Visit/FormResponse
  exports/            # ExportJob, Celery CSV export tasks
templates/            # Global templates (base.html, registration/login.html)
```

## 5 Django apps — current state

| App | What it owns | Status |
|---|---|---|
| `studies` | Study, VisitType models; dashboard, CRUD, participant add/edit/delete | Working with pagination, search, stats cards |
| `participants` | Participant, Visit, VisitDeviation; auto-scheduling | Working with signals, services, deviation tracking |
| `forms` | FormTemplate (JSON schema), FormResponse | Working with required/select/checkbox/date, edit existing |
| `audit` | AuditLog model, signals, views, templates | Wired — logs CREATE/UPDATE/DELETE/SUBMIT_FORM |
| `exports` | ExportJob model, Celery CSV export tasks | Working — create, run async, download |

## Scheduling system

Visit types/timing can come from **either** the DB (`VisitType` per study, configured during study creation) **or** the hardcoded fallback in `apps/participants/protocol.py`. The `services.py` scheduler tries DB first, then falls back to `VISIT_SCHEDULE`.

Auto-scheduling runs via `post_save` signal on `Participant` (`apps/participants/signals.py` → `services.py`). Only fires on creation; skips if visits already exist.

## Custom template filters

`apps/studies/templatetags/study_extras.py` provides a `get_item` filter for dict/attribute access in templates. Load with `{% load study_extras %}`.

## Known fixed bugs

- `Visit.__str__` now uses `self.visit_code` (was `self.visit_type`)
- `FormResponse.__str__` now uses `self.template.name` (was `self.form_name`)
- All routes now have consistent trailing slashes
- `forms/urls.py` URL pattern fixed (was missing `visit_id` parameter)

## Environment & services

- **Database**: PostgreSQL 16 at `db:5432`, user `appuser` / `apppass`, database `appdb`
- **Redis**: `redis://redis:6379/0` — used as Celery broker
- **Celery**: `worker` container runs `celery -A config worker -l info`; tasks defined in `apps/exports/tasks.py`
- **Settings**: env vars set in `docker-compose.yml` — no `.env` file needed

## Features implemented

All 20 features from `remaining_features.md` are implemented. Key additions:
1. **Study Setup** — VisitType model per study, configured during study create/edit
2. **Visit Detail/Complete/Validation** — Enhanced page with deviation tracking, window validation
3. **Deviation Model** — `VisitDeviation` with reason, created_by, timestamp
4. **Audit Trail** — Signals on Study/Participant/Visit/FormResponse; browsable log with filters
5. **CSV Export via Celery** — Async export tasks, job status tracking, download
6. **Forms Improvements** — Supports `required`, `select` (with options), `checkbox`, `date` in schema
7. **View/Edit Submitted Forms** — View response page, edit existing submissions
8. **Edit/Delete Operations** — Edit/delete for studies and participants with confirmation
9. **Authentication** — Login/logout via django.contrib.auth; nav shows user state
10. **Dashboard Cards** — Total studies, participants, overdue counts
11. **Search/Pagination/Filters** — Study search, participant search+filter, all lists paginated
12. **REST API** — `/api/` endpoints for studies, participants, visits, form-templates, form-responses
13. **Tests** — Test files for all 5 apps covering models, views, scheduling, audit

## Style conventions

- Django apps use `apps.<app_name>` as the Python package path (e.g., `apps.studies`, `apps.participants.apps.ParticipantsConfig`)
- Models in `apps/<app>/models.py`; views in `apps/<app>/views.py`
- Templates use Bootstrap 5.3, extend `templates/base.html`
- Signal imports go in `apps/<app>/apps.py` `ready()` method
- Template filters in `apps/studies/templatetags/`

## DB access

```bash
docker compose exec db bash
psql -h db -U appuser -d appdb
# Password: apppass
```
