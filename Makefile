install:
	poetry install

shell:
	poetry env activate

migrate:
	poetry run alembic upgrade head

integration:
	poetry run alembic revision --autogenerate

seed:
	poetry run python -m app.seed.seed_data

run:
	poetry run uvicorn app.main:app --reload

test:
	poetry run test