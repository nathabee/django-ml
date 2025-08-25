#!/usr/bin/env bash

echo start backup
set -euo pipefail
mkdir -p backups/pg backups/wp

# shell env
set -a; [ -f .env ] && . ./.env; set +a

# Postgres
PG_FILE="backups/pg/${POSTGRES_DB:-app}_$(date +%F_%H%M).sql.gz"
docker compose exec -T db pg_dump -U "${POSTGRES_USER:-app}" -d "${POSTGRES_DB:-app}" \
  --no-owner --no-privileges | gzip > "$PG_FILE"
echo "✅ PG dump -> $PG_FILE"

# MariaDB (handles MYSQL_* or MARIADB_* names)
WP_FILE="backups/wp/${WP_DB_NAME:-wordpress}_$(date +%F_%H%M).sql.gz"
docker compose exec -T wpdb sh -lc '
  DB="${MARIADB_DATABASE:-$MYSQL_DATABASE}";
  USER="${MARIADB_USER:-$MYSQL_USER}";
  PASS="${MARIADB_PASSWORD:-$MYSQL_PASSWORD}";
  exec mariadb-dump -u"$USER" -p"$PASS" "$DB"
' | gzip > "$WP_FILE"
echo "✅ WP dump -> $WP_FILE"
