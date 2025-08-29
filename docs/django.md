# Django Service (Backend API)

The **django** service provides the backend API and authentication.

- **Framework**: Django 5 + Django REST Framework
- **Auth**: JWT via `djangorestframework-simplejwt`
- **Port**: exposed at [http://localhost:8001](http://localhost:8001)

## Endpoints
- userApi :  `/api/user`
- pomolobee Api :  `/api/pomolobee/`
- competence Api :  `/api/competence`


### user endpoints (UserCore)
- userApi + `/health` → simple health check
- userApi + `/hello` → returns a "Hello from Django" message
- userApi + `/auth/login` → accepts `{username, password}`, returns JWT access/refresh
- userApi + `/auth/refresh` → renews an access token
- userApi + `/me` → requires `Authorization: Bearer <token>`, returns current user info

## Database

- Uses **Postgres 16** (service `db`)
- Connection: `postgresql://app:app@db:5432/app`
- Tables are created via migrations at startup
- Users managed via Django’s built-in auth system

### datafile system

In order to be able to serve the django media file with apache, we create a named volume media_data.
-Mount it in Django at /app/media (Django writes here).
-Mount the same volume in WordPress (Apache) at /var/www/html/media (Apache serves it).
-Set MEDIA_ROOT=/app/media and MEDIA_URL=/media/ in Django.

Frontend / URLs :
This way, we can access Django media at http://localhost:8082/media/... 
and WP uploads at http://localhost:8082/wp-content/uploads/....

 
### Create a user for testing

```bash
docker exec -it beelab-api bash -lc "python manage.py createsuperuser"
````

## Dev Notes

* API auto-reloads in dev mode inside Docker.
* Data persists in the Docker volume `beelab_db_data`.
 


---

### Test django with CURL

#### create superuser to test a superuser



```bash
# we create pomotest/pomotest
docker compose exec django python manage.py createsuperuser

````

#### get token

```bash
 curl -s -X POST http://localhost:8001/api/auth/login   -H 'content-type: application/json'   -d '{"username":"pomotest","password":"pomotest"}'

 # set the value of ACCESS with the token value
 
 ACCESS=
````

###
````bash
curl -s -H "Authorization: Bearer <TOKEN>" http://localhost:8001/api/pomolobee/farms/ | jq
````