# Django Workout Planner

Simple web app that generates a workout session from selected muscle groups and a target duration.

## Stack

- Django 6 + Django REST Framework
- PostgreSQL for the main application database
- React + Vite frontend

## Backend setup

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and update the PostgreSQL values.
4. Run `python backend/manage.py migrate`.
5. Start the API with `python backend/manage.py runserver`.

## Frontend setup

1. In `frontend/`, run `npm install`.
2. Set `VITE_API_BASE_URL` in `.env` if needed.
3. Start the app with `npm run dev`.

## Makefile shortcuts

- `make setup` creates `.venv`, installs Python dependencies, and installs frontend packages.
- `make env` copies `.env.example` to `.env` if needed.
- `make migrate` runs Django migrations.
- `make backend` starts the Django development server.
- `make frontend` starts the Vite development server.
- `make dev` starts the backend in the background and the frontend in the foreground.
- `make test` runs both backend and frontend tests.
- `make build` builds the frontend for production.

## Tests

- Backend: `python backend/manage.py test`
- Frontend: `npm test`
