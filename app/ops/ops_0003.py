import re

import discord

from app.ops.ops_0000 import run_bot
from app.repository.event_repository import EventRepository
from app.service.event_service import EventUiView
from config.discord import NOTIFICATION_CHANNEL_ID


async def func(bot: discord.Client):
    guid: discord.Guild = await bot.fetch_guild(1287057723363688521)
    channel: discord.TextChannel = await guid.fetch_channel(NOTIFICATION_CHANNEL_ID)
    async for message in channel.history(limit=200):
        print(message.content)
        pattern = r"https://discord\.com/events/\d+/(\d+)"
        match = re.search(pattern, message.content)
        if match:
            event_id = match.group(1)
            print("抽出されたイベントID:", event_id)
        else:
            print("イベントIDが見つかりませんでした。")
            continue

        event_entity = EventRepository.get_by_scheduled_event_id(event_id)
        event_entity.message_id = message.id

        EventRepository.update(event_entity)

        await message.edit(
            content=message.content,
            view=EventUiView(),
        )


run_bot(func)
