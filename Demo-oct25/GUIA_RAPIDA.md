# 🚀 Guía Rápida - DocPol Demo Backend

## ⚡ Instalación Rápida

### 1. Instalar Dependencias

```bash
# Opción A: Usar requirements simplificado (recomendado para demo)
pip install -r requirements_demo.txt

# Opción B: Si ya tienes el requirements.txt completo
pip install -r requirements.txt
```

### 2. Verificar Inkscape

```bash
# MacOS
/Applications/Inkscape.app/Contents/MacOS/inkscape --version

# Linux
/usr/bin/inkscape --version

# Windows
"C:\Program Files\Inkscape\bin\inkscape.exe" --version
```

Si Inkscape no está instalado: https://inkscape.org/release

### 3. Reemplazar Archivos

```bash
# Respaldar archivos originales (opcional)
cp __init__.py __init__.py.backup
cp main.py main.py.backup

# Copiar archivos de la versión demo
cp __init__.py.NEW __init__.py
cp main.py.NEW main.py
```

## 🎯 Uso Básico

### Ejecutar Demo Completo

```bash
python main.py
```

**Output esperado:**
```
=======================================
=======================================
 ____   ___   ____ ____   ___  _     
|  _ \ / _ \ / ___|  _ \ / _ \| |    
| | | | | | | |   | |_) | | | | |    
| |_| | |_| | |___|  __/| |_| | |___ 
|____/ \___/ \____|_|    \___/|_____|
 v.1.0.1
      DEMO - MODO BACKEND
=======================================
=======================================

==================================================
INICIANDO DEMO COMPLETO DE DOCPOL
==================================================

=== DEMO: Sistema de Logging ===
...
=== DEMO: Gestión de Rutas ===
...
=== DEMO: Modificación de SVG ===
...

==================================================
DEMO COMPLETADO
Revisa el archivo bitacora.log para más detalles
==================================================
```

### Ejecutar Demos Individuales

**Editar main.py:**

```python
def Main():
    proyecto = Docpol()
    
    # Opción 1: Solo logging
    proyecto.demo_logger()
    
    # Opción 2: Solo rutas
    # proyecto.demo_rutas()
    
    # Opción 3: Solo SVG
    # proyecto.demo_modificar_svg()
    
    # Opción 4: Todo (por defecto)
    # proyecto.ejecutar_demo_completo()
```

## 📂 Estructura de Archivos

```
DocPol_Nucleos_V1/
├── __init__.py          ← ⚡ REEMPLAZAR con versión demo
├── main.py              ← ⚡ REEMPLAZAR con versión demo
├── common/              ← ✅ Mantener sin cambios
│   ├── gral.py
│   └── logs.py
├── controller/          ← ✅ Mantener sin cambios
│   ├── control.py
│   └── modifySvg.py
├── temp/                ← Archivos generados aparecen aquí
├── templates/           ← ✅ Mantener sin cambios
│   └── svgFiles/
└── bitacora.log         ← Logs aparecen aquí
```

## 🔍 Verificar Funcionamiento

### 1. Revisar Logs

```bash
tail -f bitacora.log
```

### 2. Revisar Archivos Generados

```bash
ls -la temp/
```

Deberías ver:
- `P1-temp.svg`
- `P1-temp.pdf`
- Otros archivos SVG/PDF generados

### 3. Verificar Métodos Disponibles

```python
from __init__ import Docpol

proyecto = Docpol()
print(dir(proyecto))  # Ver todos los métodos disponibles
```

## 🐛 Solución de Problemas

### Error: "No module named 'lorem_text'"

```bash
pip install lorem-text
```

### Error: "No se encuentra Inkscape"

**Editar `controller/control.py`:**

```python
# Línea ~30
# Cambiar según tu sistema:
self.pathInkscape = "/Applications/Inkscape.app/Contents/MacOS/inkscape"  # MacOS
# self.pathInkscape = "/usr/bin/inkscape"  # Linux
# self.pathInkscape = "C:\\Program Files\\Inkscape\\bin\\inkscape.exe"  # Windows
```

### Error: "No such file or directory: templates/"

Verifica que existan las carpetas:
```bash
mkdir -p templates/svgFiles
mkdir -p templates/PDF
mkdir -p templates/texts
mkdir -p temp
```

### Los logs no se generan

```bash
# Verificar permisos
chmod 644 bitacora.log
# O crear el archivo
touch bitacora.log
```

## 📊 Qué Hace Cada Demo

### `demo_logger()`
- Genera mensajes en diferentes niveles (DEBUG, INFO, WARNING, ERROR)
- Escribe en `bitacora.log`
- Demuestra el sistema de logging

### `demo_rutas()`
- Muestra rutas de templates SVG
- Muestra rutas de imágenes
- Muestra rutas de archivos temporales
- Muestra el path principal del proyecto

### `demo_modificar_svg()`
- Lee template SVG
- Modifica texto en el SVG
- Genera texto lorem ipsum
- Exporta a PDF
- Guarda en carpeta `temp/`

## 📚 Recursos Adicionales

- `README_DEMO.md` - Documentación completa
- `COMPARACION.md` - Diferencias entre versiones
- `requirements_demo.txt` - Dependencias mínimas

## ⚙️ Configuración Avanzada

### Cambiar el Path de Inkscape Globalmente

```python
# En __init__.py, agregar después de self.control = Control():
self.control.pathInkscape = "/tu/ruta/a/inkscape"
```

### Cambiar el Nivel de Logging

```python
# En common/logs.py, línea ~25:
self.logger.setLevel(logging.DEBUG)  # Más detallado
# self.logger.setLevel(logging.INFO)   # Normal
# self.logger.setLevel(logging.WARNING)  # Solo advertencias y errores
```

### Agregar Tus Propias Demos

```python
# En __init__.py, agregar después de demo_modificar_svg():

def mi_demo_personalizado(self):
    """Mi demo personalizado"""
    self.logger.info("=== MI DEMO PERSONALIZADO ===")
    
    # Tu código aquí
    template = self.gral.get_template_path("MiPlantilla")
    self.logger.info(f"Procesando: {template}")
    
    # Más código...
    
    self.logger.info("✓ Demo personalizado completado")
```

## 🎓 Próximos Pasos

1. **Familiarízate con los demos**
   ```bash
   python main.py
   ```

2. **Revisa los logs generados**
   ```bash
   cat bitacora.log
   ```

3. **Inspecciona los archivos generados**
   ```bash
   ls -la temp/
   ```

4. **Modifica y experimenta**
   - Cambia textos en los demos
   - Crea tus propias funciones
   - Prueba con diferentes templates

5. **Lee la documentación completa**
   - `README_DEMO.md`
   - `COMPARACION.md`

## ✅ Checklist de Instalación

- [ ] Python 3.9.6+ instalado
- [ ] Inkscape instalado y en PATH
- [ ] Dependencias instaladas (`pip install -r requirements_demo.txt`)
- [ ] Archivos `__init__.py` y `main.py` reemplazados
- [ ] Carpetas `common/`, `controller/`, `temp/`, `templates/` existen
- [ ] Ejecutaste `python main.py` exitosamente
- [ ] Archivo `bitacora.log` se generó
- [ ] Archivos en `temp/` se generaron

## 🎉 ¡Listo!

Si completaste todos los pasos, tu demo de DocPol está funcionando correctamente.

**¿Preguntas o problemas?** Revisa:
- `bitacora.log` para logs detallados
- `README_DEMO.md` para documentación completa
- `COMPARACION.md` para entender las diferencias con la versión completa
