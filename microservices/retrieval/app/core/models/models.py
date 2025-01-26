from pydantic import BaseModel, Field
from typing import List

class Movie(BaseModel):
    """
    Modelo que representa un registro de una película en el sistema.
    """
    title: str = Field(..., description="Título de la película.")
    image: str = Field(..., description="URL de la imagen del póster de la película.")
    plot: str = Field(..., description="Resumen de la trama de la película.")

class Embedding(BaseModel):
    """
    Modelo que representa un vector de embedding generado para un texto.
    """
    vector: List[float] = Field(..., description="Vector numérico del embedding.")
    content: str = Field(..., description="Texto que generó este embedding.")

class MovieWithEmbedding(BaseModel):
    """
    Modelo que combina un registro de película con su correspondiente embedding.
    """
    movie: Movie = Field(..., description="Información de la película.")
    embedding: Embedding = Field(..., description="Embedding asociado con la película.")
