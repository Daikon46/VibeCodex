SHELL := /bin/bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PYTHON) backend/manage.py
NPM := npm --prefix frontend
COMPOSE := docker compose
ENV_FILE := .env
RUNTIME_DIR := .run
BACKEND_PID_FILE := $(RUNTIME_DIR)/backend.pid
FRONTEND_PID_FILE := $(RUNTIME_DIR)/frontend.pid
BACKEND_LOG_FILE := $(RUNTIME_DIR)/backend.log
FRONTEND_LOG_FILE := $(RUNTIME_DIR)/frontend.log
SUPERUSER_USERNAME ?= admin
SUPERUSER_EMAIL ?= admin@example.com
SUPERUSER_PASSWORD ?= admin123

.PHONY: help check-python check-npm check-docker check-compose backend-install frontend-install init migrate ensure-superuser backend frontend run check stop db-pull db-up db-down db-logs db-reset backend-test frontend-test test build lint

help:
	@printf "Essential commands:\n"
	@printf "  make init            Create .env if needed, install backend/frontend dependencies, and validate Docker Compose config\n"
	@printf "  make run             Start PostgreSQL, run migrations, then start backend and frontend headlessly\n"
	@printf "  make check           Show whether postgres, backend, and frontend are running\n"
	@printf "  make stop            Stop backend, frontend, and PostgreSQL to free ports\n"
	@printf "\nOther commands:\n"
	@printf "  make db-pull         Pull the PostgreSQL image with retries for transient network issues\n"
	@printf "  make db-up           Start the PostgreSQL container and wait for it to become healthy\n"
	@printf "  make db-down         Stop the PostgreSQL container\n"
	@printf "  make db-logs         Tail PostgreSQL container logs\n"
	@printf "  make db-reset        Remove the PostgreSQL container and its persistent volume\n"
	@printf "  make migrate         Run Django migrations using .env values\n"
	@printf "  make ensure-superuser Create the Django admin user if it does not exist\n"
	@printf "  make backend         Start the Django development server\n"
	@printf "  make frontend        Start the Vite development server with VITE_* vars from .env\n"
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

init: backend-install frontend-install check-compose
	@if [ ! -f $(ENV_FILE) ]; then cp .env.example $(ENV_FILE); fi
	@$(COMPOSE) config >/dev/null

migrate: backend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(MANAGE) migrate'

ensure-superuser: backend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; \
	export DJANGO_SUPERUSER_USERNAME="$${DJANGO_SUPERUSER_USERNAME:-$(SUPERUSER_USERNAME)}"; \
	export DJANGO_SUPERUSER_EMAIL="$${DJANGO_SUPERUSER_EMAIL:-$(SUPERUSER_EMAIL)}"; \
	export DJANGO_SUPERUSER_PASSWORD="$${DJANGO_SUPERUSER_PASSWORD:-$(SUPERUSER_PASSWORD)}"; \
	$(MANAGE) shell -c "from django.contrib.auth import get_user_model; import os; User = get_user_model(); username = os.environ[\"DJANGO_SUPERUSER_USERNAME\"]; email = os.environ[\"DJANGO_SUPERUSER_EMAIL\"]; password = os.environ[\"DJANGO_SUPERUSER_PASSWORD\"]; user, created = User.objects.update_or_create(username=username, defaults={\"email\": email, \"is_staff\": True, \"is_superuser\": True}); user.set_password(password); user.save(); print(\"Created Django superuser.\" if created else \"Ensured Django superuser exists.\")"'

backend: backend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(MANAGE) runserver'

frontend: frontend-install
	@bash -lc 'set -a; source $(ENV_FILE); set +a; $(NPM) run dev -- --host 127.0.0.1'

db-pull: check-compose
	@bash -lc 'set -a; source $(ENV_FILE); set +a; \
	attempt=1; \
	max_attempts=3; \
	while [ $$attempt -le $$max_attempts ]; do \
		echo "Pulling postgres image (attempt $$attempt/$$max_attempts)..."; \
		if $(COMPOSE) pull postgres; then \
			exit 0; \
		fi; \
		if [ $$attempt -lt $$max_attempts ]; then \
			echo "Pull failed. Waiting before retrying..."; \
			sleep $$((attempt * 3)); \
		fi; \
		attempt=$$((attempt + 1)); \
	done; \
	echo "Failed to pull the PostgreSQL image after $$max_attempts attempts."; \
	echo "Check Docker daemon access, internet connectivity, DNS, VPN/proxy settings, then retry."; \
	exit 1'

db-up: db-pull
	@$(COMPOSE) up -d --wait postgres

db-down: check-compose
	@$(COMPOSE) stop postgres

db-logs: check-compose
	@$(COMPOSE) logs -f postgres

db-reset: check-compose
	@$(COMPOSE) down -v

run: init db-up migrate ensure-superuser
	@mkdir -p $(RUNTIME_DIR)
	@bash -lc 'if [ -f "$(BACKEND_PID_FILE)" ] && kill -0 "$$(cat "$(BACKEND_PID_FILE)")" 2>/dev/null; then \
		echo "Backend is already running with PID $$(cat "$(BACKEND_PID_FILE)")"; \
	else \
		rm -f "$(BACKEND_PID_FILE)"; \
		nohup bash -lc '\''set -a; source "$(ENV_FILE)"; set +a; $(MANAGE) runserver'\'' >"$(BACKEND_LOG_FILE)" 2>&1 & \
		echo $$! >"$(BACKEND_PID_FILE)"; \
		echo "Started backend (PID $$!). Log: $(BACKEND_LOG_FILE)"; \
	fi'
	@bash -lc 'if [ -f "$(FRONTEND_PID_FILE)" ] && kill -0 "$$(cat "$(FRONTEND_PID_FILE)")" 2>/dev/null; then \
		echo "Frontend is already running with PID $$(cat "$(FRONTEND_PID_FILE)")"; \
	else \
		rm -f "$(FRONTEND_PID_FILE)"; \
		nohup bash -lc '\''set -a; source "$(ENV_FILE)"; set +a; $(NPM) run dev -- --host 127.0.0.1'\'' >"$(FRONTEND_LOG_FILE)" 2>&1 & \
		echo $$! >"$(FRONTEND_PID_FILE)"; \
		echo "Started frontend (PID $$!). Log: $(FRONTEND_LOG_FILE)"; \
	fi'
	@echo "Backend:  http://127.0.0.1:8000"
	@echo "Admin:    http://127.0.0.1:8000/admin/"
	@echo "Frontend: http://127.0.0.1:5173"
	@echo "PostgreSQL: localhost:5432"
	@bash -lc 'set -a; source $(ENV_FILE); set +a; \
	echo "Superuser username: $${DJANGO_SUPERUSER_USERNAME:-$(SUPERUSER_USERNAME)}"; \
	echo "Superuser email:    $${DJANGO_SUPERUSER_EMAIL:-$(SUPERUSER_EMAIL)}"; \
	echo "Superuser password: $${DJANGO_SUPERUSER_PASSWORD:-$(SUPERUSER_PASSWORD)}"'
	@echo "Use 'make check' to inspect status and 'make stop' to stop services."

check:
	@bash -lc 'if docker ps --format "{{.Names}}" >/dev/null 2>&1; then \
		if docker ps --format "{{.Names}}" | grep -qx "django-workout-postgres"; then \
			echo "postgres: running"; \
		else \
			echo "postgres: stopped"; \
		fi; \
	else \
		echo "postgres: unknown (Docker unavailable)"; \
	fi; \
	if [ -f "$(BACKEND_PID_FILE)" ] && kill -0 "$$(cat "$(BACKEND_PID_FILE)")" 2>/dev/null; then \
		echo "backend: running (PID $$(cat "$(BACKEND_PID_FILE)"))"; \
	else \
		echo "backend: stopped"; \
	fi; \
	if [ -f "$(FRONTEND_PID_FILE)" ] && kill -0 "$$(cat "$(FRONTEND_PID_FILE)")" 2>/dev/null; then \
		echo "frontend: running (PID $$(cat "$(FRONTEND_PID_FILE)"))"; \
	else \
		echo "frontend: stopped"; \
	fi'

stop:
	@bash -lc 'if [ -f "$(BACKEND_PID_FILE)" ]; then \
		pid="$$(cat "$(BACKEND_PID_FILE)")"; \
		if kill -0 "$$pid" 2>/dev/null; then \
			kill "$$pid" && echo "Stopped backend (PID $$pid)"; \
		else \
			echo "Backend was not running"; \
		fi; \
		rm -f "$(BACKEND_PID_FILE)"; \
	else \
		echo "Backend was not running"; \
	fi'
	@bash -lc 'if [ -f "$(FRONTEND_PID_FILE)" ]; then \
		pid="$$(cat "$(FRONTEND_PID_FILE)")"; \
		if kill -0 "$$pid" 2>/dev/null; then \
			kill "$$pid" && echo "Stopped frontend (PID $$pid)"; \
		else \
			echo "Frontend was not running"; \
		fi; \
		rm -f "$(FRONTEND_PID_FILE)"; \
	else \
		echo "Frontend was not running"; \
	fi'
	@$(COMPOSE) stop postgres >/dev/null 2>&1 || true
	@echo "PostgreSQL stopped if it was running."

backend-test: backend-install
	cd backend && ../$(PYTHON) manage.py test

frontend-test: frontend-install
	$(NPM) test

test: backend-test frontend-test

build: frontend-install
	$(NPM) run build

lint: frontend-install
	$(NPM) run lint
