import pytest
from mock import patch


@pytest.fixture(autouse=True)
def mock_config():
    """
    Mock para las configuraciones globales.
    """
    with patch("app.core.utils.config.Config.CONSUMER_ID", "mocked-consumer-id"):
        yield

@pytest.fixture()
def sample_headers():
    """
    Headers de ejemplo para las pruebas
    """
    return {"x-consumer-id": "mocked-consumer-id", "Content-Type": "application/json"}


def test_health_endpoint(client):
    """
    Prueba el endpoint de salud (/health/).
    """
    headers = {"x-consumer-id": "mocked-consumer-id"}
    response = client.get("/health/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_question_answer_success(client, sample_question, sample_headers):
    """
    Prueba que el endpoint de /question-answer/ genera una respuesta exitosa.
    """
    payload = {"question": sample_question}
    response = client.post("/question-answer/", json=payload, headers=sample_headers)

    assert response.status_code == 200
    assert response.json()["status_code"] == 200
    assert response.json()["message"] == "Respuesta generada con éxito."
    assert response.json()["data"] == "Esta es una respuesta dummy."


def test_question_answer_internal_error(client, sample_question, mock_container, sample_headers):
    """
    Prueba que el endpoint de /question-answer/ maneja errores internos correctamente.
    """
    mock_container.get_question_answer_use_case.return_value.execute.side_effect = RuntimeError("Error interno")

    payload = {"question": sample_question}
    response = client.post("/question-answer/", json=payload, headers=sample_headers)

    assert response.status_code == 500
    assert response.json()["detail"] == "Error interno del servidor."
