# wipes DB & node_modules volumes for this project
docker compose --profile dev down --volumes --remove-orphans
docker volume rm django-ml_db_data django-ml_web_node_modules 2>/dev/null || true

# fresh start
docker compose --profile dev up -d --build
# then (if you didn’t automate it)
 
# --- load Pomolobee fixtures ---------------------------------------  
echo "📥 Loading fixtures into Django..."
set +e
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_superuser.json || echo "⚠️ superuser fixture failed (ok if you’ll create one interactively)"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_farms.json   || echo "⚠️ farms fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fields.json  || echo "⚠️ fields fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fruits.json  || echo "⚠️ fruits fixture failed"
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_rows.json    || echo "⚠️ rows fixture failed"


# --- load Competence fixtures --------------------------------------- 

docker compose exec django python manage.py copy_data_init || true
docker compose exec django python manage.py populate_data_init || true
docker compose exec django python manage.py create_groups_and_permissions || true
docker compose exec django python manage.py populate_teacher || true
docker compose exec django python manage.py create_translations_csv || true
docker compose exec django python manage.py populate_translation || true