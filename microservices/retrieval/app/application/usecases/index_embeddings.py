from typing import List
from app.core.models.models import Movie, Embedding, MovieWithEmbedding
from app.core.utils.logger import get_logger

class IndexEmbeddingsUseCase:
    """
    Caso de uso para generar e indexar embeddings en la base de datos.
    """

    def __init__(self, embedding_service, repository, batch_size: int = 10):
        """
        Inicializa el caso de uso con el servicio de embeddings y el repositorio.

        :param embedding_service: Servicio para generar embeddings.
        :param repository: Repositorio para interactuar con la base de datos.
        :param batch_size: Tamaño del lote para procesar los registros.
        """
        self.embedding_service = embedding_service
        self.repository = repository
        self.batch_size = batch_size
        self.logger = get_logger(self.__class__.__name__)

    def execute(self, movies: List[Movie]) -> None:
        """
        Genera e indexa los embeddings para una lista de películas.

        :param movies: Lista de instancias de Movie que contienen los datos a procesar.
        """
        self.logger.info(f"Iniciando el proceso de indexación para {len(movies)} películas.")

        for i in range(0, len(movies), self.batch_size):
            batch = movies[i:i + self.batch_size]
            self.logger.info(f"Procesando lote {i // self.batch_size + 1} \
            con {len(batch)} películas.")

            texts_to_embed = [
                f"Title: {movie.title}. Image: {movie.image}. Plot: {movie.plot}"
                for movie in batch
            ]

            try:
                embeddings_data = self.embedding_service.generate_embeddings(texts_to_embed)

                movies_with_embeddings = [
                    MovieWithEmbedding(
                        movie=movie,
                        embedding=Embedding(
                            vector=embedding_data["embedding"],
                            content=texts_to_embed[i]
                        )
                    )
                    for i, (movie, embedding_data) in enumerate(zip(batch, embeddings_data))
                ]

                self.repository.save_batch(movies_with_embeddings)
                self.logger.info(f"Lote {i // self.batch_size + 1} indexado exitosamente.")

            except Exception as e:
                self.logger.error(f"Error al procesar el lote {i // self.batch_size + 1}: {str(e)}")
                raise

        self.logger.info("El proceso de indexación ha finalizado exitosamente.")
