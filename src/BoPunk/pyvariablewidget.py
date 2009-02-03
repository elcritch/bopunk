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
import BoolVariableWidget

TYPE_INT = ['int','integer']
TYPE_FLOAT = ['real','double','float']
TYPE_BOOL = ['bool','boolean','check']

class PyBoolVariableWidget(QWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, name="Sample",desc="sample variable", 
                 value=False, kind='bool', *args):
        QWidget.__init__(self,*args)
        
        # setup text
        self._name = name
        self._desc = desc

        self.ui = BoolVariableWidget.Ui_Form()
        self.ui.setupUi(self)
        self.setupSignals()
        
        # set value
        self.setValue(value)
    
    def setupSignals(self):
        """configures connections for a bool widget"""
        self.connect(
            self.ui.checkBox,
            SIGNAL("stateChanged(int)"),
            self.emitChange
        )    
    
    def emitChange(self):
        print "updated:", self.value()
        self.emit(SIGNAL("variableChanged(QObject)"),self)
    
    def setValue(self, val):
        if val:
            val = QtCore.Qt.Checked
        else:
            val = QtCore.Qt.Unchecked
        
        self.ui.checkBox.setCheckState(val)
    
    def value(self):
        """return check value"""
        state = self.ui.checkBox.checkState()
        if state:
            return True
        else:
            return False 
    


class PyVariableWidget(QWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, name="Sample",desc="sample variable", 
                 value=0, range=(0,50), kind='int', *args):
        QWidget.__init__(self,*args)
        
        # setup text
        self._name = name
        self._desc = desc
        self._range = range
        self._kind = kind.lower()
        
        # add ui form
        self.ui = VariableWidget.Ui_Form()
        self.ui.setupUi(self)
        
        # promote spinner box to double type
        if self._kind in ['double','real', 'float']:
            # remove old spinner
            spinner = self.ui.spinner
            spinner.setParent(None)
            del spinner
            
            self.ui.spinner = QDoubleSpinBox(self.ui.varBox)
            self.ui.spinner.setObjectName("spinner")
            self.ui.gridLayout.addWidget(self.ui.spinner, 1, 0, 1, 1)
            self.setupRange(range)
            
        # configure variables/connections, titles
        self.setupSignals()
        self.setupRange(range)
        self.ui.varBox.setTitle(name)
        self.ui.desc.setText(desc)
        
        # finally set the default value
        self.setValue(value)
        
    def debug(self):
        """docstring for debug"""
        print "destroyed:"
    
    def setupRange(self, range):
        self.ui.spinner.setRange(*range)
        self.ui.slider.setRange(*range)
        
    def setupSignals(self):
        # slider change updates spinner using int
        self.connect(
            self.ui.slider,
            SIGNAL("valueChanged(int)"),
            # self.ui.spinner.setValue
            self.setValue
        )
        
        # spinner calls setSlider to update slider (if double or int)
        self.connect( 
            self.ui.spinner,
            SIGNAL("valueChanged(QString)"),
            self.setValue
        )
        
        self.connect( 
            self.ui.spinner,
            SIGNAL("valueChanged(QString)"),
            self.emitChange
        )
    
    def emitChange(self):
        print "updated:", self.value()
        self.emit(SIGNAL("variableChanged(QObject)"),self)
        
    def setValue(self, val):
        """sets both the slider and spinner widgets"""
        val = int(val) if self._kind in TYPE_INT else float(val)
        self.ui.slider.setValue(int(val))
        self.ui.spinner.setValue(val)
    
    def value(self):
        """return value"""
        return self.ui.spinner.value()


if __name__=="__main__":
    dir(VariableWidget)
    
    from sys import argv
    app=QApplication(argv)
    window = QWidget()
    
    w = PyVariableWidget(kind='int')
    v = PyVariableWidget(kind='real')
    z = PyBoolVariableWidget()
    
    layout = QVBoxLayout()
    layout.addWidget(w)
    layout.addWidget(v)
    layout.addWidget(z)
    
    window.setLayout(layout)
    window.show()
    
    
    app.connect(app, SIGNAL("lastWindowClosed()")
                , app, SLOT("quit()"))
    app.exec_()
