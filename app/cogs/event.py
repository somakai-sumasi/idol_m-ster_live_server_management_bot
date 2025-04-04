import discord
from cogs.base_cog import BaseUserCog
from discord.ext import commands
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
        await EventService.join_event(event, user)

    @commands.Cog.listener()
    async def on_scheduled_event_user_remove(
        self, event: discord.ScheduledEvent, user: discord.User
    ):
        await EventService.leave_event(event, user)


async def setup(bot: commands.Bot):
    await bot.add_cog(Event(bot))
