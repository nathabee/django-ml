# django-ml

A learning stack for Docker + multi-service development:

- **Django**: Django 5 backend (dev server, REST API, auth)
- **Web**: Next.js 14 frontend (dev server)
- **DB**: Postgres 16 (persistent volume)

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd django-ml
````

### 2. Install dependencies (run once)

```bash
docker compose --profile dev run --rm web npm install
```

### 3. Build & run all services

```bash
docker compose --profile dev up --build
```

### 4. Access the stack

* **Web (Next.js)** → [http://localhost:8080](http://localhost:8080)
* **Django API** → [http://localhost:8001](http://localhost:8001)
* Health checks: `/health`, `/api/hello`

---

## 🗄 Database (Postgres)

Check DB schema:

```bash
# open psql inside db container
docker exec -it $(docker ps --filter "name=django-ml-db" --format "{{.ID}}") bash
psql -U app -d app -h localhost
\dt   -- list tables
```

From Django side:

```bash
docker exec -it django-ml-api bash
python manage.py showmigrations
python manage.py dbshell
```

Data is persisted in Docker volume `django-ml_db_data`.

---

## 🔑 Authentication (JWT)

Authentication is handled directly by the Django service using **Django REST Framework + SimpleJWT**.

### Create a user

```bash
docker exec -it django-ml-api bash -lc "python manage.py createsuperuser"
```

### Login

```bash
curl -s -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"<youruser>","password":"<yourpass>"}' | jq
```

This returns `{ "access": "...", "refresh": "..." }`.

### Call protected route

```bash
ACCESS=<paste-token>
curl -s http://localhost:8001/api/me \
  -H "Authorization: Bearer $ACCESS" | jq
```

### Web Integration

The Next.js frontend includes:

* a login form (POSTs to `/api/login`)
* sets an HttpOnly cookie with the token
* fetches `/api/me` through a server route that forwards the JWT

---