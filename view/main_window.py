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
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QPushButton, QFileDialog, QLabel, QApplication, QVBoxLayout, QWidget
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage

from controller.svg_edits import apply_svg_edits, restore_from_backup
from common.gral import General


class CustomPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"[JS] {message}")


class MainWindow(QMainWindow):
    def __init__(self, svg_path):
        super().__init__()
        self.gral = General()
        self.setWindowTitle("Vista PNG con análisis de tspans")
        self.resize(700, 800)

        self.svg_path = Path(svg_path)
        self.png_path = self.svg_path.with_suffix(".png")

        # Layout principal
        central_widget = QWidget()
        self.layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # QLabel para mostrar PNG
        self.image_label = QLabel("Cargando imagen...")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Toolbar
        self.toolbar = QToolBar("Herramientas")
        self.addToolBar(self.toolbar)
        self._add_toolbar_buttons()

        # QWebEngine invisible para correr JS
        self.browser = QWebEngineView()
        self.browser.setPage(CustomPage(self.browser))
        self.browser.hide()  # No mostrar

        if self.svg_path and self.svg_path.exists():
            self._load_svg(self.svg_path)
        else:
            print("No se cargó SVG inicial.")

    def _load_svg(self, path_svg):
        self.svg_path = Path(path_svg)
        self.png_path = self.svg_path.with_suffix(".png")
        abs_path = self.svg_path.resolve()
        self.browser.load(QUrl.fromLocalFile(str(abs_path)))
        self.browser.loadFinished.connect(self._procesar_svg)
        self.image_label.setText("Cargando imagen...")

    def load_svg(self, path_svg):
        """Método público para cargar o recargar un SVG dinámicamente."""
        if Path(path_svg).exists():
            self._load_svg(path_svg)
        else:
            self.image_label.setText("Archivo SVG no encontrado.")



        # Cargar SVG y correr análisis
        abs_path = self.svg_path.resolve()
        self.browser.load(QUrl.fromLocalFile(str(abs_path)))
        self.browser.loadFinished.connect(self._procesar_svg)

    def _add_toolbar_buttons(self):
        aplicar_btn = QPushButton("Aplicar Ediciones")
        aplicar_btn.clicked.connect(self._aplicar)
        self.toolbar.addWidget(aplicar_btn)

        restaurar_btn = QPushButton("Restaurar Original")
        restaurar_btn.clicked.connect(self._restaurar)
        self.toolbar.addWidget(restaurar_btn)

        exportar_pdf_btn = QPushButton("Exportar PDF")
        exportar_pdf_btn.clicked.connect(self.exportar_pdf)
        self.toolbar.addWidget(exportar_pdf_btn)

    def _procesar_svg(self):
        """Cuando el SVG se carga, inyecta el JS y luego exporta a PNG."""
        self.inyectar_js()
        self._export_svg_to_png()
        self._mostrar_png()

    def _export_svg_to_png(self):
        fondo_color = "#ffffff"
        command = [
            "/Applications/Inkscape.app/Contents/MacOS/inkscape",
            str(self.svg_path),
            "--export-type=png",
            f"--export-filename={self.png_path}",
            "--export-dpi=300",
            f"--export-background={fondo_color}",
            "--export-background-opacity=1"
        ]
        subprocess.run(command, check=True)

    def _mostrar_png(self):
        if self.png_path.exists():
            pixmap = QPixmap(str(self.png_path))
            self.image_label.setPixmap(
                pixmap.scaled(650, 650, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            print(f"✅ PNG mostrado: {self.png_path}")
        else:
            print("❌ No se pudo mostrar el PNG")

    def _aplicar(self):
        if apply_svg_edits(self.svg_path, self.gral.get_file_edits("ediciones_utf8")):
            self._procesar_svg()

    def _restaurar(self):
        if restore_from_backup(self.svg_path):
            self._procesar_svg()

    def exportar_pdf(self):
        sugerido = str(self.svg_path.with_suffix(".pdf"))
        archivo_pdf, _ = QFileDialog.getSaveFileName(
            self, "Guardar como PDF", sugerido, "Archivos PDF (*.pdf)"
        )
        if archivo_pdf:
            command = [
                "/Applications/Inkscape.app/Contents/MacOS/inkscape",
                str(self.svg_path),
                "--export-type=pdf",
                f"--export-filename={archivo_pdf}",
            ]
            subprocess.run(command, check=True)
            print(f"📄 PDF exportado: {archivo_pdf}")
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
    app = QApplication(sys.argv)
    win = MainWindow("test.svg")  # Cambia por tu SVG real
    win.show()
    sys.exit(app.exec())
