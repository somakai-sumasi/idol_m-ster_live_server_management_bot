import logging

import discord
from config.discord import TOKEN
from discord.ext import commands

INITIAL_EXTENSIONS = ["cogs.event"]


class MainBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for cog in INITIAL_EXTENSIONS:
            await self.load_extension(cog)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


bot = MainBot()
handler = logging.FileHandler(filename="./logs/discord.log", encoding="utf-8", mode="a")
bot.run(TOKEN, log_handler=handler)
