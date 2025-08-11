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

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
import json
import os
import uuid
from common.gral import General
from controller.control import Control
import asyncio

class APIServer:
    def __init__(self, queue=None):
        self.app = FastAPI()
        self.queue = queue
        self.gral = General()
        self.control = Control()
        self._docpol_api()

    def _docpol_api(self):
        @self.app.post("/docpolSaveFiles")
        async def save_files(svg_file: UploadFile = File(...), json_file: UploadFile = File(...)):
            try:
                # Guardar JSON temporalmente
                temp_json_path = self.gral.save_files_user("temp",uuid.uuid4().hex,"tempFile", f"temp_{uuid.uuid4().hex}.json")
                with open(temp_json_path, "wb") as f:
                    shutil.copyfileobj(json_file.file, f)

                # Leer JSON
                with open(temp_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Obtener datos de nameUser
                name_user_data = data.get("User", {})
                username = name_user_data.get("nameUser", None)
                
                filename = os.path.splitext(svg_file.filename)[0]
                final_json_path = self.gral.save_files_user("uploads",username, filename,f"{username}_{filename}.json") 
                # Renombrar JSON
                os.rename(temp_json_path, final_json_path)
               
                svg_path = self.gral.save_files_user("uploads",username,filename ,svg_file.filename)
                with open(svg_path, "wb") as f:
                    shutil.copyfileobj(svg_file.file, f)

                # Extraer ediciones para procesar
                ediciones = data.get("ediciones", {})
                print("📄 Ediciones:", ediciones)
                print("👤 Datos usuario:", name_user_data)
                    
                png_path = os.path.join(os.path.dirname(svg_path), f"{filename}.png")
                await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path)

                # Procesar el SVG con las ediciones (aquí pones tu lógica real)
                resultado_path = Path("resultado.svg")
                self.procesar_svg_con_instrucciones(Path(svg_path), ediciones, resultado_path)

                # Si usas la cola
                if self.queue:
                    self.queue.put("archivo_recibido")

                # Devolver archivo procesado
                return FileResponse(png_path, media_type="image/png", filename=f"{filename}.png")

            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

    def procesar_svg_con_instrucciones(self, svg_path: Path, instrucciones: dict, output_path: Path):
        contenido = svg_path.read_text(encoding="utf-8")
        # Aquí iría tu lógica real para modificar el SVG
        output_path.write_text(contenido, encoding="utf-8")
