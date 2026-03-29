SHELL := /bin/bash

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
MANAGE := $(PYTHON) backend/manage.py
NPM := npm --prefix frontend

.PHONY: help setup backend-install frontend-install env migrate backend frontend dev backend-test frontend-test test build lint

help:
	@printf "Available targets:\n"
	@printf "  make setup           Create the backend venv, install deps, and install frontend packages\n"
	@printf "  make env             Copy .env.example to .env if it does not already exist\n"
	@printf "  make migrate         Run Django migrations\n"
	@printf "  make backend         Start the Django development server\n"
	@printf "  make frontend        Start the Vite development server\n"
	@printf "  make dev             Start backend in the background and frontend in the foreground\n"
	@printf "  make backend-test    Run Django tests\n"
	@printf "  make frontend-test   Run frontend tests\n"
	@printf "  make test            Run backend and frontend tests\n"
	@printf "  make build           Build the frontend for production\n"
	@printf "  make lint            Run the frontend linter\n"

$(PYTHON):
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

backend-install: $(PYTHON)

frontend-install:
	$(NPM) install

setup: backend-install frontend-install

env:
	@if [ ! -f .env ]; then cp .env.example .env; fi

migrate: backend-install
	$(MANAGE) migrate

backend: backend-install
	$(MANAGE) runserver

frontend: frontend-install
	$(NPM) run dev

dev: backend-install frontend-install
	@$(MANAGE) runserver & \
	BACKEND_PID=$$!; \
	trap 'kill $$BACKEND_PID' EXIT INT TERM; \
	$(NPM) run dev

backend-test: backend-install
	cd backend && ../$(PYTHON) manage.py test

frontend-test: frontend-install
	$(NPM) test

test: backend-test frontend-test

build: frontend-install
	$(NPM) run build

lint: frontend-install
	$(NPM) run lint
