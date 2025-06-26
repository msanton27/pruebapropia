import logging
import azure.functions as func
from PIL import Image
from io import BytesIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("⚠️ Función Azure llamada: transformar imagen JPG a TIFF")

    try:
        file_bytes = req.get_body()
        if not file_bytes:
            return func.HttpResponse(
                "No se ha enviado ninguna imagen",
                status_code=400
            )

        # Cargar imagen JPG desde los bytes recibidos
        image = Image.open(BytesIO(file_bytes))

        # Convertir a TIFF en memoria
        output_stream = BytesIO()
        image.save(output_stream, format='TIFF')
        output_stream.seek(0)

        # Devolver la imagen TIFF como binario
        return func.HttpResponse(
            output_stream.read(),
            mimetype="image/tiff",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error al procesar imagen: {e}")
        return func.HttpResponse(
            f"Error interno: {str(e)}",
            status_code=500
        )
