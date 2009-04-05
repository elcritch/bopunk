"""
Provieds a class to get a file

Author: Jarremy Creechley
License: See License.txt for more details

Copyright (C) 2009 Bocolabs <info@bocolab.org>

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
from __future__ import with_statement 

import os, sys
import shelve

from PyQt4 import QtCore
from PyQt4.QtCore import QString, Qt, QVariant, SIGNAL, SLOT, QSettings
from PyQt4.QtGui import *
import BoPunk.lib.plistlib as plistlib

DEFAULT_SETTINGS = {
    'dir/firmware_cache':"/firms/",
    'dir/manual_firms_db':"/firms/manual_firms.plist",
    'url/feed':"http://www.bocolab.org/bopunks/feeds/firms.atom.xml",
    'serial/port':0,
}

# Note: Not used for System settings currently. 
class PListDict(dict):
    def __init__(self, path):
        # TODO: could use plist as a format for QSettings... maybe another day
        """init dict with plist from given path. 
        
        This just simplifies storing settings dict as a plist. 
        It operates as a normal dict with initialization from plist or 
        sync'ing it to disk when done.
        """        
        self.__path = path
        try:
            with open(self.__path,'r') as plist_fl:
                d = plistlib.readPlist(plist_fl)
                dict.__init__(self, d)
        except (Exception), io:
            print "Settings:PListDict:init:", io
            dict.__init__(self, DEFAULT_SETTINGS)
        
    def sync(self):
        """synchronize list of manual objects. """
        try:
            with open(self.__path,'w') as plist_fl:
                print "FirmwareFeed:PListDict:sync: Writing ", self.__path
                plistlib.writePlist(dict(self),plist_fl)        
        except (IOError), io:
            print "Settings:PListDict:sync: Error:", io


## Singleton class
class Settings:
    """Provide singleton persistant dictionary like object for settings.

    Also, returned object attributes can be used to store run-time global
    references while standard dictionary interface can be used for
    persistant settings. Note, writeback is turned on, so size of settings
    should be limited for performance reasons. The Settings class is a
    wrapper for the global Singleton instance.
    """
    ## Stores the unique singleton instance-
    __instance = None

    ## Class used with this Python singleton design pattern
    class Singleton:
        """Actual class used to hold settings. """
        def __init__(self):
            """init method, shouldn't be called directly."""
            
            # self.qsettings = QSettings("Bocolab", "BoPunk")
            #### Important: sets location of main setup file
            # TODO: hack. should use QtSettings Class
            settings = QSettings(
                QSettings.IniFormat,
                QSettings.UserScope,
                "Bocolab","BoPunk"
                )
            settings.setFallbacksEnabled(False)
            self._settings = settings
            
            self._settings_filename = os.path.abspath(str(settings.fileName()))
            self._settings_dirname = os.path.dirname(self._settings_filename)
            self._homedir = str(QtCore.QDir.homePath())
                        
            if not settings.value("initialized").toBool():
                # Initialize Default Values
                for key, value in DEFAULT_SETTINGS.iteritems():
                    if key.startswith("dir/"): 
                        # Configure directories to use default user directory
                        value = os.path.normpath(value.replace("dir/",""))
                        value = self._settings_dirname+value
                        settings.setValue(key,QVariant(value))
                    else:
                        settings.setValue(key,QVariant(DEFAULT_SETTINGS[key]))
            
                settings.setValue("initialized",QVariant(True))
            
        def settings(self):
            """Return settings object. """
            return self._settings
        
        def getSettingsDir(self):
            """Return directory name of settings folder. """
            return self._settings_dirname
            
        def value(self, key,toType="toString",convert=str):
            """Return value from persistant settings object. """
            return convert( getattr(self._settings.value(key),toType)() )
        
        def setValue(self, key, value):
            """Return value from persistant settings object. """
            return self._settings.setValue(key, QVariant(value))
        
        def sync(self):
            """Synchronize settings to disk file. """
            self._settings.sync()
            
    def __init__( self ):
        """If singleton settings instance not present, instantiate it. """
        if not Settings.__instance:
            Settings.__instance = Settings.Singleton()

    def __getattr__(self, attr):
        """Wrap all attribute accesses to Singleton instance. """
        return getattr(self.__instance,attr)

    def __setattr__(self, key, value):
        """Wrap all attribute sets to Singleton instance. """
        setattr(self.__instance,key,value)

    def __getitem__(self, key):
        """Wrap all item/dict accesses to Singleton instance. """
        return self.__instance.value(key)

    def __setitem__(self, key, value):
        """Wrap all item/dict updates to Singleton instance. """
        self.__instance.setValue(key,value)


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
    print "settings"
    print dir(Settings._Settings__instance)


