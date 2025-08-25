Great start! I tweaked your “install after reset” steps to be accurate, minimal, and repeatable. Copy/paste this into your README and you’ll be golden.

---

# django-ml : Dockerized PomoloBee (Django + Next.js + Postgres + WordPress + MariaDB)

A learning stack for Docker + multi-service development:

* **Django**: Django 5 backend (REST API, JWT auth; PomoloBee code inside)
* **Web**: Next.js 14 frontend (server routes call Django)
* **DB**: Postgres 16 (persistent volume)
* **WordPress**: `wordpress` service (Apache + PHP official image)
* **WP DB**: `wpdb` service (MariaDB 11)


```mermaid
flowchart LR
  %% ====== Styles ======
  classDef svc fill:#eaf5ff,stroke:#1e88e5,stroke-width:1px,color:#0b3a67;
  classDef db  fill:#fff8e6,stroke:#fb8c00,stroke-width:1px,color:#5a3b00;
  classDef vol fill:#f6f6f6,stroke:#9e9e9e,stroke-dasharray: 4 3,color:#333;
  classDef host fill:#ffffff,stroke:#bdbdbd,color:#333;

  %% ====== Host (ports) ======
  subgraph Host["Host (localhost)"]
    direction TB
    H8080["http://localhost:8080 → Web"]:::host
    H8001["http://localhost:8001 → Django API"]:::host
    H8082["http://localhost:8082 → WordPress"]:::host
  end

  %% ====== Docker network ======
  subgraph Docker["Docker (default bridge network)"]
    direction LR

    Web["Next.js dev<br/>container: <code>django-ml-web</code><br/>port: 3000"]:::svc
    Django["Django dev server<br/>container: <code>django-ml-api</code><br/>port: 8000"]:::svc
    PG[(Postgres 16<br/>service: <code>db</code><br/>port: 5432)]:::db
    WP["WordPress 6 / PHP 8.3<br/>container: <code>django-ml-wp</code><br/>port: 80"]:::svc
    WPDB[(MariaDB 11<br/>service: <code>wpdb</code><br/>port: 3306)]:::db

    %% Service links
    Web -- "internal HTTP<br/><code>http://django:8000</code>" --> Django
    Django -- "psql 5432<br/><code>postgresql://app:app@db:5432/app</code>" --> PG
    WP -- "mysql 3306<br/><code>wpdb:3306</code>" --> WPDB

    %% Volumes & bind mounts
    Web --- VNM["volume: <code>web_node_modules</code>"]:::vol
    PG  --- VPG["volume: <code>db_data</code>"]:::vol
    WP  --- VWP["volume: <code>wp_data</code>"]:::vol
    WPDB --- VWPD["volume: <code>wp_db_data</code>"]:::vol

    Web --- BWEB["bind: <code>./web → /app</code>"]:::vol
    Django --- BDJ["bind: <code>./django → /app</code>"]:::vol
    WP --- BTH["bind: <code>./wordpress/wp-content/themes/pomolobee-theme → /var/www/html/wp-content/themes/pomolobee-theme</code>"]:::vol
    WP --- BPL["bind: <code>./wordpress/wp-content/plugins/pomolobee → /var/www/html/wp-content/plugins/pomolobee</code>"]:::vol
  end

  %% ====== Port mappings (host → containers) ======
  H8080 -->|":8080 → 3000"| Web
  H8001 -->|":8001 → 8000"| Django
  H8082 -->|":8082 → 80"|   WP
```

---

## 🚀 Getting Started (fresh / after reset)

### 0) Prereqs

* Docker 24+, Docker Compose v2

**Wipe the stack (optional destructive reset):**

```bash
docker compose --profile dev down --rmi local --volumes --remove-orphans
```

### 1) Clone

```bash
git clone <your-repo-url>
cd django-ml
```

### 2) Create project-root `.env` (one file for everything)

```env
# Django
SECRET_KEY=dev-insecure                 # replace with a real key for anything public
DEBUG=1
ALLOWED_HOSTS=*
DATABASE_URL=postgresql://app:app@db:5432/app
BYPASS_MEDIA=1

# Next.js
BACKEND_INTERNAL_URL=http://django:8000
WEB_PORT=3000

# Postgres
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=app

# WordPress / MariaDB (optional: keep defaults or set explicitly)
WP_DB_NAME=wordpress
WP_DB_USER=wp
WP_DB_PASSWORD=wp
WP_DB_ROOT_PASSWORD=root
WP_TABLE_PREFIX=wp_
```

> Tip: generate a strong Django key in dev too:
> `openssl rand -base64 48 | tr -d '\n'` → paste as `SECRET_KEY=...`

### 3) Seed web dependencies (first run only)

```bash
docker compose --profile dev run --rm web npm ci
```

* You **do not** seed Django or WordPress deps manually; Django deps are baked into the image; WordPress/wpcli use official images.

### 4) Build & start everything

```bash
docker compose --profile dev up -d --build
```

* This starts **Postgres**, **Django** (which runs `python manage.py migrate && runserver`), **Next.js** (dev server), **MariaDB** (`wpdb`) and **WordPress** (after `wpdb` is healthy).
* Don’t run `runserver` or `npx next dev` manually—compose already does it.

### 5) Sanity checks

```bash
docker compose ps
curl -s http://localhost:8001/health      # Django -> {"status":"ok"}
curl -s http://localhost:8080/api/hello   # Web (proxies backend hello)
# WordPress UI: http://localhost:8082
```

### 6) Initialize Django data (first install of this DB)

**Use fixtures to populate the database :**

 

```bash
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_superuser.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_farms.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fields.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_fruits.json
docker compose exec django python manage.py loaddata PomoloBeeCore/fixtures/initial_rows.json
```

**create a superuser interactively if you need to log**

```bash
docker compose exec django python manage.py createsuperuser
```
 

### 7) Finish WordPress installer (first run)

1. Open **[http://localhost:8082](http://localhost:8082)** and complete the standard WordPress install (site title, admin user, password).
2. Activate the **Pomolobee** theme (if not already).

### 8) Apply WordPress site options with wpcli (optional but recommended)

If you added `wpcli` service, you can run your script to set title, tagline, permalinks, and logo reproducibly:

```bash
chmod +x wordpress/wp-content/themes/pomolobee-theme/scripts/init-site.sh
docker compose run --rm wpcli bash /var/www/html/wp-content/themes/pomolobee-theme/scripts/init-site.sh
```

> Put your logo at
> `wordpress/wp-content/themes/pomolobee-theme/assets/images/logo.(png|svg)`
> The script will import it and set it as the site logo.

### 9) Export Site Editor changes back into the theme (so they live in Git)

If you customize colors/templates in **Appearance → Editor**:

* Open the **⋯** (top-right) → **Tools → Export** and download the ZIP.
* Copy the ZIP contents (e.g. `theme.json`, `templates/`, `parts/`) into:

  ```
  wordpress/wp-content/themes/pomolobee-theme/
  ```
* Commit to Git.

---

## Useful commands

**Logs / status**

```bash
docker compose --profile dev ps -a
docker compose --profile dev logs -f django
docker compose --profile dev logs -f web
docker compose --profile dev logs -f wpdb
docker compose --profile dev logs -f wordpress
```

**Stop everything**

```bash
docker compose --profile dev down
```

**Clean DB only (danger)**

```bash
docker compose --profile dev down
docker volume rm django-ml_db_data
docker compose --profile dev up -d
```

**Clean WordPress only (danger)**

```bash
docker compose --profile dev stop wordpress wpdb
docker compose --profile dev rm -f wordpress wpdb
docker volume rm django-ml_wp_db_data django-ml_wp_data
docker compose --profile dev up -d wpdb wordpress
```

**backup database django and wordpress**
in root project
```bash
bash scripts/backup.sh
``` 
---
## data structure



```text
django-ml/
├─ compose.yaml
├─ .env
├─ django/                      # Django project (config + apps)
│  ├─ manage.py
│  ├─ config/
│  └─ PomoloBeeCore/            # PomoloBee django app
│  └─ UserCore/                 # User Auth... app
├─ web/                         # Next.js app (dev server)
│  ├─ app/
│  └─ package.json
├─ wordpress/
│  └─ wp-content/
│     ├─ themes/
│     │  └─ pomolobee-theme/    # your theme (theme.json, templates, assets, scripts)
│     └─ plugins/
│        └─ pomolobee/          # (optional) your plugin
└─ (volumes managed by Docker)
   • db_data        (Postgres)
   • web_node_modules
   • wp_db_data     (MariaDB)
   • wp_data        (WordPress files)
```