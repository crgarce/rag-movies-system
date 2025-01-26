from typing import List
import openai
from app.core.utils.logger import get_logger
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
    def generate_embeddings(self, texts: List[str]) -> List[dict]:
        """
        Genera embeddings para una lista de textos.

        :param texts: Lista de textos para generar embeddings.
        :return: Lista de diccionarios con los embeddings generados.
        :raises ValueError: Si la lista de textos está vacía.
        :raises RuntimeError: Si ocurre un error con la API de OpenAI.
        """
        if not texts:
            self.logger.warning("Se intentó generar embeddings con una lista vacía.")
            raise ValueError("La lista de textos está vacía. No se pueden generar embeddings.")

        openai.api_key = self.api_key
        max_batch_size = 100
        results = []

        try:
            for i in range(0, len(texts), max_batch_size):
                batch = texts[i:i + max_batch_size]
                self.logger.info(f"Generando embeddings para un batch de {len(batch)} textos...")
                response = openai.Embedding.create(
                    model=self.model,
                    input=batch
                )
                results.extend(response["data"])
                self.logger.info(f"Batch procesado exitosamente. Tamaño del batch: {len(batch)}")

            self.logger.info("Embeddings generados exitosamente.")
            return results

        except openai.error.OpenAIError as e:
            self.logger.error(f"Error al generar embeddings: {str(e)}")
            raise RuntimeError(f"Error al generar embeddings: {str(e)}")
