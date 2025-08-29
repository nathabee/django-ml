#!/usr/bin/env bash
set -euo pipefail

PROFILE=${PROFILE:-dev}

# --- helpers ----------------------------------------------------
abort() { echo "❌ $*" >&2; exit 1; }

yes_no() {
  # yes_no "Question?" default_yes|default_no
  local q="$1" def="${2:-default_no}" ans
  local prompt="[y/N]"; [[ "$def" == "default_yes" ]] && prompt="[Y/n]"
  read -r -p "$q $prompt " ans || true
  ans="${ans,,}"  # to lowercase
  if [[ -z "$ans" ]]; then
    [[ "$def" == "default_yes" ]] && return 0 || return 1
  fi
  [[ "$ans" =~ ^y(es)?$ ]]
}

need() { command -v "$1" >/dev/null 2>&1 || abort "Missing dependency: $1"; }

wait_http_200() {
  # wait_http_200 URL TIMEOUT_SECONDS
  local url="$1" timeout="${2:-60}" t=0
  echo "⏳ Waiting for $url ..."
  until curl -fsS "$url" >/dev/null 2>&1; do
    sleep 2; t=$((t+2))
    if (( t >= timeout )); then
      echo "⚠️  Timed out waiting for $url"; return 1
    fi
  done
  echo "✅ $url is up"
}

# --- sanity & env ------------------------------------------------
need docker
need bash

# must be repo root (compose file present)
[[ -f "compose.yaml" || -f "docker-compose.yml" ]] || abort "Run from project root (compose.yaml not found)."

# .env required
[[ -f .env ]] || abort "Missing .env in project root. First clone repo (e.g. git clone git@github.com:nathabee/ml-django.git) and create .env."

# load .env (export all vars temporarily)
set -a; source ./.env; set +a

echo "ℹ️  Running from repo root: $(pwd)"
echo "ℹ️  This is a development helper. Do NOT use in production."
echo

# --- full reset prompt ------------------------------------------
if ! yes_no "Are you sure you want a TOTAL RESET of Docker resources (images, containers, *volumes*)? This ERASES all data." default_no; then
  echo "➡️  Cancelled."
  exit 0
fi

# --- down & prune ------------------------------------------------
if yes_no "Remove containers/images/volumes now?" default_yes; then
  echo "🧹 docker compose --profile $PROFILE down --rmi local --volumes --remove-orphans"
  docker compose --profile "$PROFILE" down --rmi local --volumes --remove-orphans
else
  echo "➡️  Skipping prune."
fi

# --- seed web deps (1st time) -----------------------------------
echo "📦 Seeding web/node modules (npm ci in one-off container)..."
docker compose --profile "$PROFILE" run --rm web npm ci


# migrate
docker compose --profile dev exec django bash -lc "
python manage.py makemigrations usercore &&
python manage.py makemigrations pomolobeecore competencecore &&
python manage.py showmigrations &&
python manage.py migrate --noinput
"


# --- up ----------------------------------------------------------
echo "🚀 Starting stack"
docker compose --profile "$PROFILE" up -d --build




# --- wait for Django --------------------------------------------
# Django maps host 8001 -> container 8000
wait_http_200 "http://localhost:8001/health" 90 || true

# --- load Django Migration if necessary --------------------------------------- 

# --- migrations -------------------------------------------------
echo "🛠 Running makemigrations..."
docker compose exec django python manage.py makemigrations --noinput

echo "🛠 Running migrate..."
docker compose exec django python manage.py migrate --noinput





# --- create superuser (optional) --------------------------------
echo "Create Django superuser now?" 
docker compose exec django python manage.py createsuperuser

# create and set perms inside the container
docker compose exec django bash -lc "mkdir -p /app/media && chown -R 1000:1000 /app/media"
docker compose exec django bash -lc 'cat > /app/media/.htaccess << "EOF"
Options -Indexes
<FilesMatch "\.(php|phps|phtml|phar)$">
  Require all denied
</FilesMatch>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/* "access plus 30 days"
</IfModule>
EOF'


# --- WordPress init ---------------------------------------------
echo "Run WordPress init script activate theme, permalinks, logo?"
echo "📋 Open WordPress installer at: http://localhost:8082"
echo "   Create the initial admin user, then return here."
if yes_no "Ready?" default_no; then
  #  wp-perms.sh is called in wp-init.sh
  if [[ -x ./scripts/wp-init.sh ]]; then
    ./scripts/wp-init.sh
  else
    echo "⚠️ ./scripts/wp-init.sh not found or not executable skipping."
  fi
fi





# --- load Pomolobee fixtures ---------------------------------------  
echo "📥 Loading fixtures into Django..."
set +e
docker compose exec django python manage.py seed_pomolobee --clear
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_superuser.json || echo "⚠️ superuser fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_farms.json   || echo "⚠️ farms fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fields.json  || echo "⚠️ fields fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fruits.json  || echo "⚠️ fruits fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_rows.json    || echo "⚠️ rows fixture failed"


# --- load Competence fixtures --------------------------------------- 
docker compose exec django python manage.py seed_competence --clear  
docker compose exec django python manage.py populate_data_init || true
docker compose exec django python manage.py create_groups_and_permissions || true
docker compose exec django python manage.py populate_teacher || true
docker compose exec django python manage.py create_translations_csv || true
docker compose exec django python manage.py populate_translation || true
set -e
 

# --- health checks ----------------------------------------------
echo "Run health checks now?" 
if [[ -x ./scripts/health-check.sh ]]; then
  ./scripts/health-check.sh
else
  echo "⚠️ ./scripts/health-check.sh not found or not executable skipping."
fi
 

echo
echo "✅ Done."
echo "🖥  Web:     http://localhost:8080"
echo "🔌 Django:  http://localhost:8001 health, /api/user/hello"
echo "📝 WP:      http://localhost:8082"
