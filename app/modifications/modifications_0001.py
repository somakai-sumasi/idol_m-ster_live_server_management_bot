from modifications.modifications_0000 import run_bot
import discord
import sys


async def func(bot: discord.Client):
    guid: discord.Guild = await bot.fetch_guild(713594826343579681)
    channel: discord.TextChannel = await guid.fetch_channel(713601276465905715)
    message: discord.Message = await channel.fetch_message(1348584964253552660)
    content = (
        "<#1348693348537335858>\n"
        "[イベント内容](https://discord.com/events/1287057723363688521/1348693337632407614)\n"
        "[Googleカレンダーに追加](https://www.google.com/calendar/render?action=TEMPLATE&text=Let%E2%80%99s%20AMUSEMENT%21%21%21%20%E6%9D%B1%E4%BA%AC%E5%85%AC%E6%BC%94&dates=20250311T080000Z/20250426T110000Z&details=&location=%E6%9C%89%E6%98%8E%E3%82%A2%E3%83%AA%E3%83%BC%E3%83%8A)"
    )
    await message.edit(content=content)
    sys.exit()


run_bot(func)
