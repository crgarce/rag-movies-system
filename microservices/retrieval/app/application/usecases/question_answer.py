from typing import List
from app.core.models.models import Movie, Embedding
from app.infra.services.embedding_service import EmbeddingService
from app.infra.repositories.pgvector_repository import PgVectorRepository
from app.infra.services.response_generator import ResponseGenerator
from app.core.utils.logger import get_logger
from fastapi import HTTPException

class QuestionAnswerUseCase:
    """
    Caso de uso para gestionar preguntas y generar respuestas.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        repository: PgVectorRepository,
        response_generator: ResponseGenerator,
        top_k: int = 5
    ):
        """
        Inicializa el caso de uso.

        :param embedding_service: Servicio para generar embeddings.
        :param repository: Repositorio para consultar la base de datos.
        :param response_generator: Servicio para generar respuestas.
        :param top_k: Número máximo de resultados relevantes a recuperar.
        """
        self.embedding_service = embedding_service
        self.repository = repository
        self.response_generator = response_generator
        self.top_k = top_k
        self.logger = get_logger(self.__class__.__name__)

    def execute(self, question: str) -> str:
        """
        Procesa la pregunta y genera una respuesta basada en los datos recuperados.

        :param question: Pregunta del usuario.
        :return: Respuesta generada.
        :raises HTTPException: Si ocurre un error durante el flujo.
        """
        self.logger.info(f"Pregunta recibida: {question}")

        try:
            embedding = self.embedding_service.generate_embedding(question)
            self.logger.debug(f"Embedding generado: {embedding}")
        except Exception as e:
            self.logger.error(f"Error al generar embedding: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al generar el embedding para la pregunta.")

        try:
            movies = self.repository.query_similar_movies(embedding, self.top_k)
            if not movies:
                self.logger.warning("No se encontraron resultados relevantes.")
                return "Lo siento, no encontré información relevante para tu pregunta."
            self.logger.info(f"Películas relevantes encontradas: {[movie.title for movie in movies]}")
        except Exception as e:
            self.logger.error(f"Error al consultar la base de datos: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al consultar la base de conocimiento.")

        try:
            response = self.response_generator.generate_response(question, movies)
            self.logger.info(f"Respuesta generada: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error al generar la respuesta: {str(e)}")
            raise HTTPException(status_code=500, detail="Error al generar la respuesta basada en los datos.")
