DESTDIR = 
prefix = /usr
DDIR = $(DESTDIR)$(prefix)
bindir = $(DDIR)/bin
mandir = $(DDIR)/share/man/man1
datadir = $(DDIR)/share/charm-tools
helperdir = $(DDIR)/share/charm-helper
confdir = $(DESTDIR)/etc
INSTALL = install

all:

install:
	$(INSTALL) -d $(mandir)
	$(INSTALL) -t $(mandir) charm.1
	$(INSTALL) -d $(datadir)
	$(INSTALL) -t $(datadir) charm
	$(INSTALL) -d $(bindir)
	$(INSTALL) -d $(helperdir)
	$(INSTALL) -d $(confdir)/bash_completion.d
	$(INSTALL) misc/bash-completion $(confdir)/bash_completion.d/charm
	ln -sf $(datadir)/charm $(bindir)
	gzip $(mandir)/charm.1
	cp -rf scripts templates $(datadir)
	cp -rf helpers/* $(helperdir)

lint:
	@find setup.py charmworldlib tests -name '*.py' -print0 | xargs -r0 flake8

test:
	@echo Testing Python 2...
	@nosetests --nologcapture
	@echo Testing Python 3...
	@nosetests3 --nologcapture


coverage:
	@nosetests --with-coverage --cover-package=charmworldlib --cover-tests -s tests/test_*.py

check: integration test lint

clean:
	find . -name '*.pyc' -delete
	find . -name '*.bak' -delete
