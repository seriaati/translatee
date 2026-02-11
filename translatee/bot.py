from __future__ import annotations

import anyio
import discord
from discord.ext import commands
from tortoise import Tortoise

from translatee.bot_translator import BotTranslator, CommandTreeTranslator


class Translatee(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=intents,
            allowed_contexts=discord.app_commands.AppCommandContext(
                guild=True, dm_channel=True, private_channel=True
            ),
            allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True),
        )

    async def _load_cogs(self) -> None:
        async for cog_path in anyio.Path("translatee/cogs").glob("*.py"):
            cog_name = cog_path.stem
            await self.load_extension(f"translatee.cogs.{cog_name}")
        await self.load_extension("jishaku")

    async def setup_hook(self) -> None:
        BotTranslator.load_translations()
        await self._load_cogs()
        await self.tree.set_translator(CommandTreeTranslator())

        await Tortoise.init(
            db_url="sqlite://db.sqlite3", modules={"models": ["translatee.db.models"]}
        )
        await Tortoise.generate_schemas()

    async def close(self) -> None:
        await Tortoise.close_connections()
        await super().close()
