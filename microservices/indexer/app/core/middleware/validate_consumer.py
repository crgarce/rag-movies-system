from fastapi import Request, HTTPException
from core.utils.config import Config
from core.utils.logger import get_logger

logger = get_logger("middleware")

async def validate_consumer_id(request: Request, call_next):
    """
    Middleware para validar la Key (Consumer-ID) en las cabeceras.

    :param request: Objeto Request de FastAPI.
    :param call_next: Llamada al siguiente middleware o endpoint.
    :return: Respuesta HTTP.
    :raises HTTPException: Si la Key no es válida.
    """
    consumer_id = request.headers.get("x-consumer-id")
    if consumer_id != Config.CONSUMER_ID:
        logger.warning("Intento de acceso con Consumer-ID inválido.")
        raise HTTPException(status_code=403, detail="Consumer-ID inválido.")

    logger.info("Consumer-ID válido.")
    response = await call_next(request)
    return response
