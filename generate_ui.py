#!/usr/bin/env python

import os

def build(src,dst):
    """builds ui"""
    command = "pyuic4 -o src/BoPunk/%s ui/%s"%(dst,src)
    print "Running:",command
    os.system(command)

ui = (
    ('BoPunkMainWindow.ui','MainWindow.py'),
    ('VariableWidget.ui','VariableWidget.py'),
)

for src,dst in ui:
    build(src,dst)