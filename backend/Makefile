.PHONY: format format-check lint test

AUTOPEP8_ARGS = --recursive --experimental --aggressive --aggressive

format:
	autopep8 $(AUTOPEP8_ARGS) --in-place .
	autoflake --in-place --recursive .
	isort .

format-check:
	autopep8 $(AUTOPEP8_ARGS) --diff --exit-code .
	autoflake --check --recursive --quiet .
	isort --check-only .

lint:
	flake8

test:
	python manage.py test
