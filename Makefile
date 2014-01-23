all: install test

install:
	@python3 setup.py install
	@python2 setup.py install

check: test lint

build:
	@python setup.py sdist

venv: 
	./bin/configure

test: venv
	./bin/test

coverage: venv
	./bin/test coverage

lint: venv
	@./bin/lint

clean:
	rm -rf .venv-* 
	find . -name __pycache__ -type d -delete
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
	find . -name '*.py[co]' -delete
	find . -type f -name '*~' -delete
	find . -name '*.bak' -delete

clean-all: clean
	rm -rf .pip-cache
