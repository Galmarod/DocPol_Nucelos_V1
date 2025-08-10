# worker/processor.py
import os
import subprocess
import tempfile
from google.cloud import storage

# ⚠️ Si quieres usar tu propia lógica de modificación SVG, impórtala aquí
# from controller.modifySvg import process_svg

GCS_BUCKET = os.environ.get("RESULTS_BUCKET")

def run_inkscape(input_svg_path: str, output_path: str, export_format: str = "pdf") -> str:
    cmd = ["inkscape", input_svg_path, f"--export-type={export_format}", "--export-filename", output_path]
    subprocess.check_call(cmd)
    return output_path

def upload_to_gcs(local_path: str, dest_blob: str):
    client = storage.Client()
    bucket_name = GCS_BUCKET
    if not bucket_name:
        raise RuntimeError("RESULTS_BUCKET no está configurado")
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(dest_blob)
    blob.upload_from_filename(local_path)
    return blob.public_url

def handle_task(payload: dict):
    svg_path = payload.get("svg_path")
    export_format = payload.get("export_format", "pdf")

    if not svg_path:
        raise ValueError("svg_path es requerido en la tarea")

    with tempfile.TemporaryDirectory() as tmp:
        processed_svg = svg_path  # Aquí podrías llamar a process_svg() si quieres modificarlo
        out_file = os.path.join(tmp, f"result.{export_format}")
        run_inkscape(processed_svg, out_file, export_format=export_format)

        # Si no quieres usar GCS en pruebas locales, devuelves el path local
        if not GCS_BUCKET:
            return {"local_path": out_file}

        public_url = upload_to_gcs(out_file, os.path.basename(out_file))
    return {"gcs_url": public_url}
