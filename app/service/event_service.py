import urllib.parse

import discord

from app.entity.event_entity import EventEntity
from app.repository.event_repository import EventRepository
from config.discord import BOTTOM_CHANNEL_ID, NOTIFICATION_CHANNEL_ID


class EventService:
    @classmethod
    async def create_event(cls, scheduled_event: discord.ScheduledEvent):
        guild = scheduled_event.guild
        guild_channel = discord.utils.get(guild.channels, id=BOTTOM_CHANNEL_ID)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
        }

        category = await guild.create_category(
            name=scheduled_event.name,
            overwrites=overwrites,
        )

        await category.move(after=guild_channel)

        text_channel = await guild.create_text_channel(
            "公式情報", category=category, position=0
        )
        await guild.create_text_channel("大事な内容", category=category, position=1)
        await guild.create_text_channel("雑談", category=category, position=2)

        EventRepository.create(
            EventEntity(scheduled_event_id=scheduled_event.id, category_id=category.id),
        )

        notification_channel: discord.TextChannel = discord.utils.get(
            guild.channels, id=NOTIFICATION_CHANNEL_ID
        )
        calendar_url = cls.creation_calendar_url(scheduled_event)

        message = (
            f"{text_channel.mention}\n"
            f"[イベント内容]({scheduled_event.url})\n"
            f"[Googleカレンダーに追加]({calendar_url})\n"
        )

        await notification_channel.send(message)

    @classmethod
    def creation_calendar_url(cls, scheduled_event: discord.ScheduledEvent) -> str:
        google_calendar_url = "https://www.google.com/calendar/render?action=TEMPLATE&"
        text = urllib.parse.quote(scheduled_event.name)
        start_time = scheduled_event.start_time.strftime("%Y%m%dT%H%M%SZ")
        end_time = scheduled_event.end_time.strftime("%Y%m%dT%H%M%SZ")
        dates = f"{start_time}/{end_time}"
        details = urllib.parse.quote(scheduled_event.description)
        location = urllib.parse.quote(scheduled_event.location)

        return (
            f"{google_calendar_url}text={text}&dates={dates}"
            f"&details={details}&location={location}"
        )

    @classmethod
    async def join_event(
        cls, scheduled_event: discord.ScheduledEvent, user: discord.User
    ):
        event = EventRepository.wait_for_get_by_scheduled_event_id(scheduled_event.id)

        guild = scheduled_event.guild
        category = discord.utils.get(guild.categories, id=event.category_id)
        await category.set_permissions(
            target=user, read_messages=True, send_messages=True
        )
