# controller/GPDF.py
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
    DEFAULT_FONT = "OpenSans"

    # Target font names (buscaremos coincidencias en las fuentes registradas)
    PREFERRED_TITLE_NAME = "SairaCondensed-Regular"
    PREFERRED_BODY_NAME = "Montserrat-Regular"

    # tamaños pedidos
    TITLE_SIZE = 32
    BODY_SIZE = 12

    ALIGN_OPTIONS = {
        "Justificado": TA_JUSTIFY,
        "Izquierda": TA_LEFT,
        "Centrado": TA_CENTER,
        "Derecha": TA_RIGHT,
    }

    def __init__(self):
        # Inicializar logging y rutas
        Loger()
        self.logger = logging.getLogger('bitacora')
        self.gral = General()

        # Registrar fuentes y elegir las que usaremos
        self.register_fonts(self.FONT_DIR)
        self.title_font = self._find_registered_font(self.PREFERRED_TITLE_NAME) or self.DEFAULT_FONT
        self.body_font = self._find_registered_font(self.PREFERRED_BODY_NAME) or self.DEFAULT_FONT

        self.logger.info(f"Fuente título: {self.title_font}; fuente cuerpo: {self.body_font}")

    # ==============================================================
    # === REGISTRO Y BÚSQUEDA DE FUENTES ===
    # ==============================================================

    def register_fonts(self, font_dir):
        """Registra todas las fuentes .ttf encontradas en FONT_DIR (si existe)."""
        try:
            if not os.path.isdir(font_dir):
                self.logger.warning(f"Directorio de fuentes no existe: {font_dir}")
                return

            for font_name in os.listdir(font_dir):
                if font_name.lower().endswith(".ttf"):
                    font_path = os.path.join(font_dir, font_name)
                    try:
                        reg_name = os.path.splitext(font_name)[0]
                        pdfmetrics.registerFont(TTFont(reg_name, font_path))
                    except Exception as e:
                        # no interrumpimos la ejecución por una fuente problemática
                        self.logger.debug(f"No se pudo registrar {font_name}: {e}")
            self.logger.info("Proceso de registro de fuentes finalizado.")
        except Exception as e:
            self.logger.warning(f"Error registrando fuentes: {e}")

    def _find_registered_font(self, substring):
        """
        Busca entre las fuentes registradas una cuyo nombre contenga `substring` (case-insensitive).
        Retorna el nombre exacto de la fuente registrada o None.
        """
        substring = substring.lower()
        try:
            for fname in pdfmetrics.getRegisteredFontNames():
                if substring in fname.lower():
                    return fname
        except Exception:
            pass
        return None

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
        """Define estilos usando las fuentes seleccionadas y los tamaños requeridos."""
        return {
            "title": ParagraphStyle(name="Title", fontName=self.title_font, fontSize=self.TITLE_SIZE,
                                    leading=int(self.TITLE_SIZE * 1.1), alignment=TA_CENTER,
                                    textColor=colors.HexColor("#002F49")),
            "subtitle": ParagraphStyle(name="Subtitle", fontName=self.title_font, fontSize=18,
                                       leading=20, alignment=TA_LEFT, textColor=colors.HexColor("#333333")),
            "body": ParagraphStyle(name="Body", fontName=self.body_font, fontSize=self.BODY_SIZE,
                                   leading=int(self.BODY_SIZE * 1.4), alignment=TA_JUSTIFY, textColor=colors.black),
            "foot": ParagraphStyle(name="Foot", fontName=self.body_font, fontSize=10,
                                   leading=12, alignment=TA_RIGHT, textColor=colors.HexColor("#FFFFFF")),
        }

    # ==============================================================
    # === FUNCIONES DE INSERCIÓN DE ELEMENTOS ===
    # ==============================================================

    def agregar_texto(self, elements, texto, estilo):
        """Agrega texto formateado al documento (usa estilo ya creado)."""
        formatted_text = self.estilo_texto(texto)
        elements.append(Paragraph(formatted_text, estilo))
        elements.append(Spacer(1, 10))

    def agregar_imagen(self, elements, ruta_imagen, ancho=None, alto=None):
        """Agrega imagen (SVG o PNG/JPG) al PDF centrada y escalada."""
        if not ruta_imagen or not os.path.exists(ruta_imagen):
            self.logger.warning(f"Imagen no encontrada: {ruta_imagen}")
            return

        page_width, page_height = A4
        max_width = page_width - 3 * inch  # márgenes
        max_height = page_height - 3 * inch

        if ruta_imagen.lower().endswith(".svg"):
            drawing = svg2rlg(ruta_imagen)

            # Escalado proporcional
            scale_x = max_width / drawing.width
            scale_y = max_height / drawing.height
            scale = min(scale_x, scale_y)
            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)

            # Centrar en página
            drawing.hAlign = 'CENTER'
            elements.append(drawing)

        else:
            img = Image(ruta_imagen, width=ancho or max_width, height=alto or max_height)
            img.hAlign = 'CENTER'
            elements.append(img)

        elements.append(Spacer(1, 10))

    # ==============================================================
    # === FUNCIONES DE PLANTILLA SVG Y PIE DE PÁGINA ===
    # ==============================================================

    @staticmethod
    def add_svg_template(canvas, svg_path, foot_style):
        """Dibuja la plantilla SVG de fondo y pie de página. Añade número de página."""
        if svg_path and os.path.exists(svg_path):
            try:
                drawing = svg2rlg(svg_path)
                renderPDF.draw(drawing, canvas, 0, 0)
            except Exception:
                # no interrumpimos la generación si la plantilla falla
                pass

        canvas.setFillColor(foot_style.textColor)
        canvas.setFont(foot_style.fontName, foot_style.fontSize)
        canvas.drawString(500, 20, f"Página {canvas.getPageNumber()}")

    # ==============================================================
    # === FUNCIÓN PRINCIPAL DE GENERACIÓN ===
    # ==============================================================

    def create_pdf(self, svg_name="K0", json_name="contenido", output_name="resultado.pdf"):
        """
        Crea un PDF usando la plantilla svg (por defecto K0.svg) y un JSON con la siguiente
        estructura (ver ejemplo más abajo). El JSON se busca dentro de templates/texts/.
        """
        try:
            # 1) rutas desde la clase General
            svg_path = self.gral.get_template_path(f"{svg_name}.svg")  # templates/svgFiles/K0.svg
            # localizamos el folder de templates/svgFiles y desde ahí llegamos a templates/texts/
            svg_dir = os.path.dirname(svg_path) if svg_path else None
            texts_dir = os.path.join(os.path.dirname(svg_dir), "texts") if svg_dir else None
            json_path = os.path.join(texts_dir, f"{json_name}.json") if texts_dir else None

            # output en temp con set_file_temp
            output_path = self.gral.set_file_temp(output_name)

            self.logger.info(f"Generando PDF desde plantilla: {svg_path}; JSON: {json_path}; Salida: {output_path}")

            # 2) estilos
            estilos = self.definir_estilos()

            # 3) leer JSON de textos
            if not json_path or not os.path.exists(json_path):
                raise FileNotFoundError(f"JSON de textos no encontrado: {json_path}")

            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 4) preparar documento
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                leftMargin=0.5 * inch,
                rightMargin=0.5 * inch,
                topMargin=1 * inch,
                bottomMargin=1 * inch
            )

            elements = []

            # 5) título e introducción fijos (pueden venir en el JSON)
            titulo = data.get("titulo", "Informe General")
            introduccion = data.get("introduccion", "Documento generado automáticamente.")

            # insertar título grande (Saira Condensed 32)
            self.agregar_texto(elements, titulo, estilos["title"])
            # insertar introducción (Montserrat 12)
            self.agregar_texto(elements, introduccion, estilos["body"])

            # 6) procesar secciones: para cada sección respetamos el orden titulo -> texto -> imagen
            #    se espera que cada sección tenga: "titulo" (opcional), "texto" (string) y "imagen" (archivo svg sin ruta)
            for bloque in data.get("secciones", []):
                # título de sección (usa la fuente de título, pero tamaño menor)
                if "titulo" in bloque and bloque["titulo"]:
                    self.agregar_texto(elements, bloque["titulo"], estilos["subtitle"])

                # texto de sección (puede venir multilínea)
                if "texto" in bloque and bloque["texto"]:
                    self.agregar_texto(elements, bloque["texto"], estilos["body"])

                # imagen de sección (nombre base; la ruta la obtiene General.get_image_path)
                if "imagen" in bloque and bloque["imagen"]:
                    # obtener ruta via helper (espera nombre o nombre.ext)
                    img_candidate = bloque["imagen"]
                    try:
                        img_path = self.gral.get_image_path(img_candidate)
                        # Fallback: algunos árboles de proyecto usan 'assests' tipográfico
                        if not os.path.exists(img_path):
                            # probar carpeta raíz 'assests' si existe
                            alt_path = os.path.join(self.gral.main_path, "assests", img_candidate)
                            if os.path.exists(alt_path):
                                img_path = alt_path
                        if not os.path.exists(img_path):
                            self.logger.warning(f"Imagen no encontrada con get_image_path ni en fallback: {img_candidate}")
                        else:
                            self.agregar_imagen(elements, img_path, ancho=400)
                    except Exception as e:
                        self.logger.warning(f"No se pudo obtener imagen {img_candidate}: {e}")

            # 7) construir PDF aplicando la plantilla svg (pie con número de página)
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
