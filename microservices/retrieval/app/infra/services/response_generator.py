import openai
from app.core.models.models import Movie
from app.core.utils.logger import get_logger

class ResponseGenerator:
    """
    Servicio para construir respuestas utilizando el modelo GPT de OpenAI.
    """

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.logger = get_logger(self.__class__.__name__)

    def generate_response(self, question: str, movies: list[Movie]) -> str:
        """
        Genera una respuesta basada en los datos recuperados.

        :param question: Pregunta del usuario.
        :param movies: Películas relevantes recuperadas.
        :return: Respuesta generada.
        """
        openai.api_key = self.api_key

        context = "\n".join([
            f"- Titulo: {movie.title}:\n  Descripción: {movie.plot}\n  Imagen: {movie.image}"
            for movie in movies
        ])

        system_content = (
            "You are a friendly and humorous assistant with a youthful and vibrant personality. Your task "
            "is to answer questions solely based on the provided context. The context includes a link to "
            "an image from the movie, a description, and a similarity metric that indicates how relevant "
            "the context is to the question based on documents retrieved from the database. Avoid using "
            "any external information or personal knowledge. If the context does not provide enough "
            "information to answer the question, respond with 'No lo sé basándome en el contexto "
            "proporcionado por la base de datos'. If the question is nonsensical or cannot be answered "
            "based on the provided context, explain this politely and humorously in your response."
            "Ensure your answers are natural, concise, and directly related to the given context. Include "
            "the link to the image, the movie description, and the similarity metric in your response only "
            "if the question explicitly requests it. Your tone should be fresh and youthful, with a touch "
            "of Caribbean Colombian slang and humor, while remaining polite and respectful. Always respond "
            "in Spanish and make your answers sound like they come from a cool and relaxed coastal friend "
            "who enjoys making the conversation enjoyable. Use phrases and expressions typical of Colombia's "
            "Caribbean coast."
        )
        prompt = f"Pregunta: {question}\nContexto:\n{context}\nRespuesta:"

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response["choices"][0]["message"]["content"]#.strip()
            self.logger.info(f"Respuesta generada por OpenAI: {answer}")
            return answer
        except Exception as e:
            self.logger.error(f"Error al generar la respuesta: {str(e)}")
            raise
