import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Clase para manejar las configuraciones globales del proyecto.

    Carga las configuraciones desde el archivo `.env` y permite
    el acceso a estas como atributos de clase.
    """

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "rag_db")
    DB_USER: str = os.getenv("DB_USER", "ragadmin")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", None)

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", None)
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    CHAT_COMPLETION_MODEL: str = os.getenv("CHAT_COMPLETION_MODEL", "gpt-4")
    TOP_K: int = int(os.getenv("TOP_K", 5))

    CONSUMER_ID: str = os.getenv("CONSUMER_ID", None)

    @staticmethod
    def validate():
        """
        Valida que las variables esenciales estén configuradas correctamente.

        Lanza una excepción si falta alguna configuración crítica.
        """
        if not Config.DB_PASSWORD:
            raise ValueError("DB_PASSWORD no está definida en el archivo .env")
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no está definida en el archivo .env")
        if not Config.CONSUMER_ID:
            raise ValueError("CONSUMER_ID no está definida en el archivo .env")

Config.validate()
