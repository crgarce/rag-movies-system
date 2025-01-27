import pytest
from mock import MagicMock, patch
from app.core.models.models import Movie
from app.application.usecases.question_answer import QuestionAnswerUseCase
from fastapi.testclient import TestClient
from app.main import app
from app.core.utils.config import Config


@pytest.fixture
def mock_embedding_service():
    """
    Mock para el servicio de embeddings.
    Simula la generación de embeddings a partir de texto.
    """
    with patch("app.infra.services.embedding_service.EmbeddingService") as MockEmbeddingService:
        embedding_service = MockEmbeddingService(api_key="fake-key", model="text-embedding-ada-002")

        def generate_embedding_side_effect(text):
            if not text:
                raise ValueError("El texto esta vacio. No se pueden generar embeddings.")
            return [0.1, 0.2, 0.3]

        embedding_service.generate_embedding.side_effect = generate_embedding_side_effect
        yield embedding_service


@pytest.fixture
def mock_pgvector_repository():
    """
    Mock para el repositorio de PGVector.
    Simula las operaciones de consulta en la base de datos.
    """
    repository = MagicMock()
    repository.query_similar_movies.return_value = [
        Movie(title="Movie 1", image="http://image1.com", plot="Plot 1"),
        Movie(title="Movie 2", image="http://image2.com", plot="Plot 2"),
    ]
    return repository


@pytest.fixture(autouse=True)
def mock_pgvector_connection():
    """
    Mockea la conexión de PgVectorRepository para evitar conexiones reales a la base de datos.
    """
    with patch("app.infra.repositories.pgvector_repository.psycopg2.connect") as mock_connect:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()

        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_connection

        yield mock_connect


@pytest.fixture
def mock_response_generator():
    """
    Mock para el generador de respuestas.
    Simula la generación de respuestas usando OpenAI.
    """
    response_generator = MagicMock()
    response_generator.generate_response = MagicMock(return_value="Esta es una respuesta dummy.")
    return response_generator


@pytest.fixture
def question_answer_use_case(mock_embedding_service, mock_pgvector_repository, mock_response_generator):
    """
    Caso de uso para pruebas, inyectando dependencias mockeadas.
    """
    return QuestionAnswerUseCase(
        embedding_service=mock_embedding_service,
        repository=mock_pgvector_repository,
        response_generator=mock_response_generator,
        top_k=2
    )


@pytest.fixture
def sample_question():
    """
    Pregunta de prueba para las pruebas unitarias.
    """
    return "CUal es la pelicula de un zorro y una espada?"


@pytest.fixture
def sample_movies():
    """
    Lista de películas simuladas para las pruebas.
    """
    return [
        Movie(title="Movie 1", image="http://image1.com", plot="Plot 1"),
        Movie(title="Movie 2", image="http://image2.com", plot="Plot 2")
    ]


@pytest.fixture
def sample_embedding():
    """
    Embedding de prueba para las pruebas unitarias.
    """
    return [0.1, 0.2, 0.3]


@pytest.fixture
def mock_container(mock_embedding_service, mock_pgvector_repository, mock_response_generator):
    """
    Mock del contenedor con dependencias simuladas.
    """
    container = MagicMock()
    container.embedding_service = mock_embedding_service
    container.pg_repository = mock_pgvector_repository
    container.response_generator = mock_response_generator

    mock_use_case = MagicMock()
    mock_use_case.execute = MagicMock(return_value="Esta es una respuesta dummy.")
    container.get_question_answer_use_case.return_value = mock_use_case

    return container




@pytest.fixture
def client(mock_container):
    """
    Cliente de prueba para interactuar con los endpoints de FastAPI.
    """
    with patch("app.main.Container", return_value=mock_container):
        yield TestClient(app)
