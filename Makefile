.PHONY: isort black flake8 mypy

lint: isort black flake8

isort:
	isort -y -rc backend

black:
	black backend/

flake8:
	flake8 backend/

mypy:
	mypy backend/

