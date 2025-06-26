import logging
import azure.functions as func
import os
from PIL import Image

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🔔 Función Azure llamada: transformar imagen JPG a TIFF")

    try:
        file_bytes = req.get_body()
        if not file_bytes:
            return func.HttpResponse("No se ha enviado ninguna imagen", status_code=400)

        # === Guardar imagen JPG temporal ===
        input_path = "/tmp/entrada.jpg"
        with open(input_path, "wb") as f:
            f.write(file_bytes)

        # === Convertir a TIFF ===
        output_path = "/tmp/salida.tiff"
        img = Image.open(input_path).convert("RGB")
        img.save(output_path, format="TIFF", compression="tiff_lzw")

        size = os.path.getsize(output_path)

        # === Eliminar archivos temporales ===
        os.remove(input_path)
        os.remove(output_path)

        return func.HttpResponse(
            body=f"""{{
                "nombre_original": "imagen.jpg",
                "formato_salida": "TIFF",
                "procesado_correctamente": true,
                "tamaño_bytes": {size}
            }}""",
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f" Error en la función: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
