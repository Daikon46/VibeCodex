SHELL := /bin/bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PYTHON) backend/manage.py
NPM := npm --prefix frontend
COMPOSE := docker compose
ENV_FILE := .env

.PHONY: help check-python check-npm check-docker check-compose backend-install frontend-install env init migrate backend frontend run db-up db-down db-logs db-reset backend-test frontend-test test build lint

help:
	@printf "Available targets:\n"
	@printf "  make init            Create .env if needed, install backend/frontend dependencies, and validate Docker Compose config\n"
	@printf "  make env             Copy .env.example to .env if it does not already exist\n"
	@printf "  make db-up           Start the PostgreSQL container and wait for it to become healthy\n"
	@printf "  make db-down         Stop the PostgreSQL container\n"
	@printf "  make db-logs         Tail PostgreSQL container logs\n"
	@printf "  make db-reset        Remove the PostgreSQL container and its persistent volume\n"
	@printf "  make migrate         Run Django migrations using .env values\n"
	@printf "  make backend         Start the Django development server\n"
	@printf "  make frontend        Start the Vite development server with VITE_* vars from .env\n"
	@printf "  make run             Start PostgreSQL, run migrations, then start backend and frontend locally\n"
	@printf "  make backend-test    Run Django tests\n"
	@printf "  make frontend-test   Run frontend tests\n"
	@printf "  make test            Run backend and frontend tests\n"
	@printf "  make build           Build the frontend for production\n"
	@printf "  make lint            Run the frontend linter\n"

check-python:
	@command -v python3 >/dev/null || { echo "python3 is required"; exit 1; }

check-npm:
	@command -v npm >/dev/null || { echo "npm is required"; exit 1; }

check-docker:
	@command -v docker >/dev/null || { echo "docker is required"; exit 1; }

check-compose: check-docker
	@$(COMPOSE) version >/dev/null

$(PYTHON): check-python
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

backend-install: $(PYTHON)

frontend-install: check-npm
	$(NPM) install

env:
	@if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); fi

init: env backend-install frontend-install check-compose
	@$(COMPOSE) config >/dev/null

migrate: env backend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(MANAGE) migrate'

backend: env backend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(MANAGE) runserver'

frontend: env frontend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(NPM) run dev -- --host 127.0.0.1'

db-up: env check-compose
	@$(COMPOSE) up -d --wait postgres

db-down: check-compose
	@$(COMPOSE) stop postgres

db-logs: check-compose
	@$(COMPOSE) logs -f postgres

db-reset: check-compose
	@$(COMPOSE) down -v

run: init db-up migrate
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(MANAGE) runserver & \
	BACKEND_PID=$$!; \
	trap 'kill $$BACKEND_PID' EXIT INT TERM; \
	$(NPM) run dev -- --host 127.0.0.1'

backend-test: backend-install
	cd backend && ../$(PYTHON) manage.py test

frontend-test: frontend-install
	$(NPM) test

test: backend-test frontend-test

build: frontend-install
	$(NPM) run build

lint: frontend-install
	$(NPM) run lint
