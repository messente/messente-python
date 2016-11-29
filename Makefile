prepare:
	pip install setuptools wheel twine

clean:
	rm -rf dist build messente_python.egg-info/

build: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel --universal

publish: clean prepare build
	twine upload dist/*

.PHONY: build publish
