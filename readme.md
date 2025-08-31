<center><H1>Proyecto Docpol</H1></center>

```bash
📁 Docpol_Nucleos_V1/
│
├── 📁 api/                  ← APIs de sistemas
│   ├── __init__.py
│   └── api_server.py
│
├── 📁 assets/               ← Recursos visuales (logos, imágenes, etc.)
│   ├── alineamiento_plot.png
│   ├── image_prueba1.png
│   └── Tabla-interpretacion.png
│
├── 📁 common/               ← Utilidades generales y funciones compartidas
│   ├── gral.py
│   └── logs.py
│
├── 📁 controller/           ← Lógica de control y edición de SVG
│   ├── control.py
│   ├── modifySvg.py
│   └── svg_edits.py
│
├── 📁 edits/                ← Instrucciones para modificar los SVG (JSON)
│   └── ediciones_utf8.json
│
├── 📁 model/                ← Módulos para procesamiento de datos/SVG
│   └── analyze_svg.py
│
├── 📁 temp/                 ← Archivos temporales generados (PDF/SVG)
│   ├── P1-temp.svg
│   ├── P1-temp.pdf
│   └── ...
│
├── 📁 templates/            ← Plantillas base (SVG, textos, PDF)
│   ├── PDF/
│   ├── svgFiles/
│   └── texts/
│
├── 📁 uploads/              ← Archivos de los usuarios
│   
│
├── 📁 test/                 ← Scripts de prueba
│   └── test_path.py
│
├── 📁 view/                 ← Interfaz gráfica (GUI)
│   └── main_window.py
│
├── bitacora.log             ← Archivo de registro
├── main.py                  ← Punto de entrada principal del programa
├── readme.md                ← Documentación del proyecto
├── Dockerfile               ← Instrucciones para crear una imagen de Docker
├── requirements.txt         ← Lista de dependencias
└── DocPol_Nucelos_V1.py     ← Script principal (puede migrar a main.py)
```

## Guía de Instalación y Configuración

### Prerrequisitos 

* Python 3.8 o superior
* pip (gestor de paquetes de Python)
* Git (para clonar el repositorio)

## Instalación
1.- Clonar repositorio
```bash
git clone git@github.com:Galmarod/DocPol_Nucelos_V1.git
cd Docpol_Nucleos_V1
git checkout /dev/javimenba
```

2.- Configurar entorno virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Linux/macOS:
source .venv/bin/activate
# Linux/macOS con Fish
# source .venv/bin/activate.fish 
# Windows:
# .venv\Scripts\activate
```

3.- Instalar dependencias
```bash
pip install -r requirements.txt
```

4.- Verificar Instalación
```bash
python -c "import sys; print(f'Python version: {sys.version}')"
pip list
```

## Uso del proyecto
```bash
python main.py
```
## Docker run
```bash
 docker build -t mi-worker .
 docker run -p 8000:8000 -v $(pwd)/test_data:/data mi-worker 
``` 

