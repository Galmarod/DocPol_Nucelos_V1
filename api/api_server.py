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

import shutil
import os
import io
import zipfile
import asyncio

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.responses import StreamingResponse, JSONResponse
from pathlib import Path


from common.gral import General
from controller.control import Control
#from controller.svg_edits import apply_svg_edits, restore_from_backup
from controller.svg_edits import SvgEdits

from model.analyze_svg import AnalyzeSvg


class APIServer:
    def __init__(self, queue=None):
        self.app = FastAPI()
        self.queue = queue
        self.gral = General()
        self.control = Control()
        self.analyzesvg = AnalyzeSvg()
        self.svgedits = SvgEdits()
        self._docpol_api()

    def _docpol_api(self):
        @self.app.post("/docpolSaveFiles")
        async def save_files(svg_file: UploadFile = File(...), json_file: UploadFile = File(...)):
            try:
                svg_path, filename, png_path, temp_json_path, final_json_path, name_file_user = self.gral.save_file_api(json_file,svg_file)
                json_path = os.path.join(os.path.dirname(svg_path), f"{filename}_TspanAlisis.json")
                

                await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path) 
                await asyncio.to_thread(self.analyzesvg.run_analyze_svg, svg_path, json_path)
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zipf:
                    zipf.write(png_path, arcname=f"{filename}.png")
                    zipf.write(json_path, arcname=f"{filename}.json")
                zip_buffer.seek(0)
                
                # Si usas la cola
                if self.queue:
                    self.queue.put("archivo_recibido")

                try:
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
                svg_path, filename, png_path, temp_json_path, final_json_path, name_file_user = self.gral.save_file_api(json_file)
                await asyncio.to_thread(self.svgedits.runSvgEdits, final_json_path, svg_path)
                await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path)                
                if self.queue:
                    self.queue.put("archivo_recibido")
                try:
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
                    shutil.rmtree(os.path.dirname(temp_json_path))
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"⚠️ No se pudo eliminar carpeta temporal: {e}")
                return FileResponse(png_path, media_type="image/png", filename=f"{filename}_edit.png")

            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

        @self.app.post("/docpolRestoreSvg")
        async def restore_files(json_file: UploadFile = File(...)):
            try:
                svg_path, filename, png_path, temp_json_path, final_json_path, data = self.gral.save_file_api(json_file)  
                name_file_user = data.get("Svginformation",{})            
                restore = name_file_user.get("restore",None)   

                if restore == 1:
                    await asyncio.to_thread(self.svgedits.restore_from_backup, Path(svg_path))
                    await asyncio.to_thread(self.control.export_svg_to_png, svg_path, png_path)

                if self.queue:
                    self.queue.put("archivo_recibido")
                try:
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
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
                svg_path, filename, png_path, temp_json_path, final_json_path, data = self.gral.save_file_api(json_file)  
                name_file_user = data.get("Svginformation",{})  
                exportPDF = name_file_user.get("exportPDF",None)
                pdf_path = os.path.join(os.path.dirname(svg_path), f"{filename}.pdf")
              
                if exportPDF == 1:
                    await asyncio.to_thread(self.control.export_svg_to_pdf, svg_path, pdf_path)

                if self.queue:
                    self.queue.put("archivo_recibido")
                try:
                    os.remove(final_json_path)
                except FileNotFoundError:
                    pass

                try:
                    shutil.rmtree(os.path.dirname(temp_json_path))
                except FileNotFoundError:
                    pass
                except OSError as e:
                    print(f"?? No se pudo eliminar carpeta temporal: {e}")
                # Devolver archivo procesado
                return FileResponse(pdf_path, media_type="application/pdf", filename=f"{filename}.pdf")

            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

    
