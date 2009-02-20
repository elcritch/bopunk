"""
The main model class for displaying firmware lists as retrieved from RSS source.

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

class FirmwareTableModel(QtCore.QAbstractTableModel):
    """Creates the model for displaying the firmware list.

    This should be used in conjuction with a QTableView to provide
    the data for the display. It overrides several key methods.
    """

    def __init__(self, feed, headings, parent=None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        # datain should be a dict
        self.myheader = headings
        self.feed = feed

    def rowCount(self, parent):
        """Returns number of rows for model.

        To resize use insert/remove Column/Rows.
        """
        return len(self.feed)

    def columnCount(self, parent):
        """Returns number of columns for model using column headers.

        The header list passed in at initialization is used to determine
        the number of columns, even if data has more information (columns).
        """
        return len(self.myheader)

    def data(self, index, role):
        """Returns the data for the various 'roles' used in a table.

        Currently only the DisplayRole is implemented. This could be extended
        for icons, etc.
        """
        # TODO: add more roles, such as tooltip.
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()

        # return the data for a given row/col
        # use the header to get the proper key for the index
        row = index.row()
        key = self.myheader[index.column()].lower()
        return QVariant(self.feed[row].get(key))

    def headerData(self, section, orientation, role):
        """Returns the names for the headers.

        We also use the myheader data to get the column count. Returns
        emtpy QVariant for roles other than DisplayRole.
        """
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            # return the header name for the section
            return QVariant( self.myheader[section] )
        else:
            return QVariant(str(section))


    def insertRows(self, row, count, parent = QtCore.QModelIndex()):
        """Call this to add to the firmware list.

        The tableView will not update data unless this is called after
        inserting new rows.
        """
        # begin/end must be called
        self.beginInsertRows(parent, row, row+count-1)
        # do any necessary actions...
        self.endInsertRows()
        return True


    def removeRows(self, row, count, parent = QtCore.QModelIndex()):
        """Call this to remove from the firmware list.

        The tableView will not update data unless this is called after
        deleting new rows.
        """
        # begin/end must be called
        self.beginRemoveRows(parent, row, row+count-1)
        # do action
        self.endRemoveRows()
        return True


