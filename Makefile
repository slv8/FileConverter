PROJECT := converter
VIRTUAL_ENV ?= .venv
PYTHON_VERSION ?= 3.12
PIP_VERSION ?= 25.1.1
PIP_TOOLS_VERSION ?= 7.4.1
DOTENV_VERSION ?= 1.1.0
REQ_DIR ?= .requirements
PIP := $(VIRTUAL_ENV)/bin/pip
PIP_COMPILE := $(VIRTUAL_ENV)/bin/pip-compile --all-extras --no-header -v --no-emit-trusted-host --no-emit-index-url

_install_tools:
	$(PIP) install pip==$(PIP_VERSION)
	$(PIP) install pip-tools==$(PIP_TOOLS_VERSION)
	$(PIP) install python-dotenv==$(DOTENV_VERSION)

_create_venv:
	python -m venv $(VIRTUAL_ENV) --prompt $(PROJECT)

init: _create_venv _install_tools

install:
	$(PIP) install -r $(REQ_DIR)/dev.txt

compile:
	$(PIP_COMPILE) $(REQ_DIR)/prod.in -o $(REQ_DIR)/prod.txt -v
	$(PIP_COMPILE) $(REQ_DIR)/dev.in $(REQ_DIR)/prod.in -o $(REQ_DIR)/dev.txt

venv: init install

upgrade_db:
	dotenv -f .env run alembic upgrade head

downgrade_db:
	dotenv -f .env run alembic downgrade -1

generate_migration:
	dotenv -f .env run alembic revision --autogenerate

format:
	black app/
	isort app/ --settings-file pyproject.toml

lint:
	flake8 app/