.DEFAULT_GOAL := help

PYTHON ?= $(if $(wildcard .venv/bin/python),.venv/bin/python,python3)

.PHONY: help run test lint format frontend-install frontend-run frontend-build

help:
	@echo "run                Start the API with reload enabled"
	@echo "test               Run backend tests"
	@echo "lint               Check Python style and imports"
	@echo "format             Format Python files"
	@echo "frontend-install   Install frontend dependencies"
	@echo "frontend-run       Start the Vite frontend with an API proxy"
	@echo "frontend-build     Type-check and build the frontend"

run:
	$(PYTHON) -m uvicorn app.main:app --app-dir backend --reload

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check backend

format:
	$(PYTHON) -m ruff format backend

frontend-install:
	npm --prefix frontend install

frontend-run:
	npm --prefix frontend run dev

frontend-build:
	npm --prefix frontend run build
