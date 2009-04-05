from __future__ import with_statement 
import sys, os, uuid
import time, shutil, tempfile, threading, thread
# from __future__ import print_function # import future print function

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
# from PyQt4.QtGui import *


settings = QSettings(QSettings.IniFormat,QSettings.UserScope,"example","Settings Test")

value = settings.value("app/value1").toString()
print "value:",type(value), value
value = settings.value("app/value2").toString()
print "value:",type(value), value
value = settings.value("app/value3").toMap()
print "value:",type(value), value
value = settings.value("app/value3")
print "type:",type(value), value.typeName()

settings.setValue("app/value1",QVariant("works"))
settings.setValue("app/value2",QVariant(4))
settings.setValue("app/value3",QVariant({"a":1}))
settings.sync()

filename = str(settings.fileName())
qfile = QFile(filename)
dirname = os.path.dirname(str(filename))

homepath = str(QDir.homePath())
# dirname = os.path.dirname(filename)

print "fileName:",filename
print "fileNameDir:", dirname
print "fileHomePath:", homepath

# print "listdir:", os.listdir(dirname)[:5]
