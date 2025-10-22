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

import subprocess
import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QPushButton, QFileDialog, QLabel, QApplication, QVBoxLayout, QWidget,
    QMessageBox
)
from PySide6.QtCore import Qt, QUrl, QMimeData
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QAction, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

from controller.svg_edits import apply_svg_edits, restore_from_backup
from common.gral import General


class CustomPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS] {message}")


class MainWindow(QMainWindow):
    def __init__(self, svg_path=None):
        super().__init__()
        self.gral = General()
        self.setWindowTitle("DocPol editor")
        self.resize(700, 800)
        
        # Set window icon
        logo_path = str(Path(__file__).parent.parent / "assets" / "material" / "icon_w.ico")
        self.setWindowIcon(QIcon(logo_path))
        
        # Habilitar drag & drop
        self.setAcceptDrops(True)
        
        self.svg_path = Path(svg_path) if svg_path else None
        self.png_path = self.svg_path.with_suffix(".png") if self.svg_path else None
        self.custom_json_path = None  # Para almacenar la ruta del JSON personalizado

        # Layout principal
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Toolbar
        self.toolbar = QToolBar("Herramientas")
        self.addToolBar(self.toolbar)
        self._add_toolbar_buttons()
        
        # QLabel para mostrar PNG o mensaje inicial
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # QWebEngine invisible para correr JS
        self.browser = QWebEngineView()
        self.browser.setPage(CustomPage(self.browser))
        self.browser.hide()  # No mostrar

        if self.svg_path and self.svg_path.exists():
            self._load_svg(self.svg_path)
        else:
            self.image_label.setText("Arrastra un archivo SVG aquí\no usa el botón 'Abrir SVG'")
            self.image_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #999;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 14px;
                    color: #666;
                }
            """)
            
            
    def _add_toolbar_buttons(self):        
        # Botón para abrir SVG
        abrir_svg_btn = QPushButton("Abrir SVG")
        abrir_svg_btn.clicked.connect(self._abrir_svg)
        self.toolbar.addWidget(abrir_svg_btn)
        
        select_edits_btn = QPushButton("Seleccionar Ediciones")
        select_edits_btn.clicked.connect(self._seleccionar_edits)
        self.toolbar.addWidget(select_edits_btn)
        
        aplicar_btn = QPushButton("Aplicar Ediciones")
        aplicar_btn.clicked.connect(self._aplicar)
        self.toolbar.addWidget(aplicar_btn)

        restaurar_btn = QPushButton("Restaurar Original")
        restaurar_btn.clicked.connect(self._restaurar)
        self.toolbar.addWidget(restaurar_btn)

        exportar_pdf_btn = QPushButton("Exportar PDF")
        exportar_pdf_btn.clicked.connect(self.exportar_pdf)
        self.toolbar.addWidget(exportar_pdf_btn)
        
        refresh_png_action = QAction("Actualizar PNG", self)
        refresh_png_action.triggered.connect(self._refresh_viewport_png)
        self.toolbar.addAction(refresh_png_action)
        

    def _load_svg(self, path_svg):
        self.svg_path = Path(path_svg)
        self.png_path = self.svg_path.with_suffix(".png")
        abs_path = self.svg_path.resolve()
        self.browser.load(QUrl.fromLocalFile(str(abs_path)))
        self.browser.loadFinished.connect(self._procesar_svg)
        self.image_label.setText("Cargando imagen...")
        # Set dashed border while loading
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed #999;
                border-radius: 8px;
                padding: 20px;
                font-size: 14px;
                color: #666;
            }
        """)

    def load_svg(self, path_svg):
        """Método público para cargar o recargar un SVG dinámicamente."""
        if Path(path_svg).exists():
            self._load_svg(path_svg)
            self.image_label.setText("Cargando imagen...")
        else:
            self.image_label.setText("Archivo SVG no encontrado.")



        # Cargar SVG y correr análisis
        abs_path = self.svg_path.resolve()
        self.browser.load(QUrl.fromLocalFile(str(abs_path)))
        self.browser.loadFinished.connect(self._procesar_svg)


    def _procesar_svg(self):
        """Cuando el SVG se carga, inyecta el JS y luego exporta a PNG."""
        self.inyectar_js()
        self._export_svg_to_png()
        self._mostrar_png()
        # Remove the dashed border after loading
        self.image_label.setStyleSheet("")

    def _export_svg_to_png(self):
        fondo_color = "#ffffff"
        # Use "inkscape" command directly if it's in PATH, otherwise use full path for Windows
        inkscape_path = "inkscape"  # Default to command name if in PATH
        if sys.platform == "win32":
            possible_paths = [
                r"C:\Program Files\Inkscape\bin\inkscape.exe",
                r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
                r"C:\Program Files\Inkscape\inkscape.exe",
                r"C:\Program Files (x86)\Inkscape\inkscape.exe"
            ]
            for path in possible_paths:
                if Path(path).exists():
                    inkscape_path = path
                    break
                    
        command = [
            inkscape_path,
            str(self.svg_path),
            "--export-type=png",
            f"--export-filename={self.png_path}",
            "--export-dpi=300",
            f"--export-background={fondo_color}",
            "--export-background-opacity=1"
        ]
        try:
            subprocess.run(command, check=True)
        except FileNotFoundError:
            print("❌ Error: Inkscape no encontrado. Por favor, asegúrate de que Inkscape está instalado y en el PATH del sistema.")
            self.image_label.setText("Error: Inkscape no encontrado.\nPor favor, instala Inkscape.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al ejecutar Inkscape: {e}")
            self.image_label.setText("Error al procesar el archivo SVG.")

    def _mostrar_png(self):
        if self.png_path.exists():
            pixmap = QPixmap(str(self.png_path))
            self.image_label.setPixmap(
                pixmap.scaled(650, 650, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            print(f"✅ PNG mostrado: {self.png_path}")
        else:
            print("❌ No se pudo mostrar el PNG")

    def _seleccionar_edits(self):
        """Abre un diálogo para seleccionar un archivo JSON de ediciones."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo JSON de ediciones",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*.*)"
        )
        if archivo:
            self.custom_json_path = archivo
            print(f"✅ Archivo de ediciones seleccionado: {archivo}")

    def _aplicar(self):
        """Aplica las ediciones desde el JSON seleccionado o el predeterminado."""
        if not self.svg_path:
            QMessageBox.warning(self, "Error", "No hay un archivo SVG cargado.")
            return

        # Usar el JSON personalizado si existe, sino usar el predeterminado
        json_path = self.custom_json_path if self.custom_json_path else self.gral.get_file_edits("ediciones_utf8")
        
        if apply_svg_edits(self.svg_path, json_path):
            # Reload the SVG file after applying edits
            self._load_svg(str(self.svg_path))
        
        self._refresh_viewport_png()

    def _restaurar(self):
        if restore_from_backup(self.svg_path):
            self._procesar_svg()

    def exportar_pdf(self):
        if not self.svg_path:
            QMessageBox.warning(self, "Error", "No hay un archivo SVG cargado.")
            return
            
        sugerido = str(self.svg_path.with_suffix(".pdf"))
        archivo_pdf, _ = QFileDialog.getSaveFileName(
            self, "Guardar como PDF", sugerido, "Archivos PDF (*.pdf)"
        )
        if archivo_pdf:
            # Use "inkscape" command directly if it's in PATH, otherwise use full path for Windows
            inkscape_path = "inkscape"  # Default to command name if in PATH
            if sys.platform == "win32":
                possible_paths = [
                    r"C:\Program Files\Inkscape\bin\inkscape.exe",
                    r"C:\Program Files (x86)\Inkscape\bin\inkscape.exe",
                    r"C:\Program Files\Inkscape\inkscape.exe",
                    r"C:\Program Files (x86)\Inkscape\inkscape.exe"
                ]
                for path in possible_paths:
                    if Path(path).exists():
                        inkscape_path = path
                        break

            command = [
                inkscape_path,
                str(self.svg_path),
                "--export-type=pdf",
                f"--export-filename={archivo_pdf}",
            ]
            try:
                subprocess.run(command, check=True)
                print(f"📄 PDF exportado: {archivo_pdf}")
            except FileNotFoundError:
                print("❌ Error: Inkscape no encontrado")
                QMessageBox.critical(self, "Error", "Inkscape no encontrado. Por favor, asegúrate de que Inkscape está instalado y en el PATH del sistema.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error al exportar PDF: {e}")
                QMessageBox.critical(self, "Error", f"Error al exportar el PDF: {e}")
            
    def _abrir_svg(self):
        """Abre un diálogo para seleccionar un archivo SVG."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo SVG",
            "",
            "Archivos SVG (*.svg);;Todos los archivos (*.*)"
        )
        if archivo:
            self._load_svg(archivo)
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Maneja el evento cuando se arrastra un archivo sobre la ventana."""
        mime = event.mimeData()
        if mime.hasUrls() and len(mime.urls()) == 1:
            url = mime.urls()[0]
            if url.isLocalFile() and url.toLocalFile().lower().endswith('.svg'):
                event.acceptProposedAction()
                
    def dropEvent(self, event: QDropEvent):
        """Maneja el evento cuando se suelta un archivo en la ventana."""
        mime = event.mimeData()
        if mime.hasUrls():
            url = mime.urls()[0]
            if url.isLocalFile():
                file_path = url.toLocalFile()
                if file_path.lower().endswith('.svg'):
                    self._load_svg(file_path)
                    event.acceptProposedAction()
                    
    def _refresh_viewport_png(self):
        # Convertir SVG a PNG nuevamente
        self._export_svg_to_png()
        # Mostrar el PNG actualizado
        self._mostrar_png()
        print(f"✅ PNG actualizado: {self.png_path}")
                    
    def inyectar_js(self):
        print("🚀 Inyectando JS para analizar tspans...")

        js = """
        (function() {
            const svg = document.querySelector('svg');
            if (!svg) return;

            const tspans = svg.querySelectorAll("tspan");
            const tspanHijos = [];
            const tspanIndependientes = [];

            tspans.forEach(tspan => {
                const id = tspan.id || "(sin ID)";
                const hijos = tspan.querySelectorAll("tspan");
                let tipo = "🔹 INDEPENDIENTE";

                if (hijos.length > 0) {
                    const hijos_ids = Array.from(hijos).map(h => h.id || "(sin ID)");
                    tipo = "🟣 PADRE de: " + hijos_ids.join(", ");
                    hijos.forEach(h => tspanHijos.push(h));
                } else if (
                    tspan.parentElement &&
                    tspan.parentElement.tagName.toLowerCase() === "tspan"
                ) {
                    const padre = tspan.parentElement;
                    tipo = "🟢 HIJO de: " + (padre.id || "(sin ID)");
                    tspanHijos.push(tspan);
                } else {
                    tspanIndependientes.push(tspan);
                }

                console.log(`[${id}] → ${tipo}`);
            });

            console.log(`✅ Se encontraron ${tspanHijos.length} tspans hijos.`);
            tspanHijos.forEach(t => {
                console.log(`📦 Hijo: ${t.id || "(sin ID)"}, texto: "${t.textContent.trim()}"`);
            });

            console.log(`✅ Se encontraron ${tspanIndependientes.length} tspans independientes.`);
            tspanIndependientes.forEach(t => {
                console.log(`📦 Independiente: ${t.id || "(sin ID)"}, texto: "${t.textContent.trim()}"`);
            });
        })()
        """
        self.browser.page().runJavaScript(js)
    # def inyectar_js(self):
    #     """Analiza tspans del SVG."""
    #     js = """
    #     (function() {
    #         const svg = document.querySelector('svg');
    #         if (!svg) return;
    #
    #         const tspans = svg.querySelectorAll("tspan");
    #         const tspanHijos = [];
    #         const tspanIndependientes = [];
    #
    #         tspans.forEach(tspan => {
    #             const id = tspan.id || "(sin ID)";
    #             const hijos = tspan.querySelectorAll("tspan");
    #             let tipo = "INDEPENDIENTE";
    #
    #             if (hijos.length > 0) {
    #                 const hijos_ids = Array.from(hijos).map(h => h.id || "(sin ID)");
    #                 tipo = "PADRE de: " + hijos_ids.join(", ");
    #                 hijos.forEach(h => tspanHijos.push(h));
    #             } else if (
    #                 tspan.parentElement &&
    #                 tspan.parentElement.tagName.toLowerCase() === "tspan"
    #             ) {
    #                 const padre = tspan.parentElement;
    #                 tipo = "HIJO de: " + (padre.id || "(sin ID)");
    #                 tspanHijos.push(tspan);
    #             } else {
    #                 tspanIndependientes.push(tspan);
    #             }
    #
    #             console.log(`[${id}] → ${tipo}`);
    #         });
    #
    #         console.log(`Hijos: ${tspanHijos.length}`);
    #         console.log(`Independientes: ${tspanIndependientes.length}`);
    #     })()
    #     """
    #     self.browser.page().runJavaScript(js)


if __name__ == "__main__":
    import sys
    from splash_screen import SplashScreen
    
    app = QApplication(sys.argv)
    
    # Show splash screen
    splash = SplashScreen()
    splash.show()
    
    # Create main window but don't show it yet
    win = MainWindow("test.svg")  # Cambia por tu SVG real
    
    # When splash screen closes, show main window
    splash.fade_anim.finished.connect(win.show)
    
    sys.exit(app.exec())
