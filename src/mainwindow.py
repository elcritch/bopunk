#!/usr/bin/python2.5
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


class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, parent = None):
        
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Variables
        # TODO: add persistent settings and configure
        
        # Configure tabs
        self.setupTabs()
        
        # Setup and start Firmware List
        self.setupFirmwareProxy()
        self.setupFirmwareTable()
        # self.refreshFirmwareTable()
        
        # Connect slots/signals and actions
        self.setupConnections()
        
    def setupTabs(self):
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
        
    def setupFirmwareProxy(self):
        """Configures the firmware tab and interacts with FirmwareProxy"""
        self.boPunk = FirmwareProxy(self)
        
        
    def setupFirmwareTable(self):
        """setup the table of firmware with title/author, etc"""
        
        self.header = ["Title","Updated","Author","Summary"]
        self.feed_url = "http://onyx.boisestate.edu/~jcreechl/bopunk/feeds/firms.atom.xml"
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
        # create an anonymous object with functions for row/column
        qmi = type('', (), {'row':lambda s: 0, 'column':lambda s: 0})()
        self.updateSelection(qmi,0)
        
        self.splitter.setStretchFactor(1,4)        
        
    
    def refreshFirmwareTable(self):
        """
        Download and refresh RSS list of firmware and then parse
        and add the firmwares to the table model
        """
        print "Running refreshFirmwareTable"
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
            print "ERROR refreshFirmwareTable:", inst
        
        
    
    def updateSelection(self, current, previous):
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
    
    def retreiveFirmware(self, sig = "debugButton"):
        """implements Upload button: retreive firmware"""
        item = self.feed[self._current_row]
        print "retreiveFirmware: link:", item.links[0]['href']
        self.firmcache.getfirm(item, sig)
        
    def saveDeviceFirmware(self):
        """Implements functionality for downloading a firmware from device"""
        print "Action: downloadFirmware"
    
    def uploadFirmware(self):
        self.retreiveFirmware(sig="upload_to_device")
        
    def manualFirmware(self):
        """ Opens an open file dialog to add a file"""
        print "manualFirmware"
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
    
    def upload_to_device(self, *resource):
        """take a file name (and or file object?) and flash device"""
        print "upload_to_device...", resource
        
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
    
    def setupConnections(self):
        connect = self.connect 
                
        connect( # Updates html desc page when user selects firmware
            self.firmwareTable.selectionModel(), 
            SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"), 
            self.updateSelection
        )
        
        bindings = {
            'actionUpload': self.manualFirmware, # Upload menu
            'actionDownload': self.saveDeviceFirmware,
            'actionAbout': self.action_About,
            'actionExit': QtGui.qApp.quit,
        }
        # Configure action bindings
        for name in bindings:
            connect( getattr(self,name), SIGNAL("triggered()"), bindings[name] )
        
        # Now Bind buttons 
        buttons = [ var for var in dir(self) if var.startswith("button") ]
        print "Buttons", buttons
        buttons_bindings = {
            'buttonDialogVariables':["clicked()",self.debugButton],
            'buttonSettings': ["clicked(bool)",self.settingsDialog],
            'buttonAddFirmware': ["clicked()",self.manualFirmware],
            'buttonRefresh': ["clicked()",self.refreshFirmwareTable],
            'buttonUpdate': ["clicked()",self.retreiveFirmware],
            'buttonUpload': ["clicked()",self.uploadFirmware],
        }
        for name in buttons_bindings:
            bind = buttons_bindings[name]
            connect( getattr(self,name), SIGNAL(bind[0]), bind[1] )
        
        # progress bar to set_progress
        connect(self, SIGNAL("set_value(int)"), self.progressBar.setValue)
        connect(self, SIGNAL("set_text(QString)"), self.progressLabel.setText)
        
        connect(self, SIGNAL("upload_to_device"), self.upload_to_device)
        connect(self, SIGNAL("debugButton"), self.debugButton)
        
    def settingsDialog(self):
        """creates and shows a dialog box for the device settings."""
        print "button: settings dialog"
    
    def set_progress(self, value, msg):
        time.sleep(0.01)
        self.emit(SIGNAL("set_text(QString)"), msg)
        self.emit(SIGNAL("set_value(int)"), int(value))
    
    def reset_progress(self, do_emit, val):
        self.emit(SIGNAL("set_text(QString)"), "")
        self.emit(SIGNAL("set_value(int)"), 0)
        self.emit(SIGNAL(do_emit), *val)
    
    
    def debugButton(self, dat = ""):
        print "Button Clicked: ", dat
    
    
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
