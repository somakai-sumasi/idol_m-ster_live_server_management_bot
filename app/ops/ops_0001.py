import sys

import discord
from app.ops.ops_0000 import run_bot


async def func(bot: discord.Client):
    guid: discord.Guild = await bot.fetch_guild(1287057723363688521)
    channel: discord.TextChannel = await guid.fetch_channel(1288306808850612315)
    message: discord.Message = await channel.fetch_message(1348693353155395625)
    content = (
        "<#1348693348537335858>\n"
        "[イベント内容](https://discord.com/events/1287057723363688521/1348693337632407614)\n"
        "[Googleカレンダーに追加](https://www.google.com/calendar/render?action=TEMPLATE&text=Let%E2%80%99s%20AMUSEMENT%21%21%21%20%E6%9D%B1%E4%BA%AC%E5%85%AC%E6%BC%94&dates=20250311T080000Z/20250426T110000Z&details=&location=%E6%9C%89%E6%98%8E%E3%82%A2%E3%83%AA%E3%83%BC%E3%83%8A)"
    )
    await message.edit(content=content)
    sys.exit()


run_bot(func)
