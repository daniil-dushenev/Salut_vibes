import os
from openai import OpenAI
from app.logger import logger
import json
import re
from typing import Dict, Any, Optional

OPENAI_BASE_URL = os.getenv("RUNPOD_GEMMA_BASE_URL")
MODEL_NAME = os.getenv("RUNPOD_GEMMA_MODEL")
API_KEY = os.getenv("RUNPOD_API_KEY")
MAX_TOKENS = int(os.getenv("GEMMA_MAX_TOKENS"))


logger.debug(f"Connecting to Gemma OpenAI client with creds:\n BASE_URL: {OPENAI_BASE_URL},\n API_KEY: {API_KEY},\n MODEL_NAME: {MODEL_NAME},\n GEMMA_MAX_TOKENS: {MAX_TOKENS}")
client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=API_KEY,
)

def try_fix_partial_json(text: str) -> Optional[dict]:
    try:
        last = text.rfind("}")
        if last != -1:
            return json.loads(text[:last + 1])
    except Exception:
        pass
    return None


def get_llm_response(prompt: str) -> Optional[Dict[str, Any]]:
    try:
        messages = [
            {"role": "system", "content": "Ты — специалист по внешности. Работай строго в JSON."},
            {"role": "user", "content": prompt}
        ]

        logger.info("Отправка запроса в Gemma RunPod (OpenAI API mode)...")

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3,
            top_p=0.8,
            max_tokens=MAX_TOKENS,
        )

        logger.debug(f"RunPod Gemma response: {response}")
        content = response.choices[0].message.content
        logger.debug(f"RunPod Gemma OpenAI ответ: {content}")

        if content.startswith("```json"):
            content = content[7:].strip()
        elif content.startswith("```"):
            content = content[3:].strip()

        match = re.search(r'\{.*', content, re.DOTALL)
        if match:
            fixed = try_fix_partial_json(match.group(0))
            if fixed:
                return fixed

        logger.warning("⚠️ Ответ не содержит валидного JSON. Ответ: %s", content)
        return None

    except Exception as e:
        logger.exception("Ошибка при получении ответа от RunPod OpenAI API")
        return None
