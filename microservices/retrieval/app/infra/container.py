from app.core.utils.config import Config
from app.core.utils.logger import get_logger
from app.infra.repositories.pgvector_repository import PgVectorRepository
from app.infra.services.embedding_service import EmbeddingService
from app.infra.services.response_generator import ResponseGenerator
from app.application.usecases.question_answer import QuestionAnswerUseCase

class Container:
    """
    Contenedor para inyectar dependencias en la aplicación.

    Atributos:
        config (Config): Configuraciones globales de la aplicación.
        pg_repository (PgVectorRepository): Repositorio para interactuar con la base de datos.
        embedding_service (EmbeddingService): Servicio para generación de embeddings.
        response_generator (ResponseGenerator): Servicio para generar respuestas.
        question_answer_use_case (QuestionAnswerUseCase): Caso de uso para gestionar preguntas.
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info("Inicializando el contenedor de dependencias.")

        self.config = Config()
        self.logger.info("Configuraciones cargadas exitosamente.")

        self.pg_repository = PgVectorRepository(
            db_host=self.config.DB_HOST,
            db_port=self.config.DB_PORT,
            db_name=self.config.DB_NAME,
            db_user=self.config.DB_USER,
            db_password=self.config.DB_PASSWORD
        )
        self.logger.info("Repositorio de base de datos inicializado.")

        self.embedding_service = EmbeddingService(
            api_key=self.config.OPENAI_API_KEY,
            model=self.config.EMBEDDING_MODEL
        )
        self.logger.info("Servicio de embeddings inicializado.")

        self.response_generator = ResponseGenerator(
            api_key=self.config.OPENAI_API_KEY,
            model=self.config.CHAT_COMPLETION_MODEL
        )
        self.logger.info("Generador de respuestas inicializado.")

        self.question_answer_use_case = QuestionAnswerUseCase(
            embedding_service=self.embedding_service,
            repository=self.pg_repository,
            response_generator=self.response_generator,
            top_k=self.config.TOP_K
        )
        self.logger.info("Caso de uso inicializado.")

    def get_question_answer_use_case(self) -> QuestionAnswerUseCase:
        """
        Retorna el caso de uso para gestionar preguntas y respuestas.
        """
        return self.question_answer_use_case

    def close_resources(self):
        """
        Cierra la conexión a la base de datos gestionada por el contenedor.
        """
        self.logger.info("Cerrando recursos del contenedor...")
        self.pg_repository.close_connection()
        self.logger.info("Recursos cerrados exitosamente.")
