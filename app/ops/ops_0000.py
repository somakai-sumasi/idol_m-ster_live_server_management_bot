import discord
from discord.ext import commands

from config.discord import TOKEN


class BaseBot(commands.Bot):
    def __init__(self, callback_func: callable) -> None:
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents)
        self.callback_func = callback_func

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        await self.callback_func(self)


def run_bot(callback_func: callable):
    bot = BaseBot(callback_func)
    bot.run(TOKEN)
