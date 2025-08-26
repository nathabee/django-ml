#!/usr/bin/env bash
set -euo pipefail 

# shell env
set -a; [ -f .env ] && . ./.env; set +a


# choose a file
PG_DUMP="backups/pg/app_YYYY-MM-DD_HHMM.sql.gz"

# (optional) reset schema if you want a clean restore
docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c \
  "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO $POSTGRES_USER;"

# restore
gunzip -c "$PG_DUMP" | docker compose exec -T db psql -U "$POSTGRES_USER" -d "$POSTGRES_DB"
