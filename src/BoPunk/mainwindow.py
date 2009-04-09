#/usr/bin/env python

"""
mainwindow.py

The main window of the BoPunk Application.

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
import sys, os, uuid
import time, shutil, tempfile, threading, thread
# from __future__ import print_function # import future print function

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, Qt, QVariant, SIGNAL, SLOT, QUrl
from PyQt4.QtGui import *
import sip # for bbfreeze

import BoPunk
import BoPunk.lib

import BoPunk.lib.urlcache as urlcache
import BoPunk.FirmwareFeed as firmfeed

from BoPunk.ui.MainWindow import Ui_MainWindow
from BoPunk.PySettingsDialog import *

from BoPunk.lib.firmcache import *
from BoPunk.lib.ErrorClasses import *
from BoPunk.lib.serial.serialutil import SerialException, SerialTimeoutException

from BoPunk.FirmwareTableModel import FirmwareTableModel
from BoPunk.FirmwareProxy import FirmwareProxy
from BoPunk.FirmwareFeed import *

class MainWindow(QMainWindow, Ui_MainWindow):
    """Main BoPunk Application Window.

    Implements the main window for the bopunk application.
    The method naming scheme trys to describe the purpose
    and the action for the method.

    This class aggregates several other modules/objects
    to do work such as the FirmwareProxy or FirmwareTable
    classes.
    """
    def __init__(self, parent = None):
        """calls appropriate setup methods."""
        # Setup the Gui
        QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Variables
        # TODO: add persistent settings and configure
        self.settings = Settings()
        # attributes of settings are non-persistent
        self.settings.MainWindow = self
        
        # Configure tabs
        self.setup_general()
        self.setup_tabs()

        # Setup and start Firmware List
        self.setup_firmware_proxy()
        self.setup_firmtable()
        # self.firmtable_refresh()

        # Connect slots/signals and actions
        self.setup_connections()

    def setup_tabs(self):
        """configure generic settings of the firmware/downloads tabs."""
        # setup Main window
        self.statusBar().hide()
        self.progressLabel.setText("")
        self.progressBar.reset()
        self.descriptionText.setOpenExternalLinks(True)

        # cache for images/http descriptions
        self.cache_loc = tempfile.mkdtemp()
        self.cache = urlcache.build_opener(self.cache_loc)
        self.descriptionText.setResourceCache(self.cache)

        # cache for firmware downloads
        self.firmcache = FirmCache(self.set_progress, self.reset_progress)
        # set firmcache reference
        self.settings.firmcache = self.firmcache
        
    def setup_general(self):
        """General configuration, also configures extra buttons. """
        # reference dialog box buttons by name


    def setup_firmware_proxy(self):
        """Configures the FirmwareProxy as self.device. """
        self.device = FirmwareProxy(self)
        try:
            self.device.connectDevice()
        except (SerialException), err:
            print "setup_firmware_proxy:",err
        

    def setup_firmtable(self):
        """Setup the Firmware Description Table/Tab.

        Creates and configures FirmwareTableModel which is used to drive
        the self.firmwareTable table widget. The Headers used for the
        columns are also configured here. Also, basic table parameters
        are set here.
        The FirmwareFeed which fetches ATOM feed is also retrieved
        and configured here.
        """

        # TODO: move feed_url to global settings.
        self.header = ["Title","Updated","Author","Summary"]
        self.feed = FirmwareFeed(url=self.settings['url/feed'])
        
        # set global reference
        self.settings.feed = self.feed
        
        # setup table
        self.tableModel = FirmwareTableModel(self.feed, self.header, self)
        table = self.firmwareTable
        table.setModel(self.tableModel)
        table.verticalHeader().hide()
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)

        # set default selection
        table.selectRow(0)

        # fun hack! but ... still a hack
        # create an anonymous object with null functions for row/column
        qmi = type('', (), {'row':lambda s: 0, 'column':lambda s: 0})()
        self.firmtable_select(qmi,0)

        self.splitter.setStretchFactor(1,4)


    ############################################################################
    ## Firmware Methods
    ############################################################################

    def firmtable_refresh(self):
        """Refreshes the FirmwareFeed and repopulates FirmwareTableModel.

        Download and refresh RSS list of firmware and then parse
        and add the firmwares to the table model.
        """
        self.descriptionText.setHtml("")
        self.tableModel.removeRows(0, len(self.feed))
        self.feed.refresh()
        self.tableModel.insertRows(0, len(self.feed))

        loc = self.cache_loc
        try:
            files = os.listdir(self.cache_loc)
            for file in files:
                os.remove(os.path.join(self.cache_loc,file))

        except IOError, inst:
            # TODO: set status bar message?
            print "ERROR firmtable_refresh:", inst

        # set default selection
        self.firmwareTable.selectRow(0)


    def firmtable_select(self, current, previous):
        """Update the index of selected row in the table model.

        The current and previous args need to be selectionModel objects.
        Also updates the contents of the description pane.
        """
        selectionModel = self.firmwareTable.selectionModel()
        indexes = selectionModel.selectedIndexes()
        row = current.row()
        print "selecting index: ", row
        self._current_row = row
        # Use index to set the descriptionText
        if len(self.feed):
            item = self.feed[row]
        else: return

        if item.islocal:
            content = item.getContent(name='value')
            self.descriptionText.setHtml(content)
        else:
            content = item.getContent()
            self.descriptionText.setSource(QUrl(content))

    def firmware_upload(self):
        """Wrapper function to retrieve firmware and then upload it. """
        self.action_retrieve("action_upload")
    
    def firmware_retrieve(self):
        """Wrapper function to retrieve firmware and then upload it. """
        self.action_retrieve("")
    
    
    def firmware_manual(self):
        """ Opens an open file dialog to add a firmware file."""
        print "firmware_manual"
        filename = QtGui.QFileDialog.getOpenFileName(
            self,self.tr("Select Firmware"), "",
            self.tr("Firmware Files ( *.firm *.bin)")
        )
        
        if not filename:
            return
        else:
            self._firmware_add(filename)

        
    def firmware_save(self):
        """ Opens an open file dialog to save a firmware file to file."""
        print "firmware_save"
        filename = QtGui.QFileDialog.getSaveFileName(
            self, self.tr("Save Firmware as"), "",
            self.tr("Firmware Files ( *.firm *.bin)")
        )
        
        self.device.downloadFirmwareDevice( filename, 
            self.set_progress, self.reset_progress)
        
        if not filename or not os.path.exists(filename):
            return
        else:
            self._firmware_add(filename)
    
    def _firmware_add(self, filename):
        """Adds manual firmware to manual firmware feed which is a persistant store. """
        
        filename = str(filename)
        print "firmware_add:", filename
        
        # This should be more robust, the interface is klunky.
        item = firmfeed.createLocalItem(self.feed, filename)
        self.firmcache.getfirm(item,"action_additem")
        self.feed.addManualItem(item)
        self.__manual_item = item
        self.firmcache.getfirm(item, "action_manualitem")
        
    ############################################################################
    ## Action Methods
    ############################################################################
    def action_connect(self):
        """connects device to firmware. """
        try:
            if self.device.check():
                print "action_connect:reset"
                self.device.resetDevice()
            else:
                print "action_connect:connect"
                self.device.connectDevice()
        
        except (SerialException), err:
            print "setup_firmware_proxy:",err
            
        
    def action_manualitem(self,args):
        item = self.__manual_item
        url, resource = args
        print "action_manualitem:args:",args
        print "action_manualitem:resource:",resource
        if not self.firmcache.checkfile(resource):
            # error!
            msg = "Error adding manual item! %s"%(resource)
            self.set_message(3,msg)
            self.feed.delManualItem(item)
        else:
            self.tableModel.insertRows(len(self.feed), 1)
            self.firmtable_refresh()
            
        self.__manual_item = None
            
    def action_retrieve(self, sig):
        """Retrieve firmware using FirmwareCache.

        sig -- action (function) to run when firmware is downloaded from cache.
        """
        item = self.feed[self._current_row]
        print "firmware_retrieve: link:", item.links[0]['href']
        self.firmcache.getfirm(item, sig)
                
        
    def action_upload(self, args):
        """Take a resource name and flash device after asking user.

        resource -- a firmware cache string representing a firmware file.
        """
        url, resource = args
        print "action_upload:resource:", resource
        
        # Check for file before uploading
        if not self.firmcache.checkfile(resource):
            self.set_progress(0, "")
            msg = "Firmware cache file cannot be found!\n%s"%resource
            QtGui.QMessageBox.about(
                self,
                self.tr("Error"),
                self.tr(msg)
            )
            self.set_message(3,msg)
            return
        
        # ask user if they really want to do this?
        warn = QMessageBox()
        warn.setText("Uploading Firmware to BoPunk.")
        warn.setInformativeText("Are you sure you want to upload the firmware?")
        warn.setStandardButtons(QMessageBox.Yes | QMessageBox.Abort)
        warn.setDefaultButton(QMessageBox.Save)
        ret = warn.exec_()

        if ret == QMessageBox.Yes:
            print "upload: Yes"
            # create a new thread for uploading
            thread.start_new_thread(
                self.device.uploadFirmwareDevice,
                (resource,self.set_progress, self.reset_progress)
            )
        elif ret == QMessageBox.Abort:
            print "upload: Aborted"
        

    def action_About(self):
        """displays about dialog. """
        QtGui.QMessageBox.about(
            self,
            self.tr("About"),
            self.tr("BoPunk Firmware Management Application")
        )
    
    def action_settings_dialog(self):
        """Displays settings dialog. 
        
        This should sync settings after it is called.
        """
        print "action_settings_dialog:"
        ps = PySettings()
        
        # set values in dialog
        port = int( Settings()['serial/port'] )
        ps.port_number.setRange(0,255)
        ps.port_number.setValue(port)
        
        ps.feed_url.setText(Settings()['url/feed'])
        
        ret = ps.exec_()
        
        print "action_settings_dialog:ret:",ret
        
        # TODO: save/store settings
        if ret or ret == 1:
            # set values in dialog
            Settings()['serial/port'] = int(ps.port_number.value())
            Settings()['url/feed'] = str(ps.feed_url.text())
            Settings().sync()
        
    def action_settings(self):
        """Creates and shows a dialog box for the device settings."""
        print "action_settings: settings dialog"
        # TODO: implement settings box.

    def action_restore_vars(self):
        """Calls firmware proxy to reset all firmware variable values. """
        print "action_restorevariables:"
        self.device.resetVariableDefaults()

    def action_refresh_device(self):
        """Refresh the device connection. """
        print "action_restorevariables:"
        self.device.refreshDevice()

    def setup_connections(self):
        """Configures all connects for buttons/actions."""

        connect = self.connect

        connect( # Updates html desc page when user selects firmware
            self.firmwareTable.selectionModel(),
            SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),
            self.firmtable_select
        )

        bindings = {
            'actionUpload': self.firmware_manual, # Upload menu
            'actionDownload': self.firmware_save,
            'actionPreferences': self.action_settings_dialog,
            'actionAbout': self.action_About,
            'actionExit': QtGui.qApp.quit,
        }
        # Configure action bindings
        for name in bindings:
            connect(getattr(self,name),SIGNAL("triggered()"),bindings[name])

        # Now Bind buttons
        buttons = [ var for var in dir(self) if var.startswith("button") ]
        print "Buttons", buttons
        buttons_bindings = {
            'buttonAddFirmware': ["clicked()",self.firmware_manual],
            'buttonRefresh': ["clicked()",self.firmtable_refresh],
            'buttonUpdate': ["clicked()",self.firmware_retrieve],
            'buttonUpload': ["clicked()",self.firmware_upload],
            # Buttons from Dialog Box
            'buttonVarsRestore': ["clicked()",self.action_restore_vars],
            'buttonFirmConnect': ["clicked()",self.action_connect],
            'buttonFirmRefresh': ["clicked()",self.action_refresh_device],
            'buttonFirmDump': ["clicked()",self.device.printer],
        }

        for name in buttons_bindings:
            sig, act = buttons_bindings[name]
            connect( getattr(self,name), SIGNAL(sig), act )


        # progress bar to set_progress
        connect(self, SIGNAL("set_value(int)"), self.progressBar.setValue)
        connect(self, SIGNAL("set_text(QString)"), self.progressLabel.setText)

        connect(self, SIGNAL("action_upload"), self.action_upload)
        connect(self, SIGNAL("action_manualitem"), self.action_manualitem)
        connect(self, SIGNAL("action_manualitem"), self.action_manualitem)
        connect(self, SIGNAL("actionFinishDialog"), self.action_finished_dialog)
        
        connect(self, SIGNAL("debugButton"), self.debugButton)

    def action_finished_dialog(self,val):
        """Display a finished upload dialog when firmware flashing complete."""
        
        msg = "Firmware finished uploading!"
        QtGui.QMessageBox.about(
            self,
            self.tr("Error"),
            self.tr(msg)
        )
        
        
    ############################################################################
    ## Utility Functions
    ############################################################################
    def set_message(self, interval, msg, value=0):
        """Set a message to display for a given amount of time."""
        self.set_progress(value, msg)
        threading.Timer(interval, self.reset_progress, ("", None)).start()
        
    def set_progress(self, value, msg):
        """This sets the text in bottom status bar.

        Agrs:
        value -- value from 0 to 100 to set scroll bar too.
        msg -- text with which to set status label.
        """
        self.emit(SIGNAL("set_text(QString)"), msg)
        self.emit(SIGNAL("set_value(int)"), int(value))

    def reset_progress(self, do_emit, val):
        """Reset the bottom status bar.

        Args:
        do_emit -- signal string to be emitted when completed.
        val -- arguement list which is passed to do_emit signal.
        """
        self.emit(SIGNAL("set_text(QString)"), "")
        self.emit(SIGNAL("set_value(int)"), 0)
        self.emit(SIGNAL(do_emit), val)


    def debugButton(self, dat = ""):
        """Debug print method."""
        print "Button Clicked: ", dat


def runner():
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


if __name__ == "__main__":
    runner()