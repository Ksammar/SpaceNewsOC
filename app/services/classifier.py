import re

from app.models import CategoryEnum

SPACE_KEYWORDS = [
    "spacex", "starlink", "starship", "falcon 9", "falcon heavy",
    "crew dragon", "дрэгон", "dragon spacecraft",
    "elon musk", "илон маск",
    "blue origin", "new glenn", "new shepard",
    "rocket lab", "electron rocket",
    "virgin galactic", "virgin orbit",
    "relativity space", "terran",
    "firefly", "firefly aerospace", "blue ghost",
    "boeing starliner", "starliner",
    "sierra space", "dream chaser",
    "atlas v", "delta iv", "vulcan centaur",
    "nasa", "esa", "roscosmos", "cnsa", "jaxa", "isro",
    "artemis", "orion spacecraft", "sls rocket",
    "iss ", "international space station", " мкс ",
    "hubble", "james webb", "webb telescope", "jwst", "телескоп уэбб",
    "mars rover", "perseverance", "curiosity", "ingenuity",
    "марсоход",
    "mars ", " марс", "марсе", "марсиан",
    "юпитер", "сатурн", "венер", "меркурий", "нептун", "уран",
    "плутон",
    "лун", "lunar", "moon",
    "космическ", "космос", "космонавт", "космодром",
    "космический аппарат", "космических аппарат",
    "спутник", "спутников", "спутники",
    "телескоп", "telescope", "обсерватори", "observatory",
    "экзопланет", "exoplanet",
    "галактик", "galaxy", "galaxies",
    "чёрная дыр", "черная дыр", "black hole",
    "астероид", "asteroid", "комет", "comet",
    "сверхнова", "supernova", "нейтронн", "neutron star",
    "солнечн", "solar system",
    "spacecraft", "rocket", "rockets",
    "ракет", "ракетн",
    "запуск", "запустил", "запустила", "запущен",
    "орбит", "орбиту", "орбита",
    "астронавт", "astronaut",
    "космонавт", "cosmonaut",
    "spaceflight", "space flight", "spacewalk",
    "выход в открытый космос",
    "млечный путь", "milky way",
    "space force", "космические войска",
    "байконур", "восточный", "восточном", "плесецк",
    "ангара", "союз", "прогресс", "протон",
    "ркк энергия", "главкосмос",
    "sr space", "частная компани", "частная космонавтик",
    "коммерческий запуск", "частный запуск",
    "commercial crew", "commercial resupply",
    "ракета-носител", "ракеты-носител",
    "deep space", "interstellar",
    "planetar", "planetary science",
    "sputnik",
    "gravitational wave", "гравитационн",
    "dark matter", "dark energy", "темная матери",
    "space telescope", "космический телескоп",
    "astrophysics", "астрофизик",
    "mars mission",
    "kennedy space center", "cape canaveral",
    "гиперзвук",
    "reusable rocket",
    "разгонный блок",
    "космический корабл",
    "пилотируем",
    "стыковк",
    "space station",
    "вселенн",
    "звезд", "звёзд",
    "планет", "planet",
    "астроном",
    "пульсар", "pulsar",
    "квазар", "quasar",
    "туманност", "nebula",
    "spacex", "spacex",
    "noaa", "goes satellite",
    "спутниковая",
    "межпланетн",
    "международная космическая",
    "орбитальная",
    "звездолет",
    "космический полет",
    "полет в космос",
    "spacex",
]

RUSSIA_KEYWORDS = [
    "роскосмос", "roscosmos",
    "байконур", "baikonur",
    "восточный", "восточном", "vostochny",
    "ангара", "союз", "souz", "soyuz",
    "прогресс", "progress",
    "протон", "proton",
    "плесецк", "plesetsk",
    "космодром",
    "ракета-носител", "разгонный блок",
    "российский", "российские", "российского", "российских",
    "российская орбитальная",
    "russian cosmonaut",
    "russian space",
    "russian spacecraft",
    "russian rocket",
    "russian satellite",
    "ркк энергия", "главкосмос",
    "гкнпц", "имба иш",
    "госкорпорация",
    "россия", "рф",
]

SCIENCE_KEYWORDS = [
    "телескоп", "уэбб", "хаббл", "jwst",
    "экзопланет", "exoplanet",
    "чёрная дыр", "черная дыр", "black hole",
    "галактик", "galaxy", "galaxies",
    "марсоход", "mars rover",
    "нейтронн", "сверхнова", "supernova",
    "комет", "астероид", "asteroid",
    "вселенн", "млечный", "солнечн",
    "звезд", "звёзд",
    "планет", "planet", "planetary",
    "обсерватори", "observatory",
    "марс", "юпитер", "сатурн",
    "венер", "меркурий", "нептун", "уран",
    "лун", "lunar",
    "плутон",
    "космический телескоп",
    "гравитационн", "gravitational",
    "темная матери", "dark matter",
    "темная энерги", "dark energy",
    "all planet", "solar system",
    "space telescope",
    "астроном", "astronom",
    "astrophysics", "астрофизик",
    "нейтронная звезд",
    "пульсар", "pulsar",
    "квазар", "quasar",
    "туманност", "nebula",
    "астрофизик",
]

PRIVATE_KEYWORDS = [
    "spacex", "илон маск", "ilon mask",
    "falcon", "starship", "starlink",
    "crew dragon", "dragon spacecraft",
    "blue origin", "new glenn", "new shepard",
    "rocket lab", "electron rocket", "neutron rocket",
    "relativity space", "terran",
    "sr space",
    "частная компани", "частная космонавтик",
    "коммерческий запуск", "частный запуск",
    "private space",
    "astra", "firefly", "firefly aerospace",
    "virgin galactic", "virgin orbit",
    "boeing starliner", "starliner",
    "sierra space", "dream chaser",
    "коммерческая космонавтик",
    "space startup", "spacex",
    "starship", "spacex",
]


def is_space_related(text: str, title: str = "") -> bool:
    combined = (title + " " + text).lower()
    return any(kw.lower() in combined for kw in SPACE_KEYWORDS)


def classify_article(text: str, title: str = "") -> CategoryEnum | None:
    combined = (title + " " + text).lower()

    if not is_space_related(combined):
        return None

    score_russia = sum(1 for kw in RUSSIA_KEYWORDS if kw in combined)
    score_science = sum(1 for kw in SCIENCE_KEYWORDS if kw in combined)
    score_private = sum(1 for kw in PRIVATE_KEYWORDS if kw in combined)

    if score_russia == 0 and score_science == 0 and score_private == 0:
        return CategoryEnum.science

    if score_russia >= score_science and score_russia >= score_private and score_russia > 0:
        return CategoryEnum.russia
    if score_private >= score_science and score_private >= score_russia and score_private > 0:
        return CategoryEnum.private

    return CategoryEnum.science


def classify_with_llm(text: str, title: str, api_key: str | None) -> CategoryEnum | None:
    if not api_key:
        return None

    try:
        from app.config import settings
        import httpx as httpx_module

        prompt = (
            "Определи категорию новости о космосе. Верни ТОЛЬКО одно слово: "
            "russia (если новость о российской государственной космонавтике), "
            "science (если новость о науке, астрофизике, планетах, телескопах, открытиях), "
            "private (если новость о частной космонавтике — SpaceX, Blue Origin, Rocket Lab, SR Space и т.д.).\n\n"
            f"Заголовок: {title}\n\nТекст: {text[:2000]}"
        )

        response = httpx_module.post(
            f"{settings.openai_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.openai_model,
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
