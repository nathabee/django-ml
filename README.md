# django-ml (Django backend + Next.js web)

Dev stack for learning Docker + multi-service:
- **django**: Django 5 backend (dev server)
- **web**: Next.js 14 (dev server)
- **db**: Postgres 16 (persistent volume)



# seed node_modules (run once)
docker compose --profile dev run --rm web npm install

# build & run everything
docker compose --profile dev up --build
That gives you:

Web (Next.js) → http://localhost:8080

Django → http://localhost:8001

Health: /health, /api/hello



# database POSTGRES

How to verify that PASTGRES DB is created and acess it

See the DB is up and schema exists
## shell into the db container
docker exec -it $(docker ps --filter "name=django-ml-db" --format "{{.ID}}") bash
## inside:
psql -U app -d app -h localhost

-- in psql:
\dt                      -- list tables
SELECT * FROM django_migrations ORDER BY applied DESC LIMIT 5;
\q

## From Django container
docker exec -it django-ml-api bash
python manage.py showmigrations
python manage.py dbshell   # then \dt, etc.

## Where the data lives

On your host (Linux): under Docker’s volumes, typically
/var/lib/docker/volumes/db_data/_data (managed by Docker; don’t edit directly).