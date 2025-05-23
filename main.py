import os
from fastapi import FastAPI, HTTPException
from app.model import AppearanceExtractionModel
from app.logger import logger
import httpx
import uuid
from datetime import datetime
from typing import List

app = FastAPI()
model = AppearanceExtractionModel()


@app.post("/predict")
async def predict_vibe(image_urls: List[str]):
    """
    Анализирует вайб места по изображению из публичного URL.
    Возвращает описание, список вайбов и мета-данные.
    """
    request_id = uuid.uuid4().hex
    timestamp = datetime.utcnow().isoformat()

    try:
        result = await model.predict_venue_vibe(image_urls)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

    return {
        "request_id": request_id,
        "timestamp": timestamp,
        "source_urls": image_urls,
        "vibes": result["vibes"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)