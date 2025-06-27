import logging
import azure.functions as func
from PIL import Image, UnidentifiedImageError
from io import BytesIO

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("🟡 Función Azure iniciada: transformación de imagen JPG a TIFF")

    try:
        file_bytes = req.get_body()
        if not file_bytes:
            logging.warning("⚠️ No se recibió ningún cuerpo en la petición")
            return func.HttpResponse(
                "No se ha enviado ninguna imagen",
                status_code=400
            )

        logging.info("📥 Bytes recibidos. Tamaño: %d bytes", len(file_bytes))

        # Intentar abrir la imagen
        try:
            image = Image.open(BytesIO(file_bytes))
        except UnidentifiedImageError:
            logging.warning("🚫 El archivo recibido no es una imagen válida")
            return func.HttpResponse(
                "El archivo recibido no es una imagen válida",
                status_code=415
            )

        # Verificar que sea formato JPEG
        if image.format not in ["JPEG", "JPG"]:
            logging.warning(f"❌ Formato de imagen no compatible: {image.format}")
            return func.HttpResponse(
                "Solo se permiten imágenes en formato JPG",
                status_code=400
            )

        logging.info("🖼️ Imagen JPG cargada correctamente. Formato: %s", image.format)

        # Convertir a TIFF en memoria
        output_stream = BytesIO()
        image.save(output_stream, format='TIFF')
        output_stream.seek(0)

        logging.info("✅ Imagen convertida a TIFF en memoria. Tamaño final: %d bytes", output_stream.getbuffer().nbytes)

        return func.HttpResponse(
            output_stream.read(),
            mimetype="image/tiff",
            status_code=200
        )

    except Exception as e:
        logging.error("❌ Error al procesar la imagen: %s", str(e), exc_info=True)
        return func.HttpResponse(
            f"Error interno del servidor: {str(e)}",
            status_code=500
        )
