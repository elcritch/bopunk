#/usr/bin/env python

"""
mainwindow.py

The main window of the BoPunk Application.

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
import sys, os, uuid
import time, shutil, tempfile
# from __future__ import print_function # import future print function

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QString, Qt, QVariant, SIGNAL, SLOT, QUrl
from PyQt4.QtGui import *
import sip # for bbfreeze

import BoPunk
import BoPunk.lib

from BoPunk.MainWindow import Ui_MainWindow
from BoPunk.FirmwareTableModel import FirmwareTableModel

import BoPunk.lib.urlcache as urlcache
from BoPunk.FirmwareProxy import FirmwareProxy
from BoPunk.FirmwareFeed import *
from BoPunk.lib.firmcache import * 

SETTINGS = {
    "firmware_cache":"../cache/firms/",
    "image_cache":"../cache/imgs/"
} 

def dprint(*line):
    print line

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent = None):
        
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Variables
        # TODO: add persistent settings and configure
        
        # reference dialog box buttons by name
        std_button = QDialogButtonBox.StandardButton
        std_buttons = [ bt for bt in dir(QDialogButtonBox) 
            if type(getattr(QDialogButtonBox, bt)) == std_button ]
        stdButtons = \
            dict((getattr(QDialogButtonBox,v),v) for v in std_buttons)
        
        self._dynamicButtons = []
        for b in self.buttonDialogVariables.buttons():
            r = self.buttonDialogVariables.standardButton(b)
            attrname = "buttonDialog"+stdButtons[r]
            self._dynamicButtons.append(attrname)
            setattr(self,attrname, b)
            
        
        # Configure tabs
        self.setup_tabs()
        
        # Setup and start Firmware List
        self.setup_firmware_proxy()
        self.setup_firmtable()
        # self.firmtable_refresh()
        
        # Connect slots/signals and actions
        self.setup_connections()
        
    def setup_tabs(self):
        """configure generic settings of the firmware/downloads tabs"""
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
        
        # DEBUG: tmp
        self.firmcache.clear()
        
    def setup_firmware_proxy(self):
        """Configures the firmware tab and interacts with FirmwareProxy"""
        self.device = FirmwareProxy(self)
        
        
    def setup_firmtable(self):
        """setup the table of firmware with title/author, etc"""
        
        self.header = ["Title","Updated","Author","Summary"]
        self.feed_url = "http://www.bocolab.org/bopunks/feeds/firms.atom.xml"
        self.feed = FirmwareFeed(url=self.feed_url)
        
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
        
    
    def firmtable_refresh(self):
        """
        Download and refresh RSS list of firmware and then parse
        and add the firmwares to the table model
        """
        print "Running firmtable_refresh"
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
            print "ERROR firmtable_refresh:", inst
        
        # set default selection
        self.firmwareTable.selectRow(0)
    
    
    def firmtable_select(self, current, previous):
        """updates the index of selected row"""
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
    
    def firmware_retreive(self, sig = "debugButton"):
        """implements Upload button: retreive firmware"""
        item = self.feed[self._current_row]
        print "firmware_retreive: link:", item.links[0]['href']
        self.firmcache.getfirm(item, sig)
        
    def firmware_save_device(self):
        """Implements functionality for downloading a firmware from device"""
        print "Action: downloadFirmware"
    
    def firmware_upload(self):
        self.firmware_retreive(sig="firmware_upload")
        
    def firmware_manual(self):
        """ Opens an open file dialog to add a file"""
        print "firmware_manual"
        filename = QtGui.QFileDialog.getOpenFileName(
            self,self.tr("Select Firmware"), "", 
            self.tr("Firmware Files ( *.firm *.bin)")
        )
        if not filename:
            return
        
        resource = ""
        item = createLocalItem(self.feed, filename, resource)
        self.feed.addManualItem(item)
        self.tableModel.insertRows(len(self.feed), 1)
    
    def firmware_upload(self, *resource):
        """take a file name (and or file object?) and flash device"""
        print "firmware_upload...", resource
        
        warn = QMessageBox()
        
        warn.setText("Uploading Firmware to BoPunk.")
        warn.setInformativeText("Are you sure you want to upload the firmware?")
        warn.setStandardButtons(QMessageBox.Yes | QMessageBox.Abort)
        warn.setDefaultButton(QMessageBox.Save)
        ret = warn.exec_()
        if ret == QMessageBox.Yes:
            print "upload: Yes"
        elif ret == QMessageBox.Abort:
            print "upload: Abort"
    
    def action_About(self):
        QtGui.QMessageBox.about(
            self,
            self.tr("About"),
            self.tr("BoPunk Firmware Management Application")
        )
    
    def action_settings(self):
        """creates and shows a dialog box for the device settings."""
        print "button: settings dialog"


    def setup_connections(self):
        connect = self.connect 
                
        connect( # Updates html desc page when user selects firmware
            self.firmwareTable.selectionModel(), 
            SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), 
            self.firmtable_select
        )
        
        bindings = {
            'actionUpload': self.firmware_manual, # Upload menu
            'actionDownload': self.firmware_save_device,
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
            'buttonUpdate': ["clicked()",self.firmware_retreive],
            'buttonUpload': ["clicked()",self.firmware_upload],
        }
        
        for name in buttons_bindings:
            sig, act = buttons_bindings[name]
            connect( getattr(self,name), SIGNAL(sig), act )
        
        # try adding any autoconnect methods to dynamic buttons
        on_names = [ on for on in dir(self) if on.startswith('on_') ]
        for on in on_names:
            name, action = on.split('_')[1:]
            sig = "%s()"%action
            connect(getattr(self,name),SIGNAL(sig),getattr(self,on))
        
        # progress bar to set_progress
        connect(self, SIGNAL("set_value(int)"), self.progressBar.setValue)
        connect(self, SIGNAL("set_text(QString)"), self.progressLabel.setText)
        
        connect(self, SIGNAL("firmware_upload"), self.firmware_upload)
        connect(self, SIGNAL("debugButton"), self.debugButton)        
    
    @QtCore.pyqtSignature("on_buttonDialogRestoreDefaults_clicked()")
    def on_buttonDialogRestoreDefaults_clicked(self):
        print "on_buttonDialogRestoreDefaults_clicked!"
        self.device.resetVariableDefaults()
        
    @QtCore.pyqtSignature("on_buttonDialogReset_clicked()")
    def on_buttonDialogRestoreDefaults_clicked(self):
        print "on_buttonDialogReset_clicked!"
        # self.device.resetVariableDefaults()
        
    def set_progress(self, value, msg):
        self.emit(SIGNAL("set_text(QString)"), msg)
        self.emit(SIGNAL("set_value(int)"), int(value))
    
    def reset_progress(self, do_emit, val):
        self.emit(SIGNAL("set_text(QString)"), "")
        self.emit(SIGNAL("set_value(int)"), 0)
        self.emit(SIGNAL(do_emit), *val)
    
    
    def debugButton(self, dat = ""):
        print "Button Clicked: ", dat
    
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
    
    sys.exit(app.exec_())
