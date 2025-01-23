import numpy as np

def normalize_embedding(embedding):
    """
    Normaliza un vector usando la norma L2.

    La normalización L2 escala el vector de tal manera que la suma de los cuadrados de sus componentes sea igual a 1.
    Esto se logra dividiendo cada componente del vector por la norma L2 del vector.

    Args:
        embedding (numpy.ndarray): Vector a normalizar.

    Returns:
        numpy.ndarray: Vector normalizado.
    """
    embedding = np.array(embedding)
    norm = np.linalg.norm(embedding)
    return embedding / norm if norm != 0 else embedding
