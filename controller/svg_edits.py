
import json
import shutil
import xml.etree.ElementTree as ET
import re
import logging
from typing import Dict, List, Any
from pathlib import Path

from common.logs import Loger
class SvgEdits:
    def __init__(self):
        Loger()
        self.logger = logging.getLogger('bitacora')
    # ==================== FUNCIONES DE ANÁLISIS SVG ====================
    def analyze_svg_structure(self, svg_content: str) -> Dict[str, Any]:
        """Analiza la estructura del SVG para identificar elementos editables"""
        try:
            namespaces = {
                'svg': 'http://www.w3.org/2000/svg',
                'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
                'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'
            }
            
            for prefix, uri in namespaces.items():
                ET.register_namespace(prefix, uri)
            
            root = ET.fromstring(svg_content)
            
            resultados = {
                "elementos_editables": {"textos": [], "imagenes": []},
                "elementos_decorativos": [],
                "metadata": {
                    "dimensiones": root.get('width', '') + ' × ' + root.get('height', ''),
                    "viewBox": root.get('viewBox', '')
                }
            }
            
            textos_editables = self.analyze_text_elements(root, namespaces)
            resultados["elementos_editables"]["textos"] = textos_editables
            
            placeholders_imagen = self.analyze_image_placeholders(root, namespaces)
            resultados["elementos_editables"]["imagenes"] = placeholders_imagen
            
            return resultados
            
        except Exception as e:
            return {"error": f"Error al analizar SVG: {str(e)}"}

    def analyze_text_elements(self, root, ns) -> List[Dict[str, Any]]:
        """Analiza elementos de texto editables"""
        textos_editables = []
        
        text_elements = root.findall('.//{http://www.w3.org/2000/svg}text')
        if not text_elements:
            text_elements = root.findall('.//text')
        
        for text_elem in text_elements:
            text_id = text_elem.get('id', '')
            style = text_elem.get('style', '')
            
            tspans = text_elem.findall('.//{http://www.w3.org/2000/svg}tspan')
            if not tspans:
                tspans = text_elem.findall('.//tspan')
            
            for tspan in tspans:
                tspan_id = tspan.get('id', '')
                contenido = self.get_tspan_content(tspan)
                
                if self.is_editable_text(tspan, text_elem, contenido, style):
                    textos_editables.append({
                        "id": tspan_id or f"tspan_in_{text_id}",
                        "tipo": self.determine_text_type(contenido, style),
                        "contenido_actual": contenido,
                        "estilo": self.extract_style_info(style),
                        "posicion": self.estimate_position(text_elem),
                        "elemento_padre": text_id
                    })
        
        return textos_editables

    def get_tspan_content(self, tspan) -> str:
        """Obtiene el contenido completo de un tspan"""
        contenido = tspan.text or ""
        for child in tspan:
            if child.tag.endswith('tspan') or '{http://www.w3.org/2000/svg}tspan' in child.tag:
                contenido += self.get_tspan_content(child)
            elif child.text:
                contenido += child.text
            elif child.tail:
                contenido += child.tail
        return contenido.strip()

    def is_editable_text(self, tspan, text_elem, contenido, style) -> bool:
        """Determina si un texto es editable"""
        if not contenido or contenido.startswith(('##', '{{', '%%')):
            return True
        if 'font-size:15.9996px' in style or 'font-size:26.6667px' in style:
            return True
        if 'shape-inside:url(' in (text_elem.get('style', '') + style):
            return True
        
        placeholder_patterns = [r'titulo', r'título', r'texto', r'content', r'placeholder']
        contenido_lower = contenido.lower()
        if any(pattern in contenido_lower for pattern in placeholder_patterns):
            return True
        
        if len(contenido) < 5 and contenido.isalpha():
            return True
        
        return False

    def determine_text_type(self, contenido: str, style: str) -> str:
        """Determina el tipo de texto"""
        style_lower = style.lower()
        contenido_lower = contenido.lower() if contenido else ""
        
        if 'font-size:26.6667px' in style_lower or 'font-weight:bold' in style_lower:
            if any(word in contenido_lower for word in ['titulo', 'título', 'title']):
                return "titulo"
            return "subtitulo"
        
        if 'font-size:15.9996px' in style_lower:
            return "cuerpo"
        
        if 'tabla' in contenido_lower or 'table' in contenido_lower:
            return "leyenda_tabla"
        
        return "texto"

    def extract_style_info(self, style: str) -> Dict[str, str]:
        """Extrae información del estilo CSS"""
        return {
            "font_size": self.extract_style_value(style, 'font-size'),
            "font_weight": self.extract_style_value(style, 'font-weight'),
            "fill": self.extract_style_value(style, 'fill')
        }

    def extract_style_value(self, style: str, property_name: str) -> str:
        """Extrae el valor de una propiedad CSS"""
        match = re.search(f'{property_name}:(#[0-9a-fA-F]+|[^;]+)', style, re.IGNORECASE)
        return match.group(1).strip() if match else ''

    def estimate_position(self, element) -> str:
        """Estima la posición basada en coordenadas"""
        try:
            x = float(element.get('x', '0'))
            y = float(element.get('y', '0'))
            if y < 50: return "superior"
            if y > 200: return "inferior"
            return "central"
        except:
            return "desconocida"

    def analyze_image_placeholders(self, root, ns) -> List[Dict[str, Any]]:
        """Identifica placeholders de imagen"""
        placeholders = []
        rects = root.findall('.//{http://www.w3.org/2000/svg}rect')
        if not rects:
            rects = root.findall('.//rect')
        
        for rect in rects:
            rect_id = rect.get('id', '')
            style = rect.get('style', '')
            fill_color = self.extract_style_value(style, 'fill')
            
            if fill_color in ['#000000', '#000', '#cccccc', '#ccc', '#eeeeee']:
                placeholders.append({
                    "id": rect_id,
                    "tipo": "placeholder_imagen",
                    "dimensiones": f"{rect.get('width', '')} × {rect.get('height', '')}",
                    "posicion": f"{rect.get('x', '')}, {rect.get('y', '')}",
                    "color_relleno": fill_color
                })
        
        return placeholders

    # ==================== FUNCIONES DE EDICIÓN SVG ====================
    def reemplazar_texto_svg(self, svg_content: str, elemento_id: str, nuevo_texto: str) -> str:
        """Reemplaza texto en un SVG manteniendo todos los atributos"""
        try:
            namespaces = {
                'svg': 'http://www.w3.org/2000/svg',
                'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
                'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'
            }
            
            for prefix, uri in namespaces.items():
                ET.register_namespace(prefix, uri)
            
            root = ET.fromstring(svg_content)
            elemento = self.find_element_by_id(root, elemento_id)
            
            if elemento is None:
                self.logger.warning(f"⚠️  Elemento {elemento_id} no encontrado")
                return svg_content
            
            # Reemplazar texto manteniendo atributos
            elemento.text = nuevo_texto
            # Limpiar hijos para mantener simple
            for child in list(elemento):
                elemento.remove(child)
            
            return ET.tostring(root, encoding='unicode', method='xml')
            
        except Exception as e:
            self.logger.error(f"❌ Error editando {elemento_id}: {str(e)}")
            return svg_content

    def find_element_by_id(self, root, element_id: str):
        """Encuentra un elemento por ID"""
        elementos = root.findall(f'.//*[@id="{element_id}"]')
        if elementos:
            return elementos[0]
        
        elementos = root.findall(f'.//{{http://www.w3.org/2000/svg}}*[@id="{element_id}"]')
        if elementos:
            return elementos[0]
        
        return None

    def procesar_instrucciones(self, archivo_instrucciones, archivo_svg):
        """Procesa el archivo de instrucciones JSON y aplica las ediciones"""
        try:
            # Leer instrucciones JSON
            with open(archivo_instrucciones, 'r', encoding='utf-8') as f:
                instrucciones = json.load(f)
            
            # Leer SVG
            with open(archivo_svg, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            svg_path = Path(archivo_svg)   
            backup_path = svg_path.with_suffix(".svg.bak")
            if not backup_path.exists():
                shutil.copy(svg_path, backup_path)
                self.logger.info(f"Copia de seguridad creada: {backup_path.name}")
            # Aplicar TODAS las ediciones
            ediciones = instrucciones.get("ediciones", {})
            total_ediciones = len(ediciones)
            ediciones_aplicadas = 0
            
            self.logger.info(f"📋 Procesando {total_ediciones} ediciones...")
            
            for elemento_id, nuevo_texto in ediciones.items():
                self.logger.info(f"   Editing {elemento_id}...")
                svg_content = self.reemplazar_texto_svg(svg_content, elemento_id, nuevo_texto)
                ediciones_aplicadas += 1
            
            # Guardar resultado
            #archivo_salida = archivo_svg.replace('.svg', '_editado.svg')
            with open(archivo_svg, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            # Generar reporte
            usuario = instrucciones.get("User", {}).get("nameUser", "Desconocido")
            fecha = instrucciones.get("Svginformation", {}).get("lastmodificacion", "Desconocida")
            
            self.logger.info(f"\n✅ PROCESAMIENTO COMPLETADO")
            self.logger.info(f"   👤 Usuario: {usuario}")
            self.logger.info(f"   📅 Fecha: {fecha}")
            self.logger.info(f"   📊 Ediciones: {ediciones_aplicadas}/{total_ediciones} aplicadas")
            self.logger.info(f"   💾 Guardado como: {archivo_svg}")
            
            return {
                "estado": "éxito",
                "ediciones_aplicadas": ediciones_aplicadas,
                "total_ediciones": total_ediciones,
                "archivo_salida": archivo_svg
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error procesando instrucciones: {str(e)}")
            return {"estado": "error", "mensaje": str(e)}

    def analizar_svg_desde_instrucciones(self, archivo_instrucciones, svgPath):
        """Analiza el SVG especificado en las instrucciones"""
        try:
            with open(archivo_instrucciones, 'r', encoding='utf-8') as f:
                instrucciones = json.load(f)
            
            nombre_svg = instrucciones.get("Svginformation", {}).get("nameFileSvg")
            if not nombre_svg:
                raise ValueError("No se especificó archivo SVG en las instrucciones")
            
            with open(svgPath, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            resultado = self.analyze_svg_structure(svg_content)
            
            # Guardar análisis
            archivo_analisis = nombre_svg.replace('.svg', '_analisis.json')
            with open(archivo_analisis, 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"📊 Análisis guardado en: {archivo_analisis}")
            return resultado
            
        except Exception as e:
            self.logger.error(f"❌ Error analizando SVG: {str(e)}")
            return {"error": str(e)}

    def restore_from_backup(self, svg_path: Path):
        backup_path = svg_path.with_suffix(".svg.bak")
        if backup_path.exists():
            shutil.copy(backup_path, svg_path)
            self.logger.info("✅ Archivo restaurado desde copia de seguridad.")
            return True
        else:
            self.logger.warning("⚠️ No se encontró una copia de seguridad.")
            return False


    def runSvgEdits(self, jsonPath, svgPath):
        self.procesar_instrucciones(jsonPath, svgPath)

