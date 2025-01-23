import os
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from app.infrastructure.db.pgvector_repository import PGVectorRepository
from app.infrastructure.openai.embedding_service import generate_embedding
from app.infrastructure.logger.logger import get_logger
from app.infrastructure.utils.tools import normalize_embedding

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logger = get_logger()

def process_batch(batch):
    """
    Procesa un lote de filas del DataFrame para generar embeddings y normalizarlos.

    Args:
        batch (pd.DataFrame): Lote de datos.

    Returns:
        list: Lista de tuplas con los datos procesados (título, trama, imagen, embedding).
    """
    try:
        combined_texts = [f"{row['title']}. {row['plot']}. {row['image']}" for _, row in batch.iterrows()]
        titles = [row['title'] for _, row in batch.iterrows()]
        plots = [row['plot'] for _, row in batch.iterrows()]
        images = [row['image'] for _, row in batch.iterrows()]

        embeddings = generate_embedding(combined_texts)
        normalized_embeddings = [normalize_embedding(embedding) for embedding in embeddings]

        return [(title, plot, image, embedding.tolist()) for title, plot, image, embedding in zip(titles, plots, images, normalized_embeddings)]
    except Exception as e:
        logger.error(f"Error processing batch: {e}")
        return []

def index_embeddings():
    """
    Procesa un archivo CSV para generar embeddings y almacenarlos en la base de datos.

    Pasos:
    1. Verifica la existencia del archivo CSV.
    2. Lee el archivo CSV en un DataFrame de pandas.
    3. Elimina filas con valores nulos en las columnas 'title', 'plot' e 'image'.
    4. Divide el DataFrame en lotes y procesa cada lote en paralelo.
    5. Inserta los embeddings generados en la base de datos.

    Manejo de errores:
    - FileNotFoundError: Si el archivo CSV no se encuentra.
    - pd.errors.EmptyDataError: Si el archivo CSV está vacío.
    - Exception: Para cualquier otro error durante el procesamiento.
    """
    csv_file = os.path.join(BASE_DIR, "../data/movies-dataset-min.csv")
    # csv_file = os.path.join(BASE_DIR, "../data/movies-dataset.csv")
    repository = PGVectorRepository()

    if not os.path.exists(csv_file):
        logger.error("CSV file not found.")
        raise FileNotFoundError("CSV file not found.")

    try:
        movies_df = pd.read_csv(csv_file)
        movies_df = movies_df.dropna(subset=['title', 'plot', 'image'])

        batch_size = 10
        batches = [movies_df[i:i + batch_size] for i in range(0, len(movies_df), batch_size)]

        processed_batches = 0
        total_batches = len(batches)

        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_batch = {executor.submit(process_batch, batch): batch for batch in batches}
            for future in as_completed(future_to_batch):
                try:
                    batch_result = future.result()
                    if batch_result:
                        repository.insert_batch(batch_result)
                        processed_batches += 1
                        logger.info(f"Lote procesado e insertado {processed_batches}/{total_batches}")
                except Exception as exc:
                    logger.error(f"El procesamiento del lote generó una excepción: {exc}")

        logger.info("Indexación completada exitosamente.")
    except FileNotFoundError as fnf_error:
        logger.error(f"Error de archivo no encontrado: {fnf_error}")
    except pd.errors.EmptyDataError as ede_error:
        logger.error(f"Error de datos vacíos en el CSV: {ede_error}")
    except Exception as e:
        logger.error(f"Ocurrió un error al procesar los embeddings: {e}")
        raise
