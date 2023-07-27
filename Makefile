# include environment variables from a file
-include .env

.PHONY: requirements
requirements:
	rm -rf venv
	python3 -m venv venv 
	. venv/bin/activate
	venv/bin/pip3 install -r requirements/dev.txt

.PHONY: lint
lint: requirements
	. venv/bin/activate
	venv/bin/yamllint .
	venv/bin/black --check src 
	venv/bin/isort --check-only src/**/*.py
	venv/bin/rst-lint *.rst
	venv/bin/flake8 src

.PHONY: lint-fix
lint-fix: requirements
	. venv/bin/activate
	venv/bin/yamllint .
	venv/bin/black src 
	venv/bin/isort src/**/*.py
	venv/bin/rst-lint *.rst
	venv/bin/flake8 src

.PHONY: build
build: requirements
	. venv/bin/activate
	venv/bin/ariadne-codegen --config ariadne.toml
	venv/bin/black src
	venv/bin/isort src/**/*.py
	docker build .

.PHONY: install
install:
	rm -rf venv
	python3 -m venv venv
	. venv/bin/activate
	venv/bin/pip3 install -r requirements/common.txt && venv/bin/python3 setup.py sdist bdist_wheel
	venv/bin/pip3 install --force-reinstall dist/*.whl

.PHONY: publish
publish: install
	venv/bin/pip3 install twine
	TWINE_PASSWORD=${TWINE_PASSWORD} venv/bin/twine upload --username __token__ --disable-progress-bar dist/*

.PHONY: bump
bump:
	bumpversion --allow-dirty --verbose patch

.PHONY: clean
clean:
	rm -rf build dist
	rm -rf venv
