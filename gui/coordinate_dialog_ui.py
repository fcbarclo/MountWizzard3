# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coordinate_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CoordinateDialog(object):
    def setupUi(self, CoordinateDialog):
        CoordinateDialog.setObjectName("CoordinateDialog")
        CoordinateDialog.resize(791, 671)
        self.windowTitle = QtWidgets.QLabel(CoordinateDialog)
        self.windowTitle.setGeometry(QtCore.QRect(0, 0, 791, 31))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.windowTitle.setFont(font)
        self.windowTitle.setAutoFillBackground(True)
        self.windowTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.windowTitle.setObjectName("windowTitle")
        self.btn_selectClose = QtWidgets.QPushButton(CoordinateDialog)
        self.btn_selectClose.setGeometry(QtCore.QRect(750, 0, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_selectClose.setFont(font)
        self.btn_selectClose.setObjectName("btn_selectClose")
        self.modelPointsPlot = QtWidgets.QGraphicsView(CoordinateDialog)
        self.modelPointsPlot.setGeometry(QtCore.QRect(10, 70, 771, 371))
        self.modelPointsPlot.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.modelPointsPlot.setAcceptDrops(False)
        self.modelPointsPlot.setAutoFillBackground(True)
        self.modelPointsPlot.setFrameShadow(QtWidgets.QFrame.Plain)
        self.modelPointsPlot.setInteractive(False)
        self.modelPointsPlot.setSceneRect(QtCore.QRectF(0.0, 0.0, 769.0, 369.0))
        self.modelPointsPlot.setObjectName("modelPointsPlot")
        self.modellingLog = QtWidgets.QTextBrowser(CoordinateDialog)
        self.modellingLog.setGeometry(QtCore.QRect(10, 480, 771, 181))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(8)
        self.modellingLog.setFont(font)
        self.modellingLog.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.modellingLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.modellingLog.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.modellingLog.setAcceptRichText(False)
        self.modellingLog.setObjectName("modellingLog")
        self.le_telescopeAzimut = QtWidgets.QLineEdit(CoordinateDialog)
        self.le_telescopeAzimut.setGeometry(QtCore.QRect(50, 40, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.le_telescopeAzimut.setFont(font)
        self.le_telescopeAzimut.setMouseTracking(False)
        self.le_telescopeAzimut.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_telescopeAzimut.setAcceptDrops(False)
        self.le_telescopeAzimut.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_telescopeAzimut.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_telescopeAzimut.setReadOnly(True)
        self.le_telescopeAzimut.setObjectName("le_telescopeAzimut")
        self.le_telescopeAltitude = QtWidgets.QLineEdit(CoordinateDialog)
        self.le_telescopeAltitude.setGeometry(QtCore.QRect(210, 40, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.le_telescopeAltitude.setFont(font)
        self.le_telescopeAltitude.setMouseTracking(False)
        self.le_telescopeAltitude.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_telescopeAltitude.setAcceptDrops(False)
        self.le_telescopeAltitude.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_telescopeAltitude.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_telescopeAltitude.setReadOnly(True)
        self.le_telescopeAltitude.setObjectName("le_telescopeAltitude")
        self.label_9 = QtWidgets.QLabel(CoordinateDialog)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 31, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(CoordinateDialog)
        self.label_10.setGeometry(QtCore.QRect(170, 40, 41, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_109 = QtWidgets.QLabel(CoordinateDialog)
        self.label_109.setGeometry(QtCore.QRect(130, 40, 21, 20))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_109.setFont(font)
        self.label_109.setAlignment(QtCore.Qt.AlignCenter)
        self.label_109.setWordWrap(False)
        self.label_109.setObjectName("label_109")
        self.label_110 = QtWidgets.QLabel(CoordinateDialog)
        self.label_110.setGeometry(QtCore.QRect(290, 40, 21, 20))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_110.setFont(font)
        self.label_110.setAlignment(QtCore.Qt.AlignCenter)
        self.label_110.setWordWrap(False)
        self.label_110.setObjectName("label_110")
        self.label_142 = QtWidgets.QLabel(CoordinateDialog)
        self.label_142.setGeometry(QtCore.QRect(620, 40, 41, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_142.setFont(font)
        self.label_142.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_142.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_142.setObjectName("label_142")
        self.le_SQR = QtWidgets.QLineEdit(CoordinateDialog)
        self.le_SQR.setGeometry(QtCore.QRect(660, 40, 81, 21))
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.le_SQR.setFont(font)
        self.le_SQR.setMouseTracking(False)
        self.le_SQR.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_SQR.setAcceptDrops(False)
        self.le_SQR.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_SQR.setMaxLength(8)
        self.le_SQR.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_SQR.setReadOnly(True)
        self.le_SQR.setObjectName("le_SQR")
        self.label_87 = QtWidgets.QLabel(CoordinateDialog)
        self.label_87.setGeometry(QtCore.QRect(740, 40, 41, 20))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        self.label_87.setFont(font)
        self.label_87.setAlignment(QtCore.Qt.AlignCenter)
        self.label_87.setWordWrap(False)
        self.label_87.setObjectName("label_87")
        self.label_11 = QtWidgets.QLabel(CoordinateDialog)
        self.label_11.setGeometry(QtCore.QRect(530, 450, 41, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.le_modelingStatus = QtWidgets.QLineEdit(CoordinateDialog)
        self.le_modelingStatus.setGeometry(QtCore.QRect(570, 450, 61, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_modelingStatus.setFont(font)
        self.le_modelingStatus.setMouseTracking(False)
        self.le_modelingStatus.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_modelingStatus.setAcceptDrops(False)
        self.le_modelingStatus.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_modelingStatus.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_modelingStatus.setReadOnly(True)
        self.le_modelingStatus.setObjectName("le_modelingStatus")
        self.bar_modelingStatusPercent = QtWidgets.QProgressBar(CoordinateDialog)
        self.bar_modelingStatusPercent.setGeometry(QtCore.QRect(10, 450, 511, 23))
        self.bar_modelingStatusPercent.setMaximum(1000)
        self.bar_modelingStatusPercent.setProperty("value", 1)
        self.bar_modelingStatusPercent.setTextVisible(False)
        self.bar_modelingStatusPercent.setObjectName("bar_modelingStatusPercent")
        self.le_modelingStatusTime = QtWidgets.QLineEdit(CoordinateDialog)
        self.le_modelingStatusTime.setGeometry(QtCore.QRect(710, 450, 41, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.le_modelingStatusTime.setFont(font)
        self.le_modelingStatusTime.setMouseTracking(False)
        self.le_modelingStatusTime.setFocusPolicy(QtCore.Qt.NoFocus)
        self.le_modelingStatusTime.setAcceptDrops(False)
        self.le_modelingStatusTime.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_modelingStatusTime.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_modelingStatusTime.setReadOnly(True)
        self.le_modelingStatusTime.setObjectName("le_modelingStatusTime")
        self.label_12 = QtWidgets.QLabel(CoordinateDialog)
        self.label_12.setGeometry(QtCore.QRect(650, 450, 61, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(CoordinateDialog)
        self.label_13.setGeometry(QtCore.QRect(760, 450, 21, 21))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.checkRunTrackingWidget = QtWidgets.QCheckBox(CoordinateDialog)
        self.checkRunTrackingWidget.setGeometry(QtCore.QRect(340, 40, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkRunTrackingWidget.setFont(font)
        self.checkRunTrackingWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.checkRunTrackingWidget.setChecked(True)
        self.checkRunTrackingWidget.setObjectName("checkRunTrackingWidget")

        self.retranslateUi(CoordinateDialog)
        QtCore.QMetaObject.connectSlotsByName(CoordinateDialog)

    def retranslateUi(self, CoordinateDialog):
        _translate = QtCore.QCoreApplication.translate
        CoordinateDialog.setWindowTitle(_translate("CoordinateDialog", "Modeling Plot Window"))
        self.windowTitle.setText(_translate("CoordinateDialog", "Modeling Plot Window"))
        self.btn_selectClose.setToolTip(_translate("CoordinateDialog", "Sets dual tracking on / off"))
        self.btn_selectClose.setText(_translate("CoordinateDialog", "X"))
        self.modellingLog.setHtml(_translate("CoordinateDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.le_telescopeAzimut.setText(_translate("CoordinateDialog", "130,05"))
        self.le_telescopeAltitude.setText(_translate("CoordinateDialog", "80,50"))
        self.label_9.setText(_translate("CoordinateDialog", "AZ:"))
        self.label_10.setText(_translate("CoordinateDialog", "ALT:"))
        self.label_109.setText(_translate("CoordinateDialog", "°"))
        self.label_110.setText(_translate("CoordinateDialog", "°"))
        self.label_142.setText(_translate("CoordinateDialog", "SQR:"))
        self.le_SQR.setToolTip(_translate("CoordinateDialog", "shows the refraction correction status on / off"))
        self.le_SQR.setText(_translate("CoordinateDialog", "19.00"))
        self.label_87.setText(_translate("CoordinateDialog", "mpas"))
        self.label_11.setText(_translate("CoordinateDialog", "Point:"))
        self.le_modelingStatus.setToolTip(_translate("CoordinateDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Progress in modeling.</span></p></body></html>"))
        self.le_modelingStatus.setText(_translate("CoordinateDialog", "-- of --"))
        self.le_modelingStatusTime.setToolTip(_translate("CoordinateDialog", "<html><head/><body><p><span style=\" font-size:10pt;\">Progress in modeling.</span></p></body></html>"))
        self.le_modelingStatusTime.setText(_translate("CoordinateDialog", "--:--"))
        self.label_12.setText(_translate("CoordinateDialog", "est. finish"))
        self.label_13.setText(_translate("CoordinateDialog", "min"))
        self.checkRunTrackingWidget.setToolTip(_translate("CoordinateDialog", "<html><head/><body><p>Checked if you would like to see the tracking line and flip time in the window</p></body></html>"))
        self.checkRunTrackingWidget.setText(_translate("CoordinateDialog", "Show Track"))
