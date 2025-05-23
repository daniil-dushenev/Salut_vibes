import os
from openai import OpenAI
from app.logger import logger
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("OPENAI_MODEL")
API_KEY = os.getenv("OPENAI_API_TOKEN")


logger.debug(f"Connecting to Gemma OpenAI client with creds:\n BASE_URL: {OPENAI_BASE_URL},\n API_KEY: {API_KEY},\n MODEL_NAME: {MODEL_NAME}")
client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=API_KEY,
)

class VibeName(str, Enum):
    COZY_AND_INTIMATE = "Cozy and Intimate"
    ENERGETIC_AND_PARTY = "Energetic and Party"
    MINIMAL_AND_AESTHETIC = "Minimal and Aesthetic"
    BOHEMIAN_AND_CREATIVE = "Bohemian and Creative"
    PREMIUM_AND_LUXURIOUS = "Premium and Luxurious"
    ACTIVE_AND_SPORTY = "Active and Sporty"
    FAMILY_AND_FRIENDLY = "Family and Friendly"
    UNKNOWN = "unknown"

class VibesResponse(BaseModel):
    """Структурированный ответ LLM."""
    vibes: List[VibeName] = Field(
        ...,
        description=(
            "Список выявленных вайбов. Допустимые значения см. VibeName Enum."
        ),
    )


def get_llm_response(prompt: str, image_urls: List[str]) -> Optional[Dict[str, Any]]:
    user_content: List[dict] = [{"type": "input_text", "text": prompt}]
    user_content += [
        {"type": "input_image", "image_url": url} for url in image_urls
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "Ты — специалист по внешности. Отвечай *строго* JSON-объектом "
                'формы {"vibes": ["..."]} без пояснений.'
            ),
        },
        {"role": "user", "content": user_content},
    ]

    try:
        logger.info("Запрос ChatGPT с structured_output…")

        response = client.responses.parse(
                model=MODEL_NAME,
                input=messages,
                text_format=VibesResponse
            ).output_parsed

        logger.debug("Parsed response: %s", response)
        return response

    except Exception as exc:
        logger.exception("Ошибка structured-запроса: %s", exc)
        return None
