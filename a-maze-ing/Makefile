# A-Maze-ing Makefile
# Strict adherence to Chapter 3 rules

PYTHON := python3
export PYTHONPATH := src

.PHONY: all install run debug clean lint lint-strict test

all: run

install:
	$(PYTHON) -m pip install --break-system-packages flake8 mypy build setuptools || true

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ src/__pycache__ src/mazegen/__pycache__ tests/__pycache__
	rm -rf .mypy_cache .pytest_cache build dist *.egg-info

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

test:
	$(PYTHON) -m unittest discover -s tests
