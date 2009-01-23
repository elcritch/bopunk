#!/usr/bin/env python

import os

command = "pyuic4 -o src/BoPunk/MainWindow.py ui/BoPunkMainWindow.ui"
print "Running:",command

os.system(command)
