"""
Provides a widget class for setting up variables for boPunk device values. 

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
import VariableWidget

class PyVariableWidget(QWidget, VariableWidget.Ui_Form):
    """create and manage an instance of VariableWidget"""
    def __init__(self, name="",desc="sample variable", range=(0,100), isDouble=False, *args):
        QWidget.__init__(self,*args)
        self.setupUi(self)
        self.isDouble = isDouble
        
        # setup text
        self.varBox.setTitle(name)
        self.desc.setText(desc)
        
        # If variable is double override default type
        if self.isDouble:
            del self.spinner
            self.spinner = QDoubleSpinBox(self.varBox)
            self.spinner.setObjectName("spinner")
            self.gridLayout.addWidget(self.spinner, 1, 0, 1, 1)
        
        
        # slider change updates spinner using int
        self.connect(
            self.slider,
            SIGNAL("valueChanged(int)"),
            self.spinner.setValue
        )
        
        # spinner calls setSlider to update slider (if double or int)
        kind = "double" if self.isDouble else "int"
        self.connect( 
            self.spinner,
            SIGNAL("valueChanged(%s)"%kind),
            self.setSlider
        )
        
    
    def setSlider(self, val):
        """provide a wrapper for int/double values to set slider"""
        print "setSlider:", val, self
        self.slider.setValue(int(val))

    def value(self):
        """return value"""
        return self.spinner.value()


if __name__=="__main__":
    dir(VariableWidget)
    
    from sys import argv
    app=QApplication(argv)
    
    
    w = PyVariableWidget(isDouble=True)
    w.show()

    app.connect(app, SIGNAL("lastWindowClosed()")
                , app, SLOT("quit()"))
    app.exec_()
