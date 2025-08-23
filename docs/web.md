# Web Service (Next.js)

The **web** service provides the frontend for the project.

- **Framework**: Next.js 14 (TypeScript, App Router)
- **Runs in dev mode** with hot reload inside Docker
- **Port**: exposed at [http://localhost:8080](http://localhost:8080)

## Features

- Fetches `api/hello` from Django backend to display a simple message.
- Includes `/welcome` page as a static route.
- Provides login form that:
  - Calls `/api/login` (proxy to Django)
  - Stores JWT access token in an HttpOnly cookie
  - Allows calling `/api/me` (proxy) to fetch authenticated user info.

## Dev Notes

- `npm install` must be seeded once into the container volume:
  ```bash
  docker compose --profile dev run --rm web npm install
````

* Next.js files live in `web/`:

  * `app/page.tsx` → home page
  * `app/welcome/page.tsx` → welcome page
  * `app/api/*` → proxy API routes (login, me)

````

---