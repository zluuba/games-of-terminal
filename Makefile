install:
	poetry install

build:
	poetry build

package-install:
	python3 -m pip install --user dist/*.whl

reinstall:
	python3 -m pip install --force-reinstal --user dist/*.whl

lint:
	poetry run flake8 terminal_games
