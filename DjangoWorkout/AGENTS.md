# Repository Guidelines

## Project Structure & Module Organization
- `backend/` contains the Django project. Core settings and URL wiring live in `backend/config/`, and the workout domain lives in `backend/workouts/`.
- `backend/workouts/` holds models, API serializers/views, generation logic, admin setup, migrations, and backend tests in `tests.py`.
- `frontend/` contains the React + Vite SPA. Main UI code is in `frontend/src/`, public static assets are in `frontend/public/`, and production output is generated into `frontend/dist/`.
- Root-level config includes `requirements.txt`, `.env.example`, and `README.md`.

## Build, Test, and Development Commands
- Backend setup: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Run Django migrations: `.venv/bin/python backend/manage.py migrate`
- Start backend locally: `.venv/bin/python backend/manage.py runserver`
- Start frontend locally: `cd frontend && npm install && npm run dev`
- Run backend tests: `cd backend && ../.venv/bin/python manage.py test`
- Run frontend tests: `cd frontend && npm test`
- Build frontend: `cd frontend && npm run build`

## Coding Style & Naming Conventions
- Use 4 spaces for Python indentation and follow Django conventions for module layout.
- Use `snake_case` for Python functions/variables, `PascalCase` for Django models, and `UPPER_SNAKE_CASE` for constants.
- In React, use `PascalCase` component names, `camelCase` props/state/helpers, and keep component files in `frontend/src/`.
- Follow the existing ESLint setup in `frontend/eslint.config.js`. Avoid adding unused starter assets or dead code.

## Testing Guidelines
- Backend tests use Django’s test runner and `rest_framework.test.APIClient`.
- Frontend tests use Vitest and Testing Library.
- Name tests descriptively around behavior, for example `test_generates_workout` or `shows validation when no muscle groups are selected`.
- Add or update tests for any change to API contracts, workout generation rules, or theme behavior.

## Commit & Pull Request Guidelines
- Current history uses short, imperative commit subjects such as `Add web tic-tac-toe game` and `Separated two projects`. Keep that style.
- Prefer focused commits with a single intent.
- PRs should include: a short summary, impacted areas (`backend`, `frontend`, or both), test results, and screenshots for visible UI changes.

## Security & Configuration Tips
- Copy `.env.example` to `.env` and keep secrets out of git.
- PostgreSQL is the default app database; tests fall back to SQLite.
- Do not commit `.venv/`, `frontend/node_modules/`, or generated build output unless explicitly required.
