PYTHON=/usr/bin/env python

all: generate
	# $(PYTHON) src/mainwindow.py
	

generate:
	$(PYTHON) generate_ui.py
	
run:
	$(PYTHON) src/mainwindow.py
	
run25:
	/usr/bin/env python2.5 src/mainwindow.py 

build-osx:
	$(PYTHON) setup-py2app.py py2app

build-winxp:
	$(PYTHON) setup-cxfreeze.py build
	

unittest:
	# TODO: need to fix folder location problem for unittest
	find src -name "*Test.py" | xargs -I % $(PYTHON) %