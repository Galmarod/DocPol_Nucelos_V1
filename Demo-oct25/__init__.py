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


#from lorem_text import lorem
import pyfiglet
import logging

# Importar clases o funciones necesarias
from common.gral import General
from common.logs import Loger
from controller.control import Control
from controller.modifySvg import ModifySvg


class Docpol:
    """
    Clase principal de DocPol - Versión Demo Backend
    
    Esta versión simplificada está diseñada para demostrar
    las funcionalidades principales sin API ni interfaz gráfica.
    """
    
    def __init__(self):
        # Inicializa el sistema de logging
        Loger()
        
        # Inicializa componentes principales
        self.gral = General() 
        self.control = Control()
        self.modifySvg = ModifySvg()
        
        # Configura el logger
        self.logger = logging.getLogger('bitacora')
        
        # Banner de inicio
        docpol = pyfiglet.figlet_format("DOCPOL")
        self.logger.info('=======================================')
        self.logger.info('=======================================')
        self.logger.info(f'{docpol} v.{DOCPOL_VERSION}')
        self.logger.info('      DEMO - MODO BACKEND')
        self.logger.info('=======================================')
        self.logger.info('=======================================')
        

    def demo_logger(self):
        """
        Demuestra el funcionamiento del logger con diferentes niveles
        """
        self.logger.info("=== DEMO: Sistema de Logging ===")
        self.logger.debug("Mensaje de DEBUG")
        self.logger.info("Mensaje de INFO")
        self.logger.warning("Mensaje de WARNING")
        self.logger.error("Mensaje de ERROR")
        self.logger.info("Logs guardados en: bitacora.log")
        

    def demo_rutas(self):
        """
        Demuestra la gestión de rutas con la clase General
        """
        self.logger.info("=== DEMO: Gestión de Rutas ===")
        
        # Demostrar rutas de templates
        template_path = self.gral.get_template_path("P1")
        self.logger.info(f"Ruta template P1: {template_path}")
        
        # Demostrar rutas de imágenes
        image_path = self.gral.get_image_path("alineamiento_plot")
        self.logger.info(f"Ruta imagen: {image_path}")
        
        # Demostrar archivos temporales
        temp_file = self.gral.set_file_temp("demo-temp.svg")
        self.logger.info(f"Archivo temporal: {temp_file}")
        
        # Demostrar path principal
        self.logger.info(f"Path principal del proyecto: {self.gral.main_path}")
        

    def demo_modificar_svg(self):
        """
        Demuestra la modificación de archivos SVG
        """
        self.logger.info("=== DEMO: Modificación de SVG ===")
        
        try:
            # Modificar SVG simple
            self.modifySvg.modify_svg_1("Demo DocPol - Backend")
            self.logger.info("✓ SVG modificado correctamente")
            
            # Modificar SVG con texto generado
            sentences = [lorem.sentence() for _ in range(4)]
            texto_demo = "".join(sentences)
            self.modifySvg.modify_svg_2_1(texto_demo, "Usuario Demo", "DocPol Backend")
            self.logger.info("✓ SVG con texto generado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error al modificar SVG: {str(e)}")
            

    def ejecutar_demo_completo(self):
        """
        Ejecuta todas las demostraciones en secuencia
        """
        self.logger.info("\n" + "="*50)
        self.logger.info("INICIANDO DEMO COMPLETO DE DOCPOL")
        self.logger.info("="*50 + "\n")
        
        # 1. Demo del logger
        self.demo_logger()
        
        # 2. Demo de gestión de rutas
        self.demo_rutas()
        
        # 3. Demo de modificación de SVG
        self.demo_modificar_svg()
        
        self.logger.info("\n" + "="*50)
        self.logger.info("DEMO COMPLETADO")
        self.logger.info("Revisa el archivo bitacora.log para más detalles")
        self.logger.info("="*50 + "\n")

    def demo_pdf(self):
        from controller.GPDF2 import GPDF
        g = GPDF()
        ruta_pdf = g.create_pdf(svg_name="K0", json_name="contenido", output_name="informe_demo.pdf")
        self.logger.info(f"PDF generado correctamente en: {ruta_pdf}")
