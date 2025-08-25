# django-ml

A learning stack for Docker + multi-service development:

- **Django**: Django 5 backend (REST API, JWT auth)
- **Web**: Next.js 14 frontend (dev server, server routes proxy to Django)
- **DB**: Postgres 16 (persistent volume)

---

## 🚀 Getting Started

### 0) Prereqs
- Docker 24+, Docker Compose v2

### 1) Clone
```bash
git clone <your-repo-url>
cd django-ml
````

### 2) Create a project-root `.env`

```env
# Django
SECRET_KEY=dev-insecure
DEBUG=1
ALLOWED_HOSTS=*
DATABASE_URL=postgresql://app:app@db:5432/app
BYPASS_MEDIA=1

# Next.js
BACKEND_INTERNAL_URL=http://django:8000
WEB_PORT=3000

# Postgres
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=app
```

### 3) Seed web dependencies (first time)

```bash
docker compose --profile dev run --rm web npm ci
```

> Use `npm install` only when you add/update packages locally.

### 4) Build & run

**One-liner (dev):**
it starts the services and (in your compose) runs migrations automatically. it does not create a user not initialise data the first time
the next docker command will in fact execute "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

```bash
docker compose --profile dev up -d --build
```

this is equivalent to the 3 commands:

```bash
docker compose --profile dev build
docker compose --profile dev up -d
docker compose exec django python manage.py migrate

``` 

**for the first installation we also need to create a superuser or load fixtures.**

```bash
docker compose exec django python manage.py createsuperuser
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_superuser.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_farms.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fields.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fruits.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_rows.json
```

### 5) Sanity checks

```bash
# Show final config after .env interpolation
docker compose config

# Ensure schema exists
docker compose exec django python manage.py migrate

# Smoke
curl -s http://localhost:8001/health
curl -s http://localhost:8001/api/hello
```

### 6) Access

* **Web (Next.js)** → [http://localhost:8080](http://localhost:8080)
* **Django API** → [http://localhost:8001](http://localhost:8001)
* Health checks: `/health`, `/api/hello`

---

## 🗄 Database (Postgres)

From **Django**:

```bash
docker compose exec django python manage.py showmigrations
# dbshell needs psql installed in the image; otherwise use the db container:
# docker compose exec django python manage.py dbshell
```

From **Postgres**:

```bash
docker compose exec db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
\dt   -- list tables
```

Data persists in the `django-ml_db_data` volume.

---

## 🔑 Authentication (JWT)

Create a user:

```bash
docker compose exec django python manage.py createsuperuser
```

Login:

```bash
curl -s -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"<user>","password":"<pass>"}' | jq
# => { "access": "...", "refresh": "..." }
```

Call protected route:

```bash
ACCESS=<paste_access_token>
curl -s http://localhost:8001/api/me -H "Authorization: Bearer $ACCESS" | jq
```

**Web integration:** the Next.js app uses server routes (e.g. `/api/hello`, `/api/login`, `/api/me`) to proxy to `http://django:8000/...` inside the Docker network, so the browser stays same-origin (no CORS).

---

## 🛠 Useful commands

Logs:

```bash
docker compose --profile dev logs -f web
docker compose --profile dev logs -f django
```

Rebuild web deps cleanly:

```bash
docker compose down
docker volume rm django-ml_web_node_modules
docker compose --profile dev run --rm web npm ci
docker compose --profile dev up -d
```

Tear down:

```bash
docker compose down
# add -v to remove volumes if you want a clean DB
# docker compose down -v
```


Work just on django image/container:

```bash
# rebuild only the django image
docker compose --profile dev build django

# (re)create/start only the django container
docker compose --profile dev up -d django

# see logs for django
docker compose --profile dev logs -f django

```
These commands :
* won’t remove your Postgres data, node_modules, or any files on your host bind mounts.
* won’t delete old images automatically (use prune or --rmi flags).

---

## 🧹 Clean reinstall / full reset (DANGER: deletes data)

> ⚠️ This will remove containers, images built by this project, and **all persistent data** (Postgres DB volume, web `node_modules` volume). Do this only if you really want a fresh start.

### One-liner (destructive)
```bash
# stop & remove containers, project network, volumes, and images built by compose
docker compose --profile dev down --rmi local --volumes --remove-orphans

``` 

### or step by step (destructive)


```bash
# 1) Stop containers (and remove the project network)
docker compose --profile dev down --remove-orphans

# 2) List project volumes (DB + web node_modules)
docker volume ls | grep '^local\s\+django-ml_'
#   typically: django-ml_db_data, django-ml_web_node_modules

# 3) Remove project volumes (DELETES DB DATA)
docker volume rm django-ml_db_data django-ml_web_node_modules

# (Optional) remove any other project volumes that might exist
docker volume ls --filter name=django-ml_ -q | xargs -r docker volume rm

# 4) List images built by this repo
docker images | grep -E '^django-ml-(django|web)\s'

# 5) Remove those images
docker rmi django-ml-django django-ml-web 2>/dev/null || true
# (or) remove by pattern:
docker images --format '{{.Repository}}:{{.Tag}} {{.ID}}' \
  | grep '^django-ml-' \
  | awk '{print $2}' \
  | xargs -r docker rmi -f

# 6) (Optional) prune dangling images & build cache (global)
docker image prune -f
# docker builder prune -f          # prune build cache
# docker system prune -f --volumes # ⚠️ VERY destructive across ALL projects


``` 

###  Data persistency

 Where persistence lives in your stack

* **Postgres data** → named volume: `django-ml_db_data`
* **Web `node_modules`** → named volume: `django-ml_web_node_modules`
* **Django files on disk** (e.g., `media/`, `staticfiles/`) → in your **host repo** because you bind-mount `./django:/app`
  (so those persist as normal files in your project folder)

---

#### How to remove/reset persistent data

##### Nuke everything for this project (containers + volumes + local images)

```bash
docker compose --profile dev down --rmi local --volumes --remove-orphans
```

##### Or, remove specific pieces only

**Postgres data (DB reset):**

```bash
docker volume rm django-ml_db_data
# then recreate & migrate
docker compose --profile dev up -d db
docker compose --profile dev up -d django
docker compose exec django python manage.py migrate
```

**Web node\_modules volume (reseed deps):**

```bash
docker volume rm django-ml_web_node_modules
docker compose --profile dev run --rm web npm ci
```

**Django uploaded media & collected static (because they’re on your host):**

```bash
rm -rf django/media/*           # only if you want to delete uploads
rm -rf django/staticfiles/*     # only if you ran collectstatic and want to reset
# optionally clear pyc
find django -name '__pycache__' -type d -prune -exec rm -rf {} +
```

**Remove just the django container (not the image/volumes):**

```bash
docker compose rm -sf django
```

**Force a fresh image for Django only:**

```bash
docker compose --profile dev build --no-cache django
docker compose --profile dev up -d django
```

---

## 📝 Notes

* Next.js dev server binds to `0.0.0.0:3000` and is exposed as `http://localhost:8080`.
* The browser must **not** call `http://django:8000` directly. Use the Next.js server routes (`/api/...`) which proxy to Django internally.
* In dev you shouldn’t need CORS; if you decide to call Django from the browser, enable CORS in Django and point the frontend to `http://localhost:8001`.

```
 