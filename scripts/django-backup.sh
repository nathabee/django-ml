#!/usr/bin/env bash
set -euo pipefail
mkdir -p backups/pg 

# shell env
set -a; [ -f .env ] && . ./.env; set +a


# loads your .env into the shell (so $POSTGRES_DB etc. expand)
set -a; . ./.env; set +a

# dump and gzip into backups/pg/
docker compose exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" \
  --no-owner --no-privileges \
| gzip > "backups/pg/${POSTGRES_DB}_$(date +%F_%H%M).sql.gz"



#archive the volume
docker run --rm -v django-ml_db_data:/vol -v "$PWD/backups:/backup" alpine \
  sh -c 'cd /vol && tar czf /backup/pg_volume_$(date +%F_%H%M).tgz .'