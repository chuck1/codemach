pkg=$(shell cat NAME.txt)

version=$(shell python3 -c 'import ws_storage;print(ws_storage.__version__)')

test:
	python3 -m unittest $(pkg).tests

upload:
	@mkdir -p dist
	@rm -f dist/*whl
	python3 setup.py bdist_wheel
	twine upload dist/*whl

req:
	pipenv run pip3 freeze > requirements.txt
	cat requirements.txt

