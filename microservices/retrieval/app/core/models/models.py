from typing import List
from pydantic import BaseModel, Field

class Movie(BaseModel):
    """
    Modelo que representa una película recuperada de la base de conocimiento.
    """
    title: str = Field(..., description="Título de la película.")
    image: str = Field(..., description="URL de la imagen del póster.")
    plot: str = Field(..., description="Resumen de la trama.")

class Embedding(BaseModel):
    """
    Modelo que representa un vector de embedding.
    """
    vector: List[float] = Field(..., description="Vector numérico del embedding.")
