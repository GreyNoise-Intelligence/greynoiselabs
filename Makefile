# include environment variables from a file
-include .env

.PHONY: requirements
requirements:
	( \
    	rm -rf venv; \
		python3 -m venv venv; \
		source venv/bin/activate; \
		venv/bin/pip3 install -r requirements/dev.txt; \
    )

.PHONY: lint
lint: requirements
	( \
    	source venv/bin/activate; \
    	yamllint .; \
		black --check src ; \
		isort --check-only src/**/*.py; \
		rst-lint *.rst; \
		flake8 src; \
    )

.PHONY: lint-fix
lint-fix: requirements
	( \
    	source venv/bin/activate; \
    	yamllint .; \
		black src; \
		isort src/**/*.py; \
		rst-lint *.rst; \
		flake8 src; \
    )

.PHONY: build
build: requirements
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
		pip3 install -r requirements/common.txt; \
		python3 setup.py sdist bdist_wheel; \
		pip3 install --force-reinstall dist/*.whl; \
    )

.PHONY: publish
publish: install
	( \
    	source venv/bin/activate; \
    	pip3 install twine; \
		TWINE_PASSWORD=${TWINE_PASSWORD} twine upload --username __token__ --disable-progress-bar dist/*; \
    )

.PHONY: bump
bump:
	( \
    	rm -rf venv; \
    	python3 -m venv venv; \
		source venv/bin/activate; \
		pip3 install -r requirements/dev.txt; \
		bumpversion --allow-dirty --verbose patch; \
    )

.PHONY: clean
clean:
	rm -rf build dist
	rm -rf venv
