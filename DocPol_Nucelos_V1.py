#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 10:51:46 2024

@author: galmarod
"""
__author__     = "Guillermo Almazán Rodríguez"
__copyright__  = "Copyright 2024, RevelCode"
__credits__    = ["galmarod"]
__license__    = "GPL"
__version__    = "1.0.1"
__maintainer__ = "Francisco Javier Mendoza Bautista"
__email__      = "javimenba.developer@gmail.com"
__status__     = "Development"
__date__       = "Oct-2024"
#En este programa se pretende conjuntar todos los códigos para la generación de reportes pdf
#automáticos del proyecto PABLO

from lxml import etree as ET
import subprocess
from PyPDF2 import PdfMerger

dict_patos={'1':'Chikungunya',
    '2':'COVID-19',
       '3':'Dengue',
       '4':'Influenza_A',
       '5':'RSV'}

                    # FUNCIONES COMPLETAS #

#################################################################
##################### Exportar SVG a PDF ########################
#################################################################

def export_svg_to_pdf(svg_file, pdf_file):
    # Define el comando de Inkscape
    command = ["/Applications/Inkscape.app/Contents/MacOS/inkscape", "--pipe", f"--export-filename={pdf_file}"]

    # Abre el archivo SVG y pasa su contenido al comando de Inkscape
    try:
        with open(svg_file, 'rb') as svg_content:
            subprocess.run(command, input=svg_content.read(), check=True)
        print(f"Archivo '{svg_file}' exportado exitosamente a PDF como '{pdf_file}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al exportar '{svg_file}' a PDF: {e}")
    except FileNotFoundError:
        print(f"El archivo '{svg_file}' no se encontró.")
'''
#################################################################
# Uso del programa
raiz='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/'
export_svg_to_pdf(raiz+"P2_1-temp.svg", raiz+"P2_1-temp.pdf")
#################################################################
'''
#################################################################
########################## Unir PDF #############################
#################################################################

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    merger.write(output_path)
    merger.close()
'''
#################################################################
# Ejemplo de uso
raiz='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/'
pdfs = [raiz+"P1-temp.pdf", raiz+"P2_1-temp.pdf"]
output = raiz+"archivo_unido.pdf"
#merge_pdfs(pdfs, output)
print(f"PDFs unidos en: {output}")
#################################################################
'''
#################################################################
####################### Plantilla P1 ############################
#################################################################

def modify_svg_1(new_text):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    tspan_id_text = 'tspan2'
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P1.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P1-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P1-temp.pdf'
    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()
    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text = root.find(f".//svg:tspan[@id='{tspan_id_text}']", namespaces)
    if tspan_text is not None:
        # Modificar el texto del tspan
        tspan_text.text = new_text
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text}'")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P1-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
text_portada= "Generación de sistema de diagnóstico por IA de "
new_text = (text_portada + 'Patógeno X')
modify_svg_1(new_text)
#################################################################
'''
#################################################################
####################### Plantilla P2_1 ##########################
#################################################################
def modify_svg_2_1(resumen, new_tittle1, new_text1):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P2_1.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P2_1-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P2_1-temp.pdf'
    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()
    # ID del tspan que quieres modificar
    tspan_id_tittle1 = 'tspan50'
    tspan_id_text1 = 'tspan51'
    tspan_id_resumen = 'tspan4'
    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_tittle1 = root.find(f".//svg:tspan[@id='{tspan_id_tittle1}']", namespaces)
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']", namespaces)
    tspan_resumen = root.find(f".//svg:tspan[@id='{tspan_id_resumen}']", namespaces)
    
    if tspan_resumen is not None:
        # Modificar el texto del tspan
        tspan_resumen.text = resumen
        print("El texto ha sido modificado y guardado en P2_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_resumen}'")
    if tspan_tittle1 is not None:
        # Modificar el texto del tspan
        tspan_tittle1.text = new_tittle1
        print("El texto ha sido modificado y guardado en ")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tittle1}'")
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = new_text1
        print("El texto ha sido modificado y guardado en P2_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text1}'")
    
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P2_1-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_tittle1 = 'Título patógeno Parkinson'
new_text1 = 'Patógeno de Parkinson 2 siiiu'
resumen = """El sistema de diagnóstico por IA generado por PABLO está diseñado para la identificación específica del o los patógenos causantes de  Parkinson y _________________ en ADN ó ARN, tomadas de acuerdo con los lineamientos establecidos por el InDRE (Lineamiento estandarizado para la vigilancia epidemiológica y por laboratorio de la enfermedad respiratoria viral, Octubre, 2021).
El ARN es amplificado por RT-qPCR (si es el caso) y la detección de los blancos se realiza por medio de la lectura de fluorescencia de las sondas diseñadas de forma específica: FAM (Pato1________), Texas Red (Pato2__________), HEX (____________) y Cy5 (_____________________) 
El objetivo de esta prueba es servir como auxiliar en el diagnóstico, en combinación de factores clínicos y epidemiológicos.
Agente de diagnóstico para uso in vitro."""
modify_svg_2_1(resumen, new_tittle1, new_text1)
#################################################################
'''
#################################################################
####################### Plantilla P2_2 ##########################
#################################################################

def modify_svg_2_2(new_tittle1, new_text1, new_tittle2, new_text2):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P2_2.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P2_2-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P2_2-temp.pdf'
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
    tspan_tittle1 = root.find(f".//svg:tspan[@id='{tspan_id_tittle1}']", namespaces)
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']", namespaces)
    
    if tspan_tittle1 is not None:
        # Modificar el texto del tspan
        tspan_tittle1.text = new_tittle1
        print("El texto ha sido modificado y guardado en P2_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tittle1}'")
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = new_text1
        print("El texto ha sido modificado y guardado en P2_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text2}'")
    
    #Segundo texto y título
    tspan_tittle2 = root.find(f".//svg:tspan[@id='{tspan_id_tittle2}']", namespaces)
    tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_text2}']", namespaces)
    
    if tspan_tittle2 is not None:
        # Modificar el texto del tspan
        tspan_tittle2.text = new_tittle2
        print("El texto ha sido modificado y guardado en P2_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tittle2}'")
    if tspan_text2 is not None:
        # Modificar el texto del tspan
        tspan_text2.text = new_text2
        print("El texto ha sido modificado y guardado en P2_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text2}'")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P2_2-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_tittle1 = 'Título patógeno1-X'
new_text1 = 'Patógeno X'
new_tittle2 = 'Título patógeno 2-Y'
new_text2 = 'Patógeno Y'
modify_svg_2_2(new_tittle1, new_text1, new_tittle2, new_text2)
#################################################################
'''
#################################################################
####################### Plantilla P3_1 ##########################
#################################################################
def modify_svg_3_1(new_tittle1, new_text1, new_text2):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P3_1.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P3_1-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P3_1-temp.pdf'
    #Última patología
    tspan_id_tittle1 = 'tspan7'
    tspan_id_text1 = 'tspan8'
    
    #Texto descriptivo e imagen
    tspan_id_text2 = 'tspan9'
    
    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_tittle1 = root.find(f".//svg:tspan[@id='{tspan_id_tittle1}']", namespaces)
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']", namespaces)
    if tspan_tittle1 is not None:
        # Modificar el texto del tspan
        tspan_tittle1.text = new_tittle1
        print("El texto ha sido modificado y guardado en P3_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tittle1}'")
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = new_text1
        print("El texto ha sido modificado y guardado en P3_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text1}'")
        
    # Encontrar el tspan del texto de la imagen
    tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_text2}']", namespaces)
    
    if tspan_text2 is not None:
        # Modificar el texto del tspan
        tspan_text2.text = new_text2
        print("El texto ha sido modificado y guardado en P3_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text2}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_tabla1 = 'rect3'
    element = root.find(f".//svg:*[@id='{element_id_tabla1}']", namespaces)
    
    #Agregar imagen de Tabla 1
    if element is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element.attrib.get('x', '0'),
            'y': element.attrib.get('y', '0'),
            'width': element.attrib.get('width', '100'),
            'height': element.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element.getparent()
        parent.replace(element, new_image)
        print("La imagen ha sido modificada en P3_1-temp.svg")
    else:
        print(f"Elemento con id '{element_id_tabla1}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P3_1-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_tittle1 = 'Título patógeno X'
new_text1 = 'Patógeno X-2'

text_imagen= "Estos son los mejores oligonucleótidos y sondas diseñados por Pablo para el diagnóstico de "
new_text2 = (text_imagen + new_text1)
             
modify_svg_3_1(new_tittle1, new_text1, new_text2)
#################################################################
'''
#################################################################
####################### Plantilla P3_2 ##########################
#################################################################
def modify_svg_3_2(text_tabla2, text_figura1):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P3_2.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P3_2-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P3_2-temp.pdf'
    #Texto a modificar
    tspan_id_tabla2 = 'tspan4'
    tspan_id_figura1 = 'tspan8'
    
    
    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_tabla2}']", namespaces)
    tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", namespaces)
    
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = text_tabla2
        print("El texto ha sido modificado y guardado en P3_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tabla2}'")
    if tspan_text2 is not None:
        # Modificar el texto del tspan
        tspan_text2.text = text_figura1
        print("El texto ha sido modificado y guardado en P3_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_tabla2 = 'rect4'
    element_id_figura1= 'rect3'
    element1 = root.find(f".//svg:*[@id='{element_id_tabla2}']", namespaces)
    element2 = root.find(f".//svg:*[@id='{element_id_figura1}']", namespaces)
    
    #Agregar imagen de Tabla 2
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P3_2-temp.svg")
    else:
        print(f"Elemento con id '{element_id_tabla2}' no encontrado.")
    
    #Agregar imagen de Figura 1
    
    if element2 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element2.attrib.get('x', '0'),
            'y': element2.attrib.get('y', '0'),
            'width': element2.attrib.get('width', '100'),
            'height': element2.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element2.getparent()
        parent.replace(element2, new_image)
        print("La imagen ha sido modificada en P3_2-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura1}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P3_2-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text1 = 'Patógeno X-2.1'
text_tabla2 = ' Protocolo de qPCR para ' + new_text1

new_text2 = 'Patógeno Y-2.1'
text_figura1 = 'Esta es la mejor región del alineamiento para ' + new_text2
             
modify_svg_3_2(text_tabla2, text_figura1)
#################################################################    
'''
#################################################################
####################### Plantilla P3_3 ##########################
#################################################################
def modify_svg_3_3(new_text1, text_tabla2):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P3_3.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P3_3-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P3_3-temp.pdf'
    #Texto a modificar
    tspan_id_text1 = 'tspan1'
    tspan_id_tabla2 = 'tspan6'

    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_text1}']", namespaces)
    tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_tabla2}']", namespaces)
    
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = new_text1
        print("El texto ha sido modificado y guardado en P3_3-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text1}'")
    if tspan_text2 is not None:
        # Modificar el texto del tspan
        tspan_text2.text = text_tabla2
        print("El texto ha sido modificado y guardado en P3_3-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tabla2}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_tabla2 = 'rect3'
    element_id_figura1= 'rect4'
    element1 = root.find(f".//svg:*[@id='{element_id_tabla2}']", namespaces)
    element2 = root.find(f".//svg:*[@id='{element_id_figura1}']", namespaces)
    
    #Agregar imagen de Tabla 2
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P3_3-temp.svg")
    else:
        print(f"Elemento con id '{element_id_tabla2}' no encontrado.")
    
    #Agregar imagen de Figura 1
    
    if element2 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element2.attrib.get('x', '0'),
            'y': element2.attrib.get('y', '0'),
            'width': element2.attrib.get('width', '100'),
            'height': element2.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element2.getparent()
        parent.replace(element2, new_image)
        print("La imagen ha sido modificada en P3_3-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura1}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P3_3-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text = 'Patógeno X-1.1'

new_text1 = "Estos son los mejores oligonucleótidos y sondas diseñados por Pablo para el diagnóstico de " + new_text
text_tabla2 = 'Protocolo de qPCR para ' + new_text
       
modify_svg_3_3(new_text1, text_tabla2)
#################################################################
'''
#################################################################
####################### Plantilla P4_1 ##########################
#################################################################
def modify_svg_4_1(text_figura1):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P4_1.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_1-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_1-temp.pdf'
    #Texto a modificar
    tspan_id_figura1 = 'tspan8'

    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", namespaces)
    
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = text_figura1
        print("El texto ha sido modificado y guardado en P4_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_figura1 = 'rect3'
    element_id_ampli= 'rect3-4'
    element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", namespaces)
    element2 = root.find(f".//svg:*[@id='{element_id_ampli}']", namespaces)
    
    #Agregar imagen de Tabla 2
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P4_1-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura1}' no encontrado.")
    
    #Agregar imagen de Figura 1
    
    if element2 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element2.attrib.get('x', '0'),
            'y': element2.attrib.get('y', '0'),
            'width': element2.attrib.get('width', '100'),
            'height': element2.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element2.getparent()
        parent.replace(element2, new_image)
        print("La imagen ha sido modificada en P4_1-temp.svg")
    else:
        print(f"Elemento con id '{element_id_ampli}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P4_1-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text1 = 'Patógeno X.1'

text_figura1 = 'Esta es la mejor región del alineamiento para ' + new_text1
             
modify_svg_4_1(text_figura1)
#################################################################   
'''
#################################################################
####################### Plantilla P4_2 ##########################
#################################################################
def modify_svg_4_2(text_figura1, text_figura2):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P4_2.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_2-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_2-temp.pdf'
    #Texto a modificar
    tspan_id_figura1 = 'tspan3'
    tspan_id_figura2 = 'tspan6'

    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", namespaces)
    tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_figura2}']", namespaces)
    
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = text_figura1
        print("El texto ha sido modificado y guardado en P4_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")
    if tspan_text2 is not None:
        # Modificar el texto del tspan
        tspan_text2.text = text_figura2
        print("El texto ha sido modificado y guardado en P4_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figura2}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_figura1 = 'rect3'
    element_id_figura2 = 'rect11'
    element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", namespaces)
    element2 = root.find(f".//svg:*[@id='{element_id_figura2}']", namespaces)
    
    #Agregar imagen de Tabla 2
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P4_2-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura1}' no encontrado.")
    
    #Agregar imagen de Figura 1
    
    if element2 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element2.attrib.get('x', '0'),
            'y': element2.attrib.get('y', '0'),
            'width': element2.attrib.get('width', '100'),
            'height': element2.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element2.getparent()
        parent.replace(element2, new_image)
        print("La imagen ha sido modificada en P4_2-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura2}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P4_2-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text1 = 'Patógeno X-1.1'
new_text2 = 'Patógeno Y-1.1'

text_figura1 = 'Esta es la mejor región del alineamiento para ' + new_text1
text_figura2 = 'Esta es la mejor región del alineamiento para ' + new_text2
             
modify_svg_4_2(text_figura1, text_figura2)
#################################################################  
'''
#################################################################
####################### Plantilla P4_3 ##########################
#################################################################
def modify_svg_4_3(text_figura1, text_figura2):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P4_3.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_3-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_3-temp.pdf'
    #Texto a modificar
    tspan_id_figura1 = 'tspan4'
    tspan_id_figura2 = 'tspan7'

    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text1 = root.find(f".//svg:tspan[@id='{tspan_id_figura1}']", namespaces)
    tspan_text2 = root.find(f".//svg:tspan[@id='{tspan_id_figura2}']", namespaces)
    
    if tspan_text1 is not None:
        # Modificar el texto del tspan
        tspan_text1.text = text_figura1
        print("El texto ha sido modificado y guardado en P4_3-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figura1}'")
    if tspan_text2 is not None:
        # Modificar el texto del tspan
        tspan_text2.text = text_figura2
        print("El texto ha sido modificado y guardado en P4_3-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figura2}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_figura1 = 'rect3'
    element_id_figura2 = 'rect11'
    element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", namespaces)
    element2 = root.find(f".//svg:*[@id='{element_id_figura2}']", namespaces)
    
    #Agregar imagen de Figura 1
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P4_3-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura1}' no encontrado.")
    
    #Agregar imagen de Figura 2
    
    if element2 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element2.attrib.get('x', '0'),
            'y': element2.attrib.get('y', '0'),
            'width': element2.attrib.get('width', '100'),
            'height': element2.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element2.getparent()
        parent.replace(element2, new_image)
        print("La imagen ha sido modificada en P4_3-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura2}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P4_3-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text1 = 'Patógeno Xalaka'
new_text2 = 'Patógeno Yuri'

text_figura1 = 'Esta es la mejor región del alineamiento para ' + new_text1
text_figura2 = 'Esta es la mejor región del alineamiento para ' + new_text2
             
modify_svg_4_3(text_figura1, text_figura2)
#################################################################  
'''
#################################################################
####################### Plantilla P4_4 ##########################
#################################################################
def modify_svg_4_4(text_figuraX, new_text):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P4_4.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_4-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P4_4-temp.pdf'
    #Texto a modificar
    tspan_id_figuraX = 'tspan14'
    tspan_id_text = 'tspan16'

    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_figuraX = root.find(f".//svg:tspan[@id='{tspan_id_figuraX}']", namespaces)
    tspan_text = root.find(f".//svg:tspan[@id='{tspan_id_text}']", namespaces)
    
    if tspan_figuraX is not None:
        # Modificar el texto del tspan
        tspan_figuraX.text = text_figuraX
        # Guardar los cambios en un nuevo archivo
        tree.write('/Users/galmarod/Documents/PruebasBASH/P4_4-temp.svg')
        print("El texto ha sido modificado y guardado en P4_4-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_figuraX}'")
    if tspan_text is not None:
        # Modificar el texto del tspan
        tspan_text.text = new_text
        print("El texto ha sido modificado y guardado en P4_4-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_figura1 = 'rect4'
    element_id_ampli= 'rect3'
    element1 = root.find(f".//svg:*[@id='{element_id_figura1}']", namespaces)
    element2 = root.find(f".//svg:*[@id='{element_id_ampli}']", namespaces)
    
    #Agregar imagen de Tabla 2
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P4_4-temp.svg")
    else:
        print(f"Elemento con id '{element_id_figura1}' no encontrado.")
    
    #Agregar imagen de Figura 1
    
    if element2 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element2.attrib.get('x', '0'),
            'y': element2.attrib.get('y', '0'),
            'width': element2.attrib.get('width', '100'),
            'height': element2.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/alineamiento_plot.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element2.getparent()
        parent.replace(element2, new_image)
        print("La imagen ha sido modificada en P4_4-temp.svg")
    else:
        print(f"Elemento con id '{element_id_ampli}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P4_4-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text1 = 'Patógeno X.04'

text_figuraX = 'Figura 4.04'
new_text = 'Esta es la mejor región del alineamiento para ' + new_text1       

modify_svg_4_4(text_figuraX, new_text)
################################################################# 
'''
#################################################################
####################### Plantilla P5_1 ##########################
#################################################################
def modify_svg_5_1(text_tablaX):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P5_1.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P5_1-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P5_1-temp.pdf'
    #Texto a modificar
    tspan_id_tablaX = 'tspan1'

    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_tablaX = root.find(f".//svg:tspan[@id='{tspan_id_tablaX}']", namespaces)
    
    if tspan_tablaX is not None:
        # Modificar el texto del tspan
        tspan_tablaX.text = text_tablaX
        print("El texto ha sido modificado y guardado en P5_1-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_tablaX}'")

    # Encontrar el elemento que se desea reemplazar por la imagen PNG
    element_id_tablaX = 'rect4'
    element1 = root.find(f".//svg:*[@id='{element_id_tablaX}']", namespaces)
    
    #Agregar imagen de Tabla X
    if element1 is not None:
        # Crear el nuevo elemento de imagen
        new_image = ET.Element(f"{{{namespaces['svg']}}}image", {
            'x': element1.attrib.get('x', '0'),
            'y': element1.attrib.get('y', '0'),
            'width': element1.attrib.get('width', '100'),
            'height': element1.attrib.get('height', '100'),
            '{http://www.w3.org/1999/xlink}href': '/Users/galmarod/Documents/GrupoT4/PABLO/Imagenes/Tabla-interpretacion.png'  # Asegúrate de poner la ruta correcta
        })
    
        # Reemplazar el elemento original con el nuevo elemento de imagen
        parent = element1.getparent()
        parent.replace(element1, new_image)
        print("La imagen ha sido modificada en P5_1-temp.svg")
    else:
        print(f"Elemento con id '{element_id_tablaX}' no encontrado.")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P5_1-temp.pdf completado")

################## Prueba de funcionamiento #####################
# Variables de Prueba
text_tablaX = 'Tabla 5'     

modify_svg_5_1(text_tablaX)
################################################################# 

#################################################################
####################### Plantilla P5_2 ##########################
#################################################################

def modify_svg_5_2(new_text):
    # Definir los espacios de nombres utilizados en el archivo SVG
    namespaces = {'svg': 'http://www.w3.org/2000/svg'}
    tspan_id_text = 'tspan1'
    
    #Definir los documentos de entrada (in) y salida (exp-temp.svg y exp-temp.pdf )
    p1in='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/plantillas/P5_2.svg'
    p1exp='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P5_2-temp.svg'
    p1pdf='/Users/galmarod/Documents/GrupoT4/PABLO/Programas/DocPol_Nucelos_V1/pruebas/P5_2-temp.pdf'
    
    # Cargar el archivo SVG
    tree = ET.parse(p1in)
    root = tree.getroot()

    # Encontrar el tspan Título con el id especificado utilizando los espacios de nombres
    tspan_text = root.find(f".//svg:tspan[@id='{tspan_id_text}']", namespaces)
    if tspan_text is not None:
        # Modificar el texto del tspan
        tspan_text.text = new_text
        print("El texto ha sido modificado y guardado en P5_2-temp.svg")
    else:
        print(f"No se encontró el elemento tspan con id '{tspan_id_text}'")
    # Guardar los cambios en un nuevo archivo
    tree.write(p1exp)
    export_svg_to_pdf(p1exp,p1pdf)
    print("P5_2-temp.pdf completado")
'''
################## Prueba de funcionamiento #####################
# Variables de Prueba
new_text= """    > 5.1.	Tipos de virus de influenza. Centros para el Control y la Prevención de Enfermedades.	2019.
https://www.cdc.gov/pcd/spanish/for_authors/references_guide_es.htm. Consultado el 21 de octubre de 2021.
    > 5.2.	Konala, V. M., Adapa, S., Naramala, S., Chenna, A., Lamichhane, S., Garlapati, P. R.,	& Gayam, V. (2020). A case series of patients coinfected with
influenza and COVID-19. Journal of investigative medicine high impact caseeports, 8, 2324709620934674.
   > 5.3.	Cruz, M. P., Santos, E., Cervantes, M. V., & Juárez, M. L. (2021). COVID- 19, una emergencia de salud pública mundial. Revista Clínica Española, 221(1), 55-61.
    > 5.4.	Benitez, J. A., Brac, E. S., Frías, L., & Aguirre, O. (2007). Virus sincitial respiratorio aspectos generales y básicos sobre la evolución clínica, factores de riesgo y tratamiento. Rev Posgrado Med, 171, 8-12.
   > 5.5.	Mostafa, H. H., Carroll, K. C., Hicken, R., Berry, G. J., Manji, R., Smith, E., & Loeffelholz, M. J. (2021). Multicenter evaluation of the cepheid xpert xpress SARS-CoV-2/Flu/VSR test. Journal of clinical microbiology, 59(3), e02955-20.
    > 5.6.	Cuadrado-Payán, E., Montagud-Marrahi, E., Torres-Elorza, M., Bodro, M., Blasco, M., Poch, E., & Piñeiro, G. J. (2020). SARS-CoV-2 and influenza virus co-infection. Lancet (London, England), 395(10236), 84. """

modify_svg_5_2(new_text)
#################################################################
'''






'''
                        # CONDICIONALES #

        
pathologies=[]
print(f'Esocge una de la siguientes patologías\n{dict_patos}\n')
pathologies.append(str(input('Tu respuesta: ')))

while len(pathologies) < 4:
    print(f'Si deseas elegir más patologías escoge otro número\n{dict_patos}\nDe lo contrario, escribe 0.')
    pathologies.append(input('Tu respuesta: '))
    if '0' in pathologies:
        break

#Borrar el 0 de la lista de patologías elegidas
if '0' in pathologies:
        pathologies.remove('0')
        


   
                         # TRABAJO #


#################################################################
####################### 1 PATOLOGÍA #############################
#################################################################
#################################################################

if len(pathologies) == 1:
    
    #Extraer patología(s)
    pato1= str(dict_patos[pathologies[0]])
    
    #################################################################   
    ###################### Creación de Portada ######################
    ##########################    P1    #############################
    #################################################################
    # INSERTAR TEXTO
    text_portada= "Generación de sistema de diagnóstico por IA de "
    # Se lee y almacena
    new_text = (text_portada + pato1 + '.')
    # Ruta donde guardar el nuevo archivo SVG
    modify_svg_1(new_text)
    #################################################################   
    #################### Resumen e Introducción #####################
    #########################    P2_1    ############################
    #################################################################
    # Variables de Prueba
    new_tittle1 = 'Título patógeno X'
    new_text1 = 'Patógeno X'
    resumen = f"""El sistema de diagnóstico por IA generado por PABLO está diseñado para la identificación específica del o los patógenos causantes de {pato1} en ADN ó ARN, tomadas de acuerdo con los lineamientos establecidos por el InDRE (Lineamiento estandarizado para la vigilancia epidemiológica y por laboratorio de la enfermedad respiratoria viral, Octubre, 2021).
    El ARN es amplificado por RT-qPCR (si es el caso) y la detección de los blancos se realiza por medio de la lectura de fluorescencia de las sondas diseñadas de forma específica: FAM ({pato1}). 
    El objetivo de esta prueba es servir como auxiliar en el diagnóstico, en combinación de factores clínicos y epidemiológicos.
    Agente de diagnóstico para uso in vitro."""
    modify_svg_2_1(resumen, new_tittle1, new_text1)
    #################################################################   
    ################ Características de Diagnóstico #################
    #########################    P3_3    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = f"Estos son los mejores oligonucleótidos y sondas diseñados por Pablo para el diagnóstico de {pato1}" 
    text_tabla2 = f'Protocolo de qPCR para {pato1}'
    modify_svg_3_3(new_text1, text_tabla2)
    #################################################################   
    ####### Regiones de Alineamiento y Resultados Simulación ########
    #########################    P4_1    ############################
    #################################################################
    # Variables de Prueba
    text_figura1 = f'Esta es la mejor región del alineamiento para {pato1}'
    modify_svg_4_1(text_figura1)
    #################################################################   
    ####################### Resultados Tabla ########################
    #########################    P5_1    ############################
    #################################################################
    # Variables de Prueba
    text_tablaX = 'Tabla 5'     
    modify_svg_5_1(text_tablaX)
    #################################################################   
    ################### Referencias y Simbología ####################
    #########################    P5_2    ############################
    #################################################################
    # Variables de Prueba
    new_text= """    > 5.1.	Tipos de virus de influenza. Centros para el Control y la Prevención de Enfermedades.	2019.
    https://www.cdc.gov/pcd/spanish/for_authors/references_guide_es.htm. Consultado el 21 de octubre de 2021.
        > 5.2.	Konala, V. M., Adapa, S., Naramala, S., Chenna, A., Lamichhane, S., Garlapati, P. R.,	& Gayam, V. (2020). A case series of patients coinfected with
    influenza and COVID-19. Journal of investigative medicine high impact caseeports, 8, 2324709620934674.
       > 5.3.	Cruz, M. P., Santos, E., Cervantes, M. V., & Juárez, M. L. (2021). COVID- 19, una emergencia de salud pública mundial. Revista Clínica Española, 221(1), 55-61.
        > 5.4.	Benitez, J. A., Brac, E. S., Frías, L., & Aguirre, O. (2007). Virus sincitial respiratorio aspectos generales y básicos sobre la evolución clínica, factores de riesgo y tratamiento. Rev Posgrado Med, 171, 8-12.
       > 5.5.	Mostafa, H. H., Carroll, K. C., Hicken, R., Berry, G. J., Manji, R., Smith, E., & Loeffelholz, M. J. (2021). Multicenter evaluation of the cepheid xpert xpress SARS-CoV-2/Flu/VSR test. Journal of clinical microbiology, 59(3), e02955-20.
        > 5.6.	Cuadrado-Payán, E., Montagud-Marrahi, E., Torres-Elorza, M., Bodro, M., Blasco, M., Poch, E., & Piñeiro, G. J. (2020). SARS-CoV-2 and influenza virus co-infection. Lancet (London, England), 395(10236), 84. """
    modify_svg_5_2(new_text)

#################################################################
####################### 2 PATOLOGÍAS ############################
#################################################################
#################################################################

if len(pathologies) == 2:
    
    #Extraer patología(s)
    pato1= str(dict_patos[pathologies[0]])
    pato2= str(dict_patos[pathologies[1]])
    
    #################################################################   
    ###################### Creación de Portada ######################
    ##########################    P1    #############################
    #################################################################
    # INSERTAR TEXTO
    text_portada= "Generación de sistema de diagnóstico por IA de "
    # Se lee y almacena
    new_text = f'{text_portada} {pato1} y {pato2}.'
    # Ruta donde guardar el nuevo archivo SVG
    modify_svg_1(new_text)
    #################################################################   
    #################### Resumen e Introducción #####################
    #########################    P2_1    ############################
    #################################################################
    # Variables de Prueba
    new_tittle1 = 'Título patógeno X'
    new_text1 = 'Patógeno X'
    resumen = f"""El sistema de diagnóstico por IA generado por PABLO está diseñado para la identificación específica del o los patógenos causantes de {pato1} y {pato2} en ADN ó ARN, tomadas de acuerdo con los lineamientos establecidos por el InDRE (Lineamiento estandarizado para la vigilancia epidemiológica y por laboratorio de la enfermedad respiratoria viral, Octubre, 2021).
    El ARN es amplificado por RT-qPCR (si es el caso) y la detección de los blancos se realiza por medio de la lectura de fluorescencia de las sondas diseñadas de forma específica: FAM ({pato1}) y Texas Red ({pato2}). 
    El objetivo de esta prueba es servir como auxiliar en el diagnóstico, en combinación de factores clínicos y epidemiológicos.
    Agente de diagnóstico para uso in vitro."""
    modify_svg_2_1(resumen, new_tittle1, new_text1)
    #################################################################   
    ################ Características de Diagnóstico #################
    #########################    P3_1    ############################
    #################################################################
    # Variables de Prueba
    # Variables de Prueba
    new_tittle1 = 'Título patógeno X'
    new_text1 = 'Patógeno X-2'
    text_imagen= f"Estos son los mejores oligonucleótidos y sondas diseñados por Pablo para el diagnóstico de {pato1} y {pato2}."
    new_text2 = (text_imagen + new_text1)
    modify_svg_3_1(new_tittle1, new_text1, new_text2)
    #################################################################   
    ################ Características de Diagnóstico #################
    #########################    P3_2    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = 'Patógeno X-2.1'
    text_tabla2 = f' Protocolo de qPCR para {pato2}.'
    new_text2 = 'Patógeno Y-2.1'
    text_figura1 = f'Esta es la mejor región del alineamiento para {pato1}'
    modify_svg_3_2(text_tabla2, text_figura1)
    #################################################################   
    ####### Regiones de Alineamiento y Resultados Simulación ########
    #########################    P4_4    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = 'Patógeno X.04'

    text_figuraX = 'Figura 4.04'
    new_text = f'Esta es la mejor región del alineamiento para {pato2}'      
    modify_svg_4_4(text_figuraX, new_text)
    #################################################################   
    ####################### Resultados Tabla ########################
    #########################    P5_1    ############################
    #################################################################
    # Variables de Prueba
    text_tablaX = 'Tabla 5'     
    modify_svg_5_1(text_tablaX)
    #################################################################   
    ################### Referencias y Simbología ####################
    #########################    P5_2    ############################
    #################################################################
    # Variables de Prueba
    new_text= """    > 5.1.	Tipos de virus de influenza. Centros para el Control y la Prevención de Enfermedades.	2019.
    https://www.cdc.gov/pcd/spanish/for_authors/references_guide_es.htm. Consultado el 21 de octubre de 2021.
        > 5.2.	Konala, V. M., Adapa, S., Naramala, S., Chenna, A., Lamichhane, S., Garlapati, P. R.,	& Gayam, V. (2020). A case series of patients coinfected with
    influenza and COVID-19. Journal of investigative medicine high impact caseeports, 8, 2324709620934674.
       > 5.3.	Cruz, M. P., Santos, E., Cervantes, M. V., & Juárez, M. L. (2021). COVID- 19, una emergencia de salud pública mundial. Revista Clínica Española, 221(1), 55-61.
        > 5.4.	Benitez, J. A., Brac, E. S., Frías, L., & Aguirre, O. (2007). Virus sincitial respiratorio aspectos generales y básicos sobre la evolución clínica, factores de riesgo y tratamiento. Rev Posgrado Med, 171, 8-12.
       > 5.5.	Mostafa, H. H., Carroll, K. C., Hicken, R., Berry, G. J., Manji, R., Smith, E., & Loeffelholz, M. J. (2021). Multicenter evaluation of the cepheid xpert xpress SARS-CoV-2/Flu/VSR test. Journal of clinical microbiology, 59(3), e02955-20.
        > 5.6.	Cuadrado-Payán, E., Montagud-Marrahi, E., Torres-Elorza, M., Bodro, M., Blasco, M., Poch, E., & Piñeiro, G. J. (2020). SARS-CoV-2 and influenza virus co-infection. Lancet (London, England), 395(10236), 84. """
    modify_svg_5_2(new_text)
    
#################################################################
####################### 3 PATOLOGÍAS ############################
#################################################################
#################################################################

if len(pathologies) == 3:
    
    #Extraer patología(s)
    pato1= str(dict_patos[pathologies[0]])
    pato2= str(dict_patos[pathologies[1]])
    pato3= str(dict_patos[pathologies[2]])
    
    #################################################################   
    ###################### Creación de Portada ######################
    ##########################    P1    #############################
    #################################################################
    # INSERTAR TEXTO
    text_portada= "Generación de sistema de diagnóstico por IA de "
    # Se lee y almacena
    new_text = f'{text_portada} {pato1} y {pato2}.'
    # Ruta donde guardar el nuevo archivo SVG
    modify_svg_1(new_text)
    #################################################################   
    #################### Resumen e Introducción #####################
    #########################    P2_1    ############################
    #################################################################
    # Variables de Prueba
    new_tittle1 = 'Título patógeno X'
    new_text1 = 'Patógeno X'
    resumen = f"""El sistema de diagnóstico por IA generado por PABLO está diseñado para la identificación específica del o los patógenos causantes de {pato1} y {pato2} en ADN ó ARN, tomadas de acuerdo con los lineamientos establecidos por el InDRE (Lineamiento estandarizado para la vigilancia epidemiológica y por laboratorio de la enfermedad respiratoria viral, Octubre, 2021).
    El ARN es amplificado por RT-qPCR (si es el caso) y la detección de los blancos se realiza por medio de la lectura de fluorescencia de las sondas diseñadas de forma específica: FAM ({pato1}) y Texas Red ({pato2}). 
    El objetivo de esta prueba es servir como auxiliar en el diagnóstico, en combinación de factores clínicos y epidemiológicos.
    Agente de diagnóstico para uso in vitro."""
    modify_svg_2_1(resumen, new_tittle1, new_text1)
    #################################################################   
    ########################## Introducción #########################
    #########################    P2_2    ############################
    #################################################################
    # Variables de Prueba
    new_tittle1 = f'{pato1}'
    new_text1 = 'Patógeno X'
    new_tittle2 = f'{pato2}'
    new_text2 = 'Patógeno Y'
    modify_svg_2_2(new_tittle1, new_text1, new_tittle2, new_text2)
    #################################################################   
    ################ Características de Diagnóstico #################
    #########################    P3_2    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = 'Patógeno X-2.1'
    text_tabla2 = f' Protocolo de qPCR para {pato2}.'
    new_text2 = 'Patógeno Y-2.1'
    text_figura1 = f'Esta es la mejor región del alineamiento para {pato1}'
    modify_svg_3_2(text_tabla2, text_figura1)
    #################################################################   
    ####### Regiones de Alineamiento y Resultados Simulación ########
    #########################    P4_4    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = 'Patógeno X.04'

    text_figuraX = 'Figura 4.04'
    new_text = f'Esta es la mejor región del alineamiento para {pato2}'      
    modify_svg_4_4(text_figuraX, new_text)
    #################################################################   
    ####################### Resultados Tabla ########################
    #########################    P5_1    ############################
    #################################################################
    # Variables de Prueba
    text_tablaX = 'Tabla 5'     
    modify_svg_5_1(text_tablaX)
    #################################################################   
    ################### Referencias y Simbología ####################
    #########################    P5_2    ############################
    #################################################################
    # Variables de Prueba
    new_text= """    > 5.1.	Tipos de virus de influenza. Centros para el Control y la Prevención de Enfermedades.	2019.
    https://www.cdc.gov/pcd/spanish/for_authors/references_guide_es.htm. Consultado el 21 de octubre de 2021.
        > 5.2.	Konala, V. M., Adapa, S., Naramala, S., Chenna, A., Lamichhane, S., Garlapati, P. R.,	& Gayam, V. (2020). A case series of patients coinfected with
    influenza and COVID-19. Journal of investigative medicine high impact caseeports, 8, 2324709620934674.
       > 5.3.	Cruz, M. P., Santos, E., Cervantes, M. V., & Juárez, M. L. (2021). COVID- 19, una emergencia de salud pública mundial. Revista Clínica Española, 221(1), 55-61.
        > 5.4.	Benitez, J. A., Brac, E. S., Frías, L., & Aguirre, O. (2007). Virus sincitial respiratorio aspectos generales y básicos sobre la evolución clínica, factores de riesgo y tratamiento. Rev Posgrado Med, 171, 8-12.
       > 5.5.	Mostafa, H. H., Carroll, K. C., Hicken, R., Berry, G. J., Manji, R., Smith, E., & Loeffelholz, M. J. (2021). Multicenter evaluation of the cepheid xpert xpress SARS-CoV-2/Flu/VSR test. Journal of clinical microbiology, 59(3), e02955-20.
        > 5.6.	Cuadrado-Payán, E., Montagud-Marrahi, E., Torres-Elorza, M., Bodro, M., Blasco, M., Poch, E., & Piñeiro, G. J. (2020). SARS-CoV-2 and influenza virus co-infection. Lancet (London, England), 395(10236), 84. """
    modify_svg_5_2(new_text)
    
#################################################################
####################### 4 PATOLOGÍAS ############################
#################################################################
#################################################################

if len(pathologies) == 4:
    
    #Extraer patología(s)
    pato1= str(dict_patos[pathologies[0]])
    pato2= str(dict_patos[pathologies[1]])
    pato3= str(dict_patos[pathologies[2]])
    pato4= str(dict_patos[pathologies[3]])
    
    #################################################################   
    ###################### Creación de Portada ######################
    ##########################    P1    #############################
    #################################################################
    # INSERTAR TEXTO
    text_portada= "Generación de sistema de diagnóstico por IA de "
    # Se lee y almacena
    new_text = f'{text_portada} {pato1} y {pato2}.'
    # Ruta donde guardar el nuevo archivo SVG
    modify_svg_1(new_text)
    #################################################################   
    #################### Resumen e Introducción #####################
    #########################    P2_1    ############################
    #################################################################
    # Variables de Prueba
    new_tittle1 = 'Título patógeno X'
    new_text1 = 'Patógeno X'
    resumen = f"""El sistema de diagnóstico por IA generado por PABLO está diseñado para la identificación específica del o los patógenos causantes de {pato1} y {pato2} en ADN ó ARN, tomadas de acuerdo con los lineamientos establecidos por el InDRE (Lineamiento estandarizado para la vigilancia epidemiológica y por laboratorio de la enfermedad respiratoria viral, Octubre, 2021).
    El ARN es amplificado por RT-qPCR (si es el caso) y la detección de los blancos se realiza por medio de la lectura de fluorescencia de las sondas diseñadas de forma específica: FAM ({pato1}) y Texas Red ({pato2}). 
    El objetivo de esta prueba es servir como auxiliar en el diagnóstico, en combinación de factores clínicos y epidemiológicos.
    Agente de diagnóstico para uso in vitro."""
    modify_svg_2_1(resumen, new_tittle1, new_text1)
    #################################################################   
    ################ Características de Diagnóstico #################
    #########################    P3_1    ############################
    #################################################################
    # Variables de Prueba
    # Variables de Prueba
    new_tittle1 = 'Título patógeno X'
    new_text1 = 'Patógeno X-2'
    text_imagen= f"Estos son los mejores oligonucleótidos y sondas diseñados por Pablo para el diagnóstico de {pato1} y {pato2}."
    new_text2 = (text_imagen + new_text1)
    modify_svg_3_1(new_tittle1, new_text1, new_text2)
    #################################################################   
    ################ Características de Diagnóstico #################
    #########################    P3_2    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = 'Patógeno X-2.1'
    text_tabla2 = f' Protocolo de qPCR para {pato2}.'
    new_text2 = 'Patógeno Y-2.1'
    text_figura1 = f'Esta es la mejor región del alineamiento para {pato1}'
    modify_svg_3_2(text_tabla2, text_figura1)
    #################################################################   
    ####### Regiones de Alineamiento y Resultados Simulación ########
    #########################    P4_4    ############################
    #################################################################
    # Variables de Prueba
    new_text1 = 'Patógeno X.04'

    text_figuraX = 'Figura 4.04'
    new_text = f'Esta es la mejor región del alineamiento para {pato2}'      
    modify_svg_4_4(text_figuraX, new_text)
    #################################################################   
    ####################### Resultados Tabla ########################
    #########################    P5_1    ############################
    #################################################################
    # Variables de Prueba
    text_tablaX = 'Tabla 5'     
    modify_svg_5_1(text_tablaX)
    #################################################################   
    ################### Referencias y Simbología ####################
    #########################    P5_2    ############################
    #################################################################
    # Variables de Prueba
    new_text= """    > 5.1.	Tipos de virus de influenza. Centros para el Control y la Prevención de Enfermedades.	2019.
    https://www.cdc.gov/pcd/spanish/for_authors/references_guide_es.htm. Consultado el 21 de octubre de 2021.
        > 5.2.	Konala, V. M., Adapa, S., Naramala, S., Chenna, A., Lamichhane, S., Garlapati, P. R.,	& Gayam, V. (2020). A case series of patients coinfected with
    influenza and COVID-19. Journal of investigative medicine high impact caseeports, 8, 2324709620934674.
       > 5.3.	Cruz, M. P., Santos, E., Cervantes, M. V., & Juárez, M. L. (2021). COVID- 19, una emergencia de salud pública mundial. Revista Clínica Española, 221(1), 55-61.
        > 5.4.	Benitez, J. A., Brac, E. S., Frías, L., & Aguirre, O. (2007). Virus sincitial respiratorio aspectos generales y básicos sobre la evolución clínica, factores de riesgo y tratamiento. Rev Posgrado Med, 171, 8-12.
       > 5.5.	Mostafa, H. H., Carroll, K. C., Hicken, R., Berry, G. J., Manji, R., Smith, E., & Loeffelholz, M. J. (2021). Multicenter evaluation of the cepheid xpert xpress SARS-CoV-2/Flu/VSR test. Journal of clinical microbiology, 59(3), e02955-20.
        > 5.6.	Cuadrado-Payán, E., Montagud-Marrahi, E., Torres-Elorza, M., Bodro, M., Blasco, M., Poch, E., & Piñeiro, G. J. (2020). SARS-CoV-2 and influenza virus co-infection. Lancet (London, England), 395(10236), 84. """
    modify_svg_5_2(new_text)
'''
