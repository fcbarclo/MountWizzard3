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
############################################################
import logging
import PyQt5
import time
from queue import Queue
from astrometry import transform
from mount import align_stars


class MountStatusRunnerSlow(PyQt5.QtCore.QObject):
    logger = logging.getLogger(__name__)

    signalDestruct = PyQt5.QtCore.pyqtSignal()
    CYCLE = 250
    CYCLE_STATUS_SLOW = 10000
    CONNECTION_TIMEOUT = 2000

    def __init__(self, app, thread, data, signalConnected, mountStatus):
        super().__init__()

        self.app = app
        self.thread = thread
        self.data = data
        self.signalConnected = signalConnected
        self.mountStatus = mountStatus
        self.mutexIsRunning = PyQt5.QtCore.QMutex()
        self.dataTimer = None
        self.cycleTimer = None
        self.isRunning = False
        self.connectCounter = 0
        self.socket = None
        self.sendLock = False
        self.messageString = ''
        self.sendCommandQueue = Queue()
        self.transform = transform.Transform(self.app)

        self.alignmentStars = align_stars.AlignStars(self.app)
        self.app.sharedMountDataLock.lockForWrite()
        self.data['starsTopo'] = list()
        self.data['starsNames'] = list()
        self.data['starsICRS'] = list()
        self.app.sharedMountDataLock.unlock()
        for name in self.alignmentStars.stars:
            self.app.sharedMountDataLock.lockForWrite()
            self.data['starsNames'].append(name)
            self.data['starsICRS'].append(self.alignmentStars.stars[name])
            self.app.sharedMountDataLock.unlock()
        self.updateAlignmentStarPositions()

    def run(self):
        self.logger.info('mount slow started')
        self.mutexIsRunning.lock()
        if not self.isRunning:
            self.isRunning = True
        self.mutexIsRunning.unlock()
        self.socket = PyQt5.QtNetwork.QTcpSocket()
        self.socket.setSocketOption(PyQt5.QtNetwork.QAbstractSocket.LowDelayOption, 1)
        self.socket.setSocketOption(PyQt5.QtNetwork.QAbstractSocket.KeepAliveOption, 1)
        self.socket.hostFound.connect(self.handleHostFound)
        self.socket.connected.connect(self.handleConnected)
        self.socket.stateChanged.connect(self.handleStateChanged)
        self.socket.disconnected.connect(self.handleDisconnect)
        self.socket.readyRead.connect(self.handleReadyRead)
        self.socket.error.connect(self.handleError)
        # timers
        self.dataTimer = PyQt5.QtCore.QTimer(self)
        self.dataTimer.setSingleShot(False)
        self.dataTimer.timeout.connect(self.getStatusSlow)
        self.dataTimer.start(self.CYCLE_STATUS_SLOW)
        self.cycleTimer = PyQt5.QtCore.QTimer(self)
        self.cycleTimer.setSingleShot(False)
        self.cycleTimer.timeout.connect(self.doCommand)
        self.cycleTimer.start(self.CYCLE)
        self.signalDestruct.connect(self.destruct, type=PyQt5.QtCore.Qt.BlockingQueuedConnection)

    def stop(self):
        self.mutexIsRunning.lock()
        if self.isRunning:
            self.isRunning = False
            self.signalDestruct.emit()
            self.signalConnected.emit({'Slow': False})
            self.thread.quit()
            self.thread.wait()
        self.mutexIsRunning.unlock()
        self.logger.info('mount slow stopped')

    @PyQt5.QtCore.pyqtSlot()
    def destruct(self):
        self.cycleTimer.stop()
        self.dataTimer.stop()
        self.signalDestruct.disconnect(self.destruct)
        self.socket.hostFound.disconnect(self.handleHostFound)
        self.socket.connected.disconnect(self.handleConnected)
        self.socket.stateChanged.disconnect(self.handleStateChanged)
        self.socket.disconnected.disconnect(self.handleDisconnect)
        self.socket.error.disconnect(self.handleError)
        self.socket.readyRead.disconnect(self.handleReadyRead)
        self.socket.abort()

    def doCommand(self):
        self.doReconnect()
        if not self.sendCommandQueue.empty() and (self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.ConnectedState):
            command = self.sendCommandQueue.get()
            if not self.sendLock:
                self.sendCommand(command)

    def doReconnect(self):
        if self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.UnconnectedState:
            if self.connectCounter == 0:
                self.app.sharedMountDataLock.lockForRead()
                self.socket.connectToHost(self.data['MountIP'], self.data['MountPort'])
                self.app.sharedMountDataLock.unlock()
                self.sendCommandQueue.queue.clear()
            else:
                # connection build up is ongoing
                pass
            if self.connectCounter * self.CYCLE > self.CONNECTION_TIMEOUT:
                self.socket.abort()
                self.connectCounter = 0
            else:
                self.connectCounter += 1
        else:
            if self.socket.state() != PyQt5.QtNetwork.QAbstractSocket.ConnectedState:
                if self.connectCounter * self.CYCLE > self.CONNECTION_TIMEOUT:
                    self.socket.abort()
                    self.connectCounter = 0
                else:
                    self.connectCounter += 1
            else:
                # connected
                pass

    @PyQt5.QtCore.pyqtSlot()
    def handleHostFound(self):
        self.app.sharedMountDataLock.lockForRead()
        self.logger.debug('Mount RunnerSlow found at {}:{}'.format(self.data['MountIP'], self.data['MountPort']))
        self.app.sharedMountDataLock.unlock()

    @PyQt5.QtCore.pyqtSlot()
    def handleConnected(self):
        self.app.sharedMountDataLock.lockForRead()
        self.logger.info('Mount RunnerSlow connected at {0}:{1}'.format(self.data['MountIP'], self.data['MountPort']))
        self.app.sharedMountDataLock.unlock()
        self.signalConnected.emit({'Slow': True})
        self.getStatusSlow()

    @PyQt5.QtCore.pyqtSlot(PyQt5.QtNetwork.QAbstractSocket.SocketError)
    def handleError(self, socketError):
        if self.socket.error() > 0:
            self.logger.warning('Mount RunnerSlow connection fault: {0}'.format(socketError))

    @PyQt5.QtCore.pyqtSlot()
    def handleStateChanged(self):
        self.logger.debug('Mount RunnerSlow connection has state: {0}'.format(self.socket.state()))

    @PyQt5.QtCore.pyqtSlot()
    def handleDisconnect(self):
        self.logger.info('Mount RunnerSlow connection is disconnected from host')
        self.signalConnected.emit({'Slow': False})

    def sendCommand(self, command):
        if self.isRunning:
            if self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.ConnectedState:
                self.socket.write(bytes(command + '\r', encoding='ascii'))
                self.socket.flush()
            else:
                self.logger.warning('Socket RunnerSlow not connected')

    def doRefractionUpdate(self):
        doRefractionUpdate = False
        pressure = 950
        temperature = 10
        if self.app.ui.checkAutoRefractionNone.isChecked():
            doRefractionUpdate = False
        if self.app.ui.checkAutoRefractionContinous.isChecked():
            doRefractionUpdate = True
            self.app.sharedEnvironmentDataLock.lockForRead()
            if 'MovingAverageTemperature' in self.app.workerEnvironment.data and 'MovingAveragePressure' in self.app.workerEnvironment.data and self.app.workerEnvironment.isRunning:
                pressure = self.app.workerEnvironment.data['MovingAveragePressure']
                temperature = self.app.workerEnvironment.data['MovingAverageTemperature']
            self.app.sharedEnvironmentDataLock.unlock()
        if self.app.ui.checkAutoRefractionNotTracking.isChecked():
            # if there is no tracking, than updating is good
            self.app.sharedMountDataLock.lockForRead()
            if 'Status' in self.data:
                # status 0 means tracking, and in tracking mode we do not want to update
                if self.data['Status'] != '0':
                    doRefractionUpdate = True
            self.app.sharedMountDataLock.unlock()
            self.app.sharedEnvironmentDataLock.lockForRead()
            if 'Temperature' in self.app.workerEnvironment.data and 'Pressure' in self.app.workerEnvironment.data and self.app.workerEnvironment.isRunning:
                pressure = self.app.workerEnvironment.data['Pressure']
                temperature = self.app.workerEnvironment.data['Temperature']
            self.app.sharedEnvironmentDataLock.unlock()
        if doRefractionUpdate:
            if (900.0 < pressure < 1100.0) and (-30.0 < temperature < 35.0):
                self.app.mountCommandQueue.put(':SRPRS{0:04.1f}#'.format(pressure))
                if temperature > 0:
                    self.app.mountCommandQueue.put(':SRTMP+{0:03.1f}#'.format(temperature))
                else:
                    self.app.mountCommandQueue.put(':SRTMP-{0:3.1f}#'.format(-temperature))

    def updateAlignmentStarPositions(self):
        # update topo data for alignment stars
        self.app.sharedMountDataLock.lockForWrite()
        self.data['starsTopo'] = list()
        self.app.sharedMountDataLock.unlock()
        for name in self.alignmentStars.stars:
            self.app.sharedMountDataLock.lockForWrite()
            ra = self.transform.degStringToDecimal(self.alignmentStars.stars[name][0], ' ')
            dec = self.transform.degStringToDecimal(self.alignmentStars.stars[name][1], ' ')
            self.data['starsTopo'].append(self.transform.transformERFA(ra, dec, 1))
            self.app.sharedMountDataLock.unlock()

    def getStatusSlow(self):
        if self.socket.state() == PyQt5.QtNetwork.QAbstractSocket.ConnectedState:
            command = ':U2#:Gev#:Gg#:Gt#:GVD#:GVN#:GVP#:GVT#:GVZ#:modelcnt#:getalst#:newalig#:endalig#'
            # command = ':U2#:Gev#:Gg#:Gt#:GVD#:GVN#:GVP#:GVT#:GVZ#'
            self.sendCommandQueue.put(command)
            self.doRefractionUpdate()
            self.updateAlignmentStarPositions()
            self.app.workerMountDispatcher.signalAlignmentStars.emit()

    @PyQt5.QtCore.pyqtSlot()
    def handleReadyRead(self):
        # Get message from socket.
        while self.socket.bytesAvailable() and self.isRunning:
            self.messageString += self.socket.read(1024).decode()
        if self.messageString.count('#') < 12:
            return
        if self.messageString.count('#') != 12:
            self.logger.error('Receiving data got error:{0}'.format(self.messageString))
            self.messageString = ''
            messageToProcess = ''
        else:
            messageToProcess = self.messageString
            self.messageString = ''
        # Try and parse the message. In Slow we expect 6
        try:
            if len(messageToProcess) == 0:
                return
            self.app.sharedMountDataLock.lockForWrite()
            valueList = messageToProcess.strip('#').split('#')
            # +0580.9#-011:42:17.3#+48:02:01.6#Oct 25 2017#2.15.8#10micron GM1000HPS#16:58:31#Q-TYPE2012#
            # all parameters are delivered
            self.logger.info('Slow raw: {0}'.format(messageToProcess))
            self.logger.info('Slow processed: {0}'.format(valueList))
            if len(valueList) >= 8:
                if len(valueList[0]) > 0:
                    self.data['SiteHeight'] = valueList[0]
                if len(valueList[1]) > 0:
                    lon1 = valueList[1]
                    # due to compatibility to LX200 protocol east is negative
                    if lon1[0] == '-':
                        self.data['SiteLongitude'] = lon1.replace('-', '+')
                    else:
                        self.data['SiteLongitude'] = lon1.replace('+', '-')
                if len(valueList[2]) > 0:
                    self.data['SiteLatitude'] = valueList[2]
                if len(valueList[3]) > 0:
                    self.data['FirmwareDate'] = valueList[3]
                if len(valueList[4]) > 0:
                    self.data['FirmwareNumber'] = valueList[4]
                    fw = self.data['FirmwareNumber'].split('.')
                    if len(fw) == 3:
                        self.data['FW'] = int(float(fw[0]) * 10000 + float(fw[1]) * 100 + float(fw[2]))
                    else:
                        self.data['FW'] = 0
                if len(valueList[5]) > 0:
                    self.data['FirmwareProductName'] = valueList[5]
                if len(valueList[6]) > 0:
                    self.data['FirmwareTime'] = valueList[6]
                if len(valueList[7]) > 0:
                    self.data['HardwareVersion'] = valueList[7]
                if len(valueList[8]) > 0:
                    self.data['NumberModelNames'] = valueList[8]
                if len(valueList[9]) > 0:
                    self.data['NumberAlignmentStars'] = valueList[9]
                self.logger.info('FW: {0} Number: {1}'.format(self.data['FirmwareNumber'], self.data['FW']))
                self.logger.info('Site Lon:    {0}'.format(self.data['SiteLongitude']))
                self.logger.info('Site Lat:    {0}'.format(self.data['SiteLatitude']))
                self.logger.info('Site Height: {0}'.format(self.data['SiteHeight']))
                self.app.signalMountSiteData.emit(self.data['SiteLatitude'], self.data['SiteLongitude'], self.data['SiteHeight'])
            else:
                self.logger.warning('Parsing Status Slow combined command valueList is not OK: length:{0} content:{1}'.format(len(valueList), valueList))
        except Exception as e:
            self.logger.error('Problem parsing response, error: {0}, message:{1}'.format(e, messageToProcess))
        finally:
            self.app.sharedMountDataLock.unlock()
        self.sendLock = False
