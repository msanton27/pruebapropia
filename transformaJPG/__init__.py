import logging
import azure.functions as func
from PIL import Image
from io import BytesIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🟡 Función Azure iniciada: transformación de imagen JPG a TIFF")

    try:
        file_bytes = req.get_body()
        logging.info("📥 Bytes recibidos. Tamaño: %d bytes", len(file_bytes))

        if not file_bytes:
            logging.warning("⚠️ No se recibió ningún cuerpo en la petición")
            return func.HttpResponse(
                "No se ha enviado ninguna imagen",
                status_code=400
            )

        image = Image.open(BytesIO(file_bytes))
        logging.info("🖼️ Imagen JPG cargada correctamente")

        output_stream = BytesIO()
        image.save(output_stream, format='TIFF')
        output_stream.seek(0)
        logging.info("✅ Imagen convertida a TIFF en memoria")

        return func.HttpResponse(
            output_stream.read(),
            mimetype="image/tiff",
            status_code=200
        )

    except Exception as e:
        logging.error(f"❌ Error al procesar la imagen: {e}", exc_info=True)
        return func.HttpResponse(
            f"Error interno: {str(e)}",
            status_code=500
        )
