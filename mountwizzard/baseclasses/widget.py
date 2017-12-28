############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017
#
# Licence APL2.0
#
############################################################
import logging
import os
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import PyQt5
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from icons import resources


class MwWidget(QWidget):

    logger = logging.getLogger(__name__)
    COLOR_ASTRO = QColor(32, 144, 192)  # blue astro color
    COLOR_BLUE = QColor(0, 0, 255)
    COLOR_YELLOW = QColor(192, 192, 0)
    COLOR_GREEN = QColor(0, 255, 0)
    COLOR_WHITE = QColor(255, 255, 255)
    COLOR_RED = QColor(255, 0, 0)
    COLOR_ORANGE = QColor(192, 96, 96)
    COLOR_BLACK = QColor(0, 0, 0)
    COLOR_POINTER = QColor(255, 0, 255)
    COLOR_POINTER1 = QColor(32, 144, 192)
    COLOR_TRACKWIDGETTEXT = QColor(255, 255, 255)
    COLOR_TRACKWIDGETPOINTS = QColor(128, 128, 128)
    COLOR_WINDOW = QColor(32, 32, 32)
    COLOR_WINDOW_TEXT = QColor(192, 192, 192)
    COLOR_BACKGROUND = QColor(53, 53, 53)
    COLOR_BASE = QColor(25, 25, 25)
    COLOR_BASE_MAIN = QColor(16, 72, 96)
    COLOR_ALTERNATE_BASE = QColor(53, 53, 53)
    COLOR_HIGHLIGHT = QColor(42, 130, 218)

    # define the basic style of the mountwizzard theme
    BASIC_STYLE = """
    QWidget {
        background-color: #181818;
    }
    QLabel {
        background-color: transparent;
        color: #C0C0C0;
    }
    QLabel#mainBackgound {
        border-width: 3px;
        border-color: rgb(16, 72, 96);
        border-style: outset;
        border-radius: 2px;
        background-color: rgb(8, 36, 48);
    }
    QLabel#picALT, QLabel#picAZ {
        border-width: 2px;
        border-color: #404040;
        border-style: outset;
        border-radius: 2px;
    }    
    /* QLine Edit*/
    QLineEdit {
        background-color: #101010;
        color: rgb(32, 144, 192);
        text-align: right;
        font-family: Arial;
        font-style: normal;
        font-weight: bold;
        border-width: 1px;
        border-color: #404040;
        border-style: outset;
        border-radius: 2px;
    }
    QLineEdit[check='false'] {
        background-color: #101010;
        color: rgb(255, 0, 0);
    }
    QLineEdit[check='true'] {
        background-color: #101010;
        color: rgb(32, 144, 192);
    }

    /* Checkboxes */
    QCheckBox {
        color: #C0C0C0;
        spacing: 8px;
    }
    QCheckBox::indicator {
        border-width: 1px;
        border-color: #404040;
        background-color: #101010;
        border-style: outset;
        border-radius: 2px;
        width: 13px;
        height: 13px;
    }
    QCheckBox::indicator:checked {
        background-color: rgb(32, 144, 192);
        image: url(:/checkmark.ico);
    }
    
    /* Spin Boxes */
    QDoubleSpinBox {
        background-color: #101010;
        color: rgb(32, 144, 192);
        text-align: right;
        font-family: Arial;
        font-style: normal;
        font-size: 10pt;
        font-weight: bold;
        border-color: #404040;
        border-width: 1px;
        border-style: outset;
        border-radius: 2px;
        padding-right: 2px;
    }
    QDoubleSpinBox::up-button {
        subcontrol-origin: border;
        subcontrol-position: top right; /* position at the top right corner */
        width: 12px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */
        border-width: 1px;
        border-radius: 2px;
        border-color: #404040;
        border-style: outset;
        background-color: #181818;
    }
    QDoubleSpinBox::up-arrow {
        image: url(:/arrow-up.ico);
        width: 12px;
        height: 16px;
    }
    QDoubleSpinBox::down-button {
        subcontrol-origin: border;
        subcontrol-position: bottom right; /* position at the top right corner */
        width: 12px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */
        border-width: 1px;
        border-style: outset;
        border-radius: 2px;
        border-color: #404040;
        background-color: #181818;
    }
    QDoubleSpinBox::down-arrow {
        image: url(:/arrow-down.ico);
        width: 12px;
        height: 16px;
    }
    
    /* Push Buttons */
    QPushButton {
        background-color: #202020;
        color: #C0C0C0;
        border-color: #404040;
        border-width: 1px;
        border-style: outset;
        border-radius: 2px;
        font: 10pt;
        min - width: 10em;
    }
    QPushButton:pressed {
        border-color: #404040;
        border-width: 2px;
        border-style: inset;
        border-radius: 2px;
    }
    QPushButton:disabled {
        background-color: #101010;
        color: #404040;
        border-color: #202020;
        border-width: 2px;
        border-style: outset;
        border-radius: 2px;
    }
    QPushButton[running='true'] {
        background-color: rgb(32, 144, 192);
        color: #000000;
    } 
    QPushButton[running='false'] {
        background-color: #202020;
        color: #C0C0C0;
    }     
    QPushButton[cancel='true'] {
        background-color: rgb(192,0, 0);
        color: #C0C0C0;
    } 
    QPushButton[cancel='false'] {
        background-color: #202020;
        color: #C0C0C0;
    }
    QPushButton[iconset='true'] {
        text-align: left;
        padding-left: 10px;
    }   
    /* Combo Boxes */
    QComboBox {
        text-align: right;
        color: #C0C0C0;
        border-color: #404040;
        border-width: 1px;
        border-style: outset;
        border-radius: 2px;
        padding-left: 5px;
        background-color: #202020;
    }
    QComboBox::drop-down {
        subcontrol-origin: border;
        subcontrol-position: right; /* position at the top right corner */
        width: 20px; /* 16 + 2*1px border-width = 15px padding + 3px parent border */
        border-color: #404040;
        border-width: 1px;
        border-style: outset;
        border-radius: 2px;
        background-color: #202020;
    }
    QComboBox::down-arrow {
        image: url(:/arrow-down.ico);
        width: 20px;
        height: 32px;
    }
    QComboBox:item {
        padding-left: 20px;  /* move text right to make room for tick mark */
        height: 30px;
        background-color: #202020;
    }
    QComboBox:item:selected {
        padding-left: 20px;
        border-width: 2px;
        border-radius: 2px;
        border-style: outset;
        border-color: rgb(16, 72, 96);
        background-color: rgb(32, 144, 192);
    }
    /* lines */
    QFrame[frameShape="4"] {/* horizontal lines */
        color: rgb(16, 72, 96);
    }
    QFrame[frameShape="5"] {/* vertical lines */
        color: rgb(16, 72, 96);
    }
    QTabWidget:pane {
        border-width: 2px;
        border-color: #404040;
        border-radius: 2px;
        border-style: outset;
    }
    QTabBar::tab {
        background-color: #202020;
        color: #C0C0C0;
        border-width: 2px;
        border-color: rgb(16, 72, 96);
        border-radius: 2px;
        border-style: outset;
        padding: 4px;
        padding-left: 4px;
        padding-right: 4px;
    }
    QTabBar::tab:selected {
        color: #000000;
        background: rgb(32, 144, 192);
    }
    QTabBar::tab:!selected {
        margin-top: 4px;
    }
    QTabBar::tab:only-one {
        margin: 1;
    }
    
    /* scroll bar */
    QScrollBar:vertical {
        background-color: #202020;
        width: 20px;
        border-width: 1px;
        border-color: #404040;
        border-radius: 2px;
        border-style: solid;
    }
    QScrollBar::handle:vertical {
        border-width: 1px;
        border-color: #404040;
        border-radius: 3px;
        border-style: solid;
        background-color: rgb(32, 144, 192);
        min-height: 15px;
        margin: 21px 0px 21px 0px;
    }
    QScrollBar:up-arrow:vertical {
        image: url(:/arrow-up.ico);
    }
    QScrollBar::down-arrow:vertical {
        image: url(:/arrow-down.ico);
    }
    
    /* progress bar */
    QProgressBar {
        background-color: #101010;
        border-radius: 2px;
        border-width: 1px;
        border-color: #404040;
        border-style: outset;
    }
    QProgressBar::chunk {
        background-color: rgb(32, 144, 192);
        width: 8px;
        margin: 1px;
        border-width: 2px;
        border-color: #404040;
        border-radius: 2px;
        border-style: outset;
    }
    """

    def __init__(self):
        # noinspection PyArgumentList
        super(MwWidget, self).__init__()
        self.palette = QPalette()
        self.bundle_dir = ''
        self.showStatus = False
        self.initUI()

    def closeEvent(self, closeEvent):
        self.showStatus = False

    @staticmethod
    def widgetIcon(gui, icon):
        gui.setIcon(PyQt5.QtGui.QIcon(icon))
        gui.setProperty('iconset', True)
        gui.style().unpolish(gui)
        gui.style().polish(gui)
        gui.setIconSize(PyQt5.QtCore.QSize(32, 16))

    # noinspection PyProtectedMember
    def initUI(self):
        # self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setWindowFlags((self.windowFlags() | Qt.CustomizeWindowHint) & ~Qt.WindowMaximizeButtonHint)
        self.setMouseTracking(True)

        # sizing in gui should be fixed, because I have a static layout
        self.setFixedSize(790, 640)
        # set app icon
        self.setWindowIcon(QIcon(':/mw.ico'))
        self.setStyleSheet(self.BASIC_STYLE)

    @staticmethod
    def selectFile(window, title, folder, filterSet, openFile=True):
        dlg = PyQt5.QtWidgets.QFileDialog()
        dlg.setWindowIcon(PyQt5.QtGui.QIcon(':/mw.ico'))
        dlg.setStyleSheet('background-color: rgb(32,32,32); color: rgb(192,192,192)')
        # dlg.setViewMode(PyQt5.QtWidgets.QFileDialog.List)
        # dlg.setFileMode(PyQt5.QtWidgets.QFileDialog.AnyFile)
        dlg.setFileMode(PyQt5.QtWidgets.QFileDialog.ExistingFile)
        dlg.setNameFilter(filterSet)

        # dialog.setDefaultSuffix("mex")
        dlg.setModal(True)

        ph = window.geometry().height()
        px = window.geometry().x()
        py = window.geometry().y()
        dw = window.width()
        dh = window.height()
        dlg.setGeometry(px, py + ph - dh, dw, dh)
        if openFile:
            value = dlg.getOpenFileName(dlg, title, os.getcwd() + folder, filterSet, options=PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog)
        else:
            value = dlg.getSaveFileName(dlg, title, os.getcwd() + folder, filterSet, options=PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog)
        return value


# class for embed the matplotlib in pyqt5 framework
class IntegrateMatplotlib(FigureCanvasQTAgg):

    def __init__(self, parent=None):
        helper = PyQt5.QtWidgets.QVBoxLayout(parent)
        self.fig = matplotlib.figure.Figure(dpi=75, facecolor=(25 / 256, 25 / 256, 25 / 256))
        FigureCanvasQTAgg.__init__(self, self.fig)
        helper.setContentsMargins(0, 0, 0, 0)
        self.setParent(parent)
        FigureCanvasQTAgg.updateGeometry(self)
        helper.addWidget(self)
