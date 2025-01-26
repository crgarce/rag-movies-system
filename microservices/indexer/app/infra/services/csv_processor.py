import pandas as pd
from io import StringIO
from fastapi import HTTPException
from app.core.models.models import Movie
from app.core.utils.logger import get_logger

class CsvProcessor:
    """
    Servicio para procesar archivos CSV y convertirlos a objetos del dominio.
    """

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def process_csv(self, file) -> list[Movie]:
        """
        Procesa un archivo CSV y lo convierte en una lista de objetos Movie.

        :param file: Archivo CSV subido por el usuario.
        :return: Lista de instancias de Movie.
        :raises HTTPException: Si el archivo tiene errores o no cumple con los requisitos.
        """
        self.logger.info(f"Procesando archivo CSV: {file.filename}")

        if not file.filename.endswith(".csv"):
            self.logger.error("El archivo no es un CSV.")
            raise HTTPException(status_code=400, detail="El archivo debe ser un CSV.")

        try:
            contents = file.file.read().decode("utf-8")
            df = pd.read_csv(StringIO(contents), encoding="utf-8-sig")

            required_columns = {"title", "image", "plot"}
            if not required_columns.issubset(df.columns):
                self.logger.error("Faltan columnas requeridas en el archivo CSV.")
                raise HTTPException(
                    status_code=400,
                    detail="El archivo CSV debe contener las columnas: title, image, plot."
                )

            movies = [
                Movie(title=row["title"], image=row["image"], plot=row["plot"])
                for _, row in df.iterrows()
            ]
            self.logger.info(f"Archivo procesado exitosamente. Registros: {len(movies)}")
            return movies

        except Exception as e:
            self.logger.error(f"Error al procesar el archivo CSV: {e}")
            raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")
