# svg_edits.py - Documentación Detallada
## Estructura de Clase

```python
class SvgEdits:
    def __init__(self):
        Loger()
        self.logger = logging.getLogger('bitacora')
    
    # ==================== FUNCIONES DE ANÁLISIS SVG ====================
    def analyze_svg_structure(self, svg_content: str) -> Dict[str, Any]
    def analyze_text_elements(self, root, ns) -> List[Dict[str, Any]]
    def get_tspan_content(self, tspan) -> str
    def is_editable_text(self, tspan, text_elem, contenido, style) -> bool
    def determine_text_type(self, contenido: str, style: str) -> str
    def extract_style_info(self, style: str) -> Dict[str, str]
    def extract_style_value(self, style: str, property_name: str) -> str
    def estimate_position(self, element) -> str
    def analyze_image_placeholders(self, root, ns) -> List[Dict[str, Any]]
    
    # ==================== FUNCIONES DE EDICIÓN SVG ====================
    def reemplazar_texto_svg(self, svg_content: str, elemento_id: str, nuevo_texto: str) -> str
    def find_element_by_id(self, root, element_id: str)
    def procesar_instrucciones(self, archivo_instrucciones, archivo_svg)
    def analizar_svg_desde_instrucciones(self, archivo_instrucciones, svgPath)
    def restore_from_backup(self, svg_path: Path)
    def runSvgEdits(self, jsonPath, svgPath)
```
## Funciones Principales

### analyze_svg_structure(svg_content: str)

Propósito: Analiza la estructura básica del SVG para identificar elementos editabales.

Retorna:
```json
{
  "elementos_editables": {
    "textos": [],
    "imagenes": []
  },
  "elementos_decorativos": [],
  "metadata": {
    "dimensiones": "width × height",
    "viewBox": "viewBox value"
  }
}
```

### reemplazar_texto_svg(svg_content, elemento_id, nuevo_texto)

Proósito: Reemplaza texto en ekementos SVG mantenuendo atributos.
Flujo:
1. Parsea el SVG
2. Encuentra elemento por ID
3. Reemplaza texto y limpia hijos
4. Retorna SVG modificado

### procesar_instrucciones(archivo_instrucciones, archivo_svg)

Propósito: procesa JSON de instrucciones y aplica ediciones al SVG.
Características:

* ✅ Crea backup automático (.svg.bak)
* ✅ Aplica múltiples ediciones
* ✅ Genera reporte de ejecución
* ✅ Manejo de errores con logging

