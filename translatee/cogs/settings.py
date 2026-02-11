from __future__ import annotations

from typing import TYPE_CHECKING

from discord import app_commands
from discord.app_commands import locale_str as _
from discord.ext import commands

from translatee.constants import SUPPORTED_LANGUAGES
from translatee.db.models import UserSettings

if TYPE_CHECKING:
    from translatee.bot import Translatee
    from translatee.types import Interaction


class SettingsCog(commands.Cog):
    def __init__(self, bot: Translatee) -> None:
        self.bot = bot

    @app_commands.command(
        name=_("set-lang", key="set_lang_cmd_name"),
        description=_("Set your target translation language", key="set_lang_cmd_desc"),
    )
    @app_commands.rename(lang=_("lang", key="set_lang_cmd_lang_name"))
    @app_commands.describe(
        lang=_("The language to set as your target language", key="set_lang_cmd_lang_desc")
    )
    async def set_language(self, i: Interaction, lang: str) -> None:
        if lang not in SUPPORTED_LANGUAGES:
            await i.response.send_message(
                "不支援的語言, 請使用自動完成選擇一個有效的語言", ephemeral=True
            )
            return

        user_settings, _ = await UserSettings.get_or_create(id=i.user.id)
        user_settings.lang = lang
        await user_settings.save()
        await i.response.send_message(
            f"你的目標語言已設定為 {SUPPORTED_LANGUAGES[lang]}", ephemeral=True
        )

    @set_language.autocomplete("lang")
    async def lang_autocomplete(
        self, _i: Interaction, current: str
    ) -> list[app_commands.Choice[str]]:
        choices: list[app_commands.Choice[str]] = []
        current_lower = current.lower()

        for code, name in SUPPORTED_LANGUAGES.items():
            if current_lower in code.lower() or current_lower in name.lower():
                choices.append(app_commands.Choice(name=f"{name}", value=code))
            if len(choices) >= 25:
                break

        return choices


async def setup(bot: Translatee) -> None:
    await bot.add_cog(SettingsCog(bot))
