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

DOCPOL_VERSION = __version__


from lorem_text import lorem
import pyfiglet
import logging  
import sys 
import uvicorn
import queue
import threading
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer


# Importar clases o funciones necesarias
from common.gral import General
from common.logs import Loger
from controller.control import Control
from controller.modifySvg import ModifySvg
from view.main_window import MainWindow
from api.api_server import APIServer

class Docpol:
    def __init__(self):
        # Inicializa Loger si es necesario
        Loger()
        self.queue = queue.Queue()
        self.gral = General() 
        self.control = Control()
        self.modifySvg = ModifySvg()
        self.api = APIServer(queue=self.queue)
        # Configura el logger
        self.logger = logging.getLogger('bitacora')
        docpol = pyfiglet.figlet_format("DOCPOL")
        self.logger.info('=======================================')
        self.logger.info('=======================================')
        self.logger.info(f'{docpol} v.{DOCPOL_VERSION}')
        #self.logger.info(f'      DOCPOL v.{DOCPOL_VERSION}')
        self.logger.info('=======================================')
        self.logger.info('=======================================')
        

    def save_Bitacora(self):
        #_template =  self.gral.get_template_path("P2_1")
        # Registrar un mensaje en el log
        """self.logger.info("Path de la plantilla solicitada {0}"
                         .format(_template))"""
        #self.control.export_svg_to_pdf("P1-temp.svg", "P1-temp.pdf")
        self.modifySvg.modify_svg_1("Docpol desde Archlinux")
        sentences = [lorem.sentence() for _ in range(4)]
        self.modifySvg.modify_svg_2_1("".join(sentences),"Javimenba","Docpol")
        self.modifySvg.modify_svg_2_2("Test 1", "".join(sentences), "Test 2", "".join(sentences))
        self.modifySvg.modify_svg_3_1("Test 1","Test 2","hola","alineamiento_plot")
        self.modifySvg.modify_svg_3_2("alineamiento_plot","image_prueba1")
        self.modifySvg.modify_svg_3_3("TEXTO 1", "TEXTO TABLA 2", "alineamiento_plot" , "image_prueba1")
        self.modifySvg.modify_svg_4_1("TEXTO FIGURA 1","image_prueba1","alineamiento_plot")

    def apitest(self):
        threading.Thread(target=lambda: uvicorn.run(self.api.app, host="0.0.0.0", port=8000), daemon=True).start()

    def remplace(self):
        
        app = QApplication([])
        windows = MainWindow( self.gral.get_template_path("temp_input.svg"))

        timer = QTimer()
        timer.timeout.connect(lambda: self.check_queue(windows))
        timer.start(500)

        windows.show()
        sys.exit(app.exec())

    def check_queue(self, window):
        try:
            while True:
                msg = self.queue.get_nowait()
                if msg == "archivo_recibido":
                    window.load_svg(self.gral.get_file_temp("temp_input.svg"))
        except queue.Empty:
            pass

