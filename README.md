# Proyecto RAG (Retrieval Augmented Generation) para Películas de los Años 1980

Este proyecto implementa un sistema basado en arquitecturas de RAG (Retrieval Augmented Generation) para responder preguntas relacionadas con una base de conocimiento sobre películas de los años 1980. El sistema utiliza datos indexados en una base de datos vectorial, APIs de modelos de lenguaje, y está desplegado en AWS siguiendo principios de arquitectura limpia.

## Microservicios

### Microservicio 1: Data Ingestion Service
#### Responsabilidades
- **Carga y procesamiento del archivo CSV**:
  - Leer el archivo CSV con información sobre películas.
  - Normalizar y limpiar los datos para asegurar consistencia en los campos (e.g., títulos, géneros, descripciones).
- **Vectorización de datos**:
  - Convertir descripciones y otros textos relevantes de las películas en embeddings utilizando un modelo preentrenado (OpenAI o similar).
- **Indexación en la base de datos PGVector**:
  - Insertar los vectores generados y los metadatos asociados (e.g., título, género, año) en PostgreSQL configurado con la extensión PGVector.

#### APIs
- `POST /ingest`: Recibe el archivo CSV y procesa los datos para indexarlos.

### Microservicio 2: Query Service
#### Responsabilidades
- **Recepción de preguntas del usuario**:
  - Recibir preguntas relacionadas con películas mediante un endpoint REST.
- **Vectorización de la pregunta**:
  - Convertir la pregunta en un embedding usando el mismo modelo que en la ingesta.
- **Búsqueda semántica en PGVector**:
  - Consultar la base de datos PGVector para recuperar los vectores más similares al embedding de la pregunta.
- **Generación de respuesta contextual**:
  - Usar la API de OpenAI para generar una respuesta basada en la pregunta del usuario y los resultados recuperados.

#### APIs
- `POST /query`: Recibe una pregunta y devuelve una respuesta basada en los datos indexados.

### Microservicio 3: Embedding Service
#### Responsabilidades
- **Interacción con OpenAI**:
  - Encapsular la lógica para generar embeddings utilizando las APIs de OpenAI.
- **Estandarización del proceso**:
  - Garantizar que todas las solicitudes de vectorización sigan el mismo formato y configuración.

#### APIs
- `POST /generate-embedding`: Recibe un texto y devuelve su embedding.

### Microservicio 4: Administration Service
#### Responsabilidades
- **Gestión de la base de conocimiento**:
  - Permitir la actualización, eliminación o reinicio de los datos indexados.
- **Monitoreo y mantenimiento**:
  - Proveer endpoints para verificar el estado del sistema (health checks).
  - Ofrecer estadísticas sobre el uso (e.g., número de preguntas respondidas, datos indexados).

#### APIs
- `GET /health`: Retorna el estado del sistema.
- `POST /reset-index`: Reinicia la base de conocimiento.

## Interacciones entre Microservicios

1. **Ingestión de datos**:
   - El Data Ingestion Service llama al Embedding Service para generar embeddings y luego almacena los datos en PGVector.
2. **Consultas**:
   - El Query Service llama al Embedding Service para generar un embedding de la pregunta, consulta PGVector para recuperar los datos relevantes y utiliza OpenAI para generar la respuesta final.
3. **Administración**:
   - El Administration Service gestiona las operaciones de mantenimiento y monitoreo del sistema.

## Arquitectura y Componentes en AWS

- **Base de datos**: Amazon RDS con PostgreSQL configurado con PGVector.
- **Almacenamiento de archivos**: Amazon S3 para almacenar temporalmente archivos CSV.
- **Servicios de computación**: AWS Lambda o ECS para ejecutar los microservicios.
- **API Gateway**: Para exponer las APIs de los microservicios.
- **Monitorización**: CloudWatch para logs y métricas.
- **Secrets Management**: AWS Secrets Manager para almacenar las claves API de OpenAI y credenciales de la base de datos.

## Diagrama Simplificado de Flujo de Datos

1. El usuario sube un archivo CSV a través del Data Ingestion Service.
2. Los datos son procesados, vectorizados y almacenados en la base de datos.
3. El usuario realiza preguntas mediante el Query Service, que genera embeddings, consulta la base de datos y utiliza OpenAI para crear respuestas.
4. El Administration Service asegura la correcta operación y mantenimiento del sistema.

---

Este sistema asegura una experiencia ágil y eficiente para responder preguntas sobre películas de los años 1980, integrando tecnologías modernas y un diseño modular para facilitar su extensión y mantenimiento.

