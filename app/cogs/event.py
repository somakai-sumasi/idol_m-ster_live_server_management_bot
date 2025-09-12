import discord
from discord.ext import commands

from app.cogs.base_cog import BaseUserCog
from app.service.event_service import EventService


class Event(BaseUserCog):
    """イベント管理Cog

    Discordのスケジュールイベントを監視し、作成・更新・削除・参加・退出の
    イベントをハンドリングする。
    """

    def __init__(self, bot: commands.Bot):
        """イベントCogを初期化する

        Parameters
        ----------
        bot : commands.Bot
            Discord Botインスタンス
        """
        super().__init__(bot)

    @commands.Cog.listener()
    async def on_scheduled_event_create(self, event: discord.ScheduledEvent):
        """スケジュールイベント作成時の処理

        Discordでスケジュールイベントが作成された時に、専用チャンネルと
        通知を作成する。

        Parameters
        ----------
        event : discord.ScheduledEvent
            作成されたスケジュールイベント
        """
        await EventService.create_event(event)

    @commands.Cog.listener()
    async def on_scheduled_event_delete(self, event: discord.ScheduledEvent):
        """スケジュールイベント削除時の処理

        Discordでスケジュールイベントが削除された時に、関連する
        チャンネルと通知を削除する。

        Parameters
        ----------
        event : discord.ScheduledEvent
            削除されたスケジュールイベント
        """
        await EventService.delete_event(event)

    @commands.Cog.listener()
    async def on_scheduled_event_update(
        self, before: discord.ScheduledEvent, after: discord.ScheduledEvent
    ):
        """スケジュールイベント更新時の処理

        Discordでスケジュールイベントが更新された時に、関連する
        チャンネル名や通知を更新する。

        Parameters
        ----------
        before : discord.ScheduledEvent
            更新前のスケジュールイベント
        after : discord.ScheduledEvent
            更新後のスケジュールイベント
        """
        await EventService.update_event(before, after)

    @commands.Cog.listener()
    async def on_scheduled_event_user_add(
        self, event: discord.ScheduledEvent, user: discord.User
    ):
        """スケジュールイベントへのユーザー参加時の処理

        ユーザーがスケジュールイベントに参加した時に、専用チャンネルへの
        アクセス権限を付与する。

        Parameters
        ----------
        event : discord.ScheduledEvent
            スケジュールイベント
        user : discord.User
            参加したユーザー
        """
        await EventService.join_event(event, user)

    @commands.Cog.listener()
    async def on_scheduled_event_user_remove(
        self, event: discord.ScheduledEvent, user: discord.User
    ):
        """スケジュールイベントからのユーザー退出時の処理

        ユーザーがスケジュールイベントから退出した時に、専用チャンネルへの
        アクセス権限を削除する。

        Parameters
        ----------
        event : discord.ScheduledEvent
            スケジュールイベント
        user : discord.User
            退出したユーザー
        """
        await EventService.leave_event(event, user)


async def setup(bot: commands.Bot):
    """イベントCogをBotに登録する

    Discord.pyのCogシステムで必要なセットアップ関数。

    Parameters
    ----------
    bot : commands.Bot
        Discord Botインスタンス
    """
    await bot.add_cog(Event(bot))
