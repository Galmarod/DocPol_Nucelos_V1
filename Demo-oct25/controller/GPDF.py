#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__     = "Guillermo Almanza Rodríguez"
__copyright__  = "Copyright 2025, RevelCode"
__credits__    = ["galmarod"]
__license__    = "GPL"
__version__    = "1.0.0"
__maintainer__ = "Guillermo Almanza Rodríguez"
__email__      = "galmarod@gmail.com"
__status__     = "Development"
__date__       = "Oct-2025"

import os
import re
import json
import logging
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from common.gral import General
from common.logs import Loger


class GPDF:
    # ==============================================================
    # === CONFIGURACIONES BASE ===
    # ==============================================================

    FONT_DIR = "/Users/galmarod/Library/Fonts"
    DEFAULT_FONT = "Helvetica"

    ALIGN_OPTIONS = {
        "Justificado": TA_JUSTIFY,
        "Izquierda": TA_LEFT,
        "Centrado": TA_CENTER,
        "Derecha": TA_RIGHT,
    }

    def __init__(self):
        # Inicializar logging
        Loger()
        self.logger = logging.getLogger('bitacora')

        # Inicializar rutas
        self.gral = General()

        # Registrar fuentes al iniciar
        self.register_fonts(self.FONT_DIR)

    # ==============================================================
    # === REGISTRO DE FUENTES ===
    # ==============================================================

    def register_fonts(self, font_dir):
        """Registra todas las fuentes TrueType en el directorio de fuentes."""
        try:
            for font_name in os.listdir(font_dir):
                if font_name.endswith(".ttf"):
                    font_path = os.path.join(font_dir, font_name)
                    try:
                        pdfmetrics.registerFont(
                            TTFont(os.path.splitext(font_name)[0], font_path)
                        )
                    except Exception:
                        pass
            self.logger.info("Fuentes registradas correctamente.")
        except Exception as e:
            self.logger.warning(f"No se pudieron registrar las fuentes: {e}")

    # ==============================================================
    # === FUNCIONES DE ESTILO Y FORMATO ===
    # ==============================================================

    @staticmethod
    def estilo_texto(texto):
        """Convierte marcadores *texto*, -texto-, _texto_ en <b>, <i>, <u>."""
        texto = re.sub(r'\*(.*?)\*', r'<b>\1</b>', texto)
        texto = re.sub(r'-(.*?)-', r'<i>\1</i>', texto)
        texto = re.sub(r'_(.*?)_', r'<u>\1</u>', texto)
        return texto

    def definir_estilos(self):
        """Define estilos básicos del documento."""
        return {
            "title": ParagraphStyle(name="Title", fontName=self.DEFAULT_FONT, fontSize=22,
                                    leading=26, alignment=TA_CENTER, textColor=colors.HexColor("#002F49")),
            "subtitle": ParagraphStyle(name="Subtitle", fontName=self.DEFAULT_FONT, fontSize=16,
                                       leading=20, alignment=TA_LEFT, textColor=colors.HexColor("#333333")),
            "body": ParagraphStyle(name="Body", fontName=self.DEFAULT_FONT, fontSize=12,
                                   leading=16, alignment=TA_JUSTIFY, textColor=colors.black),
            "foot": ParagraphStyle(name="Foot", fontName=self.DEFAULT_FONT, fontSize=10,
                                   leading=12, alignment=TA_RIGHT, textColor=colors.HexColor("#444444")),
        }

    # ==============================================================
    # === FUNCIONES DE INSERCIÓN DE ELEMENTOS ===
    # ==============================================================

    def agregar_texto(self, elements, texto, estilo):
        """Agrega texto formateado al documento."""
        formatted_text = self.estilo_texto(texto)
        elements.append(Paragraph(formatted_text, estilo))
        elements.append(Spacer(1, 10))

    def agregar_imagen(self, elements, ruta_imagen, ancho=None, alto=None):
        """Agrega imagen (PNG o SVG) al PDF."""
        if ruta_imagen.lower().endswith(".svg"):
            drawing = svg2rlg(ruta_imagen)
            elements.append(drawing)
        else:
            img = Image(ruta_imagen, width=ancho or 400, height=alto or 300)
            elements.append(img)
        elements.append(Spacer(1, 10))

    # ==============================================================
    # === FUNCIONES DE PLANTILLA SVG Y PIE DE PÁGINA ===
    # ==============================================================

    @staticmethod
    def add_svg_template(canvas, svg_path, foot_style):
        """Dibuja la plantilla SVG de fondo y pie de página."""
        if svg_path and os.path.exists(svg_path):
            drawing = svg2rlg(svg_path)
            renderPDF.draw(drawing, canvas, 0, 0)

        canvas.setFillColor(foot_style.textColor)
        canvas.setFont(foot_style.fontName, foot_style.fontSize)
        canvas.drawString(500, 20, f"Página {canvas.getPageNumber()}")

    # ==============================================================
    # === FUNCIÓN PRINCIPAL DE GENERACIÓN ===
    # ==============================================================

    def create_pdf(self, svg_name, json_name, output_name="resultado.pdf"):
        """
        Crea un PDF a partir de una plantilla SVG y un archivo JSON estructurado.
        """
        try:
            svg_path = self.gral.get_template_path(f"{svg_name}.svg")
            json_path = self.gral.get_file_temp(f"{json_name}.json")
            output_path = self.gral.set_file_temp(output_name)

            self.logger.info(f"Generando PDF desde {svg_path} con datos {json_path}")

            estilos = self.definir_estilos()

            # Cargar JSON
            with open(json_path, "r") as f:
                data = json.load(f)

            titulo = data.get("titulo", "Informe General")
            introduccion = data.get("introduccion", "Documento generado automáticamente.")

            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                leftMargin=1 * inch,
                rightMargin=1 * inch,
                topMargin=1 * inch,
                bottomMargin=1 * inch
            )

            elements = []
            
            # Agregar título e introducción
            self.agregar_texto(elements, titulo, estilos["title"])
            self.agregar_texto(elements, introduccion, estilos["body"])

            # Procesar secciones
            for bloque in data.get("secciones", []):
                if "titulo" in bloque:
                    self.agregar_texto(elements, bloque["titulo"], estilos["subtitle"])
                for item in bloque.get("contenido", []):
                    if item["tipo"] == "texto":
                        self.agregar_texto(elements, item["valor"], estilos["body"])
                    elif item["tipo"] == "imagen":
                        img_path = self.gral.get_image_path(item["ruta"])
                        self.agregar_imagen(elements, img_path, ancho=400)

            # Construir PDF con plantilla
            doc.build(
                elements,
                onFirstPage=lambda c, d: self.add_svg_template(c, svg_path, estilos["foot"]),
                onLaterPages=lambda c, d: self.add_svg_template(c, svg_path, estilos["foot"]),
            )

            self.logger.info(f"✅ PDF generado correctamente: {output_path}")
            return output_path

        except Exception as e:
            self.logger.error(f"❌ Error al generar PDF: {e}")
            raise
