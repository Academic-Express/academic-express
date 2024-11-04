.PHONY: format lint

format:
	autopep8 --in-place --recursive .
	autoflake --in-place --recursive .
	isort .

lint:
	flake8
