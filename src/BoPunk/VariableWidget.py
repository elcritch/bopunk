# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/VariableWidget.ui'
#
# Created: Fri Jan 23 18:17:36 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.varBox = QtGui.QGroupBox(Form)
        self.varBox.setGeometry(QtCore.QRect(40, 20, 311, 111))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.varBox.sizePolicy().hasHeightForWidth())
        self.varBox.setSizePolicy(sizePolicy)
        self.varBox.setObjectName("varBox")
        self.gridLayout = QtGui.QGridLayout(self.varBox)
        self.gridLayout.setObjectName("gridLayout")
        self.labelDesc = QtGui.QLabel(self.varBox)
        self.labelDesc.setObjectName("labelDesc")
        self.gridLayout.addWidget(self.labelDesc, 0, 0, 1, 1)
        self.desc = QtGui.QLabel(self.varBox)
        self.desc.setObjectName("desc")
        self.gridLayout.addWidget(self.desc, 0, 1, 1, 1)
        self.slider = QtGui.QSlider(self.varBox)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("slider")
        self.gridLayout.addWidget(self.slider, 1, 1, 1, 1)
        self.spinner = QtGui.QSpinBox(self.varBox)
        self.spinner.setObjectName("spinner")
        self.gridLayout.addWidget(self.spinner, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.varBox.setTitle(QtGui.QApplication.translate("Form", "VarName", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDesc.setText(QtGui.QApplication.translate("Form", "Description:", None, QtGui.QApplication.UnicodeUTF8))
        self.desc.setText(QtGui.QApplication.translate("Form", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))

