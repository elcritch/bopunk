# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface/BoolVariableWidget.ui'
#
# Created: Mon Feb  2 22:06:46 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.varBox = QtGui.QGroupBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.varBox.sizePolicy().hasHeightForWidth())
        self.varBox.setSizePolicy(sizePolicy)
        self.varBox.setFlat(True)
        self.varBox.setCheckable(False)
        self.varBox.setObjectName("varBox")
        self.gridLayout = QtGui.QGridLayout(self.varBox)
        self.gridLayout.setObjectName("gridLayout")
        self.labelDesc = QtGui.QLabel(self.varBox)
        self.labelDesc.setObjectName("labelDesc")
        self.gridLayout.addWidget(self.labelDesc, 0, 0, 1, 1)
        self.desc = QtGui.QLabel(self.varBox)
        self.desc.setObjectName("desc")
        self.gridLayout.addWidget(self.desc, 0, 1, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.varBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.verticalLayout.addWidget(self.varBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.varBox.setTitle(QtGui.QApplication.translate("Form", "VarName", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDesc.setText(QtGui.QApplication.translate("Form", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.desc.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Form", "Enable", None, QtGui.QApplication.UnicodeUTF8))

