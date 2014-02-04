all: build test

install:
	@python3 setup.py install
	@python2 setup.py install

check: lint test

build:
	@python setup.py sdist

.pip-cache:
	@mkdir .pip-cache

VENVS = .venv2 .venv3


.venv2: .pip-cache test-requirements.pip requirements.pip
	virtualenv --distribute -p python2 --extra-search-dir=.pip-cache $@
	$@/bin/pip install --use-mirrors -r test-requirements.pip  \
		--download-cache .pip-cache --find-links .pip-cache || \
		(touch test-requirements.pip; exit 1)
	@touch $@

.venv3: .pip-cache test-requirements.pip requirements.pip
	virtualenv --distribute -p python3 --extra-search-dir=.pip-cache $@
	$@/bin/pip install --use-mirrors -r test-requirements.pip  \
		--download-cache .pip-cache --find-links .pip-cache || \
		(touch test-requirements.pip; exit 1)
	@touch $@


setup: $(VENVS)

test: setup
	.venv2/bin/nosetests -s --verbosity=2 \
	    --with-coverage --cover-package=charmworldlib
	@rm .coverage
	.venv3/bin/nosetests -s --verbosity=2

lint: setup
	.venv2/bin/flake8 --show-source ./charmworldlib

clean:
	rm -rf $(VENVS)
	find . -name __pycache__ -exec rm -rf {} \;
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
	find . -name '*.py[co]' -delete
	find . -type f -name '*~' -delete
	find . -name '*.bak' -delete

clean-all: clean
	rm -rf .pip-cache
