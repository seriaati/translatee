from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, ClassVar

import yaml
from discord import Locale, app_commands

if TYPE_CHECKING:
    from discord.app_commands import TranslationContext, locale_str


class BotTranslator:
    _translations: ClassVar[dict[str, dict[str, str]]] = {}

    @classmethod
    def load_translations(cls) -> None:
        for file_path in pathlib.Path("l10n").glob("*.yml"):
            with pathlib.Path(file_path).open("r", encoding="utf-8") as f:
                locale_code = file_path.stem
                translations = yaml.safe_load(f)
                for key, translation in translations.items():
                    if key not in cls._translations:
                        cls._translations[key] = {}
                    cls._translations[key][locale_code] = translation

    @classmethod
    def translate(cls, key: str, locale_code: str) -> str | None:
        return cls._translations.get(key, {}).get(locale_code)


class CommandTreeTranslator(app_commands.Translator):
    async def translate(
        self, string: locale_str, locale: Locale, _context: TranslationContext
    ) -> str | None:
        key = string.extras.get("key")
        if key is None:
            return None

        locale_code = locale.value
        return BotTranslator.translate(key, locale_code)
