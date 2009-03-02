# Creating MSI executable installer for MS Windows #

MSI technology is used to package boPunk application for MS Windows. To
quickly create MSI files the open source Nullsoft 
[NSIS](http://nsis.sourceforge.net/Main_Page) is used. Instructions and 
download information can be found at the NSIS website.

Make sure the required files are found in etc and that the correct cx_Freeze
generated exe file is locate in the build directory. The required files:
etc/qt.conf
etc/gpl-2.0.txt
build/exe.win32-2.6/ (with bopunk.exe and all compiled sources)

1. Install NSIS
2. Right Click on [source dir]/etc/bopunk.nsi script. 
3. Find executable MSI script in etc dir if there were no errors. 

## Generating / Updating NSIS Scripts ##

Download and install [HM NIS EDIT](http://hmne.sourceforge.net/) . 

The HM NIS editor contains a simple wizard which automates creating NSI 
scripts. It was used to generate the current script. Follow the standard
instructions (choosing the modern gui) and selecting the correct bopunk build
directory. Also make sure to include the gpl license. The default installation
directory is $PROGRAMFILES\BoPunk.


## Windows Build ##
The windows exe build is compiled using cx_Freeze. To compile it run:

	python setup-cxfreeze.py build
or
	make build-winxp

This command is based on distutils, but the bdist_msi functionality of 
distutils seems to break on the Bopunk application. 
