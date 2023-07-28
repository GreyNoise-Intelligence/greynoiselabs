# include environment variables from a file
-include .env
SHELL := /bin/bash

# Disable echo on the config target to prevent leaking the PYPI_TOKEN
.SILENT: config

PYPI_TOKEN := $(PYPI_TOKEN)

.PHONY: lint
lint: clean
	( \
		poetry install; \
    	poetry run yamllint .; \
		poetry run black --check src ; \
		poetry run isort --check-only src/**/*.py; \
		poetry run rst-lint *.rst; \
		poetry run ruff check src; \
    )

.PHONY: lint-fix
lint-fix: clean
	( \
		poetry install; \
    	poetry run yamllint .; \
		poetry run black src; \
		poetry run isort src/**/*.py; \
		poetry run rst-lint *.rst; \
		poetry run ruff check --fix src; \
    )

.PHONY: build
build: clean
	( \
		poetry install; \
    	poetry run ariadne-codegen --config ariadne.toml; \
		poetry run yamllint .; \
		poetry run black src; \
		poetry run isort src/**/*.py; \
		poetry run rst-lint *.rst; \
		poetry run ruff check --fix src; \
		poetry build; \
		docker build -t greynoiselabs-cli .; \
    )

.PHONY: install
install:
	( \
		poetry run pip install dist/*.whl; \
    )

.PHONY: shell
shell:
	( \
		poetry shell; \
    )

.PHONY: config
config: 
	poetry config http-basic.pypi "__token__" "$(PYPI_TOKEN)"; \

.PHONY: publish
publish: clean config
	( \
    	poetry publish --build; \
    )

.PHONY: bump
bump: clean
	( \
    	poetry version patch; \
    )

.PHONY: clean
clean:
	poetry env remove --all
	rm -rf dist
	python3 -m pip uninstall greynoiselabs
