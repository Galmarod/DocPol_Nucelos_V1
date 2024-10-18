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


import logging  
from lxml import etree as ET
import subprocess
from PyPDF2 import PdfMerger

from common.gral import General
from common.logs import Loger

class Control(object):
    def __init__(self):
        # Inicializa Loger si es necesario
        Loger()
        self.logger = logging.getLogger('bitacora')
        self.gral = General()

    def export_svg_to_pdf(self, svg_file, pdf_file):
        # Ruta de Inkscape en Windows con barra invertida doblemente escapada o usar una raw string
        command = [r"C:\Program Files\Inkscape\bin\inkscape.exe", "--pipe", f"--export-filename={self.gral.get_file_temp(pdf_file)}"]    
        try:
            # Abrir el archivo SVG como binario y pasar su contenido a Inkscape
            with open(self.gral.get_file_temp(svg_file), 'rb') as svg_content:
                subprocess.run(command, input=svg_content.read(), check=True)
            self.logger.info("Archivo '{0}' exportado exitosamente a PDF como {1}."
                             .format(svg_file, pdf_file))
        except subprocess.CalledProcessError as e:
            self.logger.error("Error al exportar '{0}' a PDF {1}."
                              .format(svg_file, e))                 
        except FileNotFoundError:
            self.logger.error("El archivo {0} no se encontró."
                              .format(svg_file))


    def merge_pdfs(pdf_list, output_path):
        merger = PdfMerger()

        for pdf in pdf_list:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

    

