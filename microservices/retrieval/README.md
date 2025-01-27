# Microservicio: Movies Retrieval Generator

El microservicio `retrieval` es una parte fundamental del sistema **RAG (Retrieval-Augmented Generation)**. Su objetivo es recibir preguntas del usuario, buscar información relevante en la base de conocimiento previamente indexada, y generar respuestas claras utilizando la API de OpenAI.

---

## Estructura del Proyecto
El proyecto sigue los principios de **arquitectura limpia** para garantizar modularidad y escalabilidad. A continuación, la estructura principal:

```plaintext
/retrieval
├── app/
│   ├── application/
│   │   └── usecases/
│   │       └── question_answer.py  # Caso de uso principal
│   ├── core/
│   │   ├── middleware/
│   │   │   └── validate_consumer.py  # Middleware para validar Consumer-ID
│   │   ├── models/
│   │   │   ├── models.py  # Modelos del dominio
│   │   │   └── requests.py  # Modelos de entrada
│   │   ├── utils/
│   │   │   ├── config.py  # Configuración global
│   │   │   └── logger.py  # Logs avanzados
│   ├── infra/
│   │   ├── repositories/
│   │   │   └── pgvector_repository.py  # Repositorio para interacción con la base de datos
│   │   ├── services/
│   │   │   ├── embedding_service.py  # Generación de embeddings
│   │   │   └── response_generator.py  # Generación de respuestas
│   │   └── container.py  # Inyección de dependencias
│   └── main.py  # Punto de entrada del microservicio
├── Dockerfile  # Configuración de la imagen Docker
├── docker-compose.yml  # Levantar el servicio en local
├── requirements.txt  # Dependencias del proyecto
└── .env  # Variables de entorno (sensibles)
```

## **Dependencias**
Estas son las principales dependencias del microservicio y sus propósitos:

- **FastAPI**: Framework web para manejar los endpoints.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación.
- **OpenAI**: Cliente para interactuar con la API de OpenAI.
- **Psycopg2**: Conector para PostgreSQL.
- **Numpy**: Para cálculos numéricos necesarios en embeddings.
- **Python-dotenv**: Manejo de variables de entorno.
- **Tenacity**: Reintentos automáticos para llamadas a OpenAI.

Consulta el archivo `requirements.txt` para ver las versiones específicas.

---

## **Archivo `.env`**
El archivo `.env` contiene configuraciones sensibles y específicas del entorno. Asegúrate de crearlo en la raíz del proyecto.

**Ejemplo de contenido de `.env`:**
```env
DB_HOST=postgres-db
DB_PORT=5432
DB_NAME=rag_db
DB_USER=ragadmin
DB_PASSWORD=<tu-contraseña>
OPENAI_API_KEY=<tu-api-key-de-openai>
EMBEDDING_MODEL=text-embedding-ada-002
CHAT_COMPLETION_MODEL=gpt-3.5-turbo
CONSUMER_ID=<tu-consumer-id>
```

---

## **Cómo consumir el servicio**

El endpoint principal del microservicio es:

### **POST** `/question-answer/`
Recibe una pregunta del usuario y devuelve una respuesta generada.

#### **Headers**
```plaintext
x-consumer-id: <tu-consumer-id>
Content-Type: application/json
```

#### **Body (JSON)**
```json
{
  "question": "What is The Matrix?"
}
```

#### **Respuesta esperada**
```json
{
  "status_code": 200,
  "message": "Respuesta generada con éxito.",
  "data": "Matrix es una película de ciencia ficción lanzada en 1999..."
}
```

---

## **Cómo levantar el microservicio en local**

### **1. Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd retrieval
```

### **2. Crear y activar un entorno virtual (en linux)**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

### **4. Crear el archivo `.env`**
Configura las variables necesarias como se muestra en el ejemplo.

### **5. Levantar el servicio**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

---

## **Cómo levantarlo con Docker**

### **1. Construir la imagen Docker**
Desde el directorio del microservicio, ejecuta:
```bash
docker build -t retrieval-service .
```

### **2. Levantar el contenedor**
```bash
docker-compose up --build
```

Esto levantará el microservicio en el puerto **8001**.
IMPORTANTE: Para levantar el microservicio, la Base de Datos debe estar arriba tambien.

---

## **Explicación del flujo**

1. **Recepción de la pregunta:**
   - El usuario envía una pregunta al endpoint `/question-answer/`.
   - Se valida el `x-consumer-id` a través del middleware.

2. **Generación del embedding:**
   - La pregunta se convierte en un embedding utilizando la API de OpenAI.

3. **Consulta en la base de conocimiento:**
   - Se utiliza el embedding generado para buscar películas relevantes en PostgreSQL con PGVector.

4. **Generación de la respuesta:**
   - Con base en los resultados, se genera una respuesta utilizando la API de Chat Completion de OpenAI.

5. **Devolución al usuario:**
   - Se retorna la respuesta generada al usuario en un formato JSON.

---

## **Contacto**
Si tienes alguna duda o problema, no dudes en abrir un issue en el repositorio.
