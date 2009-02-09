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



class PyVariableWidget(QWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, variable, desc="sample variable", kind=None, *args):
        QWidget.__init__(self,*args)
        print "variable", variable
        # setup text
        self.var = variable
        self._name = variable['name']
        self._desc = desc
        self._kind = self.get_kind(variable['type'])
        self._range = (variable['min'],variable['max'])
        print "self._range", self._range
        
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
            self.setupRange(self._range)
            
        # configure variables/connections, titles
        self.setupSignals()
        self.setupRange(self._range)
        self.ui.varBox.setTitle(self._name)
        self.ui.desc.setText(desc)
        
        # finally set the default value
        self.setValue(variable['value'])
    
    def get_kind(self, tp):
        """return kind of variable"""
        if tp in TYPE_BOOL: return 'bool'
        elif tp in TYPE_FLOAT: return 'float'
        elif tp in TYPE_INT: return 'int'
    
    def setupRange(self, range):
        """configure the range and step size for widgets"""
        self.ui.spinner.setRange(*range)
        self.ui.slider.setRange(*range)
        size = 100 if self._kind == 'int' else 100.0
        step = (range[1]-range[0])/size
        step = step if not step == 0 else 1
        self.ui.spinner.setSingleStep(step)
        self.ui.slider.setSingleStep(int(step))
        
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
        val = int(val) if self._kind == 'int' else float(val)
        self.ui.spinner.setValue(val)
        if self._kind
        self.ui.slider.setValue(int(val))
    
    def value(self):
        """return value"""
        return self.ui.spinner.value()

class PyBoolVariableWidget(PyVariableWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, variable, desc='', *args):
        QWidget.__init__(self,*args)

        # setup text
        self.var = variable
        self._desc = desc
        self._name = variable['name']
        self._kind = variable['type']
        
        if not self._kind == 'bool':
            raise Exception("incorrect variable type: not bool")

        self.ui = BoolVariableWidget.Ui_Form()
        self.ui.setupUi(self)
        self.setupSignals()

        # set value
        self.setValue(variable['value'])

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



if __name__=="__main__":
    dir(VariableWidget)
    
    from sys import argv
    app=QApplication(argv)
    window = QWidget()
    vars = []
    vars.append({'name': 'Rate', 'min': 0, 'default': 15, 'max': 100, 'value': 10, 'type': 'int'})
    vars.append({'name': 'Speed', 'min': 0.0, 'default': 0.5, 'max': 1.0, 'value': 0.65000000000000002, 'type': 'real'})
    vars.append({'name': 'Intensity', 'min': 0, 'default': 100, 'max': 1000, 'value': 150, 'type': 'int'})
    vars.append({'name': 'Toggle', 'min': None, 'default': True, 'max': None, 'value': True, 'type': 'bool'})
    print "vars", vars
    w = PyVariableWidget(vars[0])
    v = PyVariableWidget(vars[1])
    z = PyBoolVariableWidget(vars[-1])
    
    layout = QVBoxLayout()
    layout.addWidget(w)
    layout.addWidget(v)
    layout.addWidget(z)
    
    window.setLayout(layout)
    window.show()
    
    
    app.connect(app, SIGNAL("lastWindowClosed()")
                , app, SLOT("quit()"))
    app.exec_()
