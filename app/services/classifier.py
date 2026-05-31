from app.models import CategoryEnum

RUSSIA_KEYWORDS = [
    "роскосмос", "байконур", "восточный", "ангара", "союз",
    "прогресс", "российский", "российская", "российские",
    "российского", "российскую", "ркк энергия", "главкосмос",
    "гкнпц", "имба иш", "насо",
]

SCIENCE_KEYWORDS = [
    "телескоп", "уэбб", "хаббл", "экзопланет", "чёрная дыр",
    "черная дыр", "галактик", "марсоход", "учёные", "ученые",
    "открытие", "исследование", "астрофизик", "планетар",
    "нейтронн", "сверхнова", "комет", "астероид", "вселен",
    "млечный", "солнечн", "звезд", "марс", "юпитер", "сатурн",
    "венер", "меркурий", "лун", "плутон", "обсерватори",
]

PRIVATE_KEYWORDS = [
    "spacex", "илон маск", "илoн маск", "falcon", "starship",
    "blue origin", "rocket lab", "relativity space", "sr space",
    "частная компани", "коммерческий запуск", "частный запуск",
    "private space", "starlink", "new glenn", "new shepard",
    "electron", "neutron", "terran", "astra", "firefly",
    "virgin galactic", "virgin orbit", "косм. частн", "частн. косм",
]


def classify_article(text: str, title: str = "") -> CategoryEnum:
    combined = (title + " " + text).lower()

    score_russia = sum(1 for kw in RUSSIA_KEYWORDS if kw in combined)
    score_science = sum(1 for kw in SCIENCE_KEYWORDS if kw in combined)
    score_private = sum(1 for kw in PRIVATE_KEYWORDS if kw in combined)

    scores = {
        CategoryEnum.russia: score_russia,
        CategoryEnum.science: score_science,
        CategoryEnum.private: score_private,
    }

    max_score = max(scores.values())

    if max_score == 0:
        return CategoryEnum.science

    if score_russia == max_score:
        return CategoryEnum.russia
    if score_private == max_score:
        return CategoryEnum.private

    return CategoryEnum.science


def classify_with_llm(text: str, title: str, api_key: str | None) -> CategoryEnum | None:
    if not api_key:
        return None

    try:
        import httpx

        prompt = (
            "Определи категорию новости о космосе. Верни ТОЛЬКО одно слово: "
            "russia (если новость о российской государственной космонавтике), "
            "science (если новость о науке, астрофизике, планетах, телескопах, открытиях), "
            "private (если новость о частной космонавтике — SpaceX, Blue Origin, Rocket Lab, SR Space и т.д.).\n\n"
            f"Заголовок: {title}\n\nТекст: {text[:2000]}"
        )

        response = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты — классификатор космических новостей. Отвечай только одним словом.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 10,
                "temperature": 0,
            },
            timeout=15,
        )

        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip().lower()

        for cat in CategoryEnum:
            if cat.value in result:
                return cat

        return None
    except Exception:
        return None
