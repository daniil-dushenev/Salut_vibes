from app.logger import logger
from app.config import LLAVA_VIBE_PROMPT, GEMMA_VIBE_TAGGING_PROMPT, translate_vibes
from app.interfaces.gemma_openai_inference import get_llm_response
from app.interfaces.llava_openai_client import llava_openai_appearance


class AppearanceExtractionModel:
    def __init__(self):
        self.logger = logger

    async def predict_venue_vibe(self, img_path: str) -> dict:
        logger.info(f"[VIBE PIPELINE] Анализ вайба места по {img_path}")

        # 1. Получаем описание места
        description = await llava_openai_appearance(img_path, prompt=LLAVA_VIBE_PROMPT)
        if not description:
            logger.warning("LLaVA не вернула описание")
            return {"description": "unknown", "vibes": ["неопределённый"]}

        logger.debug(f"Venue description: {description}")

        # 2. Подставляем описание в prompt для Gemma
        gemma_prompt = f"{GEMMA_VIBE_TAGGING_PROMPT}\n\nDescription:\n{description}"
        result = get_llm_response(gemma_prompt)

        if not result or not isinstance(result, dict) or "vibes" not in result:
            logger.warning("Gemma не смогла распознать вайб")
            return {"description": description, "vibes": ["неопределённый"]}

        translated_vibes = translate_vibes(result["vibes"])

        return {
            "description": description.strip(),
            "vibes": translated_vibes
        }