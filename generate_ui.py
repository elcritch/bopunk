#!/usr/bin/env python

import os

def build(src,dst):
    """builds ui interface files into python files"""
    command = "pyuic4 -o src/BoPunk/%s interface/%s"%(dst,src)
    print "Running:",command
    os.system(command)

ui = (
    ('BoPunkMainWindow.ui','MainWindow.py'),
    ('VariableWidget.ui','VariableWidget.py'),
)

for src,dst in ui:
    build(src,dst)
