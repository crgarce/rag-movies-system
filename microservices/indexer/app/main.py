from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.infra.container import Container
from app.core.utils.logger import get_logger
from app.core.middleware.validate_consumer import validate_consumer_id

app = FastAPI()
logger = get_logger("main")

app.middleware("http")(validate_consumer_id)

container = Container()

@app.get("/health/")
async def health():
    """
    Endpoint para verificar la salud del servicio.

    :return: Respuesta con el estado del servicio.
    """
    return {"status": "OK"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Manejador global para excepciones no controladas.
    Desempaqueta ExceptionGroup si es necesario.
    """
    if isinstance(exc, ExceptionGroup):
        logger.error(f"Se capturó un ExceptionGroup: {exc}")
        for inner_exc in exc.exceptions:
            if isinstance(inner_exc, HTTPException):
                return await http_exception_handler(request, inner_exc)
    elif isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)

    logger.error(f"Error inesperado: {exc} en {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Por favor contacte al administrador."},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manejador para excepciones HTTP controladas.
    """
    logger.warning(f"HTTPException: {exc.detail} en {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

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
