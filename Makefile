# include environment variables from a file
-include .env
SHELL := /bin/bash

# Disable echo on the config target to prevent leaking the PYPI_TOKEN
.SILENT: publish

PYPI_TOKEN := $(PYPI_TOKEN)

.PHONY: deps 
deps:
	python3 -m pip install tox

.PHONY: test 
test: clean deps
	tox -p auto -v

.PHONY: lint
lint: deps
	tox -e lint -p auto -v

.PHONY: build
build: clean
	( \
		poetry install; \
		poetry build; \
    )

.PHONY: install
install:
	( \
		poetry run pip install dist/*.whl; \
    )

.PHONY: shell
shell: build install
	( \
		poetry shell; \
    )

.PHONY: fakepublish
fakepublish: clean
	( \
		poetry config repositories.testpypi https://test.pypi.org/legacy/; \
		poetry config pypi-token.testpypi $(PYPI_TOKEN); \
    	poetry publish --build; \
    )

.PHONY: publish
publish: clean
	( \
		poetry config repositories.pypi https://pypi.org/legacy/; \
		poetry config pypi-token.pypi $(PYPI_TOKEN); \
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
	rm -rf ~/.local/share/virtualenv/py_info/
	rm -rf .tox
