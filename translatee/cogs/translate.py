from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord import app_commands
from discord.app_commands import locale_str as _
from discord.ext import commands

from translatee.api_translator import APITranslator
from translatee.constants import DEFAULT_TARGET_LANG
from translatee.db.models import UserSettings

if TYPE_CHECKING:
    from translatee.bot import Translatee
    from translatee.types import Interaction


class TranslateCog(commands.Cog):
    def __init__(self, bot: Translatee) -> None:
        self.bot = bot
        self.translate_ctx_menu = app_commands.ContextMenu(
            name=_("Translate", key="translate_ctx_cmd_name"), callback=self.translate_ctx_menu_func
        )

    async def cog_load(self) -> None:
        self.bot.tree.add_command(self.translate_ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(
            self.translate_ctx_menu.name, type=self.translate_ctx_menu.type
        )

    async def translate_ctx_menu_func(self, i: Interaction, message: discord.Message) -> None:
        await i.response.defer(ephemeral=True)

        user_settings = await UserSettings.get_or_none(id=i.user.id)
        target_lang = user_settings.lang if user_settings else DEFAULT_TARGET_LANG
        translation = await APITranslator.deepl_translate(message.content, target_lang)
        await i.followup.send(translation, ephemeral=True)

    @app_commands.command(
        name=_("translate", key="translate_cmd_name"),
        description=_("Translate a word or sentence", key="translate_cmd_desc"),
    )
    @app_commands.rename(
        text=_("text", key="translate_cmd_text_name"),
        target_lang=_("target-lang", key="translate_cmd_target_lang_name"),
    )
    @app_commands.describe(
        text=_("The text to translate", key="translate_cmd_text_desc"),
        target_lang=_(
            "The target language for the translation (defaults to /set-lang setting).",
            key="translate_cmd_target_lang_desc",
        ),
    )
    async def translate(self, i: Interaction, text: str, target_lang: str | None = None) -> None:
        await i.response.defer(ephemeral=True)

        if target_lang is None:
            user_settings = await UserSettings.get_or_none(id=i.user.id)
            target_lang = user_settings.lang if user_settings else DEFAULT_TARGET_LANG

        translation = await APITranslator.deepl_translate(text, target_lang)
        await i.followup.send(translation, ephemeral=True)


async def setup(bot: Translatee) -> None:
    await bot.add_cog(TranslateCog(bot))
