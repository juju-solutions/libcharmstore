VENVS = .venv2 .venv3
VENV2 = $(word 1, $(VENVS))
VENV3 = $(word 2, $(VENVS))

%2: PY = python2
%3: PY = python3


all: setup

install_%:
	@$(PY) setup.py install

install: install_2 install_3

check: lint test

build:
	@python setup.py sdist

.pip-cache:
	@mkdir .pip-cache

$(VENVS): .pip-cache test-requirements.pip requirements.pip
	virtualenv --distribute -p $(PY) --extra-search-dir=.pip-cache $@
	$@/bin/pip install -r test-requirements.pip  \
		--download-cache .pip-cache --find-links .pip-cache || \
		(touch test-requirements.pip; exit 1)
	@touch $@

setup: $(VENVS)

test: setup
	$(VENV3)/bin/nosetests -s --verbosity=2
	$(VENV2)/bin/nosetests -s --verbosity=2 --with-coverage --cover-package=charmworldlib
	@rm .coverage

lint: setup
	$(VENV2)/bin/flake8 --show-source ./charmworldlib

clean:
	rm -rf $(VENVS)
	-find . -name __pycache__ -type d | xargs rm -rf {}
	find . -name '*.py[co]' -delete
	find . -name '*.bak' -delete
	find . -type f -name '*~' -delete

clean-all: clean
	rm -rf .pip-cache

.PHONY: setup test lint clean clean-all install install_2 install_3

.DEFAULT_GOAL := all
