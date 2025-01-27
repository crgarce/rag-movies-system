# Sistema RAG - Microservicios `indexer` y `retrieval`

Este sistema está compuesto por dos microservicios principales (`indexer` y `retrieval`) y una base de datos PostgreSQL con la extensión **PGVector**. El objetivo del sistema es indexar datos de películas y responder preguntas del usuario utilizando técnicas de **RAG (Retrieval-Augmented Generation)** integradas con la API de OpenAI.

---

## **Microservicios y Componentes**

### **1. Microservicio `indexer`**
- **Propósito:** Indexa un archivo CSV de datos de películas en una base de datos PostgreSQL con soporte para PGVector.
- **Endpoint principal:** `/upload-csv/`
- **Detalles adicionales:** Consulta el archivo `README.md` dentro del directorio del microservicio.

### **2. Microservicio `retrieval`**
- **Propósito:** Recibe preguntas del usuario, busca información relevante en la base de datos previamente indexada, y genera respuestas utilizando la API de OpenAI.
- **Endpoint principal:** `/question-answer/`
- **Detalles adicionales:** Consulta el archivo `README.md` dentro del directorio del microservicio.

### **3. Base de datos PostgreSQL**
- **Imagen:** `ankane/pgvector`
- **Propósito:** Almacenar los datos de las películas y sus embeddings generados para búsquedas eficientes basadas en similitud vectorial.

---

## **Estructura del Proyecto**

```plaintext
/rag-system
├── microservices/
│   ├── indexer/
│   │   ├── app/  # Código fuente del microservicio indexer
│   │   ├── db/  # Script de inicializacion para la BD
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml  # Levanta el indexer y la base de datos
│   │   └── .env  # Configuraciones del microservicio indexer
│   ├── retrieval/
│   │   ├── app/  # Código fuente del microservicio retrieval
│   │   ├── Dockerfile
│   │   ├── docker-compose.yml  # Levanta el microservicio retrieval
│   │   └── .env  # Configuraciones del microservicio retrieval
├── docker-compose.yml  # Orquestación externa para todos los componentes
├── .env  # Configuraciones externas para la BD
└── README.md  # Documento actual
```

---

## **Despliegue con Docker Compose**

### **1. Variables de entorno requeridas**
Crea un archivo `.env` en cada uno de los microservicios (`indexer` y `retrieval`) con el siguiente contenido:

#### **Archivo `.env` para `indexer`:**
```env
DB_HOST=postgres-db
DB_NAME=rag_db
DB_USER=ragadmin
DB_PASSWORD=<tu-contraseña>
DB_PORT=5432
OPENAI_API_KEY=<tu-api-key-de-openai>
EMBEDDING_MODEL=text-embedding-ada-002
EMBEDDING_DIMENSION=768
BATCH_SIZE=10
CONSUMER_ID=<tu-consumer-id>
```

#### **Archivo `.env` para `retrieval`:**
```env
DB_HOST=postgres-db
DB_PORT=5432
DB_NAME=rag_db
DB_USER=ragadmin
DB_PASSWORD=<tu-contraseña>
OPENAI_API_KEY=<tu-api-key-de-openai>
EMBEDDING_MODEL=text-embedding-ada-002
CHAT_COMPLETION_MODEL=gpt-4
CONSUMER_ID=<tu-consumer-id>
```

### **2. Levantar todos los servicios**
Desde la raíz del proyecto (`rag-system`), ejecuta:
```bash
docker-compose up --build
```

Esto levantará los siguientes servicios:
- **Base de datos PostgreSQL:** Expuesta en el puerto **5432**.
- **Microservicio `indexer`:** Expuesto en el puerto **8000**.
- **Microservicio `retrieval`:** Expuesto en el puerto **8001**.

---

## **Consumo de los Endpoints**

### **Microservicio `indexer`**
- **Endpoint principal:** `/upload-csv/`
- **URL:** `http://localhost:8000/upload-csv/`
- **Método:** `POST`
- **Headers:**
  ```plaintext
  x-consumer-id: <tu-consumer-id>
  Content-Type: multipart/form-data
  ```
- **Body (form-data):**
  ```plaintext
  file: <archivo_csv>
  ```
- **Respuesta esperada:**
  ```json
  {
    "status_code": 200,
    "message": "Archivo procesado exitosamente. Se indexaron 100 películas."
  }
  ```

### **Microservicio `retrieval`**
- **Endpoint principal:** `/question-answer/`
- **URL:** `http://localhost:8001/question-answer/`
- **Método:** `POST`
- **Headers:**
  ```plaintext
  x-consumer-id: <tu-consumer-id>
  Content-Type: application/json
  ```
- **Body (JSON):**
  ```json
  {
    "question": "What is The Matrix?"
  }
  ```
- **Respuesta esperada:**
  ```json
  {
    "status_code": 200,
    "message": "Respuesta generada con éxito.",
    "data": "Matrix es una película de ciencia ficción lanzada en 1999..."
  }
  ```

---

## **Detalles adicionales**
Para obtener más información sobre cada microservicio, consulta el archivo `README.md` dentro del directorio correspondiente:

- **`indexer`:** `microservices/indexer/README.md`
- **`retrieval`:** `microservices/retrieval/README.md`

---

## **Contacto**
Si tienes dudas o problemas, no dudes en abrir un issue en el repositorio.

¡Gracias por utilizar el sistema RAG! 🚀
