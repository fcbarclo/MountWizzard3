############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #  ####
#      ##  ##  #  ##  #     #
#     # # # #  # # # #     ###
#    #  ##  #  ##  ##        #
#   #   #   #  #   #     ####
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.4
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
###########################################################
import logging
import time
import zlib
import queue
from xml.etree import ElementTree
import PyQt5
from PyQt5 import QtCore, QtNetwork, QtWidgets
import indi.indi_xml as indiXML
import astropy.io.fits as pyfits
from baseclasses import checkIP


class INDIClient(PyQt5.QtCore.QObject):
    logger = logging.getLogger(__name__)
    status = QtCore.pyqtSignal(int)
    statusCCD = QtCore.pyqtSignal(bool)
    statusEnvironment = QtCore.pyqtSignal(bool)
    statusDome = QtCore.pyqtSignal(bool)
    receivedImage = QtCore.pyqtSignal(bool)
    processMessage = QtCore.pyqtSignal(object)

    # INDI device types
    GENERAL_INTERFACE = 0
    TELESCOPE_INTERFACE = (1 << 0)
    CCD_INTERFACE = (1 << 1)
    GUIDER_INTERFACE = (1 << 2)
    FOCUSER_INTERFACE = (1 << 3)
    FILTER_INTERFACE = (1 << 4)
    DOME_INTERFACE = (1 << 5)
    GPS_INTERFACE = (1 << 6)
    WEATHER_INTERFACE = (1 << 7)
    AO_INTERFACE = (1 << 8)
    DUSTCAP_INTERFACE = (1 << 9)
    LIGHTBOX_INTERFACE = (1 << 10)
    DETECTOR_INTERFACE = (1 << 11)
    AUX_INTERFACE = (1 << 15)

    CYCLE_COMMAND = 0.2

    data = {
        'ServerIP': '',
        'ServerPort': 7624,
        'Device': {}
    }

    def __init__(self, app, thread):
        super().__init__()

        self.app = app
        self.thread = thread
        self.isRunning = False
        self.mutexIPChange = PyQt5.QtCore.QMutex()
        self.mutexIsRunning = PyQt5.QtCore.QMutex()
        self.checkIP = checkIP.CheckIP()
        self.socket = None
        self.newDeviceQueue = queue.Queue()
        self.settingsChanged = False
        self.imagePath = ''
        self.messageString = ''
        self.cameraDevice = ''
        self.environmentDevice = ''
        self.domeDevice = ''
        self.telescopeDevice = ''
        # signal slot
        #self.app.ui.le_INDIServerIP.textChanged.connect(self.setIP)
        self.app.ui.le_INDIServerIP.editingFinished.connect(self.changedINDIClientConnectionSettings)
        self.app.ui.le_INDIServerPort.textChanged.connect(self.setPort)
        self.app.ui.le_INDIServerPort.editingFinished.connect(self.changedINDIClientConnectionSettings)
        self.app.ui.checkEnableINDI.stateChanged.connect(self.enableDisableINDI)

    def initConfig(self):
        try:
            if 'INDIServerPort' in self.app.config:
                self.app.ui.le_INDIServerPort.setText(self.app.config['INDIServerPort'])
            if 'INDIServerIP' in self.app.config:
                self.app.ui.le_INDIServerIP.setText(self.app.config['INDIServerIP'])
            if 'CheckEnableINDI' in self.app.config:
                self.app.ui.checkEnableINDI.setChecked(self.app.config['CheckEnableINDI'])
        except Exception as e:
            self.logger.error('item in config.cfg not be initialize, error:{0}'.format(e))
        finally:
            pass
        # setting changes in gui on false, because the set of the config changed them already
        self.settingsChanged = True
        self.changedINDIClientConnectionSettings()
        self.enableDisableINDI()

    def storeConfig(self):
        self.app.config['INDIServerPort'] = self.app.ui.le_INDIServerPort.text()
        self.app.config['INDIServerIP'] = self.app.ui.le_INDIServerIP.text()
        self.app.config['CheckEnableINDI'] = self.app.ui.checkEnableINDI.isChecked()

    def changedINDIClientConnectionSettings(self):
        if self.settingsChanged:
            self.settingsChanged = False
            if self.isRunning:
                self.mutexIPChange.lock()
                self.stop()
                #valid, value = self.checkIP.checkIP(self.app.ui.le_INDIServerIP)
                #if valid:
                self.data['ServerIP'] = self.app.ui.le_INDIServerIP.text()
                valid, value = self.checkIP.checkPort(self.app.ui.le_INDIServerPort)
                if valid:
                    self.data['ServerPort'] = value
                self.thread.start()
                self.mutexIPChange.unlock()
            else:
                self.mutexIPChange.lock()
                #valid, value = self.checkIP.checkIP(self.app.ui.le_INDIServerIP)
                #if valid:
                self.data['ServerIP'] = self.app.ui.le_INDIServerIP.text()
                valid, value = self.checkIP.checkPort(self.app.ui.le_INDIServerPort)
                if valid:
                    self.data['ServerPort'] = value
                self.mutexIPChange.unlock()
            self.app.messageQueue.put('Setting IP address for INDI to: {0}:{1}\n'.format(self.data['ServerIP'], self.data['ServerPort']))

    def setPort(self):
        valid, value = self.checkIP.checkPort(self.app.ui.le_INDIServerPort)
        self.app.sharedINDIDataLock.lockForRead()
        self.settingsChanged = (self.data['ServerPort'] != value)
        self.app.sharedINDIDataLock.unlock()

    def setIP(self):
        valid, value = self.checkIP.checkIP(self.app.ui.le_INDIServerIP)
        self.app.sharedINDIDataLock.lockForRead()
        self.settingsChanged = (self.data['ServerIP'] != value)
        self.app.sharedINDIDataLock.unlock()

    def enableDisableINDI(self):
        if self.app.ui.checkEnableINDI.isChecked():
            if not self.isRunning:
                self.thread.start()
        else:
            if self.isRunning:
                self.stop()
            self.status.emit(0)

    def run(self):
        self.logger.info('indi started')
        self.mutexIsRunning.lock()
        if not self.isRunning:
            self.isRunning = True
        self.mutexIsRunning.unlock()
        self.socket = QtNetwork.QTcpSocket()
        self.socket.hostFound.connect(self.handleHostFound)
        self.socket.connected.connect(self.handleConnected)
        self.socket.stateChanged.connect(self.handleStateChanged)
        self.socket.disconnected.connect(self.handleDisconnect)
        self.socket.readyRead.connect(self.handleReadyRead)
        self.socket.error.connect(self.handleError)
        self.processMessage.connect(self.handleReceived)
        while self.isRunning:
            self.doReconnect()
            self.handleNewDevice()
            self.doCommand()
            time.sleep(self.CYCLE_COMMAND)
            PyQt5.QtWidgets.QApplication.processEvents()
        if self.socket.state() != PyQt5.QtNetwork.QAbstractSocket.ConnectedState:
            self.socket.abort()
        else:
            self.socket.disconnectFromHost()
        self.socket.hostFound.disconnect(self.handleHostFound)
        self.socket.connected.disconnect(self.handleConnected)
        self.socket.stateChanged.disconnect(self.handleStateChanged)
        self.socket.disconnected.disconnect(self.handleDisconnect)
        self.socket.readyRead.disconnect(self.handleReadyRead)
        self.socket.error.disconnect(self.handleError)
        self.socket.close()

    def stop(self):
        # if I leave the loop, I close the connection to remote host
        self.mutexIsRunning.lock()
        self.isRunning = False
        self.mutexIsRunning.unlock()
        self.thread.quit()
        self.thread.wait()

    def doCommand(self):
        self.app.sharedINDIDataLock.lockForRead()
        if not self.app.INDICommandQueue.empty() and (self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.ConnectedState):
            indiCommand = self.app.INDICommandQueue.get()
            self.sendMessage(indiCommand)
        self.app.sharedINDIDataLock.unlock()

    def doReconnect(self):
        if self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.UnconnectedState:
            self.app.sharedINDIDataLock.lockForRead()
            self.socket.connectToHost(self.data['ServerIP'], self.data['ServerPort'])
            self.app.sharedINDIDataLock.unlock()

    @PyQt5.QtCore.pyqtSlot()
    def handleHostFound(self):
        self.app.sharedINDIDataLock.lockForRead()
        self.logger.debug('INDI Server found at {}:{}'.format(self.data['ServerIP'], self.data['ServerPort']))
        self.app.sharedINDIDataLock.unlock()

    @PyQt5.QtCore.pyqtSlot()
    def handleConnected(self):
        self.socket.setSocketOption(PyQt5.QtNetwork.QAbstractSocket.LowDelayOption, 1)
        self.socket.setSocketOption(PyQt5.QtNetwork.QAbstractSocket.KeepAliveOption, 1)
        self.app.sharedINDIDataLock.lockForRead()
        self.logger.info('INDI Server connected at {0}:{1}'.format(self.data['ServerIP'], self.data['ServerPort']))
        self.app.sharedINDIDataLock.unlock()
        # get all informations about existing devices on the choosen indi server
        self.app.INDICommandQueue.put(indiXML.clientGetProperties(indi_attr={'version': '1.7'}))

    def handleNewDevice(self):
        if not self.newDeviceQueue.empty():
            device = self.newDeviceQueue.get()
            # now place the information about accessible devices in the gui and set the connection status
            # and configure the new devices adequately
            self.app.sharedINDIDataLock.lockForRead()
            if device in self.data['Device']:
                if 'DRIVER_INFO' in self.data['Device'][device]:
                    if int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.CCD_INTERFACE:
                        # make a shortcut for later use and knowing which is a Camera
                        self.cameraDevice = device
                        self.app.INDICommandQueue.put(
                            indiXML.newSwitchVector([indiXML.oneSwitch('On', indi_attr={'name': 'ABORT'})],
                                                    indi_attr={'name': 'CCD_ABORT_EXPOSURE', 'device': self.app.workerINDI.cameraDevice}))
                    elif int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.WEATHER_INTERFACE:
                        # make a shortcut for later use
                        self.environmentDevice = device
                    elif int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.TELESCOPE_INTERFACE:
                        # make a shortcut for later use
                        self.telescopeDevice = device
                    elif int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.DOME_INTERFACE:
                        # make a shortcut for later use
                        self.domeDevice = device
                else:
                    # if not ready, put it on the stack again !
                    self.newDeviceQueue.put(device)
            self.app.sharedINDIDataLock.unlock()

    def handleError(self, socketError):
        self.logger.warning('INDI client connection fault: {0}, error: {1}'.format(self.socket.errorString(), socketError))

    @PyQt5.QtCore.pyqtSlot()
    def handleStateChanged(self):
        self.status.emit(self.socket.state())
        self.logger.debug('INDI client connection has state: {0}'.format(self.socket.state()))

    @PyQt5.QtCore.pyqtSlot()
    def handleDisconnect(self):
        self.logger.info('INDI client connection is disconnected from host')
        self.app.sharedINDIDataLock.lockForWrite()
        self.data['Device'] = {}
        self.app.sharedINDIDataLock.unlock()
        self.cameraDevice = ''
        self.environmentDevice = ''
        self.domeDevice = ''
        self.telescopeDevice = ''
        self.app.INDIStatusQueue.put({'Name': 'Environment', 'value': '---'})
        self.app.INDIStatusQueue.put({'Name': 'CCD', 'value': '---'})
        self.app.INDIStatusQueue.put({'Name': 'Dome', 'value': '---'})

    @PyQt5.QtCore.pyqtSlot(object)
    def handleReceived(self, message):
        # central dispatcher for data coming from INDI devices. I makes the whole status and data evaluation and fits the
        # data to mountwizzard
        if 'device' not in message.attr:
            return
        device = message.attr['device']
        # receiving all definitions for vectors in indi and building them up in self.data['Device']
        if isinstance(message, indiXML.DefBLOBVector):
            self.app.sharedINDIDataLock.lockForWrite()
            if device not in self.data['Device']:
                self.data['Device'][device] = {}
            if device in self.data['Device']:
                if 'name' in message.attr:
                    defVector = message.attr['name']
                    if defVector not in self.data['Device'][device]:
                        self.data['Device'][device][defVector] = {}
                    for elt in message.elt_list:
                        self.data['Device'][device][defVector][elt.attr['name']] = ''
            self.app.sharedINDIDataLock.unlock()

        elif isinstance(message, indiXML.SetBLOBVector):
            self.app.sharedINDIDataLock.lockForRead()
            if device in self.data['Device']:
                if int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.CCD_INTERFACE:
                    name = message.attr['name']
                    # ccd1 is the main camera in INDI
                    if name == 'CCD1':
                        # format tells me raw or compressed format
                        if 'format' in message.getElt(0).attr:
                            try:
                                # todo: image should be stored in indicamera, only data should be transferred via signal
                                # todo: therefore imageHDU has to be a class variable to not be garbage collected
                                if message.getElt(0).attr['format'] == '.fits':
                                    imageHDU = pyfits.HDUList.fromstring(message.getElt(0).getValue())
                                    imageHDU.writeto(self.imagePath, overwrite=True)
                                    self.logger.debug('Image BLOB is in raw fits format')
                                else:
                                    imageHDU = pyfits.HDUList.fromstring(zlib.decompress(message.getElt(0).getValue()))
                                    imageHDU.writeto(self.imagePath, overwrite=True)
                                    self.logger.debug('Image BLOB is compressed fits format')
                                self.receivedImage.emit(True)
                            except Exception as e:
                                self.receivedImage.emit(False)
                                self.logger.debug('Could not receive Image, error:{0}'.format(e))
                            finally:
                                pass
                        else:
                            self.logger.debug('Could not find format in message from device: {0}'.format(device))
                    else:
                        self.logger.debug('Got BLOB from device: {0}, name: {1}'.format(device, name))
                else:
                    self.logger.debug('Got unexpected BLOB from device: {0}'.format(device))
            else:
                self.logger.debug('Did not find device: {0} in device list'.format(device))
            self.app.sharedINDIDataLock.unlock()

        # deleting properties from devices
        elif isinstance(message, indiXML.DelProperty):
            self.app.sharedINDIDataLock.lockForWrite()
            if device in self.data['Device']:
                if 'name' in message.attr:
                    delVector = message.attr['name']
                    if delVector in self.data['Device'][device]:
                        del self.data['Device'][device][delVector]
            self.app.sharedINDIDataLock.unlock()

        # receiving changes from vectors and updating them ins self.data['Device]
        elif isinstance(message, indiXML.SetSwitchVector) or \
                isinstance(message, indiXML.SetTextVector) or \
                isinstance(message, indiXML.SetLightVector) or \
                isinstance(message, indiXML.SetNumberVector):
            self.app.sharedINDIDataLock.lockForWrite()
            if device in self.data['Device']:
                if 'name' in message.attr:
                    setVector = message.attr['name']
                    if setVector not in self.data['Device'][device]:
                        self.data['Device'][device][setVector] = {}
                        self.logger.warning('SetVector before DefVector in INDI protocol, device: {0}, vector: {1}'.format(device, setVector))
                    if 'state' in message.attr:
                        self.data['Device'][device][setVector]['state'] = message.attr['state']
                    if 'timeout' in message.attr:
                        self.data['Device'][device][setVector]['timeout'] = message.attr['timeout']
                    for elt in message.elt_list:
                        self.data['Device'][device][setVector][elt.attr['name']] = elt.getValue()
            self.app.sharedINDIDataLock.unlock()

        # receiving all definitions for vectors in indi and building them up in self.data['Device']
        elif isinstance(message, indiXML.DefSwitchVector) or \
                isinstance(message, indiXML.DefTextVector) or \
                isinstance(message, indiXML.DefLightVector) or \
                isinstance(message, indiXML.DefNumberVector):
            self.app.sharedINDIDataLock.lockForWrite()
            if device not in self.data['Device']:
                # new device !
                self.data['Device'][device] = {}
                self.newDeviceQueue.put(device)
            if device in self.data['Device']:
                if 'name' in message.attr:
                    defVector = message.attr['name']
                    if defVector not in self.data['Device'][device]:
                        self.data['Device'][device][defVector] = {}
                    if 'state' in message.attr:
                        self.data['Device'][device][defVector]['state'] = message.attr['state']
                    if 'perm' in message.attr:
                        self.data['Device'][device][defVector]['perm'] = message.attr['perm']
                    if 'timeout' in message.attr:
                        self.data['Device'][device][defVector]['timeout'] = message.attr['timeout']
                    for elt in message.elt_list:
                        self.data['Device'][device][defVector][elt.attr['name']] = elt.getValue()
            self.app.sharedINDIDataLock.unlock()

        self.app.sharedINDIDataLock.lockForRead()
        if device in self.data['Device']:
            if 'DRIVER_INFO' in self.data['Device'][device]:
                if int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.CCD_INTERFACE:
                    self.app.INDIStatusQueue.put({'Name': 'CCD', 'value': device})
                elif int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.WEATHER_INTERFACE:
                    self.app.INDIStatusQueue.put({'Name': 'Environment', 'value': device})
                elif int(self.data['Device'][device]['DRIVER_INFO']['DRIVER_INTERFACE']) & self.DOME_INTERFACE:
                    self.app.INDIStatusQueue.put({'Name': 'Dome', 'value': device})
        self.app.sharedINDIDataLock.unlock()

    @PyQt5.QtCore.pyqtSlot()
    def handleReadyRead(self):
        # Add starting tag if this is new message.
        if len(self.messageString) == 0:
            self.messageString = "<data>"
        # Get message from socket.
        while self.socket.bytesAvailable():
            self.messageString += self.socket.read(100000).decode()
        # Add closing tag.
        self.messageString += "</data>"
        # Try and parse the message.
        try:
            messages = ElementTree.fromstring(self.messageString)
            self.messageString = ""
            for message in messages:
                xmlMessage = indiXML.parseETree(message)
                self.processMessage.emit(xmlMessage)
        # Message is incomplete, remove </data> and wait..
        except ElementTree.ParseError:
            self.messageString = self.messageString[:-7]

    def sendMessage(self, indiCommand):
        if self.socket.state() == QtNetwork.QAbstractSocket.ConnectedState:
            self.socket.write(indiCommand.toXML() + b'\n')
            self.socket.flush()
        else:
            self.logger.warning('Socket not connected')
