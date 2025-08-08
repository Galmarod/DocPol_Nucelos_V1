#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QToolBar, QPushButton, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtCore import QUrl

from controller.svg_edits import apply_svg_edits, restore_from_backup
from common.gral import General


class CustomPage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print(f"?? JS: {message}")


class MainWindow(QMainWindow):
    def __init__(self, svg_path):
        self.gral = General() 
        super().__init__()
        self.setWindowTitle("Preview Docpol v1.0.3")
        self.resize(620, 890)

        self.svg_path = Path(svg_path)
        self.browser = QWebEngineView()
        self.browser.setPage(CustomPage(self.browser))
        self.zoom_factor = 0.75
        self.browser.setZoomFactor(self.zoom_factor)

        abs_path = self.svg_path.resolve()
        self.browser.load(QUrl.fromLocalFile(str(abs_path)))
        self.browser.loadFinished.connect(self.inyectar_js)
        self.setCentralWidget(self.browser)

        self.toolbar = QToolBar("Herramientas")
        self.addToolBar(self.toolbar)

        self._add_toolbar_buttons()

    def _add_toolbar_buttons(self):
        zoom_in_btn = QPushButton("+")
        zoom_in_btn.clicked.connect(self.zoom_in)
        self.toolbar.addWidget(zoom_in_btn)

        zoom_out_btn = QPushButton("-")
        zoom_out_btn.clicked.connect(self.zoom_out)
        self.toolbar.addWidget(zoom_out_btn)

        aplicar_btn = QPushButton("Aplicar Ediciones")
        aplicar_btn.clicked.connect(self._aplicar)
        self.toolbar.addWidget(aplicar_btn)

        restaurar_btn = QPushButton("Restaurar Original")
        restaurar_btn.clicked.connect(self._restaurar)
        self.toolbar.addWidget(restaurar_btn)

        exportar_pdf_btn = QPushButton("Exportar PDF")
        exportar_pdf_btn.clicked.connect(self.exportar_pdf)
        self.toolbar.addWidget(exportar_pdf_btn)

    def zoom_in(self):
        self.zoom_factor += 0.1
        self.browser.setZoomFactor(self.zoom_factor)

    def zoom_out(self):
        self.zoom_factor = max(0.1, self.zoom_factor - 0.1)
        self.browser.setZoomFactor(self.zoom_factor)

    def _aplicar(self):
        if apply_svg_edits(self.svg_path, self.gral.get_file_edits("ediciones_utf8")):
            self.browser.reload()

    def _restaurar(self):
        if restore_from_backup(self.svg_path):
            self.browser.reload()

    def exportar_pdf(self):
        sugerido = str(self.svg_path.with_suffix(".pdf"))
        archivo_pdf, _ = QFileDialog.getSaveFileName(
            self, "Guardar como PDF", sugerido, "Archivos PDF (*.pdf)"
        )
        if archivo_pdf:
            command = [
                "/Applications/Inkscape.app/Contents/MacOS/inkscape",
                "--pipe",
                f"--export-filename={archivo_pdf}",
            ]
            with open(self.svg_path, "rb") as svg_content:
                subprocess.run(command, input=svg_content.read(), check=True)
            print(f"? PDF exportado a: {archivo_pdf}")
        else:
            print("? Exportaci?n cancelada.")

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
