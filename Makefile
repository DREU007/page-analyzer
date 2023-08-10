install:
	poetry install

build:
	poetry build
	
publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --user dist/*.whl

package-remove:
	python3 -m pip uninstall hexlet-code

test:
	poetry run pytest page_analyzer tests

lint:
	poetry run flake8 page_analyzer tests

dev:
	poetry run flask --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
