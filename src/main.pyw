#!/usr/bin/env python

"""
main.pyw

An example application for creating logos.

Copyright (C) 2007 David Boddie <david@boddie.org.uk>

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

import os, sys
from PyQt4.QtGui import QApplication
from bopunk import MainWindow

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()

    except (Exception), detail:
        import traceback
        sys.stderr.write( "BoPunk Exception:"+repr(detail) )
        traceback.print_exc(file=sys.stderr)
        exit(1)
    code = app.exec_()
    try:
        print "Syncing..."
        Settings().manual_items.sync()
        Settings().sync()
    except (Exception), fini:
        print "Exit Exception:", fini
        import traceback
        traceback.print_exc()
        traceback.print_stack()
        
    finally:
        sys.exit(code)
