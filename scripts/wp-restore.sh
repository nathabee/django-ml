#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups/wp 

WP_DUMP="backups/wp/wp_wordpress_YYYY-MM-DD_HHMM.sql.gz"

docker compose exec -T wpdb sh -lc '
  DB="${MARIADB_DATABASE:-$MYSQL_DATABASE}";
  USER="${MARIADB_USER:-$MYSQL_USER}";
  PASS="${MARIADB_PASSWORD:-$MYSQL_PASSWORD}";
  exec mariadb -u"$USER" -p"$PASS" "$DB"
' < <(gunzip -c "$WP_DUMP")
