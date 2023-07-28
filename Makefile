# include environment variables from a file
-include .env
SHELL := /bin/bash

TWINE_PASSWORD := $(TWINE_PASSWORD)

.PHONY: requirements
requirements:
	( \
    	rm -rf venv; \
		python3 -m venv venv; \
		source venv/bin/activate; \
		venv/bin/python3 -m pip install -r requirements/dev.txt; \
    )

.PHONY: lint
lint: requirements
	( \
    	source venv/bin/activate; \
    	yamllint .; \
		black --check src ; \
		isort --check-only src/**/*.py; \
		rst-lint *.rst; \
		ruff check src; \
    )

.PHONY: lint-fix
lint-fix: requirements
	( \
    	source venv/bin/activate; \
    	yamllint .; \
		black src; \
		isort src/**/*.py; \
		rst-lint *.rst; \
		ruff check --fix src; \
    )

.PHONY: build
build: clean requirements
	( \
    	source venv/bin/activate; \
    	ariadne-codegen --config ariadne.toml; \
		black src; \
		isort src/**/*.py; \
		docker build .; \
    )

.PHONY: install
install:
	( \
		rm -rf venv; \
		python3 -m venv venv; \
    	source venv/bin/activate; \
		python3 -m pip install -r requirements/common.txt; \
		python3 setup.py sdist bdist_wheel; \
		python3 -m pip install --force-reinstall dist/*.whl; \
    )

.PHONY: publish
publish: install
	( \
    	source venv/bin/activate; \
    	python3 -m pip install twine; \
		twine upload --username "__token__" --password $(TWINE_PASSWORD) --disable-progress-bar dist/*; \
    )

.PHONY: bump
bump:
	( \
    	rm -rf venv; \
    	python3 -m venv venv; \
		source venv/bin/activate; \
		python3 -m pip install -r requirements/dev.txt; \
		bumpversion --allow-dirty --verbose patch; \
    )

.PHONY: clean
clean:
	rm -rf build dist
	rm -rf venv
