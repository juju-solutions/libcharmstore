all: install test

install:
	@python3 setup.py install
	@python2 setup.py install

#test:
#	@echo Testing Python 2...
#	@nosetests --nologcapture
#	@echo Testing Python 3...
#	@nosetests3 --nologcapture


#coverage:
#	@nosetests --with-coverage --cover-package=charmworldlib --cover-tests -s tests/test_*.py

check: test lint

build: 
	./bin/configure

test: build
	./bin/test

coverage: build
	./bin/test coverage

lint:
	@./bin/lint

clean:
	rm -rf .venv
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
	find . -name '*.py[co]' -delete
	find . -type f -name '*~' -delete
	find . -name '*.bak' -delete

clean-all: clean
	rm -rf .pip-cache
