# Django Workout Planner

Simple web app that generates a workout session from selected muscle groups and a target duration.

## Stack

- Django 6 + Django REST Framework
- PostgreSQL for the main application database
- React + Vite frontend

## Local testing with Dockerized PostgreSQL

1. Ensure Docker, Docker Compose, Python 3, and npm are installed.
2. Run `make init` to create `.env` if needed, install backend dependencies into `.venv`, install frontend packages, and validate Docker Compose config.
3. Update `.env` if you need different local values.
4. Run `make run` to start PostgreSQL in Docker, apply Django migrations, then launch the backend and frontend locally.

The backend runs on `http://localhost:8000`, the frontend runs on `http://localhost:5173`, and PostgreSQL runs in Docker on `localhost:5432` using the credentials from `.env`.

## Makefile shortcuts

- `make init` prepares the local environment for first-time use.
- `make db-up` starts the PostgreSQL container and waits until it is healthy.
- `make db-down` stops the PostgreSQL container.
- `make db-logs` tails PostgreSQL container logs.
- `make db-reset` removes the PostgreSQL container and its volume.
- `make migrate` runs Django migrations using `.env` values.
- `make backend` starts the Django development server.
- `make frontend` starts the Vite development server using `VITE_*` variables from `.env`.
- `make run` starts PostgreSQL, runs migrations, then starts backend and frontend together.
- `make test` runs both backend and frontend tests.
- `make build` builds the frontend for production.

## Tests

- Backend: `python backend/manage.py test`
- Frontend: `npm test`
