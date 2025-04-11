import os
from fastapi import FastAPI, HTTPException
from app.model import AppearanceExtractionModel
from app.logger import logger
import httpx
import uuid
from datetime import datetime

app = FastAPI()
model = AppearanceExtractionModel()


@app.post("/predict")
async def predict_vibe(image_url: str):
    """
    Анализирует вайб места по изображению из публичного URL.
    Возвращает описание, список вайбов и мета-данные.
    """
    request_id = uuid.uuid4().hex
    timestamp = datetime.utcnow().isoformat()
    temp_path = f"temp_{request_id}.jpg"

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(image_url)
            response.raise_for_status()
            with open(temp_path, "wb") as f:
                f.write(response.content)

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {e}")

    try:
        result = await model.predict_venue_vibe(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return {
        "request_id": request_id,
        "timestamp": timestamp,
        "source_url": image_url,
        "description": result["description"],
        "vibes": result["vibes"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)