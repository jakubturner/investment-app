install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=src tests

debug:
	python -m pytest -vv --pdb #Debuger is invoked

format:
	black src/*.py

lint:
	pylint --disable=R,C src

all: install lint test format