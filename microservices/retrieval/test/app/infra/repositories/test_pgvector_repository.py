import pytest
from app.core.models.models import Movie
from app.infra.repositories.pgvector_repository import PgVectorRepository
from mock import MagicMock, patch


def test_query_similar_movies_success(mock_pgvector_repository, sample_movies, sample_embedding):
    """
    Prueba que el repositorio devuelve las películas más similares correctamente.
    """
    top_k = 2

    result = mock_pgvector_repository.query_similar_movies(sample_embedding, top_k)

    assert len(result) == len(sample_movies)
    assert all(isinstance(movie, Movie) for movie in result)
    assert result[0].title == "Movie 1"
    assert result[1].title == "Movie 2"


def test_query_similar_movies_db_error(mock_pgvector_repository, sample_embedding):
    """
    Prueba que se maneja correctamente un error en la base de datos.
    """
    mock_pgvector_repository.query_similar_movies.side_effect = RuntimeError("Error en la base de datos")

    top_k = 2

    with pytest.raises(RuntimeError) as exc_info:
        mock_pgvector_repository.query_similar_movies(sample_embedding, top_k)

    assert str(exc_info.value) == "Error en la base de datos"

def test_pgvector_connection_success_logs():
    """
    Prueba que verifica que los logs se generan correctamente al conectar exitosamente.
    """
    with patch("app.infra.repositories.pgvector_repository.get_logger") as mock_logger:
        with patch("psycopg2.connect"):
            PgVectorRepository("localhost", 5432, "test_db", "user", "password")
        mock_logger.return_value.info.assert_any_call(
            "Intentando conectar a la base de datos en localhost:5432/test_db"
        )
        mock_logger.return_value.info.assert_any_call(
            "Conexión a la base de datos establecida exitosamente."
        )

def test_pgvector_connection_error_logs():
    """
    Prueba que verifica que los logs registran correctamente los errores al conectar.
    """
    with patch("app.infra.repositories.pgvector_repository.get_logger") as mock_logger:
        with patch("psycopg2.connect", side_effect=Exception("Error al conectar")):
            with pytest.raises(Exception, match="Error al conectar"):
                PgVectorRepository("localhost", 5432, "test_db", "user", "password")
        mock_logger.return_value.error.assert_called_with(
            "Error al conectar a la base de datos: Error al conectar"
        )


def test_pgvector_get_cursor_logs():
    """
    Prueba que verifica que los logs se generan correctamente al usar un cursor.
    """
    with patch("app.infra.repositories.pgvector_repository.get_logger") as mock_logger:
        with patch("psycopg2.connect") as mock_connect:
            mock_cursor = MagicMock()
            mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
            repository = PgVectorRepository("localhost", 5432, "test_db", "user", "password")
            with repository.get_cursor() as cursor:
                assert cursor == mock_cursor
            mock_logger.return_value.error.assert_not_called()


def test_pgvector_get_cursor_error_logs():
    """
    Prueba que verifica que los errores al manejar un cursor se registran correctamente.
    """
    with patch("app.infra.repositories.pgvector_repository.get_logger") as mock_logger:
        with patch("psycopg2.connect") as mock_connect:
            mock_connect.return_value.cursor.side_effect = Exception("Error en el cursor")
            repository = PgVectorRepository("localhost", 5432, "test_db", "user", "password")
            with pytest.raises(RuntimeError, match="Error en la base de datos."):
                with repository.get_cursor():
                    pass
            mock_logger.return_value.error.assert_called_with(
                "Error al manejar el cursor: Error en el cursor"
            )

def test_pgvector_del_logs():
    """
    Prueba que verifica que el destructor cierra la conexión correctamente.
    """
    with patch("app.infra.repositories.pgvector_repository.get_logger") as mock_logger:
        with patch("psycopg2.connect") as mock_connect:
            mock_connection = mock_connect.return_value
            repository = PgVectorRepository("localhost", 5432, "test_db", "user", "password")
            del repository
            mock_connection.close.assert_called_once()
            mock_logger.return_value.info.assert_called_with(
                "Conexión a la base de datos cerrada exitosamente."
            )
