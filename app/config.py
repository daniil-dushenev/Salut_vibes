LLAVA_VIBE_PROMPT = """
Look carefully at the interior and visual atmosphere of the place in the image.

Do not describe people, dishes, menus, or signs. Focus only on the environment, design, layout, and the overall mood of the space.

Answer the following questions internally before writing your description (do not list the questions in your output):

1. What is the lighting like? (dim, warm, cold, bright, natural)
2. What kind of furniture is used? (plush, wooden, minimal, designer)
3. Are there decorations or art? (graffiti, paintings, candles, neon signs)
4. What materials dominate the interior? (wood, metal, velvet, glass)
5. Is the layout open and spacious or cozy and intimate?
6. How formal or casual does the space feel?
7. Is there anything that creates a sense of energy or calm? (music, colors, light movement)
8. Would this place suit quiet conversations, dancing, creative work, or family meals?
9. How trendy or luxurious does the place look?
10. Does it feel artistic, functional, extravagant, or playful?

Now, based on your analysis, describe the vibe of this place in rich, atmospheric detail.
"""

GEMMA_VIBE_TAGGING_PROMPT = """
You are a place vibe classifier. Based on the visual description of a venue's interior and mood, you must identify the most fitting vibe category (or categories) from the list below.

Choose only 1 or 2 most appropriate options. Do not guess — if the description is vague, respond with "unknown".

Respond ONLY with valid JSON:
{
  "vibes": ["VIBE_NAME"]
}

Available vibe categories:

1. Cozy and Intimate  
   - Warm, quiet atmosphere. Soft lighting, wood, candles, retro, vintage, bookshelves, blankets.

2. Energetic and Party  
   - Bright lights, loud music, DJs, dance floor, cocktail bars, neon lighting.

3. Minimal and Aesthetic  
   - Bright spaces, clean lines, designer furniture, minimalism, Instagram-friendly interiors.

4. Bohemian and Creative  
   - Eclectic, artsy, graffiti, live music stage, relaxed, expressive style.

5. Premium and Luxurious  
   - High-end service, elegant design, upscale materials, gourmet cuisine, VIP zones.

6. Active and Sporty  
   - Sports bar vibe, games, big screens, table tennis, informal and dynamic.

7. Family and Friendly  
   - Casual, warm, children-friendly, game zones, family-oriented design.

Example:
If the description mentions velvet armchairs, candles, jazz music, and bookshelves — return:
{
  "vibes": ["Cozy and Intimate"]
}

If the place features neon lights, DJ booths, and a crowd — return:
{
  "vibes": ["Energetic and Party"]
}
"""

# Vibe translations (for postprocessing)
VIBE_TRANSLATIONS = {
    "Cozy and Intimate": "Уютные и камерные",
    "Energetic and Party": "Энергичные и тусовочные",
    "Minimal and Aesthetic": "Минимализм и эстетика",
    "Bohemian and Creative": "Богемные и творческие",
    "Premium and Luxurious": "Премиум и люкс",
    "Active and Sporty": "Активные и спортивные",
    "Family and Friendly": "Семейные и дружелюбные",
    "unknown": "неопределённый"
}

def translate_vibes(vibes: list[str]) -> list[str]:
    return [VIBE_TRANSLATIONS.get(v, v) for v in vibes]