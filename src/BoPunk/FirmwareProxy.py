"""
Provides a proxy to BoPunk device. Should include USB/serial port interactions. 

Author: Jarremy Creechley
License: See License.txt for more details 

Copyright (C) 2009 Jaremy Creechley <creechley@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

from PyQt4 import QtCore
from PyQt4.QtCore import QString, Qt, QVariant, SIGNAL, SLOT
from PyQt4.QtGui import *
from pyvariablewidget import PyVariableWidget

class FirmwareProxy(QtCore.QAbstractTableModel):
    def __init__(self, mainwindow):
        """Creates Firmware Proxy for interacting with boPunk device"""
        self.mainwindow = mainwindow
        self.variablesWidget = mainwindow.variablesWidget
        self.firmwareVars = None
        self.setupVariables()
        
    def setupVariables(self):
        """configure variables for a firmware"""
        test = {
            'Rate':('Configure rate',30),
            'Intensity':('Configure intensity of the boPunk',5),
            'Randomness':('Modify the randomness of the output',75),
            'R-factor':('Modifies the R-factor',90),
            'Z-factor':('more sensitive than the R-factor',12),
        }
        
        widgets = []
        self.widgets = widgets
        
        for var, data in test.iteritems():
            print "Setting up: ", var
            pyvar = PyVariableWidget(name=var,desc=data[0])
            pyvar.setValue(data[1])
            widgets.append(pyvar)
            self.variablesWidget.layout().addWidget(pyvar)
        











