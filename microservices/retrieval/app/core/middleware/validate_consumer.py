from fastapi import Request, HTTPException
from app.core.utils.config import Config
from app.core.utils.logger import get_logger

logger = get_logger("middleware")

async def validate_consumer_id(request: Request, call_next):
    """
    Middleware para validar la Key (x-consumer-id) en las cabeceras.

    :param request: Objeto Request de FastAPI.
    :param call_next: Llamada al siguiente middleware o endpoint.
    :return: Respuesta HTTP.
    :raises HTTPException: Si la Key no es válida.
    """
    consumer_id = request.headers.get("x-consumer-id")
    if consumer_id != Config.CONSUMER_ID:
        logger.warning("Intento de acceso con x-consumer-id inválido.")
        raise HTTPException(status_code=403, detail="x-consumer-id inválido.")

    logger.debug("x-consumer-id válido.")
    return await call_next(request)
