import pytest
from mock import MagicMock, patch
from openai.error import OpenAIError
from app.infra.services.response_generator import ResponseGenerator

def test_generate_response_success(mock_response_generator, sample_movies, sample_question):
    """
    Prueba que el servicio genera una respuesta exitosa.
    """
    response = mock_response_generator.generate_response(sample_question, sample_movies)
    assert response == "Esta es una respuesta dummy."


def test_generate_response_openai_error(mock_response_generator, sample_movies, sample_question):
    """
    Prueba que se maneja correctamente un error de OpenAI.
    """
    mock_response_generator.generate_response.side_effect = RuntimeError("Error al generar la respuesta")
    with pytest.raises(RuntimeError) as exc_info:
        mock_response_generator.generate_response(sample_question, sample_movies)
    assert str(exc_info.value) == "Error al generar la respuesta"


def test_generate_response_context(mock_response_generator, sample_movies):
    """
    Prueba que verifica si el contexto generado incluye las películas correctamente.
    """
    question = "¿Qué películas de acción recomiendas?"
    expected_context = "\n".join([
        "- Titulo: Movie 1:\n  Descripción: Plot 1\n  Imagen: http://image1.com",
        "- Titulo: Movie 2:\n  Descripción: Plot 2\n  Imagen: http://image2.com"
    ])
    mock_response_generator.generate_response(question, sample_movies)
    assert "- Titulo: Movie 1" in expected_context
    assert "- Titulo: Movie 2" in expected_context


def test_generate_response_no_movies(mock_response_generator, sample_question):
    """
    Prueba que verifica el comportamiento cuando no hay películas en el contexto.
    """
    empty_movies = []
    response = mock_response_generator.generate_response(sample_question, empty_movies)
    assert response == "Esta es una respuesta dummy."

def test_generate_response_openai_specific_error(mock_response_generator, sample_movies, sample_question):
    """
    Prueba que maneja correctamente un error específico de OpenAI.
    """
    mock_response_generator.generate_response.side_effect = OpenAIError("Error de OpenAI")
    with pytest.raises(OpenAIError) as exc_info:
        mock_response_generator.generate_response(sample_question, sample_movies)
    assert str(exc_info.value) == "Error de OpenAI"


def test_generate_response_empty_question(mock_response_generator, sample_movies):
    """
    Prueba que verifica el comportamiento cuando la pregunta está vacía.
    """
    empty_question = ""
    response = mock_response_generator.generate_response(empty_question, sample_movies)
    assert response == "Esta es una respuesta dummy."


def test_generate_response_logs_with_mock(sample_question, sample_movies):
    """
    Prueba que verifica que el logger se llama correctamente durante la ejecución.
    """
    with patch("app.infra.services.response_generator.get_logger") as mock_logger:
        response_generator = ResponseGenerator(api_key="mocked-api-key", model="mocked-model")
        with patch("openai.ChatCompletion.create",
                    return_value={
                        "choices": [{"message": {"content": "Esta es una respuesta dummy."}}]
                    }):
            response_generator.generate_response(sample_question, sample_movies)
        mock_logger.return_value.info.assert_called_with("Respuesta generada por OpenAI: Esta es una respuesta dummy.")
        mock_logger.return_value.error.assert_not_called()


def test_generate_response_handles_exception(sample_question, sample_movies, caplog):
    """
    Prueba que verifica que las excepciones en generate_response se registran correctamente y se relanzan.
    """
    response_generator = ResponseGenerator(api_key="mocked-api-key", model="mocked-model")

    with patch("openai.ChatCompletion.create", side_effect=OpenAIError("Error en OpenAI")):
        with caplog.at_level("ERROR"):
            with pytest.raises(OpenAIError) as exc_info:
                response_generator.generate_response(sample_question, sample_movies)

    assert "Error al generar la respuesta: Error en OpenAI" in caplog.text
    assert str(exc_info.value) == "Error en OpenAI"
