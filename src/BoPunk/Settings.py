"""
Provieds a class to get a file 

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

## Singleton class
#
class Settings( object ):
    ## Stores the unique singleton instance-
    __instance = None
    
    ## Class used with this Python singleton design pattern
    class Singleton:
        def __init__(self):
            self._settings = SETTINGS = {'firmware_cache':"../cache/firms/"} 
        def __getitem__(self, key):
            return self._settings.get(key)
        def settings(self):
            return self._settings
        
    def __init__( self ):
        if Settings.__instance is None:
            Settings.__instance = Settings.Singleton() 
        self.__dict__['_EventHandler_instance'] = Settings.__instance
    
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)
 
    def __setattr__(self, attr, val):
        return setattr(self.__instance, attr, val)
        
    def __getitem__(self, key):
        return self._settings.get(key)
    
 
## Test script to prove that it actually works        
if __name__ == "__main__":
    a = Settings() 
    b = Settings()
    b.test = "Hello Folks"
    c = Settings()
    print a.test
    print c.test
    print "a", a
    print "a", a['firmware_cache']