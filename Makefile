VIRTUAL_ENV?=venv
PIP=$(VIRTUAL_ENV)/bin/pip
PYTHON=$(VIRTUAL_ENV)/bin/python
ISORT=$(VIRTUAL_ENV)/bin/isort
FLAKE8=$(VIRTUAL_ENV)/bin/flake8
SYSTEM_DEPENDENCIES=ffmpeg


all: virtualenv

$(VIRTUAL_ENV):
	virtualenv --python python3 venv
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

virtualenv/test: virtualenv
	$(PIP) install -r requirements/test.txt

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

clean:
	rm -rf venv/ .pytest_cache/

unittest: virtualenv/test
	$(PYTHON) manage.py test

lint/isort: virtualenv/test
	$(ISORT) --check-only --diff --skip .tox --skip venv --skip migrations --recursive

lint/flake8: virtualenv/test
	$(FLAKE8) $(SOURCES)

lint: lint/isort lint/flake8

test: unittest lint
