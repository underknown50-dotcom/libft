VENV ?= .venv

ifeq ($(OS),Windows_NT)
    PYTHON ?= python
    VENV_BIN = $(VENV)/Scripts
else
    PYTHON ?= python3
    VENV_BIN = $(VENV)/bin
endif

VENV_PYTHON = $(VENV_BIN)/python
VENV_PIP = $(VENV_BIN)/pip
VENV_FLAKE8 = $(VENV_BIN)/flake8
VENV_MYPY = $(VENV_BIN)/mypy
VENV_PYTEST = $(VENV_BIN)/pytest

CONFIG ?= config.txt

.PHONY: all install run debug clean fclean lint lint-strict test package help

all: run

$(VENV_PYTHON):
	$(PYTHON) -m venv $(VENV)

install: $(VENV_PYTHON)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt
	$(VENV_PIP) install -e .

run:
	@if [ -f "$(VENV_PYTHON)" ]; then $(VENV_PYTHON) a_maze_ing.py $(CONFIG); else $(PYTHON) a_maze_ing.py $(CONFIG); fi

debug:
	@if [ -f "$(VENV_PYTHON)" ]; then $(VENV_PYTHON) -m pdb a_maze_ing.py $(CONFIG); else $(PYTHON) -m pdb a_maze_ing.py $(CONFIG); fi

clean:
	$(PYTHON) -c "import shutil, pathlib, glob; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('*.egg-info')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.mypy_cache')]; [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('.pytest_cache')]; [shutil.rmtree(p, ignore_errors=True) for p in ['build', 'dist']]"

fclean: clean
	$(PYTHON) -c "import pathlib, glob; [pathlib.Path(f).unlink(missing_ok=True) for f in glob.glob('*.txt') if f != 'config.txt' and f != 'requirements.txt']"

lint:
	@if [ -f "$(VENV_FLAKE8)" ]; then $(VENV_FLAKE8) .; else flake8 .; fi
	@if [ -f "$(VENV_MYPY)" ]; then $(VENV_MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs; else mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs; fi

lint-strict:
	@if [ -f "$(VENV_FLAKE8)" ]; then $(VENV_FLAKE8) .; else flake8 .; fi
	@if [ -f "$(VENV_MYPY)" ]; then $(VENV_MYPY) . --strict; else mypy . --strict; fi

test:
	@if [ -f "$(VENV_PYTEST)" ]; then $(VENV_PYTEST) -v; else pytest -v; fi

package:
	@if [ -f "$(VENV_PYTHON)" ]; then $(VENV_PYTHON) -m build; else $(PYTHON) -m build; fi
	$(PYTHON) -c "import shutil, glob; [shutil.copy(f, '.') for f in glob.glob('dist/mazegen-*')]"
