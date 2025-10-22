# DocPol - Versión Demo Backend

## 📋 Descripción

Esta es una versión simplificada de DocPol diseñada específicamente para demostrar las funcionalidades principales del backend sin necesidad de API o interfaz gráfica.

## ✨ Características Incluidas

### 1. **Sistema de Logging** ✅
- Registro completo en `bitacora.log`
- Diferentes niveles: DEBUG, INFO, WARNING, ERROR
- Rotación automática de archivos de log

### 2. **Clase General** ✅
- Gestión de rutas del proyecto
- Acceso a templates SVG
- Manejo de archivos temporales
- Gestión de assets/imágenes

### 3. **Modificación de SVG** ✅
- Edición de archivos SVG
- Exportación a PDF
- Procesamiento de plantillas

## 🗂️ Estructura del Proyecto

```
DocPol_Nucleos_V1/
├── common/              ← Utilidades (gral.py, logs.py)
├── controller/          ← Lógica de control (control.py, modifySvg.py)
├── temp/                ← Archivos temporales generados
├── templates/           ← Plantillas SVG, PDF, textos
├── __init__.py          ← Clase principal Docpol (SIMPLIFICADA)
├── main.py              ← Punto de entrada (SIMPLIFICADO)
└── bitacora.log         ← Archivo de registro
```

## 🚀 Uso

### Ejecutar Demo Completo

```bash
python main.py
```

Esto ejecutará todas las demostraciones en secuencia:
1. Demo del sistema de logging
2. Demo de gestión de rutas
3. Demo de modificación de SVG

### Ejecutar Demos Individuales

Edita `main.py` y descomenta las líneas específicas:

```python
def Main():
    proyecto = Docpol()
    
    # Ejecutar demos individuales:
    proyecto.demo_logger()          # Solo logging
    proyecto.demo_rutas()           # Solo rutas
    proyecto.demo_modificar_svg()   # Solo SVG
```

## 📝 Métodos Disponibles

### `Docpol.demo_logger()`
Demuestra el funcionamiento del sistema de logging con diferentes niveles de mensajes.

### `Docpol.demo_rutas()`
Muestra cómo la clase General gestiona las rutas de:
- Templates SVG
- Imágenes
- Archivos temporales
- Path principal del proyecto

### `Docpol.demo_modificar_svg()`
Demuestra la modificación de archivos SVG y su exportación a PDF.

### `Docpol.ejecutar_demo_completo()`
Ejecuta todas las demostraciones anteriores en secuencia.

## 📊 Salida Esperada

Al ejecutar el demo, verás:
1. **En consola**: Mensajes INFO principales
2. **En bitacora.log**: Registro completo detallado de todas las operaciones
3. **En temp/**: Archivos SVG y PDF generados

## 🔧 Diferencias con la Versión Completa

### ❌ Eliminado (no necesario para demo):
- API Server (`APIServer`, `uvicorn`)
- Interfaz gráfica (`MainWindow`, `PySide6`)
- Streamlit
- Threading para API
- Queue para procesamiento asíncrono

### ✅ Mantenido (esencial para funcionalidad):
- Sistema de logging completo
- Clase General para gestión de rutas
- Controller para SVG y PDF
- ModifySvg para ediciones
- Carpetas: common, controller, temp, templates

## 💡 Casos de Uso

Esta versión demo es perfecta para:
- Probar funcionalidades básicas del backend
- Desarrollar nuevas características sin complejidad de API/GUI
- Debugging de procesamiento de SVG
- Validar el sistema de logging
- Entender el flujo de gestión de archivos

## 📌 Notas Importantes

1. Asegúrate de tener Inkscape instalado para exportar PDFs
2. Verifica que existan las carpetas `common/`, `controller/`, `temp/` y `templates/`
3. El logger se inicializa automáticamente al crear una instancia de `Docpol`
4. Todos los archivos generados se guardan en la carpeta `temp/`

## 🐛 Troubleshooting

### "No se encuentra Inkscape"
Edita `controller/control.py` y verifica la ruta de Inkscape:
```python
self.pathInkscape = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # MacOS
# self.pathInkscape = "/usr/bin/inkscape"  # Linux/Docker
```

### "No se encuentra el template"
Verifica que existan los archivos SVG en `templates/svgFiles/`

### "Error al escribir en bitacora.log"
Verifica permisos de escritura en el directorio del proyecto

## 🔄 Migración a Versión Completa

Para volver a la versión completa con API y GUI:
1. Restaura las importaciones eliminadas en `__init__.py`
2. Descomenta las líneas de `APIServer` y `MainWindow`
3. Restaura el `main.py` original
