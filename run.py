from __future__ import annotations

import os

from dotenv import load_dotenv

from translatee.bot import Translatee

load_dotenv()
bot = Translatee()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
