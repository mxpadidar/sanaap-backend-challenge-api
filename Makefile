.PHONY: install migrations migrate run lint format type-check
install:
	@uv sync

run:
	@uv run manage.py runserver

lint:
	@uv run ruff format sanaap

format:
	@uv run ruff check sanaap

type-check:
	@uv run pyright sanaap

migrations:
	@uv run manage.py makemigrations

migrate:
	@uv run manage.py migrate
