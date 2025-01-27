# Microservicio: Movies Indexer

El microservicio `indexer` es responsable de procesar un archivo CSV con información de películas, generar embeddings a partir de las descripciones utilizando la API de OpenAI, e indexarlos en una base de datos PostgreSQL con soporte para vectores gracias a PGVector.

---

## Estructura del Proyecto
El proyecto sigue los principios de **arquitectura limpia** para garantizar modularidad y escalabilidad. A continuación, la estructura principal:

```plaintext
/indexer
├── app/
│   ├── main.py  # Punto de entrada principal.
│   ├── application/
│   │   └── usecases/
│   │       └── index_embeddings.py  # Caso de uso para indexar embeddings.
│   ├── core/
│   │   ├── middleware/
│   │   │   └── validate_consumer.py  # Middleware para validar Consumer-ID.
│   │   ├── models/
│   │   │   └── models.py  # Modelos principales del dominio.
│   │   ├── utils/
│   │       ├── config.py  # Configuraciones globales.
│   │       └── logger.py  # Logger centralizado.
│   ├── infra/
│   │   ├── repositories/
│   │   │   └── pgvector_repository.py  # Repositorio para la base de datos PostgreSQL.
│   │   ├── services/
│   │   │   ├── csv_processor.py  # Procesador de archivos CSV.
│   │   │   └── embedding_service.py  # Generación de embeddings con OpenAI.
│   │   └── container.py  # Contenedor para manejar dependencias.
├── db/
│   └── init.sql  # Script SQL para inicializar la base de datos.
├── .env  # Variables de entorno.
├── Dockerfile  # Configuración para crear la imagen del microservicio.
├── docker-compose.yml  # Orquestación de servicios.
├── Makefile  # Comandos automatizados para desarrollo.
└── requirements.txt  # Dependencias del proyecto.
```

---

## Consumo del Endpoint

### **Endpoint principal:**
**`POST /movies-indexer/`**

#### **Descripción:**
Este endpoint recibe un archivo CSV con información de películas, genera embeddings para las descripciones y los indexa en la base de datos PostgreSQL.

#### **Headers requeridos:**
- `Content-Type: multipart/form-data`
- `x-consumer-id: <consumer-id>` (Clave API única para autorización)

#### **Body:**
- Tipo: `form-data`
- Campo: `file`
- Valor: Archivo CSV con las columnas `title`, `image`, y `plot`.

#### **Ejemplo de cURL:**
```bash
curl -X POST "http://localhost:8000/movies-indexer/" \
-H "x-consumer-id: <tu-consumer-id>" \
-F "file=@/ruta/al/archivo.csv"
```

#### **Ejemplo de archivo CSV:**
```csv
title,image,plot
"Matrix","https://image-url.com/matrix","A hacker discovers reality is a simulation."
"Inception","https://image-url.com/inception","Dreams within dreams."
```

#### **Respuesta exitosa:**
```json
{
  "status_code": 200,
  "message": "Archivo procesado exitosamente. Se indexaron 2 películas."
}
```

#### **Errores posibles:**
- **400 Bad Request:**
  - El archivo no es un CSV válido.
  - El archivo CSV no contiene las columnas requeridas.
- **403 Forbidden:**
  - `x-consumer-id` no es válido.
- **500 Internal Server Error:**
  - Error inesperado durante el procesamiento del archivo o la generación de embeddings.

---

## Puntos importantes a tener en cuenta

1. **Requisitos previos:**
   - PostgreSQL con PGVector configurado.
   - Clave API válida para OpenAI.
   - `consumer-id` único para autorización.

2. **Variables de entorno:**
   - Configura las siguientes variables en `.env`:
     ```env
     DB_HOST=postgres-db
     DB_PORT=5432
     DB_NAME=rag_db
     DB_USER=ragadmin
     DB_PASSWORD=securepassword
     OPENAI_API_KEY=tu-openai-api-key
     CONSUMER_ID=consumer-id-valido
     ```

3. **Flujo del sistema:**
   - **Recepción del archivo CSV.**
   - **Validación del archivo:** Formato, columnas y contenido.
   - **Generación de embeddings:** Llama a OpenAI para procesar las descripciones.
   - **Indexación:** Guarda los registros y embeddings en PostgreSQL con PGVector.

---
## **Contacto**
Si tienes alguna duda o problema, no dudes en abrir un issue en el repositorio.
