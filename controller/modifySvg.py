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
import subprocess


from lxml import etree as ET

from common.gral import General
from controller.control import Control
from common.logs import Loger
from common.decorators import *

def decorators(cls):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith("__"):
            # Aplica los decoradores a cada método
            setattr(cls, attr_name, manejar_excepciones((medir_tiempo(attr))))
    return cls

@decorators
class ModifySvg(object):
    def __init__(self):
        Loger()
        self.logger     = logging.getLogger('bitacora')
        self.gral       = General() 
        self.control    = Control()
        self.namespaces = {'svg': 'http://www.w3.org/2000/svg'}
        self.textImege  = '{http://www.w3.org/1999/xlink}href'

    def modify_svg_1(self, new_text):
        tspan_id_text = 'tspan2'
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P1")
        p1exp = self.gral.set_file_temp("P1-temp.svg")
        p1pdf = self.gral.set_file_temp("P1-temp.pdf")
        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()
        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text = root.find(f".//svg:tspan[@id='{tspan_id_text}']", self.namespaces)
        if tspan_text is not None:
            # Modificar el texto del tspan
            tspan_text.text = new_text
        else:
            self.logger.info("No se encontró el elemento tspan con id '{0}'.".
                             format(tspan_id_text))
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P1-temp.svg","P1-temp.pdf")
        self.logger.info("P1-temp.pdf completado")

    def modify_svg_2(self, new_text):
        tspan_id_text = 'tspan2'
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P1")
        p1exp = self.gral.set_file_temp("P1-temp.svg")
        p1pdf = self.gral.set_file_temp("P1-temp.pdf")
        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()
        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text = root.find(f".//svg:tspan[@id='{tspan_id_text}']", self.namespaces)
        if tspan_text is not None:
            # Modificar el texto del tspan
            tspan_text.text = new_text
        else:
            self.logger.info("No se encontró el elemento tspan con id '{0}'.".
                             format(tspan_id_text))
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P1-temp.svg","P1-temp.pdf")
        self.logger.info("P1-temp.pdf completado")

    def modify_svg_2_1(self,resumen, new_tittle1, new_text1):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P2_1")
        p1exp = self.gral.set_file_temp("P2_1-temp.svg")
        p1pdf = self.gral.set_file_temp("P2_1-temp.pdf")
        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()
        # ID del tspan que quieres modificar
        tspan_id_tittle1 = 'tspan50'
        tspan_id_text1 = 'tspan51'
        tspan_id_resumen = 'tspan4'
        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_tittle1 = root.find(f".//svg:tspan[@id='{tspan_id_tittle1}']", self.namespaces)
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']", self.namespaces)
        tspan_resumen = root.find(f".//svg:tspan[@id='{tspan_id_resumen}']", self.namespaces)
    
        if tspan_resumen is not None:
            # Modificar el texto del tspan
            tspan_resumen.text = resumen
            #self.logger.info("El texto ha sido modificado y guardado en P2_1-temp.svg")
        else:
            self.logger.error("No se encontró el elemento tspan con id '{0}'".
                              format(tspan_id_resumen))
        if tspan_tittle1 is not None:
            # Modificar el texto del tspan
            tspan_tittle1.text = new_tittle1
            #self.logger.info("El texto ha sido modificado y guardado en ")
        else:
            self.logger.error("No se encontró el elemento tspan con id '{0}'".
                              format(tspan_id_tittle1))
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = new_text1
            #self.logger.info("El texto ha sido modificado y guardado en P2_1-temp.svg")
        else:
            self.logger.error("No se encontró el elemento tspan con id '{tspan_id_text1}'".
                              format(tspan_id_text1))
    
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P2_1-temp.svg","P2_1-temp.pdf")
        self.logger.info("P2_1-temp.pdf completado")
     
    def modify_svg_2_2(self,new_tittle1, new_text1, new_tittle2, new_text2):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in = self.gral.get_template_path("P2_2.svg")
        p1exp= self.gral.set_file_temp("P2_2-temp.svg")
        p1pdf= self.gral.set_file_temp("P2_2-temp.pdf")
        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()
    
        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        #####################################################################################
    
        #Primera patología
        tspan_id_tittle1 = 'tspan1'
        tspan_id_text1 = 'tspan2'
    
        #Segunda patología
        tspan_id_tittle2 = 'tspan3'
        tspan_id_text2 = 'tspan4'
    
        #Primer texto y título
        tspan_tittle1 = root.find(f".//svg:tspan[@id='{tspan_id_tittle1}']", self.namespaces)
        tspan_text1   = root.find(f".//svg:tspan[@id='{tspan_id_text1}']",   self.namespaces)
    
        if tspan_tittle1 is not None:
            # Modificar el texto del tspan
            tspan_tittle1.text = new_tittle1
            #self.logger.info("El texto ha sido modificado y guardado en P2_2-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_tittle1}'")
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = new_text1
            #self.logger.info("El texto ha sido modificado y guardado en P2_2-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_text2}'")
    
        #Segundo texto y título
        tspan_tittle2 = root.find(f".//svg:tspan[@id='{tspan_id_tittle2}']", self.namespaces)
        tspan_text2   = root.find(f".//svg:tspan[@id='{tspan_id_text2}']",   self.namespaces)
    
        if tspan_tittle2 is not None:
            # Modificar el texto del tspan
            tspan_tittle2.text = new_tittle2
            #self.logger.info("El texto ha sido modificado y guardado en P2_2-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_tittle2}'")
        if tspan_text2 is not None:
            # Modificar el texto del tspan
            tspan_text2.text = new_text2
            #self.logger.info("El texto ha sido modificado y guardado en P2_2-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_text2}'")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P2_2-temp.svg","P2_2-temp.pdf")
        self.logger.info("P2_2-temp.pdf completado")

    def modify_svg_3_1(self, new_tittle1, new_text1, new_text2, image):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in = self.gral.get_template_path("P3_1")
        p1exp= self.gral.set_file_temp("P3_1-temp.svg")
        p1pdf= self.gral.set_file_temp("P3_1-temp.pdf")
        #Última patología
        tspan_id_tittle1 = 'tspan7'
        tspan_id_text1 = 'tspan8'
        
        #Texto descriptivo e imagen
        tspan_id_text2 = 'tspan9'
        
        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_tittle1 = root.find(f".//svg:tspan[@id='{tspan_id_tittle1}']", self.namespaces)
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']", self.namespaces)
        if tspan_tittle1 is not None:
            # Modificar el texto del tspan
            tspan_tittle1.text = new_tittle1
            #self.logger.info("El texto ha sido modificado y guardado en P3_1-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_tittle1}'")
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = new_text1
            #self.logger.info("El texto ha sido modificado y guardado en P3_1-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_text1}'")
            
        # Encontrar el tspan del texto de la imagen
        tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_text2}']", self.namespaces)
    
        if tspan_text2 is not None:
            # Modificar el texto del tspan
            tspan_text2.text = new_text2
            #self.logger.info("El texto ha sido modificado y guardado en P3_1-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_text2}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_tabla1 = 'rect3'
        element = root.find(f".//svg:*[@id='{element_id_tabla1}']", self.namespaces)
        
        #Agregar imagen de Tabla 1
        if element is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'            : element.attrib.get('x', '0'),
                'y'            : element.attrib.get('y', '0'),
                'width'        : element.attrib.get('width', '100'),
                'height'       : element.attrib.get('height', '100'),
                self.textImege : self.gral.get_image_path(image) # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element.getparent()
            parent.replace(element, new_image)
            #self.logger.info("La imagen ha sido modificada en P3_1-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_tabla1}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P3_1-temp.svg","P3_1-temp.pdf")
        self.logger.info("P3_1-temp.pdf completado")

    def modify_svg_3_2(self, table, figure):

        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P3_2.svg")
        p1exp = self.gral.set_file_temp("P3_2-temp.svg")
        p1pdf = self.gral.set_file_temp("P3_2-temp.pdf")
        #Texto a modificar
        tspan_id_tabla2 = 'tspan4'
        tspan_id_figura1 = 'tspan8'
        
        
        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_tabla2}']",  self.namespaces)
        tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", self.namespaces)
        
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = table
            #self.logger.info("El texto ha sido modificado y guardado en P3_2-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_tabla2}'")
        if tspan_text2 is not None:
            # Modificar el texto del tspan
            tspan_text2.text = figure
            #self.logger.info("El texto ha sido modificado y guardado en P3_2-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_tabla2 = 'rect4'
        element_id_figura1= 'rect3'
        element1 = root.find(f".//svg:*[@id='{element_id_tabla2}']" , self.namespaces)
        element2 = root.find(f".//svg:*[@id='{element_id_figura1}']", self.namespaces)
        
        #Agregar imagen de Tabla 2
        if element1 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'            : element1.attrib.get('x', '0'),
                'y'            : element1.attrib.get('y', '0'),
                'width'        : element1.attrib.get('width', '100'),
                'height'       : element1.attrib.get('height', '100'),
                self.textImege : self.gral.get_image_path(table)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element1.getparent()
            parent.replace(element1, new_image)
            #self.logger.info("La imagen ha sido modificada en P3_2-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_tabla2}' no encontrado.")
    
        #Agregar imagen de Figura 1
        
        if element2 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'            : element2.attrib.get('x', '0'),
                'y'            : element2.attrib.get('y', '0'),
                'width'        : element2.attrib.get('width', '100'),
                'height'       : element2.attrib.get('height', '100'),
                self.textImege : self.gral.get_image_path(figure)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element2.getparent()
            parent.replace(element2, new_image)
            #self.logger.info("La imagen ha sido modificada en P3_2-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_figura1}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P3_2-temp.svg","P3_2-temp.pdf")
        self.logger.info("P3_2-temp.pdf completado")

    def modify_svg_3_3(self, new_text1, text_tabla2, figure1, figure2):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
       
        p1in  = self.gral.get_template_path("P3_3.svg")
        p1exp = self.gral.set_file_temp("P3_3-temp.svg")
        p1pdf = self.gral.set_file_temp("P3_3-temp.pdf")
        #Texto a modificar
        tspan_id_text1 = 'tspan1'
        tspan_id_tabla2 = 'tspan6'

        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']" , self.namespaces)
        tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_tabla2}']", self.namespaces)
        
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = new_text1
            #self.logger.info("El texto ha sido modificado y guardado en P3_3-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_text1}'")
        if tspan_text2 is not None:
            # Modificar el texto del tspan
            tspan_text2.text = text_tabla2
            #self.logger.info("El texto ha sido modificado y guardado en P3_3-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_tabla2}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_tabla2 = 'rect3'
        element_id_figura1= 'rect4'
        element1 = root.find(f".//svg:*[@id='{element_id_tabla2}']" , self.namespaces)
        element2 = root.find(f".//svg:*[@id='{element_id_figura1}']", self.namespaces)
        
        #Agregar imagen de Tabla 2
        if element1 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element1.attrib.get('x', '0'),
                'y'             : element1.attrib.get('y', '0'),
                'width'         : element1.attrib.get('width', '100'),
                'height'        : element1.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure1)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element1.getparent()
            parent.replace(element1, new_image)
            #self.logger.info("La imagen ha sido modificada en P3_3-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_tabla2}' no encontrado.")
        
        #Agregar imagen de Figura 1
        
        if element2 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element2.attrib.get('x', '0'),
                'y'             : element2.attrib.get('y', '0'),
                'width'         : element2.attrib.get('width', '100'),
                'height'        : element2.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure2)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element2.getparent()
            parent.replace(element2, new_image)
            #self.logger.info("La imagen ha sido modificada en P3_3-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_figura1}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P3_3-temp.svg", "P3_3-temp.pdf")
        self.logger.info("P3_3-temp.pdf completado")
  
    def modify_svg_4_1(self, text_figura1, figure1, figure2):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P4_1.svg")
        p1exp = self.gral.set_file_temp("P4_1-temp.svg")
        p1pdf = self.gral.set_file_temp("P4_1-temp.pdf")
        #Texto a modificar
        tspan_id_figura1 = 'tspan8'

        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", self.namespaces)
        
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = text_figura1
            #self.logger.info("El texto ha sido modificado y guardado en P4_1-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_figura1 = 'rect3'
        element_id_ampli= 'rect3-4'
        element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", self.namespaces)
        element2 = root.find(f".//svg:*[@id='{element_id_ampli}']"  , self.namespaces)
        
        #Agregar imagen de Tabla 2
        if element1 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element1.attrib.get('x', '0'),
                'y'             : element1.attrib.get('y', '0'),
                'width'         : element1.attrib.get('width', '100'),
                'height'        : element1.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure1)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element1.getparent()
            parent.replace(element1, new_image)
            #self.logger.info("La imagen ha sido modificada en P4_1-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_figura1}' no encontrado.")
        
        #Agregar imagen de Figura 1
        
        if element2 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element2.attrib.get('x', '0'),
                'y'             : element2.attrib.get('y', '0'),
                'width'         : element2.attrib.get('width', '100'),
                'height'        : element2.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure2)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element2.getparent()
            parent.replace(element2, new_image)
            #self.logger.info("La imagen ha sido modificada en P4_1-temp.svg")
        else:
            self.logger.error(f"Elemento con id '{element_id_ampli}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P4_1-temp.svg","P4_1-temp.pdf") 
        self.logger.info("P4_1-temp.pdf completado")


    def modify_svg_4_2(self, text_figura1, text_figura2, figure1, figure2):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P4_2.svg")
        p1exp = self.gral.set_file_temp("P4_2-temp.svg")
        p1pdf = self.gral.set_file_temp("P4_2-temp.pdf")
        #Texto a modificar
        tspan_id_figura1 = 'tspan3'
        tspan_id_figura2 = 'tspan6'

        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", self.namespaces)
        tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_figura2}']", self.namespaces)
        
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = text_figura1
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")
        if tspan_text2 is not None:
            # Modificar el texto del tspan
            tspan_text2.text = text_figura2
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figura2}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_figura1 = 'rect3'
        element_id_figura2 = 'rect11'
        element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", self.namespaces)
        element2 = root.find(f".//svg:*[@id='{element_id_figura2}']", self.namespaces)
        
        #Agregar imagen de Tabla 2
        if element1 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'            : element1.attrib.get('x', '0'),
                'y'            : element1.attrib.get('y', '0'),
                'width'        : element1.attrib.get('width', '100'),
                'height'       : element1.attrib.get('height', '100'),
                self.textImege : self.gral.get_image_path(figure1)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element1.getparent()
            parent.replace(element1, new_image)
        else:
            self.logger.error(f"Elemento con id '{element_id_figura1}' no encontrado.")
        
        #Agregar imagen de Figura 1
        
        if element2 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'            : element2.attrib.get('x', '0'),
                'y'            : element2.attrib.get('y', '0'),
                'width'        : element2.attrib.get('width', '100'),
                'height'       : element2.attrib.get('height', '100'),
                self.textImege : self.gral.get_image_path(figure2)  # Asegúrate de poner la ruta correcta
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element2.getparent()
            parent.replace(element2, new_image)
        else:
            self.logger.error(f"Elemento con id '{element_id_figura2}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P4_2-temp.svg","P4_2-temp.pdf")
        self.logger.info("P4_2-temp.pdf completado")


    def modify_svg_4_3(self, text_figura1, text_figura2, figure1, figure2):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  = self.gral.get_template_path("P4_3.svg")
        p1exp = self.gral.set_file_temp("P4_3-temp.svg")
        p1pdf = self.gral.set_file_temp("P4_3-temp.pdf")
        #Texto a modificar
        tspan_id_figura1 = 'tspan4'
        tspan_id_figura2 = 'tspan7'

        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", self.namespaces)
        tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_figura2}']", self.namespaces)
        
        if tspan_text1 is not None:
            # Modificar el texto del tspan
            tspan_text1.text = text_figura1
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")
        if tspan_text2 is not None:
            # Modificar el texto del tspan
            tspan_text2.text = text_figura2
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figura2}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_figura1 = 'rect3'
        element_id_figura2 = 'rect11'
        element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", self.namespaces)
        element2 = root.find(f".//svg:*[@id='{element_id_figura2}']", self.namespaces)
    
        #Agregar imagen de Figura 1
        if element1 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element1.attrib.get('x', '0'),
                'y'             : element1.attrib.get('y', '0'),
                'width'         : element1.attrib.get('width', '100'),
                'height'        : element1.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure1)
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element1.getparent()
            parent.replace(element1, new_image)
        else:
            self.logger.error(f"Elemento con id '{element_id_figura1}' no encontrado.")
        
        #Agregar imagen de Figura 2
        
        if element2 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element2.attrib.get('x', '0'),
                'y'             : element2.attrib.get('y', '0'),
                'width'         : element2.attrib.get('width', '100'),
                'height'        : element2.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure2)
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element2.getparent()
            parent.replace(element2, new_image)
        else:
            self.logger.error(f"Elemento con id '{element_id_figura2}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P4_3-temp.svg","P4_3-temp.pdf")
        self.logger.info("P4_3-temp.pdf completado")


    def modify_svg_4_4(self, text_figuraX, new_text, figure1, figure2):
        #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
        p1in  =  self.gral.get_template_path("P4_4.svg")
        p1exp =  self.gral.set_file_temp("P4_4-temp.svg")
        p1pdf =  self.gral.set_file_temp("P4_4-temp.pdf")
        #Texto a modificar
        tspan_id_figuraX = 'tspan14'
        tspan_id_text = 'tspan16'

        # Cargar el archivo SVG
        tree = ET.parse(p1in)
        root = tree.getroot()

        # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
        tspan_figuraX = root.find(f".//svg:tspan[@id='{tspan_id_figuraX}']", self.namespaces)
        tspan_text = root.find(f".//svg:tspan[@id='{tspan_id_text}']",       self.namespaces)
        
        if tspan_figuraX is not None:
            # Modificar el texto del tspan
            tspan_figuraX.text = text_figuraX
            # Guardar los cambios en un nuevo archivo
            #tree.write('/Users/galmarod/Documents/PruebasBASH/P4_4-temp.svg')
            #print("El texto ha sido modificado y guardado en P4_4-temp.svg")
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_figuraX}'")
        if tspan_text is not None:
            # Modificar el texto del tspan
            tspan_text.text = new_text
        else:
            self.logger.error(f"No se encontró el elemento tspan con id '{tspan_id_text}'")

        # Encontrar el elemento que se desea reemplazar por la imagen PNG
        element_id_figura1 = 'rect4'
        element_id_ampli= 'rect3'
        element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", self.namespaces)
        element2 = root.find(f".//svg:*[@id='{element_id_ampli}']",   self.namespaces)
        
        #Agregar imagen de Tabla 2
        if element1 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element1.attrib.get('x', '0'),
                'y'             : element1.attrib.get('y', '0'),
                'width'         : element1.attrib.get('width', '100'),
                'height'        : element1.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure1)
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element1.getparent()
            parent.replace(element1, new_image)
        else:
            self.logger.error(f"Elemento con id '{element_id_figura1}' no encontrado.")
        
        #Agregar imagen de Figura 1
        
        if element2 is not None:
            # Crear el nuevo elemento de imagen
            new_image = ET.Element(f"{{{self.namespaces['svg']}}}image", {
                'x'             : element2.attrib.get('x', '0'),
                'y'             : element2.attrib.get('y', '0'),
                'width'         : element2.attrib.get('width', '100'),
                'height'        : element2.attrib.get('height', '100'),
                self.textImege  : self.gral.get_image_path(figure2)
            })
        
            # Reemplazar el elemento original con el nuevo elemento de imagen
            parent = element2.getparent()
            parent.replace(element2, new_image)
        else:
            self.logger.error(f"Elemento con id '{element_id_ampli}' no encontrado.")
        # Guardar los cambios en un nuevo archivo
        tree.write(p1exp)
        self.control.export_svg_to_pdf("P4_4-temp.svg","P4_4-temp.pdf")
        self.logger.info("P4_4-temp.pdf completado")

