import pytest
from fastapi import HTTPException
from app.application.usecases.question_answer import QuestionAnswerUseCase


@pytest.mark.parametrize(
    "question, expected_response",
    [
        ("¿Cuál es la mejor película de acción?", "Esta es una respuesta dummy."),
        ("¿Qué películas de comedia recomiendas?", "Esta es una respuesta dummy."),
    ],
)
def test_question_answer_success(question, expected_response, question_answer_use_case):
    """
    Prueba que el caso de uso genera una respuesta exitosa cuando todos los servicios funcionan correctamente.
    """
    response = question_answer_use_case.execute(question)
    assert response == expected_response


def test_question_answer_embedding_failure(question_answer_use_case, mock_embedding_service):
    """
    Prueba que se maneja correctamente un fallo en la generación de embeddings.
    """
    mock_embedding_service.generate_embedding.side_effect = Exception("Error en OpenAI")
    
    with pytest.raises(HTTPException) as exc_info:
        question_answer_use_case.execute("Pregunta inválida")
    
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error al generar el embedding para la pregunta."


def test_question_answer_db_failure(question_answer_use_case, mock_pgvector_repository):
    """
    Prueba que se maneja correctamente un fallo en la consulta a la base de datos.
    """
    mock_pgvector_repository.query_similar_movies.side_effect = Exception("Error en la base de datos")
    
    with pytest.raises(HTTPException) as exc_info:
        question_answer_use_case.execute("Pregunta que falla en la base de datos")
    
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error al consultar la base de conocimiento."


def test_question_answer_no_movies_found(question_answer_use_case, mock_pgvector_repository):
    """
    Prueba que se maneja correctamente cuando no se encuentran películas relevantes.
    """
    mock_pgvector_repository.query_similar_movies.return_value = []
    
    response = question_answer_use_case.execute("Pregunta sin resultados")
    assert response == "Lo siento, no encontré información relevante para tu pregunta."


def test_question_answer_response_generation_failure(question_answer_use_case, mock_response_generator):
    """
    Prueba que se maneja correctamente un fallo en la generación de la respuesta.
    """
    mock_response_generator.generate_response.side_effect = Exception("Error al generar la respuesta")
    
    with pytest.raises(HTTPException) as exc_info:
        question_answer_use_case.execute("Pregunta que falla en la generación de respuesta")
    
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Error al generar la respuesta basada en los datos."
