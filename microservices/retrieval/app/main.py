from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.core.models.requests import QuestionRequest
from app.infra.container import Container
from app.core.middleware.validate_consumer import validate_consumer_id
from app.core.utils.logger import get_logger

app = FastAPI()
logger = get_logger("main")

app.middleware("http")(validate_consumer_id)

def get_container():
    return Container()

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

    :param request: Objeto Request de FastAPI.
    :param exc: Excepción capturada.
    :return: Respuesta HTTP con mensaje genérico.
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

    :param request: Objeto Request de FastAPI.
    :param exc: Excepción HTTP.
    :return: Respuesta HTTP con código de estado y detalle.
    """
    logger.warning(f"HTTPException: {exc.detail} en {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.post("/question-answer/")
async def question_answer(payload: QuestionRequest, container: Container = Depends(get_container)):
    """
    Endpoint principal para responder preguntas basadas en la base de conocimiento.

    :param request: Objeto Request de FastAPI.
    :param question: Pregunta enviada por el usuario.
    :return: Respuesta generada.
    """
    try:
        question = payload.question
        logger.info(f"Pregunta recibida: {question}")
        use_case = container.get_question_answer_use_case()
        response = use_case.execute(question)
        return {"status_code": 200, "message": "Respuesta generada con éxito.", "data": response}
    except HTTPException as e:
        return {"status_code": e.status_code, "message": e.detail}

    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")
