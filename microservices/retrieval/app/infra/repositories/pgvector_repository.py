from typing import List
from contextlib import contextmanager
import psycopg2
from app.core.utils.logger import get_logger
from app.core.models.models import Movie


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
        Proporciona un cursor gestionado con cierre automático.
        """
        try:
            with self.connection.cursor() as cursor:
                yield cursor
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Error al manejar el cursor: {str(e)}")
            raise RuntimeError("Error en la base de datos.") from e

    def query_similar_movies(self, embedding: List[float], top_k: int) -> List[Movie]:
        """
        Consulta las películas más similares utilizando similitud vectorial. <->

        :param embedding: Embedding de la pregunta.
        :param top_k: Número máximo de resultados relevantes a recuperar.
        :return: Lista de objetos Movie con los resultados más relevantes.
        """
        query = """
        SELECT title, image, plot
        FROM movies
        ORDER BY embedding <-> %s::vector
        LIMIT %s;
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, (embedding, top_k))
                results = cursor.fetchall()
                self.logger.info(f"Películas encontradas: {len(results)}")
                return [
                    Movie(title=row[0], image=row[1], plot=row[2])
                    for row in results
                ]
        except Exception as e:
            self.logger.error(f"Error al consultar películas: {str(e)}")
            raise RuntimeError("Error al realizar la consulta en la base de datos.") from e

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
