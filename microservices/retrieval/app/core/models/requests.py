from pydantic import BaseModel

class QuestionRequest(BaseModel):
    """
    Modelo de entrada para el endpoint de preguntas.
    """
    question: str
