from app.core.utils.config import Config
from app.core.utils.logger import get_logger
from app.infra.repositories.pgvector_repository import PgVectorRepository
from app.infra.services.embedding_service import EmbeddingService
from app.infra.services.csv_processor import CsvProcessor
from app.application.usecases.index_embeddings import IndexEmbeddingsUseCase

class Container:
    """
    Contenedor para inyectar dependencias en la aplicación.

    Atributos:
        config (Config): Configuraciones globales de la aplicación.
        pg_repository (PgVectorRepository): Repositorio para interactuar con la base de datos.
        embedding_service (EmbeddingService): Servicio para generación de embeddings.
        index_embeddings_use_case (IndexEmbeddingsUseCase): Caso de uso para indexar películas.
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
            db_password=self.config.DB_PASSWORD,
        )
        self.logger.info("Repositorio de base de datos inicializado.")

        self.embedding_service = EmbeddingService(
            api_key=self.config.OPENAI_API_KEY,
            model=self.config.EMBEDDING_MODEL,
        )
        self.logger.info("Servicio de embeddings inicializado.")

        self.csv_processor = CsvProcessor()
        self.logger.info("Servicio de procesamiento de CSV inicializado.")

        self.index_embeddings_use_case = IndexEmbeddingsUseCase(
            embedding_service=self.embedding_service,
            repository=self.pg_repository,
            batch_size=self.config.BATCH_SIZE,
        )
        self.logger.info("Caso de uso para indexar embeddings inicializado.")

    def get_csv_processor(self):
        """
        Retorna el procesador de archivos CSV.
        """
        return self.csv_processor

    def get_index_embeddings_use_case(self):
        """
        Retorna el caso de uso para indexar los embeddings.
        """
        return self.index_embeddings_use_case

    def close_resources(self):
        """
        Cierra la conexión a la base de datos gestionada por el contenedor.
        """
        self.logger.info("Cerrando recursos del contenedor...")
        self.pg_repository.close_connection()
        self.logger.info("Recursos cerrados exitosamente.")
