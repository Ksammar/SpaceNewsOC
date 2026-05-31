import logging

from app.config import settings

logger = logging.getLogger(__name__)


def needs_translation(title: str, summary: str | None) -> bool:
    if not title:
        return False
    has_cyrillic = any("а" <= c.lower() <= "я" for c in title)
    return not has_cyrillic


def _translate_sync(text: str) -> str:
    if not text or not settings.openai_api_key:
        return text

    try:
        import httpx

        prompt = (
            "Переведи следующий текст на русский язык. Сохрани имена собственные, "
            "названия компаний и технические термины в оригинале (NASA, SpaceX, Falcon и т.д.). "
            "Верни ТОЛЬКО перевод, без пояснений.\n\n" + text
        )

        with httpx.Client(timeout=20) as client:
            response = client.post(
                f"{settings.openai_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.openai_model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "Ты — профессиональный переводчик с английского на русский.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": len(text) + 300,
                    "temperature": 0.1,
                },
            )

            response.raise_for_status()
            result = response.json()["choices"][0]["message"]["content"].strip()
            return result
    except Exception as e:
        logger.warning("Translation failed: %s", e)
        return text


def translate_article(title: str, summary: str | None) -> tuple[str | None, str | None]:
    if not needs_translation(title, summary):
        return None, None

    title_ru = None
    summary_ru = None

    if title:
        translated = _translate_sync(title)
        if translated and translated != title:
            title_ru = translated

    if summary:
        translated = _translate_sync(summary[:1500])
        if translated and translated != summary:
            summary_ru = translated

    return title_ru, summary_ru
