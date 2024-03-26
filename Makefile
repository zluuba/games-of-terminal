install:
	python3 -m pip install --user dist/*.whl

reinstall:
	python3 -m pip install --force-reinstal --user dist/*.whl

uninstall:
	python3 -m pip uninstall dist/*.whl
