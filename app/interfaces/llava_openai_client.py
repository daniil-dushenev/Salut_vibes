import os
import base64
from io import BytesIO
from PIL import Image
from typing import Optional
from openai import OpenAI
from app.logger import logger

OPENAI_BASE_URL = os.getenv("RUNPOD_LLAVA_BASE_URL")
MODEL_NAME = os.getenv("RUNPOD_LLAVA_MODEL")
API_KEY = os.getenv("RUNPOD_API_KEY")
MAX_TOKENS = int(os.getenv("LLAVA_MAX_TOKENS"))

logger.debug(f"Connecting to LLAVA OpenAI client with creds:\n BASE_URL: {OPENAI_BASE_URL},\n API_KEY: {API_KEY},\n MODEL_NAME: {MODEL_NAME},\n GEMMA_MAX_TOKENS: {MAX_TOKENS}")
client = OpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=API_KEY
)

def image_to_base64_url(img_path: str) -> str:
    img = Image.open(img_path).convert("RGB")
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{encoded}"


async def llava_openai_appearance(img_path: str, prompt: str = "Describe the person's appearance in detail.") -> Optional[str]:
    image_url = image_to_base64_url(img_path)

    messages = [
        {"role": "system", "content": "You are a visual assistant. Be precise and detailed."},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}}
            ]
        }
    ]

    try:
        logger.info("Отправка запроса в LLaVA через OpenAI совместимый API...")
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.2,
            top_p=0.8,
            max_tokens=MAX_TOKENS,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        logger.exception("Ошибка при вызове LLaVA через OpenAI API")
        return None
