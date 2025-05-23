from app.logger import logger
from app.config import LLAVA_VIBE_PROMPT, GEMMA_VIBE_TAGGING_PROMPT, translate_vibes
from app.interfaces.gemma_openai_inference import get_llm_response
from app.interfaces.llava_openai_client import llava_openai_appearance
from typing import List


class AppearanceExtractionModel:
    def __init__(self):
        self.logger = logger

    async def predict_venue_vibe(self, img_paths: List[str]) -> dict:
        logger.info(f"[VIBE PIPELINE] Анализ вайба места по {img_paths}")

        result = get_llm_response(GEMMA_VIBE_TAGGING_PROMPT, img_paths)

        translated_vibes = translate_vibes(result.vibes)

        return {
            "vibes": translated_vibes
        }