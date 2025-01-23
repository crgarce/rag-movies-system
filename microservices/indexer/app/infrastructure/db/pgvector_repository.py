import os
import psycopg2
from app.infrastructure.logger.logger import get_logger

logger = get_logger()

class PGVectorRepository:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=os.getenv("DB_PORT", 5432)
            )
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            logger.error(f"Error al conectar a la base de datos: {e}")
            raise

    def insert(self, row):
        """
        Inserta un solo registro en la base de datos.

        Args:
            row (obj): Objeto con los atributos title, content, image y embedding.
        """
        try:
            with self.connection.cursor() as cursor:
                query = """
                    INSERT INTO movies (title, content, image, embedding)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (row.title, row.content, row.image, row.embedding))
            self.connection.commit()
            logger.info("Registro insertado correctamente.")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error al insertar el registro: {e}")
            raise

    def insert_batch(self, batch_data):
        """
        Inserta múltiples documentos en la base de datos en una sola transacción.

        Args:
            batch_data (list): Lista de tuplas con datos (title, content, image, embedding).
        """
        try:
            query = """
                INSERT INTO movies (title, content, image, embedding)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.executemany(query, batch_data)
            self.connection.commit()
            logger.info(f"Se insertaron {len(batch_data)} registros en la base de datos.")
        except psycopg2.Error as e:
            self.connection.rollback()
            logger.error(f"Error al insertar el lote en la base de datos: {e}")
            raise
