sdist:
	python3 setup.py sdist

upload:
	twine upload dist/*

clear:
	rm -rf dist/ airmail.egg-info
