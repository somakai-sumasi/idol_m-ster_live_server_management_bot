import urllib.parse

import discord

from app.entity.event_entity import EventEntity
from app.repository.event_repository import EventRepository
from config.discord import BOTTOM_CHANNEL_ID, NOTIFICATION_CHANNEL_ID


class EventService:
    @classmethod
    async def create_event(cls, scheduled_event: discord.ScheduledEvent):
        guild = scheduled_event.guild
        [category, text_channel] = await cls.create_event_channels(scheduled_event)
        send_message = await cls.send_notification(scheduled_event, guild, text_channel)

        EventRepository.create(
            EventEntity(
                scheduled_event_id=scheduled_event.id,
                category_id=category.id,
                message_id=send_message.id,
            ),
        )
        await category_permission_operation(
            user=scheduled_event.creator,
            guild=guild,
            category_id=category.id,
            is_visible=True,
        )

    @classmethod
    async def delete_event(cls, scheduled_event: discord.ScheduledEvent):
        event = EventRepository.wait_for_get_by_scheduled_event_id(scheduled_event.id)
        category = discord.utils.get(
            scheduled_event.guild.categories, id=event.category_id
        )

        for channel in category.channels:
            await channel.delete()

        await category.delete()

        notification_channel: discord.TextChannel = discord.utils.get(
            scheduled_event.guild.channels, id=NOTIFICATION_CHANNEL_ID
        )
        message = await notification_channel.fetch_message(event.message_id)
        await message.delete()

    @classmethod
    async def create_event_channels(
        cls, scheduled_event: discord.ScheduledEvent
    ) -> tuple[discord.CategoryChannel, discord.TextChannel]:

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

        return category, text_channel

    @classmethod
    async def send_notification(
        cls,
        scheduled_event: discord.ScheduledEvent,
        guild: discord.Guild,
        text_channel: discord.TextChannel,
    ):
        calendar_url = cls.creation_calendar_url(scheduled_event)

        message = (
            f"{text_channel.mention}\n"
            f"[イベント内容]({scheduled_event.url})\n"
            f"[Googleカレンダーに追加]({calendar_url})\n"
        )

        notification_channel: discord.TextChannel = discord.utils.get(
            guild.channels, id=NOTIFICATION_CHANNEL_ID
        )
        # send_message = await notification_channel.send(
        #     content=message, view=EventUiView()
        # )

        send_message = await notification_channel.send(content=message)

        return send_message

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
        await category_permission_operation(
            user=user,
            guild=scheduled_event.guild,
            category_id=event.category_id,
            is_visible=True,
        )

    @classmethod
    async def leave_event(
        cls, scheduled_event: discord.ScheduledEvent, user: discord.User
    ):
        event = EventRepository.wait_for_get_by_scheduled_event_id(scheduled_event.id)
        await category_permission_operation(
            user=user,
            guild=scheduled_event.guild,
            category_id=event.category_id,
            is_visible=False,
        )


class EventUiView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="ライブ用チャンネルを見る",
        style=discord.ButtonStyle.green,
        custom_id="persistent_view:join",
    )
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        message_id = interaction.message.id

        event = EventRepository.wait_for_get_by_message_id(message_id)
        await category_permission_operation(
            user=interaction.user,
            guild=interaction.guild,
            category_id=event.category_id,
            is_visible=True,
        )

        await interaction.response.send_message(
            "ライブ用チャンネルに参加しました", ephemeral=True
        )

    @discord.ui.button(
        label="ライブ用チャンネルから抜ける",
        style=discord.ButtonStyle.red,
        custom_id="persistent_view:leave",
    )
    async def leave(self, interaction: discord.Interaction, button: discord.ui.Button):
        message_id = interaction.message.id

        event = EventRepository.wait_for_get_by_message_id(message_id)
        await category_permission_operation(
            user=interaction.user,
            guild=interaction.guild,
            category_id=event.category_id,
            is_visible=False,
        )

        await interaction.response.send_message(
            "ライブ用チャンネルから抜けました", ephemeral=True
        )


async def category_permission_operation(
    user: discord.User, guild: discord.Guild, category_id: int, is_visible: bool
):
    category = discord.utils.get(guild.categories, id=category_id)
    await category.set_permissions(
        target=user, read_messages=is_visible, send_messages=is_visible
    )
