DB_NAME ?= database
PORT ?= 8000

install:
	poetry install

build:
	./build.sh

lint:
	poetry run flake8 page_analyzer

dev:
	poetry run flask --app page_analyzer:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

schema-load:
	psql $(DB_NAME) < database.sql

db-reset:
	dropdb $(DB_NAME) || true
	createdb $(DB_NAME)

db-create:
	createdb $(DB_NAME) || echo 'skip'

db-connect:
	psql -d $(DB_NAME)

dev-setup:
	db-reset schema-load data-load
