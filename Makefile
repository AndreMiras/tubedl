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
DOCKER_IMAGE=andremiras/tubedl
SYSTEM_DEPENDENCIES=ffmpeg
SOURCES=tubedl/ videodl/


all: virtualenv

$(VIRTUAL_ENV):
	virtualenv --python $(PYTHON_WITH_VERSION) $(VIRTUAL_ENV)
	$(PIP) install --upgrade --requirement requirements.txt

virtualenv: $(VIRTUAL_ENV)

virtualenv/test: virtualenv
	$(PIP) install --upgrade --requirement requirements/test.txt

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

clean:
	rm -rf venv/ .pytest_cache/

unittest: virtualenv/test
	$(PYTEST) $(SOURCES)

lint/isort: virtualenv/test
	$(ISORT) --check-only --diff --recursive $(SOURCES)

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint/black: virtualenv/test
	$(BLACK) --check $(SOURCES)

lint: lint/isort lint/flake8 lint/black

format/isort: virtualenv/test
	$(ISORT) --recursive $(SOURCES)

format/black: virtualenv/test
	$(BLACK) $(SOURCES)

format: format/isort format/black

test: unittest lint

docker/build:
	docker build --tag=$(DOCKER_IMAGE) .

docker/run/make/%:
	docker run --env-file .env -it --rm $(DOCKER_IMAGE) make $*

docker/run/test: docker/run/make/test

docker/run/shell:
	docker run --env-file .env -it --rm $(DOCKER_IMAGE)
