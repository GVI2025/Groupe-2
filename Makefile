install:
	poetry install

shell-mac:
	poetry env activate

shell-linux:
	poetry shell

integration:
	poetry run alembic revision --autogenerate

migrate:
	poetry run alembic upgrade head

seed:
	poetry run python -m app.seed.seed_data

run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run test