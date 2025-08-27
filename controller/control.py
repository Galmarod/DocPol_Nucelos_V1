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
import shutil
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
        self.pathInkscape = "/Applications/Inkscape.app/Contents/MacOS/inkscape" #MacOs
        #self.pathInkscape = "/usr/bin/inkscape" #Docker
    def export_svg_to_pdf(self, svg_file, pdf_file):
        if not os.path.isfile(self.pathInkscape):
            raise FileNotFoundError(f"Inkscape no encontrado en {self.pathInkscape}")


        if not os.path.isfile(svg_file):
            raise FileNotFoundError(f"SVG no encontrado: {svg_file}")

        fondo_color = "#ffffff"
        command = [
            self.pathInkscape,
            str(svg_file),
            "--export-type=pdf",
            f"--export-filename={pdf_file}",
            "--export-dpi=300",
            f"--export-background={fondo_color}",
            "--export-background-opacity=1"
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.logger.info(f"PDF exportado: {pdf_file}")
            if result.stdout:
                self.logger.debug(result.stdout)
            if result.stderr:
                self.logger.warning(result.stderr)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al exportar PDF: {e.stderr}")
            raise

    
    def export_svg_to_png(self, svg_file, png_file):
        print("docker")
        if not os.path.isfile(self.pathInkscape):
            raise FileNotFoundError(f"Inkscape no encontrado en {self.pathInkscape}")        

        if not os.path.isfile(svg_file):
            raise FileNotFoundError(f"SVG no encontrado: {svg_file}")

        fondo_color = "#ffffff"
        command = [
            self.pathInkscape,
            str(svg_file),
            "--export-type=png",
            f"--export-filename={png_file}",
            "--export-dpi=300",
            f"--export-background={fondo_color}",
            "--export-background-opacity=1"
        ]

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            self.logger.info(f"PNG exportado: {png_file}")
            if result.stdout:
                self.logger.debug(result.stdout)
            if result.stderr:
                self.logger.warning(result.stderr)
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error al exportar PNG: {e.stderr}")
            raise


    def merge_pdfs(pdf_list, output_path):
        merger = PdfMerger()

        for pdf in pdf_list:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()

    

