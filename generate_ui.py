#!/usr/bin/env python
import os, sys, shutil

ui_pth = 'src/BoPunk/ui'

# setup the cmd_str, replacing dir with %s to reduce confusion
cmd_str = "pyuic4 -o DIR%sDIR interface%sDIR"%(os.sep,os.sep)
cmd_str = cmd_str.replace("DIR",'%s')

def build(src,dst):
    """builds ui interface files into python files"""
    command = cmd_str%(ui_pth,dst,src)
    print "Running:", command 
    os.system(command)

ui = (
    ('BoPunkMainWindow.ui','MainWindow.py'),
    ('VariableWidget.ui','VariableWidget.py'),
    ('BoolVariableWidget.ui','BoolVariableWidget.py'),
    ('SettingsDialog.ui','SettingsDialog.py'),
)

if not os.path.isdir(ui_pth):
    """ test if ui dir exists"""
    print "making ui directory..."
    os.mkdir(ui_pth)

if not os.path.isfile(ui_pth+os.sep+'__init__.py'):
    """make __init__.py file if not found."""
    print "making ui/__init__.py file..."
    open(ui_pth+os.sep+'__init__.py','w').close()

for src,dst in ui:
    build(src,dst)
