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
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
import socket
import sys

import PyQt5.QtCore
import skyfield.api


class Firmware(object):

    firmwareLock = PyQt5.QtCore.QReadWriteLock()

    def __init__(self):

        self._productName = ''
        self._fwNumber = ''
        self._fw = 0
        self._hwVersion = ''
        self._fwDate = ''
        self._fwTime = ''

    @property
    def productName(self):
        return self._productName

    @productName.setter
    def productName(self, value):
        self._productName = value

    @property
    def fwNumber(self):
        return self._fwNumber

    @property
    def fw(self):
        return self._fw

    @fwNumber.setter
    def fwNumber(self, value):
        self._fwNumber = value
        if value.count('.') == 2:
            _number = value.split('.')
            self._fw = int(_number[0]) * 10000 + int(_number[1]) * 100 + int(_number[2])
        else:
            self._fw = 0

    @property
    def hwVersion(self):
        return self._hwVersion

    @hwVersion.setter
    def hwVersion(self, value):
        self._hwVersion = value

    @property
    def fwDate(self):
        return self._fwDate

    @fwDate.setter
    def fwDate(self, value):
        self._fwDate = value

    @property
    def fwTime(self):
        return self._fwTime

    @fwTime.setter
    def fwTime(self, value):
        self._fwTime = value

    def __str__(self):
        output = '<Product: {0}>   <Firmware: {1}>   <Hardware: {2}>'
        value = output.format(self._productName,
                              self._fwNumber,
                              self._hwVersion,
                              )
        return value


class Site(object):

    siteLock = PyQt5.QtCore.QReadWriteLock()

    def __init__(self, timeScale):
        self._location = None
        self._timeJD = None
        self._timeSidereal = None
        self._timeScale = timeScale
        self._raJNow = 0
        self._decJNow = 0
        self._pierside = ''
        self._apparentAlt = 0
        self._apparentAz = 0
        self._status = 0
        self._statusSlew = False

    @staticmethod
    def _stringToDegree(value, splitter=':'):
        value = [float(x) for x in value.split(splitter)]
        value = value[0] + value[1] / 60 + value[2] / 3600
        return value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        lat, lon, elev = value
        lon = skyfield.api.Angle(degrees=self._stringToDegree(lon))
        lat = skyfield.api.Angle(degrees=self._stringToDegree(lat))
        self._location = skyfield.api.Topos(longitude=lon,
                                            latitude=lat,
                                            elevation_m=elev)

    @property
    def timeJD(self):
        return self._timeJD

    @timeJD.setter
    def timeJD(self, value):
        self._timeJD = self._timeScale.tt_jd(value)

    @property
    def timeSidereal(self):
        return self._timeJD

    @timeSidereal.setter
    def timeSidereal(self, value):
        self._timeSidereal = value

    @property
    def raJNow(self):
        return self._raJNow

    @raJNow.setter
    def raJNow(self, value):
        self._raJNow = value

    @property
    def decJNow(self):
        return self._decJNow

    @decJNow.setter
    def decJNow(self, value):
        self._decJNow = value

    @property
    def pierside(self):
        return self._pierside

    @pierside.setter
    def pierside(self, value):
        self._pierside = value

    @property
    def apparentAlt(self):
        return self._apparentAlt

    @apparentAlt.setter
    def apparentAlt(self, value):
        self._apparentAlt = value

    @property
    def apparentAz(self):
        return self._apparentAz

    @apparentAz.setter
    def apparentAz(self, value):
        self._apparentAz = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def statusSlew(self):
        return self._statusSlew

    @statusSlew.setter
    def statusSlew(self, value):
        self._statusSlew = value

    def __str__(self):
        output = '<Lat: {0}>   <Lon: {1}>   <Elev: {2}>'
        value = output.format(self._location.latitude,
                              self._location.longitude,
                              self._location.elevation.m,
                              )
        return value


class Setting(object):

    settingLock = PyQt5.QtCore.QReadWriteLock()

    def __init__(self):
        self._slewRate = 0
        self._timeToFlip = 0
        self._meridianLimitGuide = 0
        self._meridianLimitSlew = 0
        self._timeToMeridian = 0
        self._refractionTemperature = 0
        self._refractionPressure = 0
        self._TrackingRate = 0
        self._TelescopeTempDEC = 0
        self._statusRefraction = False
        self._statusUnattendedFlip = False
        self._statusDualAxisTracking = False
        self._currentHorizonLimitHigh = 0
        self._currentHorizonLimitLow = 0
        self._numberModelNames = 0
        self._numberAlignmentStars = 0
        self._UTCDataValid = ''
        self._UTCDataExpirationDate = ''

    @property
    def slewRate(self):
        return self._slewRate

    @slewRate.setter
    def slewRate(self, value):
        self._slewRate = value

    @property
    def timeToFlip(self):
        return self._timeToFlip

    @timeToFlip.setter
    def timeToFlip(self, value):
        self._timeToFlip = value

    @property
    def meridianLimitGuide(self):
        return self._meridianLimitGuide

    @meridianLimitGuide.setter
    def meridianLimitGuide(self, value):
        self._meridianLimitGuide = value

    @property
    def meridianLimitSlew(self):
        return self._meridianLimitSlew

    @meridianLimitSlew.setter
    def meridianLimitSlew(self, value):
        self._meridianLimitSlew = value

    @property
    def timeToMeridian(self):
        self._timeToMeridian = int(self._timeToFlip - self._meridianLimitGuide/360*24*60)
        return self._timeToMeridian

    @property
    def refractionTemperature(self):
        return self._refractionTemperature

    @refractionTemperature.setter
    def refractionTemperature(self, value):
        self._refractionTemperature = value

    @property
    def refractionPressure(self):
        return self._refractionPressure

    @refractionPressure.setter
    def refractionPressure(self, value):
        self._refractionPressure = value

    @property
    def TrackingRate(self):
        return self._TrackingRate

    @TrackingRate.setter
    def TrackingRate(self, value):
        self._TrackingRate = value

    @property
    def TelescopeTempDEC(self):
        return self._TelescopeTempDEC

    @TelescopeTempDEC.setter
    def TelescopeTempDEC(self, value):
        self._TelescopeTempDEC = value

    @property
    def refractionStatus(self):
        return self._statusRefraction

    @refractionStatus.setter
    def refractionStatus(self, value):
        self._statusRefraction = value

    @property
    def statusUnattendedFlip(self):
        return self._statusUnattendedFlip

    @statusUnattendedFlip.setter
    def statusUnattendedFlip(self, value):
        self._statusUnattendedFlip = value

    @property
    def statusDualAxisTracking(self):
        return self._statusDualAxisTracking

    @statusDualAxisTracking.setter
    def statusDualAxisTracking(self, value):
        self._statusDualAxisTracking = value

    @property
    def currentHorizonLimitHigh(self):
        return self._currentHorizonLimitHigh

    @currentHorizonLimitHigh.setter
    def currentHorizonLimitHigh(self, value):
        self._currentHorizonLimitHigh = value

    @property
    def currentHorizonLimitLow(self):
        return self._currentHorizonLimitLow

    @currentHorizonLimitLow.setter
    def currentHorizonLimitLow(self, value):
        self._currentHorizonLimitLow = value

    @property
    def numberModelNames(self):
        return self._numberModelNames

    @numberModelNames.setter
    def numberModelNames(self, value):
        self._numberModelNames = value

    @property
    def numberAlignmentStars(self):
        return self._numberAlignmentStars

    @numberAlignmentStars.setter
    def numberAlignmentStars(self, value):
        self._numberAlignmentStars = value

    @property
    def UTCDataValid(self):
        return self._UTCDataValid

    @UTCDataValid.setter
    def UTCDataValid(self, value):
        self._UTCDataValid = value

    @property
    def UTCDataExpirationDate(self):
        return self._UTCDataExpirationDate

    @UTCDataExpirationDate.setter
    def UTCDataExpirationDate(self, value):
        self._UTCDataExpirationDate = value
