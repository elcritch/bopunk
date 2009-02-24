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
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from BoPunk.ui.SettingsDialog import *

class PySettings(QDialog, Ui_Dialog):

    def __init__(self, parent = None):
    
        QDialog.__init__(self, parent)
        self.setupUi(self)


if __name__ == '__main__':
    import sys, os
    app=QApplication(sys.argv)
    # window = QWidget()
    
    ps = PySettings()
    # ps.show()
    ret = ps.exec_()
    print "Return:", ret
    exit(ret)