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
            self._settings = SETTINGS = {'firmware_cache':"./cache/firms/"} 
        def settings(self):
            return self._settings
        
    def __init__( self ):
        if not Settings.__instance:
            Settings.__instance = Settings.Singleton() 
    
    def __getattr__(self, attr):
        return self.__instance._settings.get(attr)
 
    def __setattr__(self, key, value):
        self.__instance._settings[key] = value
        
    def __getitem__(self, key):
        return self.__instance._settings.get(key)
        
    def __setitem__(self, key, value):
        self.__instance._settings[key] = value
    
 
## Test script to prove that it actually works        
if __name__ == "__main__":
    a = Settings() 
    b = Settings()
    b.test = "Hello Folks"
    c = Settings()
    print a.test
    print c.test
    print "a", a    
    print "c['firmware_cache']", c['firmware_cache']
    print "a['firmware_cache']", a['firmware_cache']
    a['firmware_cache'] = "nil!"
    print "c['firmware_cache']", c['firmware_cache']
    print "a['firmware_cache']", a['firmware_cache']
    
    