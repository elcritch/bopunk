PYTHON=`which python`
DESTDIR=/
BUILDIR=$(CURDIR)/debian/bopunk
PROJECT=bopunk
VERSION=0.5

all:
	@echo "make install - Install on local system"
	@echo "make buildosx - Generate a OS X application"
	@echo "make buildwinxp - Generate a WinXP executable"
	@echo "make buildrpm - Generate a rpm package"
	@echo "make builddeb - Generate a deb package"
	@echo "make packageosx - Generate a OS X pkg"
	@echo "make clean - Get rid of scratch and byte files"

run:
	$(PYTHON) src/bopunk.py

run25:
	/usr/bin/python2.5 src/bopunk.py 

generate:
	$(PYTHON) generate_ui.py

install:
	@echo "Installing using distutils setup..."
	$(PYTHON) setup.py install --root $(DESTDIR) $(COMPILE)

# Various build options 
buildosx:
	$(PYTHON) setup-py2app.py py2app

buildwinxp:
	$(PYTHON) setup-cxfreeze.py build

buildrpm:
	$(PYTHON) setup.py bdist_rpm --post-install=rpm/postinstall --pre-uninstall=rpm/preuninstall

builddeb:
	mkdir -p ${BUILDIR}
	DESTDIR=$(BUILDIR) dpkg-buildpackage -rfakeroot

package-osx:
	hdiutil create -srcfolder dist/bopunk.app -format UDBZ dist/BoPunk.dmg

pydoc:
	epydoc --config epydoc.conf $(shell find src -name \*.py)

docs: pydoc

unittest:
	# TODO: need to fix folder location problem for unittest
	find src -name "*Test.py" | xargs -I % $(PYTHON) %


clean:
	$(PYTHON) setup.py clean
	$(MAKE) -f $(CURDIR)/debian/rules clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
