from typing import List
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import execute_values
from core.utils.logger import get_logger
from core.models.models import MovieWithEmbedding


class PgVectorRepository:
    """
    Repositorio para interactuar con la base de datos PostgreSQL usando PGVector.
    
    Gestiona la inserción y recuperación de datos relacionados con embeddings.
    """

    def __init__(self, db_host: str, db_port: int, db_name: str, db_user: str, db_password: str):
        """
        Inicializa la conexión a la base de datos PostgreSQL.

        :param db_host: Host de la base de datos.
        :param db_port: Puerto de la base de datos.
        :param db_name: Nombre de la base de datos.
        :param db_user: Usuario de la base de datos.
        :param db_password: Contraseña de la base de datos.
        """
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info(f"Intentando conectar a la base de datos en {db_host}:{db_port}/{db_name}")
        try:
            self.connection = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_password
            )
            self.logger.info("Conexión a la base de datos establecida exitosamente.")
        except Exception as e:
            self.logger.error(f"Error al conectar a la base de datos: {e}")
            raise

    @contextmanager
    def get_cursor(self):
        """
        Proporciona un cursor de base de datos gestionado en un contexto.
        """
        try:
            with self.connection.cursor() as cursor:
                yield cursor
            self.connection.commit()
            self.logger.info("Transacción de base de datos completada exitosamente.")
        except Exception as e:
            self.connection.rollback()
            raise RuntimeError(f"Error en la base de datos: {str(e)}")

    def save_batch(self, movies_with_embeddings: List[MovieWithEmbedding]) -> None:
        """
        Inserta un lote de películas con sus embeddings en la base de datos.

        :param movies_with_embeddings: Lista de objetos MovieWithEmbedding.
        """
        insert_query = """
        INSERT INTO movies (title, image, plot, embedding)
        VALUES %s
        """

        values = [
            (
                movie_with_embedding.movie.title,
                movie_with_embedding.movie.image,
                movie_with_embedding.movie.plot,
                movie_with_embedding.embedding.vector
            )
            for movie_with_embedding in movies_with_embeddings
        ]
        self.logger.info(f"Insertando {len(values)} registros en la base de datos...")
        try:
            with self.get_cursor() as cursor:
                execute_values(cursor, insert_query, values)
        except Exception as e:
            self.logger.error(f"Error al insertar el lote: {str(e)}")
            raise

    def close_connection(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.connection:
            self.connection.close()
            self.logger.info("Conexión a la base de datos cerrada exitosamente.")

    def __del__(self):
        """
        Asegura que la conexión se cierre correctamente al destruir la instancia.
        """
        self.close_connection()
