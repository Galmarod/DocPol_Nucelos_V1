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
import os
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
        fondo_color = "#ffffff"
        command = [
                "/Applications/Inkscape.app/Contents/MacOS/inkscape",
                str(svg_file),
                "--export-type=pdf",
                f"--export-filename={pdf_file}",
                "--export-dpi=300",
                f"--export-background={fondo_color}",
                "--export-background-opacity=1"
            ]
        subprocess.run(command, check=True)

    
    def export_svg_to_png(self, svg_file, png_file):
        fondo_color = "#ffffff"
        command = [
                "/Applications/Inkscape.app/Contents/MacOS/inkscape",
                str(svg_file),
                "--export-type=png",
                f"--export-filename={png_file}",
                "--export-dpi=300",
                f"--export-background={fondo_color}",
                "--export-background-opacity=1"
            ]
        subprocess.run(command, check=True)


    def merge_pdfs(pdf_list, output_path):
        merger = PdfMerger()

        for pdf in pdf_list:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

    

