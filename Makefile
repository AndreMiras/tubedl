VENV_NAME="venv"
ACTIVATE_PATH="$(VENV_NAME)/bin/activate"
PIP=`. $(ACTIVATE_PATH); which pip`
TOX=`which tox`
PYTHON="$(VENV_NAME)/bin/python"
SYSTEM_DEPENDENCIES=python3-dev virtualenv
OS=$(shell lsb_release -si)


all: virtualenv

virtualenv:
	test -d venv || virtualenv -p python3 venv
	. venv/bin/activate
	$(PIP) install -r requirements.txt

system_dependencies:
ifeq ($(OS), Ubuntu)
	sudo apt install --yes --no-install-recommends $(SYSTEM_DEPENDENCIES)
endif

clean:
	rm -rf venv/ .tox/ .pytest_cache/

test:
	$(TOX)
