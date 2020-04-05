VIRTUAL_ENV?=venv
PIP=$(VIRTUAL_ENV)/bin/pip
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
BLACK=$(VIRTUAL_ENV)/bin/black
DOCKER_IMAGE=andremiras/tubedl
SYSTEM_DEPENDENCIES=ffmpeg
SOURCES=tubedl/ videodl/


all: virtualenv

$(VIRTUAL_ENV):
	virtualenv --python python3 venv
	$(PIP) install --upgrade --requirement requirements.txt

virtualenv: $(VIRTUAL_ENV)

virtualenv/test: virtualenv
	$(PIP) install --upgrade --requirement requirements/test.txt

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

clean:
	rm -rf venv/ .pytest_cache/

unittest: virtualenv/test
	$(PYTHON) manage.py test

lint/isort: virtualenv/test
	$(ISORT) --check-only --diff --recursive $(SOURCES)

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint/black: virtualenv/test
	$(BLACK) --check $(SOURCES)

lint: lint/isort lint/flake8 lint/black

format/isort: virtualenv/test
	$(ISORT) --diff --recursive $(SOURCES)

format/black: virtualenv/test
	$(BLACK) $(SOURCES)

format: format/isort format/black

test: unittest lint

docker/build:
	docker build --tag=$(DOCKER_IMAGE) .

docker/run/test:
	docker run --env-file .env -it --rm $(DOCKER_IMAGE) make test

docker/run/shell:
	docker run --env-file .env -it --rm $(DOCKER_IMAGE)
