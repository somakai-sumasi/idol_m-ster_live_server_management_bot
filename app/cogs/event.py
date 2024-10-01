import discord

# from discord import app_commands
from discord.ext import commands
from cogs.base_cog import BaseUserCog


class Event(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        print(event.name)
        guild = event.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }
        await guild.create_category_channel(name=event.name, overwrites=overwrites)

    @commands.Cog.listener()
    async def on_scheduled_event_user_add(
        self, event: discord.ScheduledEvent, user: discord.User
    ):
        print("ほげ")


async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
