# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface/BoPunkMainWindow.ui'
#
# Created: Sat Feb 21 23:28:53 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(864, 755)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtGui.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.downloadsTab = QtGui.QWidget()
        self.downloadsTab.setObjectName("downloadsTab")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.downloadsTab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtGui.QFrame(self.downloadsTab)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setObjectName("frame")
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.splitter = QtGui.QSplitter(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self.splitter.setLineWidth(1)
        self.splitter.setMidLineWidth(1)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setHandleWidth(4)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setSpacing(-1)
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setBaseSize(QtCore.QSize(0, 0))
        self.label_9.setObjectName("label_9")
        self.verticalLayout_3.addWidget(self.label_9)
        self.firmwareTable = QtGui.QTableView(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.firmwareTable.sizePolicy().hasHeightForWidth())
        self.firmwareTable.setSizePolicy(sizePolicy)
        self.firmwareTable.setBaseSize(QtCore.QSize(150, 300))
        self.firmwareTable.setProperty("showDropIndicator", QtCore.QVariant(False))
        self.firmwareTable.setAlternatingRowColors(True)
        self.firmwareTable.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.firmwareTable.setShowGrid(False)
        self.firmwareTable.setSortingEnabled(False)
        self.firmwareTable.setCornerButtonEnabled(False)
        self.firmwareTable.setObjectName("firmwareTable")
        self.verticalLayout_3.addWidget(self.firmwareTable)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_7.setSpacing(-1)
        self.verticalLayout_7.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_26 = QtGui.QLabel(self.layoutWidget1)
        self.label_26.setObjectName("label_26")
        self.verticalLayout_7.addWidget(self.label_26)
        self.descriptionText = PTextBrowser(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.descriptionText.sizePolicy().hasHeightForWidth())
        self.descriptionText.setSizePolicy(sizePolicy)
        self.descriptionText.setMinimumSize(QtCore.QSize(300, 300))
        self.descriptionText.setFrameShape(QtGui.QFrame.Box)
        self.descriptionText.setObjectName("descriptionText")
        self.verticalLayout_7.addWidget(self.descriptionText)
        self.verticalLayout_8.addWidget(self.splitter)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonAddFirmware = QtGui.QPushButton(self.frame)
        self.buttonAddFirmware.setObjectName("buttonAddFirmware")
        self.horizontalLayout_2.addWidget(self.buttonAddFirmware)
        self.buttonRefresh = QtGui.QPushButton(self.frame)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.horizontalLayout_2.addWidget(self.buttonRefresh)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.buttonUpdate = QtGui.QPushButton(self.frame)
        self.buttonUpdate.setObjectName("buttonUpdate")
        self.horizontalLayout_2.addWidget(self.buttonUpdate)
        self.buttonUpload = QtGui.QPushButton(self.frame)
        self.buttonUpload.setObjectName("buttonUpload")
        self.horizontalLayout_2.addWidget(self.buttonUpload)
        self.verticalLayout_8.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addWidget(self.frame)
        self.tabs.addTab(self.downloadsTab, "")
        self.firmwareTab = QtGui.QWidget()
        self.firmwareTab.setObjectName("firmwareTab")
        self.gridLayout = QtGui.QGridLayout(self.firmwareTab)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_2 = QtGui.QGroupBox(self.firmwareTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.varScrollArea = QtGui.QScrollArea(self.groupBox_2)
        self.varScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.varScrollArea.setWidgetResizable(True)
        self.varScrollArea.setObjectName("varScrollArea")
        self.varWidget = QtGui.QWidget(self.varScrollArea)
        self.varWidget.setGeometry(QtCore.QRect(0, 0, 766, 390))
        self.varWidget.setObjectName("varWidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.varWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.varLayout = QtGui.QVBoxLayout()
        self.varLayout.setSpacing(10)
        self.varLayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.varLayout.setObjectName("varLayout")
        self.gridLayout_2.addLayout(self.varLayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        self.varScrollArea.setWidget(self.varWidget)
        self.verticalLayout_5.addWidget(self.varScrollArea)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.buttonVarsRestore = QtGui.QPushButton(self.groupBox_2)
        self.buttonVarsRestore.setFlat(False)
        self.buttonVarsRestore.setObjectName("buttonVarsRestore")
        self.horizontalLayout_3.addWidget(self.buttonVarsRestore)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.groupBox_2, 4, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.firmwareTab)
        self.groupBox_3.setEnabled(True)
        self.groupBox_3.setAutoFillBackground(False)
        self.groupBox_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setContentsMargins(8, -1, -1, 12)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.d_title = QtGui.QLabel(self.groupBox_3)
        self.d_title.setObjectName("d_title")
        self.gridLayout_3.addWidget(self.d_title, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.d_id = QtGui.QLabel(self.groupBox_3)
        self.d_id.setObjectName("d_id")
        self.gridLayout_3.addWidget(self.d_id, 1, 1, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 2, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 2, 0, 1, 1)
        self.d_protocol = QtGui.QLabel(self.groupBox_3)
        self.d_protocol.setObjectName("d_protocol")
        self.gridLayout_3.addWidget(self.d_protocol, 2, 1, 1, 1)
        self.buttonFirmConnect = QtGui.QPushButton(self.groupBox_3)
        self.buttonFirmConnect.setObjectName("buttonFirmConnect")
        self.gridLayout_3.addWidget(self.buttonFirmConnect, 2, 3, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 2, 0, 1, 1)
        self.tabs.addTab(self.firmwareTab, "")
        self.verticalLayout.addWidget(self.tabs)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem5 = QtGui.QSpacerItem(420, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.progressLabel = QtGui.QLabel(self.groupBox)
        self.progressLabel.setObjectName("progressLabel")
        self.horizontalLayout.addWidget(self.progressLabel)
        self.progressBar = QtGui.QProgressBar(self.groupBox)
        self.progressBar.setProperty("value", QtCore.QVariant(24))
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 864, 22))
        self.menubar.setAutoFillBackground(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionUpload = QtGui.QAction(MainWindow)
        self.actionUpload.setObjectName("actionUpload")
        self.actionDownload = QtGui.QAction(MainWindow)
        self.actionDownload.setObjectName("actionDownload")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionUpload)
        self.menuFile.addAction(self.actionDownload)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuFile.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "BoPunk", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Firmware", None, QtGui.QApplication.UnicodeUTF8))
        self.label_26.setText(QtGui.QApplication.translate("MainWindow", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonAddFirmware.setText(QtGui.QApplication.translate("MainWindow", "Add Firmware", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonRefresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonUpdate.setText(QtGui.QApplication.translate("MainWindow", "Update", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonUpload.setText(QtGui.QApplication.translate("MainWindow", "Upload to Device", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.downloadsTab), QtGui.QApplication.translate("MainWindow", "Firmwares", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("MainWindow", "Device Firmware Variables", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonVarsRestore.setText(QtGui.QApplication.translate("MainWindow", "&Restore Defaults", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("MainWindow", "Device Firmware Information", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Firmware Title:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.d_title.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Firmware ID:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.d_id.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Lucida Grande\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Firmware Protocol:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.d_protocol.setText(QtGui.QApplication.translate("MainWindow", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonFirmConnect.setText(QtGui.QApplication.translate("MainWindow", "&Connect", None, QtGui.QApplication.UnicodeUTF8))
        self.tabs.setTabText(self.tabs.indexOf(self.firmwareTab), QtGui.QApplication.translate("MainWindow", "BoPunk Device", None, QtGui.QApplication.UnicodeUTF8))
        self.progressLabel.setText(QtGui.QApplication.translate("MainWindow", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUpload.setText(QtGui.QApplication.translate("MainWindow", "&Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDownload.setText(QtGui.QApplication.translate("MainWindow", "&Download", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About BoPunk", None, QtGui.QApplication.UnicodeUTF8))

from ptextbrowser import PTextBrowser
