# wipes DB & node_modules volumes for this project
docker compose --profile dev down --volumes --remove-orphans
docker volume rm django-ml_db_data django-ml_web_node_modules 2>/dev/null || true

# fresh start
docker compose --profile dev up -d --build
# then (if you didn’t automate it)
docker compose exec django python manage.py createsuperuser
docker compose exec django python manage.py loaddata PomolobeeCore/fixtures/initial_superuser.json
docker compose exec django python manage.py loaddata PomolobeeCore/fixtures/initial_farms.json
docker compose exec django python manage.py loaddata PomolobeeCore/fixtures/initial_fields.json
docker compose exec django python manage.py loaddata PomolobeeCore/fixtures/initial_fruits.json
docker compose exec django python manage.py loaddata PomolobeeCore/fixtures/initial_rows.json
