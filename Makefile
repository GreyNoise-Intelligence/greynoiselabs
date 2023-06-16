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
	docker build .

.PHONY: clean
clean:
	echo "clean"
