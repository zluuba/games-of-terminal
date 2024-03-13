install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

reinstall:
	poetry build
	python3 -m pip install --force-reinstal --user dist/*.whl

lint:
	poetry run flake8 games_of_terminal --exclude database_new.py,models.py,games_of_terminal/lab/

test:
	poetry run pytest

typing:
	mypy --config-file pyproject.toml games_of_terminal

check:
	make test
	make lint
	make typing

package-uninstall:
	python3 -m pip uninstall dist/*.whl
