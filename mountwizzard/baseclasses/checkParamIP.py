############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
import logging
import re
import ipaddress
from baseclasses import widget


class CheckIP(widget.MwWidget):
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    @staticmethod
    def checkPort(ui):
        cursorPosition = ui.cursorPosition()
        if ui.text().strip() != '':
            port = int(ui.text())
        else:
            port = 0
        if 1 < port < 64535:
            valid = True
            ui.setProperty('check', True)
            ui.style().unpolish(ui)
            ui.style().polish(ui)
        else:
            valid = False
            ui.setProperty('check', False)
            ui.style().unpolish(ui)
            ui.style().polish(ui)
        ui.setText('{0}'.format(port))
        ui.setCursorPosition(cursorPosition)
        return valid, port

    @staticmethod
    def checkIP(ui):
        cursorPosition = ui.cursorPosition()
        IP = ui.text().strip()
        try:
            ipaddress.ip_address(IP)
            valid = True
            ui.setProperty('check', True)
            ui.style().unpolish(ui)
            ui.style().polish(ui)
        except Exception as e:
            valid = False
            ui.setProperty('check', False)
            ui.style().unpolish(ui)
            ui.style().polish(ui)
        finally:
            pass
        ui.setText('{0}'.format(IP))
        ui.setCursorPosition(cursorPosition)
        return valid, IP

    @staticmethod
    def checkMAC(ui):
        mac = ui.text()
        mac = re.sub('[.:-]', '', mac).lower()
        mac = ''.join(mac.split())
        if len(mac) != 12 or not mac.isalnum():
            valid = False
            ui.setProperty('check', False)
            ui.style().unpolish(ui)
            ui.style().polish(ui)
        else:
            valid = True
            ui.setProperty('check', True)
            ui.style().unpolish(ui)
            ui.style().polish(ui)
            mac = ":".join(["%s" % (mac[i:i + 2]) for i in range(0, 12, 2)])
        return valid, mac
