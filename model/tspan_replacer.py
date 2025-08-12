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

import textwrap
import lxml.etree as ET


def replace_multiline_tspan_by_id(svg_path, reemplazos_por_id):
    tree = ET.parse(svg_path)
    root = tree.getroot()
    ns = {"svg": "http://www.w3.org/2000/svg"}

    for tspan in root.findall(".//svg:tspan", ns):
        tspan_id = tspan.attrib.get("id")

        if tspan_id and tspan_id in reemplazos_por_id:
            nuevo_texto = reemplazos_por_id[tspan_id]
            print(f"?? Reemplazando '{tspan_id}' con: {nuevo_texto[:60]}...")

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
                print(f"?? Eliminando <tspan id='{hijo.attrib.get('id', '(sin ID)')}'>")
                text_node.remove(hijo)

            # Dividir el nuevo texto en l�neas
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

                # ?? Guardar el SVG modificado
                tree.write(svg_path)
    print("? Reemplazo y limpieza completados.")
def analizar_tspans(svg_path, output_txt):
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Detectar si el SVG tiene namespace
    nsmap = root.nsmap
    if None in nsmap and nsmap[None]:
        ns = {'svg': nsmap[None]}
        xpath = ".//svg:tspan"
    else:
        ns = {}
        xpath = ".//tspan"

    tspans = root.findall(xpath, ns)

    tspan_hijos = []
    tspan_independientes = []

    lines = ["?? Analizando tspans...\n"]

    for tspan in tspans:
        tid = tspan.get("id", "(sin ID)")
        hijos = tspan.findall(".//svg:tspan" if ns else ".//tspan", ns)

        if hijos:
            hijos_ids = [h.get("id", "(sin ID)") for h in hijos]
            tipo = f"?? PADRE de: {', '.join(hijos_ids)}"
            tspan_hijos.extend(hijos)
        elif tspan.getparent() is not None and tspan.getparent().tag.endswith("tspan"):
            padre = tspan.getparent()
            tipo = f"?? HIJO de: {padre.get('id', '(sin ID)')}"
            tspan_hijos.append(tspan)
        else:
            tipo = "?? INDEPENDIENTE"
            tspan_independientes.append(tspan)

        lines.append(f"[{tid}] ? {tipo}")

    lines.append(f"\n? Se encontraron {len(tspan_hijos)} tspans hijos.")
    for t in tspan_hijos:
        lines.append(f"   ?? Hijo: {t.get('id', '(sin ID)')}, texto: \"{''.join(t.itertext()).strip()}\"")

    lines.append(f"\n? Se encontraron {len(tspan_independientes)} tspans independientes.")
    for t in tspan_independientes:
        lines.append(f"   ?? Independiente: {t.get('id', '(sin ID)')}, texto: \"{''.join(t.itertext()).strip()}\"")

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"?? Resultado guardado en: {output_txt}")
