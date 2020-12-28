clean:
	rm -rf *.pyc build/ dist/ column.py.egg-info/

package: clean
	python3 setup.py sdist bdist_wheel

upload: package
	python3 -m twine upload dist/*
