from __future__ import annotations

import asyncio
import os

import deepl


class APITranslator:
    @classmethod
    def _deepl_translate_sync(cls, text: str, target_lang: str) -> str:
        api_key = os.getenv("DEEPL_API_KEY")
        translator = deepl.Translator(api_key)  # pyright: ignore[reportArgumentType]
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text  # pyright: ignore[reportAttributeAccessIssue]

    @classmethod
    async def deepl_translate(cls, text: str, target_lang: str) -> str:
        return await asyncio.to_thread(cls._deepl_translate_sync, text, target_lang)
