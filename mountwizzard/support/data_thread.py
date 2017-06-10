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

# import basic stuff
import os
import logging
from PyQt5 import QtCore
import time
import urllib.request as urllib2
# windows automation
from pywinauto import Application, timings, findwindows, application
from pywinauto.controls.win32_controls import ButtonWrapper, EditWrapper
import locale


class Data(QtCore.QThread):
    logger = logging.getLogger(__name__)                                                                                    # get logger for  problems

    UTC_1 = 'http://maia.usno.navy.mil/ser7/finals.data'
    UTC_2 = 'http://maia.usno.navy.mil/ser7/tai-utc.dat'
    COMETS = 'http://www.minorplanetcenter.net/iau/MPCORB/CometEls.txt'
    ASTEROIDS = 'http://www.ap-i.net/pub/skychart/mpc/mpc5000.dat'
    SPACESTATIONS = 'http://www.celestrak.com/NORAD/elements/stations.txt'
    SATBRIGHTEST = 'http://www.celestrak.com/NORAD/elements/visual.txt'
    TARGET_DIR = os.getcwd() + '\\config\\'
    COMETS_FILE = 'comets.mpc'
    ASTEROIDS_FILE = 'asteroids.mpc'
    SPACESTATIONS_FILE = 'spacestations.tle'
    SATBRIGHTEST_FILE = 'satbrightest.tle'
    UTC_1_FILE = 'finals.data'
    UTC_2_FILE = 'tai-utc.dat'
    BLUE = 'background-color: rgb(42, 130, 218)'
    RED = 'background-color: red;'
    DEFAULT = 'background-color: rgb(32,32,32); color: rgb(192,192,192)'
    OPENDIALOG = 'Öffnen'
    if locale.getdefaultlocale()[0].find('en') != -1:
        OPENDIALOG = 'Open'

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.appAvailable = False
        self.appName = ''
        self.appInstallPath = ''
        self.appExe = 'GmQCIv2.exe'
        self.checkApplication()

    def initConfig(self):
        try:
            pass
        except Exception as e:
            self.logger.error('initConfig -> item in config.cfg not be initialize, error:{0}'.format(e))
        finally:
            pass

    def storeConfig(self):
        pass

    def checkApplication(self):
        self.appAvailable, self.appName, self.appInstallPath = self.app.checkRegistrationKeys('10micron QCI')
        if self.appAvailable:
            self.app.messageQueue.put('Found: {0}'.format(self.appName))
            self.logger.debug('checkApplicatio-> Name: {0}, Path: {1}'.format(self.appName, self.appInstallPath))
        else:
            self.logger.error('checkApplicatio-> Application 10micron Updater  not found on computer')

    def run(self):                                                                                                          # runnable for doing the work
        while True:                                                                                                         # main loop for stick thread
            if not self.app.commandDataQueue.empty():
                command = self.app.commandDataQueue.get()
                if command == 'SPACESTATIONS':
                    self.app.ui.btn_downloadSpacestations.setStyleSheet(self.BLUE)
                    self.downloadFile(self.SPACESTATIONS, self.TARGET_DIR + self.SPACESTATIONS_FILE)
                    self.app.ui.checkSpacestations.setChecked(True)
                    self.app.ui.btn_downloadSpacestations.setStyleSheet(self.DEFAULT)
                elif command == 'SATBRIGHTEST':
                    self.app.ui.btn_downloadSatbrighest.setStyleSheet(self.BLUE)
                    self.downloadFile(self.SATBRIGHTEST, self.TARGET_DIR + self.SATBRIGHTEST_FILE)
                    self.app.ui.checkSatellites.setChecked(True)
                    self.app.ui.btn_downloadSatbrighest.setStyleSheet(self.DEFAULT)
                elif command == 'ASTEROIDS':
                    self.app.ui.btn_downloadAsteroids.setStyleSheet(self.BLUE)
                    self.downloadFile(self.ASTEROIDS, self.TARGET_DIR + self.ASTEROIDS_FILE)
                    self.app.ui.checkAsteroids.setChecked(True)
                    self.app.ui.btn_downloadAsteroids.setStyleSheet(self.DEFAULT)
                elif command == 'COMETS':
                    self.app.ui.btn_downloadComets.setStyleSheet(self.BLUE)
                    self.downloadFile(self.COMETS, self.TARGET_DIR + self.COMETS_FILE)
                    self.app.ui.checkComets.setChecked(True)
                    self.app.ui.btn_downloadComets.setStyleSheet(self.DEFAULT)
                elif command == 'EARTHROTATION':
                    self.app.ui.btn_downloadEarthrotation.setStyleSheet(self.BLUE)
                    self.downloadFile(self.UTC_1, self.TARGET_DIR + self.UTC_1_FILE)
                    self.downloadFile(self.UTC_2, self.TARGET_DIR + self.UTC_2_FILE)
                    self.app.ui.checkEarthrotation.setChecked(True)
                    self.app.ui.btn_downloadEarthrotation.setStyleSheet(self.DEFAULT)
                elif command == 'ALL':
                    self.app.ui.btn_downloadAll.setStyleSheet(self.BLUE)
                    self.app.ui.btn_downloadEarthrotation.setStyleSheet(self.BLUE)
                    self.app.ui.btn_downloadSpacestations.setStyleSheet(self.BLUE)
                    self.app.ui.btn_downloadSatbrighest.setStyleSheet(self.BLUE)
                    self.app.ui.btn_downloadAsteroids.setStyleSheet(self.BLUE)
                    self.app.ui.btn_downloadComets.setStyleSheet(self.BLUE)
                    self.downloadFile(self.UTC_1, self.TARGET_DIR + self.UTC_1_FILE)
                    self.downloadFile(self.UTC_2, self.TARGET_DIR + self.UTC_2_FILE)
                    self.app.ui.checkEarthrotation.setChecked(True)
                    self.app.ui.btn_downloadEarthrotation.setStyleSheet(self.DEFAULT)
                    self.downloadFile(self.SPACESTATIONS, self.TARGET_DIR + self.SPACESTATIONS_FILE)
                    self.app.ui.checkSpacestations.setChecked(True)
                    self.app.ui.btn_downloadSpacestations.setStyleSheet(self.DEFAULT)
                    self.downloadFile(self.SATBRIGHTEST, self.TARGET_DIR + self.SATBRIGHTEST_FILE)
                    self.app.ui.checkSatellites.setChecked(True)
                    self.app.ui.btn_downloadSatbrighest.setStyleSheet(self.DEFAULT)
                    self.downloadFile(self.ASTEROIDS, self.TARGET_DIR + self.ASTEROIDS_FILE)
                    self.app.ui.btn_downloadAsteroids.setStyleSheet(self.DEFAULT)
                    self.app.ui.checkAsteroids.setChecked(True)
                    self.downloadFile(self.COMETS, self.TARGET_DIR + self.COMETS_FILE)
                    self.app.ui.btn_downloadComets.setStyleSheet(self.DEFAULT)
                    self.app.ui.checkComets.setChecked(True)
                    self.app.ui.btn_downloadAll.setStyleSheet(self.DEFAULT)
                elif command == 'UPLOADMOUNT':
                    self.app.ui.btn_uploadMount.setStyleSheet(self.BLUE)
                    self.uploadMount()
                    self.app.ui.btn_uploadMount.setStyleSheet(self.DEFAULT)
                else:
                    pass
            time.sleep(0.3)                                                                                                 # wait for the next cycle
        self.terminate()                                                                                                    # closing the thread at the end

    def __del__(self):                                                                                                      # remove thread
        self.wait()

    def getStatusFast(self):
        pass

    def getStatusMedium(self):
        self.logger.error('getStatusMedium-> error accessing weather ascom data: {}')

    def getStatusSlow(self):
        pass

    def getStatusOnce(self):
        pass

    def filterFileMPC(self, directory, filename, expression):
        numberEntry = 0
        outFile = open(directory + 'filter.mpc', 'w')
        with open(directory + filename) as inFile:
            for line in inFile:
                if line.find(expression) != -1:
                    outFile.write(line)
                    numberEntry += 1
        outFile.close()
        if numberEntry == 0:
            return False
        else:
            return True

    def downloadFile(self, url, filename):
        try:
            u = urllib2.urlopen(url)
            with open(filename, 'wb') as f:
                meta = u.info()
                meta_func = meta.getheaders if hasattr(meta, 'getheaders') else meta.get_all
                meta_length = meta_func("Content-Length")
                file_size = None
                if meta_length:
                    file_size = int(meta_length[0])
                self.app.messageQueue.put('{0}'.format(url))
                file_size_dl = 0
                block_sz = 8192
                while True:
                    buffer = u.read(block_sz)
                    if not buffer:
                        break
                    file_size_dl += len(buffer)
                    f.write(buffer)
            self.app.messageQueue.put('Downloaded {0} Bytes'.format(file_size))
        except Exception as e:
            self.logger.error('downloadFile   -> Download of {0} failed, error{1}'.format(url, e))
            self.app.messageQueue.put('Download Error {0}'.format(e))
        return

    def uploadMount(self):
        try:
            actual_work_dir = os.getcwd()
            os.chdir(os.path.dirname(self.appInstallPath))
            app = Application(backend='win32')                                                                              # backend win32 ist faster than uai
            app.start(self.appInstallPath + '\\' + self.appExe)                                                                # start 10 micro updater
            timings.Timings.Slow()
        except application.AppStartError:
            self.logger.error('uploadMount    -> error starting application')
            self.app.messageQueue.put('Failed to start updater, please check!')
            os.chdir(actual_work_dir)
            return
        try:
            dialog = timings.WaitUntilPasses(2, 0.5, lambda: findwindows.find_windows(title='GmQCIv2', class_name='#32770')[0])
            winOK = app.window_(handle=dialog)
            winOK['OK'].click()
        except TimeoutError as e:
            self.logger.error('uploadMount    -> timeout error{0}'.format(e))
        except Exception as e:
            self.logger.error('uploadMount    -> error{0}'.format(e))
        finally:
            pass
        try:
            win = app['10 micron control box update']                                                                       # link handle
            win['next'].click()                                                                                             # accept next
            win['next'].click()                                                                                             # go upload select page
            ButtonWrapper(win['Control box firmware']).uncheck()                                                            # no firmware updates
        except Exception as e:
            self.logger.error('uploadMount    -> error{0}'.format(e))
            self.app.messageQueue.put('Error in starting 10micron updater, please check!')
            os.chdir(actual_work_dir)
            return
        ButtonWrapper(win['Orbital parameters of comets']).uncheck()
        ButtonWrapper(win['Orbital parameters of asteroids']).uncheck()
        ButtonWrapper(win['Orbital parameters of satellites']).uncheck()
        ButtonWrapper(win['UTC / Earth rotation data']).uncheck()
        try:
            uploadNecessary = False
            if self.app.ui.checkComets.isChecked():
                ButtonWrapper(win['Orbital parameters of comets']).check()
                win['Edit...4'].click()
                popup = app['Comet orbits']
                popup['MPC file'].click()
                filedialog = app[self.OPENDIALOG]
                if self.app.ui.checkFilterMPC.isChecked():
                    if self.filterFileMPC(self.TARGET_DIR, self.COMETS_FILE, self.app.ui.le_filterExpressionMPC.text()):
                        uploadNecessary = True
                    EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + 'filter.mpc')                               # filename box
                else:
                    uploadNecessary = True
                    EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + self.COMETS_FILE)                           # filename box
                filedialog['Button16'].click()                                                                              # accept filename selection and proceed
                popup['Close'].click()
            else:
                ButtonWrapper(win['Orbital parameters of comets']).uncheck()
            if self.app.ui.checkAsteroids.isChecked():
                ButtonWrapper(win['Orbital parameters of asteroids']).check()
                win['Edit...3'].click()
                popup = app['Asteroid orbits']
                popup['MPC file'].click()
                filedialog = app[self.OPENDIALOG]
                if self.app.ui.checkFilterMPC.isChecked():
                    if self.filterFileMPC(self.TARGET_DIR, self.ASTEROIDS_FILE, self.app.ui.le_filterExpressionMPC.text()):
                        uploadNecessary = True
                    EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + 'filter.mpc')
                else:
                    uploadNecessary = True
                    EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + self.ASTEROIDS_FILE)                        # filename box
                filedialog['Button16'].click()                                                                              # accept filename selection and proceed
                popup['Close'].click()
            else:
                ButtonWrapper(win['Orbital parameters of asteroids']).uncheck()
            if self.app.ui.checkSatellites.isChecked():
                ButtonWrapper(win['Orbital parameters of satellites']).check()
                win['Edit...2'].click()
                popup = app['Satellites orbits']
                popup['Load from file'].click()
                filedialog = app[self.OPENDIALOG]
                EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + self.SATBRIGHTEST_FILE)                         # filename box
                filedialog['Button16'].click()                                                                              # accept filename selection and proceed
                popup['Close'].click()
                uploadNecessary = True
            else:
                ButtonWrapper(win['Orbital parameters of satellites']).uncheck()
            if self.app.ui.checkSpacestations.isChecked():
                ButtonWrapper(win['Orbital parameters of satellites']).check()
                win['Edit...2'].click()
                popup = app['Satellites orbits']
                popup['Load from file'].click()
                filedialog = app[self.OPENDIALOG]
                EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + self.SPACESTATIONS_FILE)                        # filename box
                filedialog['Button16'].click()                                                                              # accept filename selection and proceed
                popup['Close'].click()
                uploadNecessary = True
            else:
                ButtonWrapper(win['Orbital parameters of satellites']).uncheck()
            if self.app.ui.checkEarthrotation.isChecked():
                ButtonWrapper(win['UTC / Earth rotation data']).check()
                win['Edit...1'].click()
                popup = app['UTC / Earth rotation data']
                popup['Import files...'].click()
                filedialog = app['Open finals data']
                EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + self.UTC_1_FILE)                                # filename box
                filedialog['Button16'].click()                                                                              # accept filename selection and proceed
                filedialog = app['Open tai-utc.dat']
                EditWrapper(filedialog['Edit13']).SetText(self.TARGET_DIR + self.UTC_2_FILE)                                # filename box
                filedialog['Button16'].click()                                                                              # accept filename selection and proceed
                fileOK = app['UTC data']
                fileOK['OK'].click()
                uploadNecessary = True
            else:
                ButtonWrapper(win['UTC / Earth rotation data']).uncheck()
        except Exception as e:
            self.logger.error('uploadMount    -> error{0}'.format(e))
            self.app.messageQueue.put('Error in choosing upload files, please check 10micron updater!')
            os.chdir(actual_work_dir)
            return
        # uploadNecessary = False
        if uploadNecessary:
            try:
                win['next'].click()
                win['next'].click()
                win['Update Now'].click()
            except Exception as e:
                self.logger.error('uploadMount    -> error{0}'.format(e))
                self.app.messageQueue.put('Error in uploading files, please check 10micron updater!')
                os.chdir(actual_work_dir)
                return
            try:
                dialog = timings.WaitUntilPasses(60, 0.5, lambda: findwindows.find_windows(title='Update completed', class_name='#32770')[0])
                winOK = app.window_(handle=dialog)
                winOK['OK'].click()
            except Exception as e:
                self.logger.error('uploadMount    -> error{0}'.format(e))
                self.app.messageQueue.put('Error in closing 10micron updater, please check!')
                os.chdir(actual_work_dir)
                return
        else:
            try:
                win['Cancel'].click()
                winOK = app['Exit updater']
                winOK['Yes'].click()
            except Exception as e:
                self.logger.error('uploadMount    -> error{0}'.format(e))
                self.app.messageQueue.put('Error in closing Updater, please check!')
                os.chdir(actual_work_dir)
                return

if __name__ == "__main__":
    pass
