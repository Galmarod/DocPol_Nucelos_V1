#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtSvgWidgets import QSvgWidget


class MainWindow(QMainWindow):
    def __init__(self, svg_path):
        super().__init__()
        self.setWindowTitle("Previsualización SVG con PySide6")

        # Widget principal
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Widget para mostrar el SVG
        self.svg_widget = QSvgWidget(svg_path)
        self.svg_widget.setMinimumSize(800, 600)  # Tamaño inicial

        layout.addWidget(self.svg_widget)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py archivo.svg")
        sys.exit(1)

    ruta_svg = sys.argv[1]

    app = QApplication(sys.argv)
    ventana = MainWindow(ruta_svg)
    ventana.show()
    sys.exit(app.exec())
