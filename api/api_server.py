# api_server.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pathlib import Path
import shutil
import json

from common.gral import General

class APIServer:
    def __init__(self, queue=None):
        self.app = FastAPI()
        self.queue = queue
        self._add_routes()
        self.gral = General()

    def _add_routes(self):
        @self.app.post("/procesar")
        async def procesar(svg_file: UploadFile = File(...), json_file: UploadFile = File(...)):
            try:
                temp_svg =  Path(self.gral.get_template_api("temp_input.svg"))
                temp_json = Path(self.gral.get_file_edits("temp_instrucciones.json"))

                # Guardar SVG
                with open(temp_svg, "wb") as buffer:
                    shutil.copyfileobj(svg_file.file, buffer)

                # Guardar JSON
                with open(temp_json, "wb") as buffer:
                    shutil.copyfileobj(json_file.file, buffer)

                # Leer JSON
                instrucciones = json.loads(temp_json.read_text(encoding="utf-8"))

                # Procesar SVG
                resultado_path = Path("resultado.svg")
                if self.queue:
                    self.queue.put("archivo_recibido")
                self.procesar_svg_con_instrucciones(temp_svg, instrucciones, resultado_path)

                return FileResponse(resultado_path, media_type="image/svg+xml", filename=resultado_path.name)
            except Exception as e:
                return JSONResponse({"error": str(e)}, status_code=500)

    def procesar_svg_con_instrucciones(self, svg_path: Path, instrucciones: dict, output_path: Path):
        contenido = svg_path.read_text(encoding="utf-8")
        # Aquí pondrías tu lógica real
        output_path.write_text(contenido, encoding="utf-8")
