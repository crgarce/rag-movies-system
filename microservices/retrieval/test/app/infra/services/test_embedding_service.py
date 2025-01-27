import pytest
from mock import patch
from app.infra.services.embedding_service import EmbeddingService
from openai.error import OpenAIError

def test_embedding_service_initialization():
    """
    Prueba que verifica que la inicialización de EmbeddingService es correcta.
    """
    service = EmbeddingService(api_key="test-api-key", model="test-model")
    assert service.api_key == "test-api-key"
    assert service.model == "test-model"
    assert service.logger.name == "EmbeddingService"


def test_generate_embedding_logs_with_mock_success(sample_question):
    """
    Prueba que verifica que el logger registra correctamente un embedding exitoso.
    """
    with patch("app.infra.services.embedding_service.get_logger") as mock_logger:
        service = EmbeddingService(api_key="mocked-api-key", model="mocked-model")
        with patch("openai.Embedding.create", 
                    return_value={"data": [{"embedding": [0.1, 0.2, 0.3]}]}):
            result = service.generate_embedding("Texto de prueba")
            assert result == [0.1, 0.2, 0.3]
        mock_logger.return_value.info.assert_called_with(
            "Embedding generado exitosamente: [0.1, 0.2, 0.3]"
        )
        mock_logger.return_value.warning.assert_not_called()
        mock_logger.return_value.error.assert_not_called()


def test_generate_embedding_success(mock_embedding_service):
    """
    Prueba que el servicio genera un embedding exitosamente.
    """
    result = mock_embedding_service.generate_embedding("Este es un texto de prueba")
    assert result == [0.1, 0.2, 0.3]


def test_generate_embedding_empty_text(mock_embedding_service):
    """
    Prueba que se lanza un error cuando el texto está vacío.
    """
    with pytest.raises(ValueError) as exc_info:
        mock_embedding_service.generate_embedding("")
    assert str(exc_info.value) == "El texto esta vacio. No se pueden generar embeddings."


def test_generate_embedding_openai_error(mock_embedding_service):
    """
    Prueba que se maneja correctamente un error de la API de OpenAI.
    """
    mock_embedding_service.generate_embedding.side_effect = RuntimeError("Error al generar embeddings: Error en OpenAI")
    with pytest.raises(RuntimeError) as exc_info:
        mock_embedding_service.generate_embedding("Texto que causa error")
    assert str(exc_info.value) == "Error al generar embeddings: Error en OpenAI"
