#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Guillermo Almanza Rodríguez"
__copyright__  = "Copyright 2024, RevelCode"
__credits__    = ["galmarod"]
__license__    = "GPL"
__version__    = "1.0.1"
__maintainer__ = "Francisco Javier Mendoza Bautista"
__email__      = "javimenba.developer@gmail.com"
__status__     = "Development"
__date__       = "Oct-2024"

import os
import logging
import logging.handlers

class Loger():
    def __init__(self, mainpath=""):
        if mainpath=="":
            mainpath = os.getcwd()
        debugFile = os.path.join(mainpath, 'bitacora.log')

        self.logger = logging.getLogger('bitacora')
        self.logger.setLevel(logging.DEBUG)

        # Evitar añadir múltiples manejadores
        if not self.logger.hasHandlers():
            # Si maxBytes=0, no rotará el archivo por tamaño
            # Si backupCount=0, no eliminará ningún fichero rotado
            self.handler = logging.handlers.RotatingFileHandler(filename=debugFile, mode='a', maxBytes=20480000, backupCount=5)
            self.formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)-6s::%(filename)-25s::%(funcName)-15s::%(lineno)3s::%(message)-100s', datefmt='%y-%m-%d %H:%M:%S')
            self.handler.setFormatter(self.formatter)
            self.logger.addHandler(self.handler)
        
        self.loglen = 40
        self.padstr = '='
        self.flagdebug = True

    def debug(self, msg, title=False):
        if self.flagdebug:
            if title:
                msg = self.msg_format(msg, self.loglen, self.padstr)
            self.logger.debug(msg)

    def info(self, msg, title=False):
        if title:
            msg = self.msg_format(msg, self.loglen, self.padstr)
        self.logger.info(msg)

    def warning(self, msg, title=False):
        if title:
            msg = self.msg_format(msg, self.loglen, self.padstr)
        self.logger.warning(msg)

    def error(self, msg, title=False):
        if title:
            msg = self.msg_format(msg, self.loglen, self.padstr)
        self.logger.error(msg)

    def critical(self, msg, title=False):
        if title:
            msg = self.msg_format(msg, self.loglen, self.padstr)
        self.logger.critical(msg)

    def msg_format(self, msg, len, padstr):
        msg = str(msg)
        return msg.center(len, padstr)
