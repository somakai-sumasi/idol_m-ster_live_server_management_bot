import discord
from config.discord import BOTTOM_CHANNEL_ID, NOTIFICATION_CHANNEL_ID
from entity.event_entity import EventEntity
from repository.event_repository import EventRepository


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
            position=guild_channel.position + 1,
        )
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
        message = f"{text_channel.mention}\n[イベント内容]({scheduled_event.url})"
        await notification_channel.send(message)

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
