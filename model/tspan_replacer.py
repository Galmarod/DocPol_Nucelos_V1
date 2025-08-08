#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textwrap
from lxml import etree as ET

def replace_multiline_tspan_by_id(svg_path, reemplazos_por_id):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    for tspan in root.findall(".//svg:tspan", ns):
        tspan_id = tspan.attrib.get("id")

        if tspan_id and tspan_id in reemplazos_por_id:
            nuevo_texto = reemplazos_por_id[tspan_id]
            print(f"✏️ Reemplazando '{tspan_id}' con: {nuevo_texto[:60]}...")

            # Detectar el padre <text> del tspan
            text_node = tspan.getparent()
            index_inicio = list(text_node).index(tspan)

            # Detectar los tspan consecutivos a eliminar (solo del bloque actual)
            hijos_a_eliminar = []
            for hermano in list(text_node)[index_inicio:]:
                if hermano.tag.endswith("tspan"):
                    hijos_a_eliminar.append(hermano)
                else:
                    break

            # Eliminar solo los tspans relacionados
            for hijo in hijos_a_eliminar:
                print(f"🧹 Eliminando <tspan id='{hijo.attrib.get('id', '(sin ID)')}'>")
                text_node.remove(hijo)

            # Dividir el nuevo texto en líneas
            lineas = textwrap.wrap(nuevo_texto, width=95, break_long_words=True, replace_whitespace=False)


            # Coordenadas base (usa las del primer tspan)
            x = tspan.attrib["x"] if "x" in tspan.attrib else "0"
            y_inicial = float(tspan.attrib["y"]) if "y" in tspan.attrib else 0.0
            dy = 20

            # Copiar estilos del tspan original
            style_original = tspan.attrib.get("style", "")
            font_size = tspan.attrib.get("font-size")
            font_family = tspan.attrib.get("font-family")
            text_anchor = tspan.attrib.get("text-anchor")

            for i, linea in enumerate(lineas):
                nuevo = ET.SubElement(text_node, f"{{{ns['svg']}}}tspan")
                nuevo.set("x", x)
                y = str(y_inicial + i * dy)
                nuevo.set("y", y)
                nuevo.set("id", f"{tspan_id}")
                nuevo.text = linea

                # Aplicar estilos heredados
                if style_original:
                    nuevo.set("style", style_original)
                if font_size:
                    nuevo.set("font-size", font_size)
                if font_family:
                    nuevo.set("font-family", font_family)
                if text_anchor:
                    nuevo.set("text-anchor", text_anchor)

                # 🧾 Guardar el SVG modificado
                tree.write(svg_path)
    print("✅ Reemplazo y limpieza completados.")

