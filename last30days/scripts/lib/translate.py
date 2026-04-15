"""Translation module for multi-language search support.

Provides translation functionality to expand search queries across multiple
languages for better global coverage.
"""

import re
import sys
from typing import List, Dict, Optional
from lib import http


# Common translations for gaming/board game terminology
# 游戏化 / 桌游相关术语的多语言映射
GAMING_TRANSLATIONS = {
    # English → Multiple languages
    "gamification": {
        "zh": "游戏化",
        "ru": "геймификация",
        "fr": "ludification",
        "de": "Gamifizierung",
        "ar": "تألعيب",
    },
    "board game": {
        "zh": "桌游",
        "ru": "настольная игра",
        "fr": "jeu de société",
        "de": "Brettspiel",
        "ar": "لعبة لوح",
    },
    "board games": {
        "zh": "桌游",
        "ru": "настольные игры",
        "fr": "jeux de société",
        "de": "Brettspiele",
        "ar": "ألعاب لوحية",
    },
    # Chinese → English and other languages
    "游戏化": {
        "en": "gamification",
        "ru": "геймификация",
        "fr": "ludification",
        "de": "Gamifizierung",
        "ar": "تألعيب",
    },
    "桌游": {
        "en": "board game",
        "ru": "настольная игра",
        "fr": "jeu de société",
        "de": "Brettspiel",
        "ar": "لعبة لوح",
    },
}


def detect_chinese(text: str) -> bool:
    """Detect if text contains Chinese characters.

    Args:
        text: Text to check

    Returns:
        True if text contains Chinese characters
    """
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\U0002f800-\U0002fa1f]')
    return bool(chinese_pattern.search(text))


def get_translations(topic: str) -> Dict[str, str]:
    """Get translations of a topic into multiple languages.

    Uses a dictionary-based approach for common gaming terms.
    For other topics, returns the original topic for all languages.

    Args:
        topic: The topic to translate

    Returns:
        Dict mapping language codes to translated topics:
        {
            "zh": "中文翻译",
            "en": "English translation",
            "ru": "Русский",
            "fr": "Français",
            "de": "Deutsch",
            "ar": "العربية",
        }
    """
    # Normalize for lookup
    topic_lower = topic.lower().strip()

    # Check if we have a direct translation
    if topic_lower in GAMING_TRANSLATIONS:
        return GAMING_TRANSLATIONS[topic_lower]

    # Check for multi-word phrases
    for key, translations in GAMING_TRANSLATIONS.items():
        if key in topic_lower or topic_lower in key:
            # Found a partial match - use the translation
            return translations

    # No translation available - return original for all languages
    # This allows the search to proceed with the original topic
    return {
        "zh": topic,
        "en": topic,
        "ru": topic,
        "fr": topic,
        "de": topic,
        "ar": topic,
    }


def get_search_topics(topic: str) -> List[Dict[str, str]]:
    """Get a list of search topics for parallel multi-language search.

    Returns the original topic plus translations for comprehensive coverage.

    Args:
        topic: The original search topic

    Returns:
        List of dicts with language and topic:
        [
            {"lang": "original", "topic": "原始主题"},
            {"lang": "en", "topic": "English topic"},
            {"lang": "ru", "topic": "Русская тема"},
            ...
        ]
    """
    translations = get_translations(topic)

    # Build search list - always include original first
    search_topics = [{"lang": "original", "topic": topic}]

    # Add translations that are different from original
    for lang_code, translated_topic in translations.items():
        if translated_topic != topic and translated_topic.lower() != topic.lower():
            search_topics.append({"lang": lang_code, "topic": translated_topic})

    return search_topics


def should_translate(topic: str) -> bool:
    """Determine if a topic should be translated for multi-language search.

    Args:
        topic: The search topic

    Returns:
        True if topic contains non-ASCII characters or is a known translatable term
    """
    # Check for Chinese characters
    if detect_chinese(topic):
        return True

    # Check for other non-Latin scripts (Cyrillic, Arabic, etc.)
    if re.search(r'[^\x00-\x7F]', topic):
        return True

    return False


def get_primary_language(topic: str) -> str:
    """Detect the primary language of a topic.

    Args:
        topic: The search topic

    Returns:
        Language code: "zh", "en", "ru", "fr", "de", "ar", or "unknown"
    """
    if detect_chinese(topic):
        return "zh"

    # Cyrillic (Russian)
    if re.search(r'[а-яА-Я]', topic):
        return "ru"

    # Arabic
    if re.search(r'[ا-ي]', topic):
        return "ar"

    # Default to English for Latin scripts
    return "en"


def build_multilingual_query(topic: str) -> str:
    """Build a search query that includes multiple language variants.

    This is useful for platforms that support OR queries.

    Args:
        topic: The original topic

    Returns:
        A query string with multiple language variants joined by OR
        Example: "桌游 OR board game OR Brettspiel"
    """
    translations = get_translations(topic)

    # Remove duplicate topics while preserving order
    unique_topics = []
    seen = set()
    for lang, trans_topic in translations.items():
        if trans_topic.lower() not in seen:
            seen.add(trans_topic.lower())
            unique_topics.append(trans_topic)

    return " OR ".join(unique_topics)


# For backward compatibility
def translate_topic(topic: str, target_lang: str = "en") -> str:
    """Translate a topic to a target language.

    Args:
        topic: The topic to translate
        target_lang: Target language code (en, zh, ru, fr, de, ar)

    Returns:
        Translated topic, or original if no translation available
    """
    translations = get_translations(topic)
    return translations.get(target_lang, topic)


if __name__ == "__main__":
    # Test the translation functions
    test_topics = ["游戏化 桌游", "gamification", "board games"]

    for topic in test_topics:
        print(f"\nTopic: {topic}")
        print(f"Should translate: {should_translate(topic)}")
        print(f"Primary language: {get_primary_language(topic)}")
        print(f"Translations: {get_translations(topic)}")
        print(f"Search topics: {get_search_topics(topic)}")
        print(f"Multilingual query: {build_multilingual_query(topic)}")
