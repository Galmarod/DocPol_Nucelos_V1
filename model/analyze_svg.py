import json
import logging  
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Any

from common.logs import Loger



class AnalyzeSvg(object):
    def __init__(self):
        Loger()
        self.logger = logging.getLogger('bitacora')
         

    def analyze_svg_structure(self, svg_content: str) -> Dict[str, Any]:
        """
        Analiza la estructura del SVG y muestra solo los elementos óptimos para edición
        (ya sea el tspan individual o el contenedor text completo)
        """
        try:
            # Parsear el SVG y manejar namespaces
            namespaces = {
                'svg': 'http://www.w3.org/2000/svg',
                'inkscape': 'http://www.inkscape.org/namespaces/inkscape',
                'sodipodi': 'http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd'
            }
            
            for prefix, uri in namespaces.items():
                ET.register_namespace(prefix, uri)
            
            root = ET.fromstring(svg_content)
            
            resultados = {
                "elementos_editables": {
                    "textos": [],
                    "imagenes": []
                },
                "elementos_decorativos": [],
                "metadata": {
                    "dimensiones": root.get('width', '') + ' × ' + root.get('height', ''),
                    "viewBox": root.get('viewBox', '')
                }
            }
            
            # Analizar y obtener solo los elementos óptimos para edición
            textos_editables = self.get_optimal_edit_elements(root, namespaces)
            resultados["elementos_editables"]["textos"] = textos_editables
            
            # Placeholders de imagen
            placeholders_imagen = self.analyze_image_placeholders(root, namespaces)
            resultados["elementos_editables"]["imagenes"] = placeholders_imagen
            
            return resultados
            
        except Exception as e:
            return {"error": f"Error al analizar SVG: {str(e)}"}

    def get_optimal_edit_elements(self, root, ns) -> List[Dict[str, Any]]:
        """
        Retorna solo los elementos óptimos para edición:
        - Para estructuras simples: el tspan individual
        - Para estructuras complejas: el contenedor text completo
        """
        elementos_optimos = []
        text_elements_processed = set()
        
        # Buscar todos los elementos text
        text_elements = root.findall('.//{http://www.w3.org/2000/svg}text')
        if not text_elements:
            text_elements = root.findall('.//text')
        
        for text_elem in text_elements:
            text_id = text_elem.get('id', '')
            
            # Saltar si ya procesamos este text (para evitar duplicados)
            if text_id in text_elements_processed:
                continue
                
            text_elements_processed.add(text_id)
            style = text_elem.get('style', '')
            
            # Analizar estructura jerárquica completa
            estructura = self.analyze_text_structure(text_elem, ns)
            
            # Buscar tspans editables dentro de este text
            tspans_editables = []
            tspans = text_elem.findall('.//{http://www.w3.org/2000/svg}tspan')
            if not tspans:
                tspans = text_elem.findall('.//tspan')
            
            for tspan in tspans:
                tspan_id = tspan.get('id', '')
                contenido = self.get_tspan_content(tspan)
                
                if self.is_editable_text(tspan, text_elem, contenido, style):
                    tspans_editables.append({
                        'id': tspan_id,
                        'contenido': contenido,
                        'elemento': tspan
                    })
            
            # Decidir qué mostrar basado en la complejidad
            if not tspans_editables:
                continue
                
            if self.should_show_text_container(estructura, len(tspans_editables)):
                # Mostrar el CONTENEDOR TEXT completo (para casos complejos)
                elemento_info = self.create_text_container_info(text_elem, estructura, tspans_editables)
                elementos_optimos.append(elemento_info)
            else:
                # Mostrar los TSPANS individuales (para casos simples)
                for tspan_info in tspans_editables:
                    elemento_info = self.create_tspan_info(tspan_info, text_elem, estructura)
                    elementos_optimos.append(elemento_info)
        
        return elementos_optimos

    def should_show_text_container(self, estructura, num_tspans_editables) -> bool:
        """
        Decide si mostrar el contenedor text completo en lugar de los tspans individuales
        """
        # Reglas para preferir el contenedor completo
        if estructura['complejidad'] in ["muy_alta", "alta"]:
            return True
            
        if estructura['total_tspans'] > 3 and num_tspans_editables > 1:
            return True
            
        if estructura['max_profundidad'] >= 2:
            return True
            
        if estructura['tiene_dx_complejo']:
            return True
            
        return False

    def create_text_container_info(self, text_elem, estructura, tspans_editables) -> Dict[str, Any]:
        """Crea la información para un contenedor text completo"""
        style = text_elem.get('style', '')
        contenido_ejemplo = tspans_editables[0]['contenido'] if tspans_editables else ""
        
        return {
            "id": text_elem.get('id', ''),
            "tipo": "contenedor_text",
            "tipo_contenido": self.determine_text_type(contenido_ejemplo, style),
            "contenido_actual": "VARIOS_TSPANS_ANIDADOS",
            "mejor_nivel_edicion": "text_container",
            "total_tspans_hijos": estructura['total_tspans'],
            "tspans_editables": [t['id'] for t in tspans_editables],
            "complejidad_jerarquia": estructura['complejidad'],
            "niveles_anidacion": estructura['max_profundidad'],
            "tiene_dx_complejo": estructura['tiene_dx_complejo'],
            "estilo": self.extract_style_info(style),
            "posicion": self.estimate_position(text_elem),
            "recomendacion": "Editar este elemento text completo en lugar de los tspans individuales"
        }

    def create_tspan_info(self, tspan_info, text_elem, estructura) -> Dict[str, Any]:
        """Crea la información para un tspan individual"""
        tspan = tspan_info['elemento']
        style = tspan.get('style', '') or text_elem.get('style', '')
        
        return {
            "id": tspan_info['id'],
            "tipo": "tspan_individual",
            "tipo_contenido": self.determine_text_type(tspan_info['contenido'], style),
            "contenido_actual": tspan_info['contenido'],
            "mejor_nivel_edicion": "tspan_directo",
            "elemento_padre": text_elem.get('id', ''),
            "complejidad_jerarquia": estructura['complejidad'],
            "estilo": self.extract_style_info(style),
            "posicion": self.estimate_position(text_elem),
            "recomendacion": "Editar este tspan directamente"
        }

    def analyze_text_structure(self, text_elem, ns) -> Dict[str, Any]:
        """Analiza la estructura jerárquica de un elemento text"""
        tspans = text_elem.findall('.//{http://www.w3.org/2000/svg}tspan')
        if not tspans:
            tspans = text_elem.findall('.//tspan')
        
        max_profundidad = 0
        tiene_dx_complejo = False
        
        for tspan in tspans:
            profundidad = self.calculate_nesting_depth(tspan)
            max_profundidad = max(max_profundidad, profundidad)
            
            dx = tspan.get('dx', '')
            if dx and len(dx.split()) > 3:
                tiene_dx_complejo = True
        
        complejidad = self.calculate_complexity_score(text_elem, tspans, max_profundidad, tiene_dx_complejo)
        
        return {
            'total_tspans': len(tspans),
            'max_profundidad': max_profundidad,
            'complejidad': complejidad,
            'tiene_dx_complejo': tiene_dx_complejo
        }

    def calculate_nesting_depth(self, element, current_depth=0) -> int:
        """Calcula la profundidad de anidación"""
        max_depth = current_depth
        for child in element:
            if child.tag.endswith('tspan') or '{http://www.w3.org/2000/svg}tspan' in child.tag:
                child_depth = self.calculate_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, child_depth)
        return max_depth

    def calculate_complexity_score(self, text_elem, tspans, max_depth, tiene_dx_complejo) -> str:
        """Calcula score de complejidad"""
        score = 0
        
        if len(tspans) > 10: score += 3
        elif len(tspans) > 5: score += 2
        elif len(tspans) > 1: score += 1
        
        if max_depth >= 3: score += 3
        elif max_depth == 2: score += 2
        elif max_depth == 1: score += 1
        
        if tiene_dx_complejo: score += 2
        
        if score >= 5: return "muy_alta"
        elif score >= 3: return "alta"
        elif score >= 1: return "media"
        else: return "baja"

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
        """Determina el tipo de texto basado en contenido y estilo"""
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
        """Extrae información importante del estilo CSS"""
        return {
            "font_size": self.extract_style_value(style, 'font-size'),
            "font_weight": self.extract_style_value(style, 'font-weight'),
            "fill": self.extract_style_value(style, 'fill'),
            "text_anchor": self.extract_style_value(style, 'text-anchor')
        }

    def extract_style_value(self, style: str, property_name: str) -> str:
        """Extrae el valor de una propiedad CSS del estilo"""
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
        """Identifica rectángulos que son placeholders para imágenes"""
        placeholders = []
        
        rects = root.findall('.//{http://www.w3.org/2000/svg}rect')
        if not rects:
            rects = root.findall('.//rect')
        
        for rect in rects:
            rect_id = rect.get('id', '')
            style = rect.get('style', '')
            fill_color = self.extract_style_value(style, 'fill')
            
            # Criterios para identificar placeholders de imagen
            is_placeholder = (
                fill_color in ['#000000', '#000', '#cccccc', '#ccc', '#eeeeee'] or
                'placeholder' in rect_id.lower() or 'image' in rect_id.lower()
            )
            
            if is_placeholder:
                placeholders.append({
                    "id": rect_id,
                    "tipo": "placeholder_imagen",
                    "dimensiones": f"{rect.get('width', '')} × {rect.get('height', '')}",
                    "posicion": f"{rect.get('x', '')}, {rect.get('y', '')}",
                    "color_relleno": fill_color,
                    "estilo": style
                })
        
        return placeholders

    def run_analyze_svg(self, svgPath, jsonPath):
        # Uso del script
        try:
            with open(f'{svgPath}', 'r', encoding='utf-8') as f:
                svg_content = f.read()

            resultado = self.analyze_svg_structure(svg_content)

            with open(f'{jsonPath}', 'w', encoding='utf-8') as f:
                json.dump(resultado, f, indent=2, ensure_ascii=False)

            self.logger.info('✅ Análisis optimizado completado.')
            self.logger.info('📊 Solo elementos óptimos para edición en analisis_optimizado.json')
            
            # Mostrar resumen
            if "error" not in resultado:
                textos = len(resultado.get("elementos_editables", {}).get("textos", []))
                imagenes = len(resultado.get("elementos_editables", {}).get("imagenes", []))
                self.logger.info(f'\n📊 RESUMEN:')
                self.logger.info(f'   Elementos texto editables: {textos}')
                self.logger.info(f'   Placeholders de imagen: {imagenes}')
            
        except FileNotFoundError:
            self.logger.error("❌ Error: No se encontró el archivo 'certificadoSep.svg'")
        except Exception as e:
            self.logger.error(f'❌ Error: {str(e)}')
