from core.utils.config import Config
from infra.repositories.pgvector_repository import PgVectorRepository
from infra.services.embedding_service import EmbeddingService
from infra.services.csv_processor import CsvProcessor
from application.usecases.index_embeddings import IndexEmbeddingsUseCase

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
        self.config = Config()

        self.pg_repository = PgVectorRepository(
            db_host=self.config.DB_HOST,
            db_port=self.config.DB_PORT,
            db_name=self.config.DB_NAME,
            db_user=self.config.DB_USER,
            db_password=self.config.DB_PASSWORD,
        )

        self.embedding_service = EmbeddingService(
            api_key=self.config.OPENAI_API_KEY,
            model=self.config.EMBEDDING_MODEL,
        )

        self.csv_processor = CsvProcessor()

        self.index_embeddings_use_case = IndexEmbeddingsUseCase(
            embedding_service=self.embedding_service,
            repository=self.pg_repository,
            batch_size=self.config.BATCH_SIZE,
        )

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
        Cierra la conexion a la bd gestionada por el contenedor.
        """
        self.pg_repository.close_connection()
