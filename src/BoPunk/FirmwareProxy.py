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


class FirmwareVar:
    def __init__(self, line):
        """parses the output from the device for variables dump."""
        
    
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
        




class FakeFirm:
    def __init__(self):
        """provides an imitation firmware interaction"""
        self.data = {
            'Rate': { 'min':'10', 'max':'40' , 'def': '30', 'val': '23', 'type': 'int' },
            'Intensity':  { 'min':'0', 'max':'10' , 'def': '5', 'val': '5', 'type': 'int' },
            'Randomness': { 'min':'0.0', 'max':'100.0' , 'def': '80.0', 'val': '75.56', 'type': 'float' }, 
            'R-factor': { 'min':'0', 'max':'10' , 'def': '5', 'val': '5', 'type': 'int' },
            'Z-factor': { 'min':'0', 'max':'10' , 'def': '5', 'val': '5', 'type': 'int' },
            'Modulate': { 'min':'', 'max':'', 'def':'True', 'val':'True', 'type':'bool'},
        }        
        self.fmt = ['min','max','def','val','type']
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
            return self.data[args[1]]['val']
        elif cmd.startswith("set"):
            self.data[args[1]]['val'] = args[2]
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

if __name__ == '__main__':
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
    
    


