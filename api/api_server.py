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
import io
import zipfile
import os
from common.gral import General
from controller.control import Control
from controller.svg_edits import apply_svg_edits, restore_from_backup
from model.tspan_replacer import analizar_tspans
import asyncio
from fastapi.responses import StreamingResponse, JSONResponse

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
                txt_path = os.path.join(os.path.dirname(svg_path), f"{filename}_TspanAlisis.txt")
                
                await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path)                
                await asyncio.to_thread(analizar_tspans, Path(svg_path), txt_path) 
                # Crear ZIP en memoria
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zipf:
                    zipf.write(png_path, arcname=f"{filename}.png")
                    zipf.write(txt_path, arcname=f"{filename}.txt")
                zip_buffer.seek(0)
                
                # Si usas la cola
                if self.queue:
                    self.queue.put("archivo_recibido")

                # Devolver archivo procesado
                try:
                    # Eliminar JSON final
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
                    # Eliminar carpeta temporal con su JSON
                    shutil.rmtree(os.path.dirname(temp_json_path))
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"?? No se pudo eliminar carpeta temporal: {e}")
                #return FileResponse(png_path, media_type="image/png", filename=f"{filename}.png")
                # Devolver ZIP como respuesta
                return StreamingResponse(
                    zip_buffer,
                    media_type="application/zip",
                    headers={"Content-Disposition": f"attachment; filename={filename}.zip"}
                )
            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)
        
        @self.app.post("/docpolEditSvg")
        async def edit_files(json_file: UploadFile = File(...)):
            try:
                # Guardar JSON temporalmente
                temp_json_path = self.gral.save_files_user("temp",uuid.uuid4().hex,"tempFile", f"temp_{uuid.uuid4().hex}.json")
                with open(temp_json_path, "wb") as f:
                    shutil.copyfileobj(json_file.file, f)

                # Leer JSON
                with open(temp_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(data)

                # Obtener datos de nameUser
                name_user_data = data.get("User", {})
                username = name_user_data.get("nameUser", None)
                name_file_user = data.get("Svginformation",{})
                file = name_file_user.get("nameFileSvg",None)
                filename = os.path.splitext(file)[0]

                
                final_json_path = self.gral.save_files_user("uploads",username, filename,f"{username}_{filename}_ediciones.json") 
                # Renombrar JSON
                os.rename(temp_json_path, final_json_path)
               
                # Extraer ediciones para procesar
                ediciones = data.get("ediciones", {})
                print("📄 Ediciones:", ediciones)
                print("👤 Datos usuario:", name_user_data)
                
                svg_path = self.gral.save_files_user("uploads",username,filename,f"{filename}.svg")
                png_path = os.path.join(os.path.dirname(svg_path), f"{filename}_edit.png")
 
                

                await asyncio.to_thread(apply_svg_edits, Path(svg_path), final_json_path)
                await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path)
                
                #Solution bugTemporal exportPDF, after change
                await asyncio.to_thread(restore_from_backup, Path(svg_path))

                if self.queue:
                    self.queue.put("archivo_recibido")
                try:
                    # Eliminar JSON final
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
                    # Eliminar carpeta temporal con su JSON
                    shutil.rmtree(os.path.dirname(temp_json_path))
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"⚠️ No se pudo eliminar carpeta temporal: {e}")
                # Devolver archivo procesado
                return FileResponse(png_path, media_type="image/png", filename=f"{filename}_edit.png")

            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

        @self.app.post("/docpolRestoreSvg")
        async def restore_files(json_file: UploadFile = File(...)):
            try:
                # Guardar JSON temporalmente
                temp_json_path = self.gral.save_files_user("temp",uuid.uuid4().hex,"tempFile", f"temp_{uuid.uuid4().hex}.json")
                with open(temp_json_path, "wb") as f:
                    shutil.copyfileobj(json_file.file, f)

                # Leer JSON
                with open(temp_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(data)

                # Obtener datos de nameUser
                name_user_data = data.get("User", {})
                username = name_user_data.get("nameUser", None)
                name_file_user = data.get("Svginformation",{})
                file = name_file_user.get("nameFileSvg",None)
                filename = os.path.splitext(file)[0]

                
                final_json_path = self.gral.save_files_user("uploads",username, filename,f"{username}_{filename}_restore.json") 
                # Renombrar JSON
                os.rename(temp_json_path, final_json_path)
                
                # Extraer ediciones para procesar
                print("👤 Datos usuario:", name_user_data)
               
                restore = name_file_user.get("restore",None)

                svg_path = self.gral.save_files_user("uploads",username,filename,f"{filename}.svg")
                png_path = os.path.join(os.path.dirname(svg_path), f"{filename}_restore.png")
                
                print(restore)
                if restore == 1:
                    await asyncio.to_thread(restore_from_backup, Path(svg_path))
                    await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path)

                if self.queue:
                    self.queue.put("archivo_recibido")
                try:
                    # Eliminar JSON final
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
                    # Eliminar carpeta temporal con su JSON
                    shutil.rmtree(os.path.dirname(temp_json_path))
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"?? No se pudo eliminar carpeta temporal: {e}")
                # Devolver archivo procesado
                return FileResponse(png_path, media_type="image/png", filename=f"{filename}_restore.png")

            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

        @self.app.post("/docpolPdf")
        async def export_pdf(json_file: UploadFile = File(...)):
            try:
                # Guardar JSON temporalmente
                temp_json_path = self.gral.save_files_user("temp",uuid.uuid4().hex,"tempFile", f"temp_{uuid.uuid4().hex}.json")
                with open(temp_json_path, "wb") as f:
                    shutil.copyfileobj(json_file.file, f)

                # Leer JSON
                with open(temp_json_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    print(data)

                # Obtener datos de nameUser
                name_user_data = data.get("User", {})
                username = name_user_data.get("nameUser", None)
                name_file_user = data.get("Svginformation",{})
                file = name_file_user.get("nameFileSvg",None)
                filename = os.path.splitext(file)[0]

                        
                final_json_path = self.gral.save_files_user("uploads",username, filename,f"{username}_{filename}_restore.json") 
                # Renombrar JSON
                os.rename(temp_json_path, final_json_path)
                
                # Extraer ediciones para procesar
                print("👤 Datos usuario:", name_user_data)
               
                exportPDF = name_file_user.get("exportPDF",None)

                svg_path = self.gral.save_files_user("uploads",username,filename,f"{filename}.svg")
                pdf_path = os.path.join(os.path.dirname(svg_path), f"{filename}.pdf")
                
                if exportPDF == 1:
                    await asyncio.to_thread(self.control.export_svg_to_pdf, svg_path, pdf_path)

                if self.queue:
                    self.queue.put("archivo_recibido")
                try:
                    # Eliminar JSON final
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
                    # Eliminar carpeta temporal con su JSON
                    shutil.rmtree(os.path.dirname(temp_json_path))
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"?? No se pudo eliminar carpeta temporal: {e}")
                # Devolver archivo procesado
                return FileResponse(pdf_path, media_type="application/pdf", filename=f"{filename}.pdf")

            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

    def procesar_svg_con_instrucciones(self, svg_path: Path, instrucciones: dict, output_path: Path):
        contenido = svg_path.read_text(encoding="utf-8")
        # Aquí iría tu lógica real para modificar el SVG
        output_path.write_text(contenido, encoding="utf-8")
