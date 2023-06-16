# include environment variables from a file
-include .env

.PHONY: requirements
requirements: 
	pip3 install --user -r requirements/dev.txt

.PHONY: lint
lint: requirements
	yamllint .
	black --check src 
	isort --check-only src/**/*.py
	rst-lint *.rst
	flake8 src

.PHONY: build
build: requirements
	ariadne-codegen --config ariadne.toml
	black src
	isort src/**/*.py
	docker build .

.PHONY: install
install: build
	pip3 install -r requirements/common.txt && python3 setup.py sdist bdist_wheel
	pip3 install --force-reinstall dist/*.whl

.PHONY: publish
publish:
	twine upload --username __token__ --disable-progress-bar dist/*

.PHONY: clean
clean:
	rm -rf build dist
