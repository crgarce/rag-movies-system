import os
import openai
from app.infrastructure.logger.logger import get_logger

openai.api_key = os.getenv("OPENAI_API_KEY")
logger = get_logger()

def generate_embedding(text: str) -> list:
    """
    Genera un embedding para el texto proporcionado utilizando el modelo de OpenAI.

    Args:
        text (str): El texto para el cual se generará el embedding.

    Returns:
        list: Una lista que representa el embedding generado. Si ocurre un error, se devuelve una lista vacía.
    """
    try:
        logger.info("Generando embedding para el texto: %s", text)
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response["data"][0]["embedding"]
        logger.info("Embedding generado exitosamente")
        return embedding
    except openai.error.OpenAIError as e:
        logger.error(f"Error de OpenAI al generar el embedding: {e}")
        return []
    except Exception as e:
        logger.error(f"Error al generar el embedding: {e}")
        return []
