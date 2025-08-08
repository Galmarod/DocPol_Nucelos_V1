#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import shutil
from pathlib import Path
from model.tspan_replacer import replace_multiline_tspan_by_id

def apply_svg_edits(svg_path, json_path="ediciones.json"):
    ediciones_path = Path(json_path)

    if not ediciones_path.exists():
        print("? No se encontró el archivo ediciones.json.")
        return False

    # Crear copia de seguridad
    backup_path = svg_path.with_suffix(".svg.bak")
    if not backup_path.exists():
        shutil.copy(svg_path, backup_path)
        print(f"? Copia de seguridad creada: {backup_path.name}")

    # Leer reemplazos desde JSON
    with open(ediciones_path, "r", encoding="utf-8") as f:
        replacements_by_id = json.load(f)

    replace_multiline_tspan_by_id(svg_path, replacements_by_id)
    print("? Ediciones aplicadas.")
    return True

def restore_from_backup(svg_path):
    backup_path = svg_path.with_suffix(".svg.bak")
    if backup_path.exists():
        shutil.copy(backup_path, svg_path)
        print("? Archivo restaurado desde copia de seguridad.")
        return True
    else:
        print("? No se encontró una copia de seguridad.")
        return False
