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

class VarWidgetException(Exception):
    pass

class PyVariableWidget(QWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, variable, desc, *args):
        QWidget.__init__(self,*args)
        
        # setup text
        self.var = variable
        self._name = variable['name']
        self._defl = variable['default']
        self._desc = desc
        self._kind = self.get_kind(variable['type'])
        
        # configure variables/connections, titles
        self.setupUI()
        self.setupSignals()
        self.setupRange()
        
        self.ui.varBox.setTitle(self._name)
        self.ui.desc.setText(desc)
        
        
        # finally set the default value
        self.setValue(variable['value'])
        
    # @Override
    def setupUI(self):
        """add ui form"""
        abstract # will give an error if we don't override
        
    # @Override
    def setupRange(self, size = 100):
        """configure the range and step size for widgets"""
        range = self._range
        self.ui.spinner.setRange(*range)
        self.ui.slider.setRange(*range)
        step = (range[1]-range[0])/size
        step = step if not step >= 0 else 1
        self.ui.spinner.setSingleStep(step)
        self.ui.slider.setSingleStep(int(step))
    
    # @Override
    def _setSliderValue(self, val):
        """set slider"""
        self.ui.slider.setValue(int(val))
    def _setSpinnerValue(self, val):
        """sets both the slider and spinner widgets"""
        self.setValue(val)

    def get_kind(self, tp):
        """return kind of variable"""
        if tp in TYPE_BOOL: return 'bool'
        elif tp in TYPE_FLOAT: return 'float'
        elif tp in TYPE_INT: return 'int'
        
    def setupSignals(self):
        # slider change updates spinner using int
        self.connect(
            self.ui.slider,
            SIGNAL("valueChanged(int)"),
            self._setSpinnerValue
        )
        
        # spinner calls setSlider to update slider (if double or int)
        self.connect( 
            self.ui.spinner,
            SIGNAL("valueChanged(QString)"),
            self._setSliderValue
        )
        
        self.connect( 
            self.ui.spinner,
            SIGNAL("valueChanged(QString)"),
            self.emitChange
        )
    
    def emitChange(self):
        # print "updated:", self.value()
        self.emit(SIGNAL("variableChanged(QObject)"),self)
        
    def setValue(self, val):
        """sets both the slider and spinner widgets"""
        self.ui.spinner.setValue(self._type(val))
    
    def value(self):
        """return value"""
        return self.ui.spinner.value()


class PyIntVariableWidget(PyVariableWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, variable, desc, *args):
        self._type = int
        self._range = (variable['min'],variable['max'])
        
        # now call parent's setup
        PyVariableWidget.__init__(self,variable, desc, *args)
        
    def setupUI(self):
        """add ui form"""
        self.ui = VariableWidget.Ui_Form()
        self.ui.setupUi(self)


class PyFloatVariableWidget(PyVariableWidget):
    """create and manage an instance of float version of VariableWidget"""
    def __init__(self, variable, desc, *args):
        self._type = float
        self._range = (variable['min'],variable['max'])
        
        # now call parent's setup
        PyVariableWidget.__init__(self,variable, desc, *args)
            
    def setupUI(self):
        self.ui = VariableWidget.Ui_Form()
        self.ui.setupUi(self)
        
        # TODO: does this leak a widget?
        self.ui.spinner.setParent(None)
        del self.ui.spinner
        
        self.ui.spinner = QDoubleSpinBox(self.ui.varBox)
        self.ui.spinner.setObjectName("spinner")
        self.ui.gridLayout.addWidget(self.ui.spinner, 1, 0, 1, 1)
        
    def setupRange(self, size = 100.0):
        """configure the range and step size for widgets"""
        range = self._range
        step = (range[1]-range[0])/float(size)
        self.ui.spinner.setSingleStep(step)        
        self.ui.spinner.setRange(*range)
        self._step = step
        self._delta = size/(range[1]-range[0])
        
    def _setSliderValue(self, val):
        """set slider"""
        val = (self._type(val)-self._range[0])*self._delta
        self.ui.slider.setValue(int(val))
    
    def _setSpinnerValue(self, val):
        """sets both the slider and spinner widgets"""
        val = self._step*val + self._range[0]
        self.ui.spinner.setValue(val)



class PyBoolVariableWidget(PyVariableWidget):
    """create and manage an instance of VariableWidget"""
    def __init__(self, variable, desc, *args):
        PyVariableWidget.__init__(self,variable, desc, *args)

        if not self._kind == 'bool':
            raise Exception("incorrect variable type: not bool")

    
    def setupRange(self, size = 100.0):
        pass
    
    def setupUI(self):
        self.ui = BoolVariableWidget.Ui_Form()
        self.ui.setupUi(self)
    
    def setupSignals(self):
        """configures connections for a bool widget"""
        self.connect(
            self.ui.checkBox,
            SIGNAL("stateChanged(int)"),
            self.emitChange
        )    

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

def CreateVarWidget(variable, desc, *args):
    kind = variable['type']
    if kind in TYPE_INT:
        var = PyIntVariableWidget(variable, desc, *args)
    elif kind in TYPE_FLOAT:
        var = PyFloatVariableWidget(variable, desc, *args)
    elif kind in TYPE_BOOL:  
        var = PyBoolVariableWidget(variable, desc, *args)
    else:
        raise VarWidgetException("Unkown Variable Type!")
    return var

    
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

    w = CreateVarWidget(vars[0],'')
    v = CreateVarWidget(vars[1],'')
    z = CreateVarWidget(vars[-1],'')
    
    # w = PyIntVariableWidget(vars[0])
    # v = PyFloatVariableWidget(vars[1])
    # z = PyBoolVariableWidget(vars[-1])
    # 

    layout = QVBoxLayout()
    layout.addWidget(w)
    layout.addWidget(v)
    layout.addWidget(z)
    
    window.setLayout(layout)
    window.show()
    
    
    app.connect(app, SIGNAL("lastWindowClosed()")
                , app, SLOT("quit()"))
    app.exec_()
