#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Guillermo Almazán Rodríguez"
__copyright__  = "Copyright 2024, RevelCode"
__credits__    = ["galmarod"]
__license__    = "GPL"
__version__    = "1.0.1"
__maintainer__ = "Francisco Javier Mendoza Bautista"
__email__      = "javimenba.developer@gmail.com"
__status__     = "Development"
__date__       = "Oct-2024"

import os

class General(object):
    def __init__(self):
        self.main_path = ""
        self.compiled = False
        self.set_main_path()

    def set_main_path(self):
        separador = os.path.sep
        dir_actual= os.path.dirname(os.path.abspath(__file__))
        self.main_path = separador.join(dir_actual.split(separador)[:-1])


    def get_template_path(self, name):
        if not name.endswith(".svg"):
            name += ".svg"
        templateFolder = os.path.join(self.main_path, 'templates','svgFiles')
        _template      = os.path.join(templateFolder, name)
        return _template

    def get_image_path(self, name):
        if not name.endswith(".png"):
            name += ".png"
        imageFolder = os.path.join(self.main_path, 'assets') 
        _images     = os.path.join(imageFolder, name)
        return _images
    
    def get_file_temp(self, name):
        tempFolder = os.path.join(self.main_path, 'temp')
        _temp      = os.path.join(tempFolder, name)
        return _temp

    def set_file_temp(self, name):
        tempFolder = os.path.join(self.main_path, 'temp')
        _temp      = os.path.join(tempFolder, name)
        return _temp
 
    def get_file_edits(self, name):
        if not name.endswith(".json"):
            name += ".json"
        tempFolder = os.path.join(self.main_path, 'edits')
        _temp      = os.path.join(tempFolder, name)
        return _temp




