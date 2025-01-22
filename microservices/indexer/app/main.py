from fastapi import FastAPI, HTTPException
from app.usecases.index_embeddings import index_embeddings

app = FastAPI()

@app.post("/index")
async def index_data():
    try:
        # Ejecutar el caso de uso de indexación
        index_embeddings()
        return {"message": "Data indexed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
