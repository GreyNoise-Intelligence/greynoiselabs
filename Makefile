# include environment variables from a file
-include .env

.PHONY: lint
lint:
	yamllint .
	black --check src 
	isort --check-only src/**/*.py
	rst-lint *.rst
	flake8 src

.PHONY: build
build:
	pip3 install --user -r requirements/dev.txt
	ariadne-codegen --config ariadne.toml
	docker build .

.PHONY: clean
clean:
	echo "clean"
