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


from __init__ import Docpol



def Main():
    """
    Función principal del demo de DocPol
    
    Este demo muestra las funcionalidades principales:
    - Sistema de logging (bitacora.log)
    - Gestión de rutas con clase General
    - Modificación de archivos SVG
    - Exportación a PDF
    """
    
    # Inicializar DocPol
    proyecto = Docpol()
    
    # Ejecutar demo completo
    #proyecto.ejecutar_demo_completo()

    # 4. Generar PDF de demostración
    proyecto.demo_pdf()
    
    # También puedes ejecutar demos individuales:
    # proyecto.demo_logger()
    # proyecto.demo_rutas()
    # proyecto.demo_modificar_svg()
    

if __name__ == "__main__":
    Main()
