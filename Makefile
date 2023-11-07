install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	pylint --disable=R,C ./api/*.py 

test:
	python -m pytest -vv --cov=. api/test_*.py

start-services:
	docker-compose up 

run-dev:
	python api/app.py

run-prod:
	python api/app.py

init-db:
	flask --app api/app.py db init --directory api/migrations

create-migration:
	@read -p "Enter Migration Name:" migration
	flask --app api/app.py db migrate $$migration --directory api/migrations

run-migrations:
	flask --app api/app.py db upgrade --directory api/migrations

all: install lint test