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

isort-check:

	poetry run isort . --check-only --diff

isort-fix:
	poetry run isort .

black-check:
	poetry run black --check .

black-fix:
	poetry run black .

flake8-check:
	poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=150 --statistics


lint-fix:
	make isort-fix
	make black-fix

lint-check:
	make isort-check
	make black-check
	make flake8-check
	

	
