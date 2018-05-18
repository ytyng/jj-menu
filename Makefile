test:
	flake8 jj_menu
	python setup.py test

upload:
	python setup.py sdist
	twine upload dist/*

edit:
	open -a PyCharm .

virtualenv:
	python3 -m venv venv
