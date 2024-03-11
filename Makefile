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
	poetry run flake8 games_of_terminal

test:
	poetry run pytest

uninstall:
	python3 -m pip uninstall --user dist/*.whl
