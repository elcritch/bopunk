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
from pyvariablewidget import CreateVarWidget, VarWidgetException
from bopunk_sim import *

TYPE_INT = ['int','integer']
TYPE_FLOAT = ['real','double','float']
TYPE_BOOL = ['bool','boolean','check']
TYPE_STRING = ['string','str']

class DeviceError(Exception): pass

class FirmVariable:
    def __init__(self, line):
        """parses the output from the device for variables dump."""
        self.line = line = shlex.split(line) # this parses quotations 
        self.fmt = fmt = ['name','type','value','default','min','max']
        self.type = line[1] # the kind should be second
        
        # this might be overdoing it, but its already done
        self.attr = attr = {}
        attr['name'] = self.get('name')
        attr['type'] = self.get('type')
        for name in ['min','max','default','value']:
            attr[name] = self.parse_kind(self.get(name))
            
    def __getattr__(self, val):
        """return attributes as stored in self.attr"""
        if self.attr.has_key(val.lower()):
            return self.attr[val.lower()]
        
    def __getitem__(self, item):
        """method to provide overloaded bracket-[] operators."""
        return self.__getattr__(item)
        
    def __str__(self):
        """string representation"""
        return str(self.attr)
    
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
        elif self.type in TYPE_STRING:
            return str(val)
        else:
            return None
                
    
class FirmwareProxy(QtCore.QObject):
    def __init__(self, mainwindow):
        """Creates Firmware Proxy for interacting with boPunk device"""
        self.mainwindow = mainwindow
        self.varLayout = mainwindow.varLayout
        self.widgetLayout = mainwindow.varWidget.layout()
        
        self.layout = self.varLayout.layout()
        self.widgetLayout.setColumnStretch(0,3)
        self.widgetLayout.setColumnStretch(1,1)
        
        # use fake firmware for now
        self.device = None
        self.blksize = 1024 # default read size
        self.connectDevice()
                
    def connectDevice(self):
        """wrapper method to talk to connect to device"""
        device = self.device = BoPunkSimulator()
        try:
            device.open()
            self.setupVersion()
            self.setupVariables()
            self.setupWidgets()
            self._open = True
        except (SerialException), inst:
            print inst
        
    def _readDevice(self):
        """read data from device in blocksize"""
        if not self.device: raise DeviceError("read error")
        data = ''
        input = True
        while input:
            input = self.device.read(self.blksize)
            data += input
        return data
    
    def _writeDevice(self, line):
        """wrapper to write to device"""
        if not self.device: raise DeviceError("write error")
        self.device.write(line)
    
    def commandDevice(self,cmd):
        """send device a command and read and return result. cmd is command
        to be sent, returning value from device. Raises error is 'Invalid:'
        is returned in the results. """
        mode = self._readDevice()
        self._writeDevice(cmd.strip()+'\n')
        ret = self._readDevice().splitlines()
        
        if True in [ s.startswith('Invalid:') for s in ret[:2] ]:
            raise SerialException(ret)
        if not ret[-1].startswith('>'):
            raise SerialException('Response Incomplete: ')
            
        # return the heading as the first line and the rest of the data
        return ret[0], ret[1:-1]
    
    def setupVersion(self):
        """wrapper method to configure device firmware name, version, etc."""
        header, version = self.commandDevice('version')
        
        if not header.startswith("BoPunk"):
            raise SerialException("Version not for BoPunk")
            
        self.version = dict([(s.strip() for s in v.split(':')) for v in version])
        
        self.mainwindow.d_title.setText(self.version['Title'])
        self.mainwindow.d_id.setText(self.version['ID'])
        self.mainwindow.d_protocol.setText(header+" "+self.version['Protocol'])
        
        
    def setupVariables(self):
        """configure variables for a firmware"""
        header, listing = self.commandDevice('list')
        # print "listing\n", listing
        if not header.startswith('<name> <type> <value> <default>'):
            raise DeviceError('variable listing incorrect')
        
        self._variables = []
        for line in listing:
            # parse lines and create variables for widgets
            var = FirmVariable(line) 
            self._variables.append( var )
            
    def setupWidgets(self):
        """method to configure and initialize widget from FirmVariables"""
        self.widgets = widgets = []
        layout = self.layout
        for var in self._variables:
            try:
                # widgets contains both pyvariable and its variable counterpart
                pyvar = CreateVarWidget(var,"")
                widgets.append(pyvar)
                layout.addWidget(pyvar)
            except VarWidgetException, inst:
                print "inst:", inst
                print "Variable Type not implmented: ", var
                continue
                
    def resetVariableDefaults(self):
        for w in self.widgets:
            var = w.var # get variable
            w.setValue(var['default'])
            
 


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
    from FirmwareProxyTest import *
    import unittest
    unittest.main()
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestCachedHandler)
    # suite.debug()
    # unittest.TextTestRunner(verbosity=4).run(suite)
    





