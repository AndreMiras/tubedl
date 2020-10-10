VIRTUAL_ENV?=venv
PIP=$(VIRTUAL_ENV)/bin/pip
PYTHON_MAJOR_VERSION=3
PYTHON_MINOR_VERSION=8
PYTHON_VERSION=$(PYTHON_MAJOR_VERSION).$(PYTHON_MINOR_VERSION)
PYTHON_WITH_VERSION=python$(PYTHON_VERSION)
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
BLACK=$(VIRTUAL_ENV)/bin/black
PYTEST=$(VIRTUAL_ENV)/bin/pytest
GUNICORN=$(VIRTUAL_ENV)/bin/gunicorn
DOCKER_IMAGE=andremiras/tubedl
DOCKER_PORT=8000
SYSTEM_DEPENDENCIES=ffmpeg
SOURCES=tests/ tubedl/ videodl/


all: virtualenv

$(VIRTUAL_ENV):
	$(PYTHON_WITH_VERSION) -m venv $(VIRTUAL_ENV)
	$(PIP) install --upgrade --requirement requirements.txt

virtualenv: $(VIRTUAL_ENV)

virtualenv/test: virtualenv
	$(PIP) install --upgrade --requirement requirements/test.txt

virtualenv/prod: virtualenv
	$(PIP) install --upgrade --requirement requirements/prod.txt

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

clean:
	rm -rf venv/ .pytest_cache/

unittest: virtualenv/test
	$(PYTEST) tests/

lint/isort: virtualenv/test
	$(ISORT) --check-only --diff $(SOURCES)

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint/black: virtualenv/test
	$(BLACK) --check $(SOURCES)

lint: lint/isort lint/flake8 lint/black

format/isort: virtualenv/test
	$(ISORT) $(SOURCES)

format/black: virtualenv/test
	$(BLACK) $(SOURCES)

format: format/isort format/black

test: unittest lint

run/collectstatic: virtualenv/prod
	$(PYTHON) manage.py collectstatic --noinput

run/migrate: virtualenv/prod
	$(PYTHON) manage.py migrate --noinput

run/gunicorn: virtualenv/prod
	$(GUNICORN) tubedl.wsgi:application --bind 0.0.0.0:$(PORT)

docker/build:
	docker build --tag=$(DOCKER_IMAGE) .

docker/run/make/%:
	docker run --env-file .env -it --rm $(DOCKER_IMAGE) make $*

docker/run/test: docker/run/make/test

docker/run/app:
	docker run --env-file .env --env PORT=$(DOCKER_PORT) --publish $(DOCKER_PORT):$(DOCKER_PORT) -it --rm $(DOCKER_IMAGE)

docker/run/app/production:
	PRODUCTION=1 DJANGO_SECRET_KEY=1 \
	docker run --env-file .env --env PORT=$(DOCKER_PORT) --publish $(DOCKER_PORT):$(DOCKER_PORT) -it --rm $(DOCKER_IMAGE)

docker/run/shell:
	docker run --env-file .env -it --rm $(DOCKER_IMAGE) /bin/bash
