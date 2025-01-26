from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from app.infra.container import Container
from app.core.utils.logger import get_logger
from app.core.middleware.validate_consumer import validate_consumer_id

app = FastAPI()
logger = get_logger("main")
container = Container()

app.middleware("http")(validate_consumer_id)

@app.post("/movies-indexer/")
async def movies_indexer(file: UploadFile = File(...)):
    """
    Endpoint para subir un archivo CSV con información de películas.

    :param file: Archivo CSV subido por el usuario.
    :return: Respuesta con el resultado del procesamiento.
    """
    try:
        csv_processor = container.get_csv_processor()
        movies = csv_processor.process_csv(file)

        use_case = container.get_index_embeddings_use_case()
        use_case.execute(movies)

        return {
            "status_code": 200,
            "message": f"Archivo procesado exitosamente. Se indexaron {len(movies)} películas."
        }

    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail}

    except Exception as e:
        logger.error(f"Error inesperado al procesar el archivo: {e}")
        return {
            "status_code": 500,
            "message": "Error interno del servidor. Por favor contacte al administrador."
        }
