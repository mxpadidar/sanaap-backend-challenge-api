.PHONY: install migrations migrate run lint format type-check test all
all: install lint type-check test
	@echo "-> All checks passed!"

install:
	@uv sync

run:
	@uv run manage.py runserver

lint:
	@uv run ruff format sanaap tests

format:
	@uv run ruff check sanaap tests

type-check:
	@uv run pyright sanaap tests

migrations:
	@uv run manage.py makemigrations

migrate:
	@uv run manage.py migrate

test:
	@uv run pytest tests

