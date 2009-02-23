PYTHON=/usr/bin/env python

all: generate
	$(PYTHON) src/bopunk.py
	
run: generate
	$(PYTHON) src/bopunk.py

generate:
	$(PYTHON) generate_ui.py
	
	
run25:
	/usr/bin/python2.5 src/bopunk.py 

build-osx:
	$(PYTHON) setup-py2app.py py2app

build-winxp:
	$(PYTHON) setup-cxfreeze.py build

pydoc:
	$(PYTHON) generate_pydoc.py

unittest:
	# TODO: need to fix folder location problem for unittest
	find src -name "*Test.py" | xargs -I % $(PYTHON) %
