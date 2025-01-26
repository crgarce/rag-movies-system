from typing import List
import openai
from core.utils.logger import get_logger
from tenacity import retry, stop_after_attempt, wait_exponential

class EmbeddingService:
    """
    Servicio para generar embeddings usando la API de OpenAI.
    """

    def __init__(self, api_key: str, model: str):
        """
        Inicializa el servicio con las configuraciones necesarias.

        :param api_key: Clave de la API de OpenAI.
        :param model: Modelo de OpenAI a utilizar para generar embeddings.
        """
        self.api_key = api_key
        self.model = model
        self.logger = get_logger(self.__class__.__name__)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_embedding(self, text: str) -> List[float]:
        """
        Genera un embedding para un texto dado.

        :param text: Texto para generar el embedding.
        :return: Embedding generado.
        """
        if not text:
            self.logger.warning("Se intentó generar embeddings con un texto vacio")
            raise ValueError("El texto esta vacio. No se pueden generar embeddings.")

        openai.api_key = self.api_key
        try:
            response = openai.Embedding.create(
                model=self.model,
                input=text
            )
            embedding = response["data"][0]["embedding"]
            self.logger.info(f"Embedding generado exitosamente: {embedding}")
            return embedding
        except openai.error.OpenAIError as e:
            self.logger.error(f"Error al generar embeddings: {str(e)}")
            raise RuntimeError(f"Error al generar embeddings: {str(e)}")
