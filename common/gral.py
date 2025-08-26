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
import uuid
import shutil
import json
from fastapi import UploadFile

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

    def get_template_api(self, name):
        if not name.endswith(".svg"):
            name += ".svg"
        tempFolder = os.path.join(self.main_path, 'templates', 'svgFiles')
        _temp      = os.path.join(tempFolder, name)
        return _temp

    
    def save_files_user(self, folder, UserFolder,FileFolder,name):
        tempFolder = os.path.join(self.main_path, folder, UserFolder, FileFolder)
        os.makedirs(tempFolder, exist_ok=True)
        _temp      = os.path.join(tempFolder, name)
        return _temp

    def save_file_api(self, json_file, svg_file=None):
        svg_path = " "
        filename = " "
        final_json_path = " "
        name_file_user = " "
        temp_json_path = self.save_files_user("temp",uuid.uuid4().hex,"tempFile", f"temp_{uuid.uuid4().hex}.json")
        with open(temp_json_path, "wb") as f:
            shutil.copyfileobj(json_file.file, f)
        # Leer JSON
        with open(temp_json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Obtener datos de nameUser
        name_user_data = data.get("User", {})
        username = name_user_data.get("nameUser", None)
               
        if svg_file is not None:
           filename = os.path.splitext(svg_file.filename)[0]
           final_json_path = self.save_files_user("uploads",username, filename,f"{username}_{filename}.json") 
           svg_path = self.save_files_user("uploads",username,filename ,svg_file.filename)
           # Renombrar JSON
           os.rename(temp_json_path, final_json_path)
           with open(svg_path, "wb") as f:
                shutil.copyfileobj(svg_file.file, f)
        if svg_file is None:
           # Obtener datos de nameUser
           name_user_data = data.get("User", {})
           username = name_user_data.get("nameUser", None)
           name_file_user = data.get("Svginformation",{})
           file = name_file_user.get("nameFileSvg",None)
           filename = os.path.splitext(file)[0]
           final_json_path = self.save_files_user("uploads",username, filename,f"{username}_{filename}_ediciones.json")
           svg_path = self.save_files_user("uploads",username,filename,f"{filename}.svg")
           # Renombrar JSON
           os.rename(temp_json_path, final_json_path)

        # Extraer ediciones para procesar
        ediciones = data.get("ediciones", {})
        print("📄 Ediciones:", ediciones)
        print("👤 Datos usuario:", name_user_data)
            
        png_path = os.path.join(os.path.dirname(svg_path), f"{filename}.png")

        return svg_path, filename, png_path, temp_json_path, final_json_path, data

    
 






