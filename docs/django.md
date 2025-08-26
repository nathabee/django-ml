# Django Service (Backend API)

The **django** service provides the backend API and authentication.

- **Framework**: Django 5 + Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt`
- **Port**: exposed at [http://localhost:8001](http://localhost:8001)

## Endpoints

- `/health` → simple health check
- `/api/hello` → returns a "Hello from Django" message
- `/api/auth/login` → accepts `{username, password}`, returns JWT access/refresh
- `/api/auth/refresh` → renews an access token
- `/api/me` → requires `Authorization: Bearer <token>`, returns current user info

## Database

- Uses **Postgres 16** (service `db`)
- Connection: `postgresql://app:app@db:5432/app`
- Tables are created via migrations at startup
- Users managed via Django’s built-in auth system

### Create a user for testing

```bash
docker exec -it django-ml-api bash -lc "python manage.py createsuperuser"
````

## Dev Notes

* API auto-reloads in dev mode inside Docker.
* Data persists in the Docker volume `django-ml_db_data`.

```

---