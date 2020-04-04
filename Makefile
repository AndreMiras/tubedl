VIRTUAL_ENV?=venv
PIP=$(VIRTUAL_ENV)/bin/pip
TOX=`which tox`
PYTHON=$(VENV_NAME)/bin/python
SYSTEM_DEPENDENCIES=ffmpeg


all: virtualenv

$(VIRTUAL_ENV):
	virtualenv --python python3 venv
	$(PIP) install -r requirements.txt

virtualenv: $(VIRTUAL_ENV)

system_dependencies:
	apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)

clean:
	rm -rf venv/ .tox/ .pytest_cache/

test:
	$(TOX)
