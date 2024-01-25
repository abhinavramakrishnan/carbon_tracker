install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

lint:
	find . -name "*.py" -not -path "./migrations/*" | xargs pylint --disable=R,C

format:
	find . -name "*.py" -not -path "./migrations/*" | xargs black

test:
	python -m pytest -vv test_script.py

all: install lint format test 
