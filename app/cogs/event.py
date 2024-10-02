import discord
import asyncio

# from discord import app_commands
from discord.ext import commands
from cogs.base_cog import BaseUserCog

from service.event_service import EventService


class Event(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        await EventService.create_event(event)

    @commands.Cog.listener()
    async def on_scheduled_event_user_add(
        self, event: discord.ScheduledEvent, user: discord.User
    ):
        # イベント作成処理が完了しないことがあるので一旦1秒待つ
        await asyncio.sleep(1)
        print(f"{event.name} {user.name}")

        guild = event.guild
        category_name = event.name
        category = discord.utils.get(guild.categories, name=category_name)
        await category.set_permissions(
            target=user, read_messages=True, send_messages=True
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
