#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups/wp 

# shell env
set -a; [ -f .env ] && . ./.env; set +a

# dump using env from inside the container (works for MYSQL_* or MARIADB_* names)
docker compose exec -T wpdb sh -lc '
  DB="${MARIADB_DATABASE:-$MYSQL_DATABASE}";
  USER="${MARIADB_USER:-$MYSQL_USER}";
  PASS="${MARIADB_PASSWORD:-$MYSQL_PASSWORD}";
  exec mariadb-dump -u"$USER" -p"$PASS" "$DB"
' | gzip > "backups/wp/wp_${WP_DB_NAME:-wordpress}_$(date +%F_%H%M).sql.gz"

#archive the volume
docker run --rm -v django-ml_wp_data:/vol -v "$PWD/backups:/backup" alpine \
  sh -c 'cd /vol && tar czf /backup/wp_files_$(date +%F_%H%M).tgz .'

#
docker run --rm -v django-ml_wp_db_data:/vol -v "$PWD/backups:/backup" alpine \
  sh -c 'cd /vol && tar czf /backup/wp_db_volume_$(date +%F_%H%M).tgz .'
