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
TYPE_INT = ['int','integer']
TYPE_FLOAT = ['real','double','float']
TYPE_BOOL = ['bool','boolean','check']


class FirmVariable:
    def __init__(self, line):
        """parses the output from the device for variables dump."""
        self.line = line = line.split()
        self.fmt = fmt = ['name','type','value','default','min','max']
        self.type = line[1] # the kind should be second
        
        # this might be overdoing it, but its already done
        self.attr = attr = {}
        attr['name'] = self.get('name')
        attr['type'] = self.get('type')
        for name in ['min','max','default','value']:
            attr[name] = self.parse_kind(self.get(name))
    
    def __getattr__(self, val):
        if self.attr.has_key(val.lower()):
            return self.attr[val.lower()]
        
    def get(self, val):
        """find the proper index and return proper column of input line"""
        idx = self.fmt.index(val)
        return self.line[idx] if idx>=0 and idx<len(self.line) else None
    
    def parse_kind(self, val):
        """provide parsing for different types"""
        if not val: return None
        if self.type in TYPE_INT:
            return int(val)
        elif self.type in TYPE_FLOAT:
            return float(val)
        elif self.type in TYPE_BOOL:
            if val.lower() == ['false','F','0']:
                return False
            return True
                
    
class FirmwareProxy(QtCore.QAbstractTableModel):
    def __init__(self, mainwindow):
        """Creates Firmware Proxy for interacting with boPunk device"""
        self.mainwindow = mainwindow
        self.variablesWidget = mainwindow.variablesWidget
        
        # use fake firmware for now
        self.firm = FakeFirm()
        self.setupVariables()
        
        
        
    def setupVariables(self):
        """configure variables for a firmware"""
        listing = self.firm.send('list')
        
    
    def setupWidgets(self):
        self.widgets = widgets = []
        for var, data in test.iteritems():
            print "Setting up: ", var
            pyvar = PyVariableWidget(name=var,desc=data[0])
            pyvar.setValue(data[1])
            widgets.append(pyvar)
            self.variablesWidget.layout().addWidget(pyvar)
        




class FakeFirm:
    def __init__(self):
        """provides an imitation firmware interaction"""
        self.data = {
            'Rate': { 'min':'10', 'max':'40' , 'default': '30', 'value': '23', 'type': 'int' },
            'Intensity':  { 'min':'0', 'max':'10' , 'default': '5', 'value': '5', 'type': 'int' },
            'Randomness': { 'min':'0.0', 'max':'100.0' , 'default': '80.0', 'value': '75.56', 'type': 'float' }, 
            'R-factor': { 'min':'0', 'max':'10' , 'default': '5', 'value': '5', 'type': 'int' },
            'Z-factor': { 'min':'0', 'max':'10' , 'default': '5', 'value': '5', 'type': 'int' },
            'Modulate': { 'min':'', 'max':'', 'default':'True', 'value':'True', 'type':'bool'},
        }        
        self.fmt = ['type','value','default','min','max']
        # self.fmt = ['min','max','default','value','type']
        self.version = """BoPunk Cool Firmware
        Version 1.2.3
        """
        
    def format(self,name):
        val = [name]+[ str(self.data[name][v]) for v in self.fmt ]
        return ' '.join(val) + '\n'
        
    def send(self, cmd):
        args = cmd.split()
        if   cmd.startswith("list"):
            line = ''
            for k in self.data:
                line += self.format(k)
            return line
        elif cmd.startswith("info"):
            return self.format(args[1])
        elif cmd.startswith("get"):
            return self.data[args[1]]['value']
        elif cmd.startswith("set"):
            self.data[args[1]]['value'] = args[2]
        elif cmd.startswith("version"):
            return self.version
        else:
            return ''

"""
to query and set variables among other things.  Commands will be
something
like this:

list  // Dumps a list of all variables, min and max,
      // default and current values, plus a type: int, real, bool,
      // string.  An enumerated type would be good too but not
necessary
      // this round.
      // Each variable will be printed on one line and the parts will
      // be space separated.  String values will be quoted and may
contain
      // spaces but not return characters.
      // The list will be terminated by a blank line.
info <name> // Get same info for a specific variable
get <name>  // Get the value of a specific variable
            // Data returned as a ASCII value on a single line.
set <name> <value>
version   // Dumps firmware and protocol version info.
          // Note this command can be used to test for a valid
connection.
reboot    // Reboot the device
upload <size> // upload a firmware
download  // A file size in ASCII and an end of line followed by
the data

In case an invalid variable name or value range is used the firmware
will
return a blank line followed by an error string.
"""


def testFake():
    f = FakeFirm()
    
    ret = f.send('list')
    print "list:\n", ret
    
    ret = f.send('info Rate')
    print "info:", ret
    
    ret = f.send('get Rate')
    print "'get Rate':", ret
    
    ret = f.send('set Rate 10')
    ret = f.send('get Rate')
    print "'set/get Rate 10':", ret

def testProxy():
    win = type('', (), {'variablesWidget':None})()
    proxy = FirmwareProxy(win)

def testFirmVariable():
    f = FakeFirm()
    
    ret = f.send('list')
    print "list:\n", ret
    
    for line in ret.splitlines():
        print "\nline:", line
        var = FirmVariable(line)
        print "var.name", var.name
        print "var.default", var.default
        print "var.value", var.value
        print "var.min", var.min
        print "var.max", var.max
    
if __name__ == '__main__':
    testFirmVariable()





