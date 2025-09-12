import urllib.parse

import discord

from app.entity.event_entity import EventEntity
from app.repository.event_repository import EventRepository
from config.discord import BOTTOM_CHANNEL_ID, NOTIFICATION_CHANNEL_ID


class EventService:
    """イベント管理サービス

    Discordのスケジュールイベントに関する処理を管理するサービスクラス。
    イベントの作成、更新、削除、参加/退出などの処理を提供する。
    """

    @classmethod
    def _get_notification_channel(
        cls, guild: discord.Guild
    ) -> discord.TextChannel | None:
        """通知チャンネルを取得する

        Parameters
        ----------
        guild : discord.Guild
            Discordサーバー

        Returns
        -------
        discord.TextChannel | None
            通知チャンネル（存在しない場合はNone）
        """
        return discord.utils.get(guild.channels, id=NOTIFICATION_CHANNEL_ID)

    @classmethod
    def _get_category_by_id(
        cls, guild: discord.Guild, category_id: int
    ) -> discord.CategoryChannel | None:
        """IDでカテゴリチャンネルを取得する

        Parameters
        ----------
        guild : discord.Guild
            Discordサーバー
        category_id : int
            カテゴリID

        Returns
        -------
        discord.CategoryChannel | None
            カテゴリチャンネル（存在しない場合はNone）
        """
        return discord.utils.get(guild.categories, id=category_id)

    @classmethod
    def _get_event_by_scheduled_event_id(cls, scheduled_event_id: int):
        """スケジュールイベントIDでイベントエンティティを取得する

        Parameters
        ----------
        scheduled_event_id : int
            スケジュールイベントID

        Returns
        -------
        EventEntity
            イベントエンティティ
        """
        return EventRepository.wait_for_get_by_scheduled_event_id(scheduled_event_id)

    @classmethod
    def _get_event_by_message_id(cls, message_id: int):
        """メッセージIDでイベントエンティティを取得する

        Parameters
        ----------
        message_id : int
            メッセージID

        Returns
        -------
        EventEntity
            イベントエンティティ
        """
        return EventRepository.wait_for_get_by_message_id(message_id)

    @classmethod
    def _create_notification_message(
        cls,
        scheduled_event: discord.ScheduledEvent,
        text_channel: discord.TextChannel,
    ) -> str:
        """通知メッセージを作成する

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            スケジュールイベント
        text_channel : discord.TextChannel
            テキストチャンネル

        Returns
        -------
        str
            通知メッセージの内容
        """
        calendar_url = cls.create_calendar_url(scheduled_event)
        return (
            f"{text_channel.mention}\n"
            f"[イベント内容]({scheduled_event.url})\n"
            f"[Googleカレンダーに追加]({calendar_url})\n"
        )

    @classmethod
    async def create_event(cls, scheduled_event: discord.ScheduledEvent):
        """イベントを作成する

        イベント用のカテゴリとチャンネルを作成し、通知を送信してDBに登録する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            作成するスケジュールイベント
        """
        guild = scheduled_event.guild
        [category, text_channel] = await cls.create_event_channels(scheduled_event)
        sent_message = await cls.send_notification(scheduled_event, guild, text_channel)

        EventRepository.create(
            EventEntity(
                scheduled_event_id=scheduled_event.id,
                category_id=category.id,
                message_id=sent_message.id,
            ),
        )
        await set_category_permissions(
            user=scheduled_event.creator,
            guild=guild,
            category_id=category.id,
            is_visible=True,
        )

    @classmethod
    async def delete_event(cls, scheduled_event: discord.ScheduledEvent):
        """イベントを削除する

        イベント用のカテゴリ、チャンネル、通知メッセージを削除する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            削除するスケジュールイベント
        """
        event = cls._get_event_by_scheduled_event_id(scheduled_event.id)
        category = cls._get_category_by_id(scheduled_event.guild, event.category_id)

        for channel in category.channels:
            await channel.delete()

        await category.delete()

        notification_channel = cls._get_notification_channel(scheduled_event.guild)
        message = await notification_channel.fetch_message(event.message_id)
        await message.delete()

    @classmethod
    async def update_event(
        cls, before: discord.ScheduledEvent, after: discord.ScheduledEvent
    ):
        """イベントを更新する

        イベント名が変更された場合、カテゴリとチャンネル名、通知メッセージを更新する。

        Parameters
        ----------
        before : discord.ScheduledEvent
            更新前のスケジュールイベント
        after : discord.ScheduledEvent
            更新後のスケジュールイベント
        """
        # イベント名が変更されていない場合は何もしない
        if before.name == after.name:
            return

        guild = after.guild
        # DBからイベント情報を取得
        event_entity = EventRepository.get_by_scheduled_event_id(after.id)
        if event_entity is None:
            return

        # カテゴリチャンネルの名前を更新
        category = cls._get_category_by_id(guild, event_entity.category_id)
        if category:
            await category.edit(name=after.name)

            # カテゴリ内のテキストチャンネルのトピックを更新
            for channel in category.text_channels:
                await channel.edit(topic=after.name)

        # 通知メッセージを更新
        notification_channel = cls._get_notification_channel(guild)
        if notification_channel:
            try:
                message = await notification_channel.fetch_message(
                    event_entity.message_id
                )

                # カテゴリ内の最初のテキストチャンネルを取得
                text_channel = (
                    category.text_channels[0]
                    if category and category.text_channels
                    else None
                )

                if text_channel:
                    new_content = cls._create_notification_message(after, text_channel)
                    await message.edit(content=new_content)
            except discord.NotFound:
                # メッセージが見つからない場合はログを出力
                pass

    @classmethod
    async def create_event_channels(
        cls, scheduled_event: discord.ScheduledEvent
    ) -> tuple[discord.CategoryChannel, discord.TextChannel]:
        """イベント用のチャンネルを作成する

        イベント専用のカテゴリと3つのテキストチャンネル（公式情報、大事な内容、雑談）を作成する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            スケジュールイベント

        Returns
        -------
        tuple[discord.CategoryChannel, discord.TextChannel]
            作成したカテゴリと最初のテキストチャンネル
        """

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
            "公式情報",
            category=category,
            position=0,
            topic=scheduled_event.name,
        )
        await guild.create_text_channel(
            "大事な内容",
            category=category,
            position=1,
            topic=scheduled_event.name,
        )
        await guild.create_text_channel(
            "雑談",
            category=category,
            position=2,
            topic=scheduled_event.name,
        )

        return category, text_channel

    @classmethod
    async def send_notification(
        cls,
        scheduled_event: discord.ScheduledEvent,
        guild: discord.Guild,
        text_channel: discord.TextChannel,
    ):
        """イベント通知を送信する

        通知チャンネルにイベントの詳細とボタンUIを含むメッセージを送信する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            スケジュールイベント
        guild : discord.Guild
            Discordサーバー
        text_channel : discord.TextChannel
            イベント用のテキストチャンネル

        Returns
        -------
        discord.Message
            送信したメッセージ
        """
        message = cls._create_notification_message(scheduled_event, text_channel)

        notification_channel = cls._get_notification_channel(guild)
        sent_message = await notification_channel.send(
            content=message, view=EventUIView()
        )

        return sent_message

    @classmethod
    def create_calendar_url(cls, scheduled_event: discord.ScheduledEvent) -> str:
        """Googleカレンダー追加URLを生成する

        スケジュールイベントの情報からGoogleカレンダーに追加するためのURLを生成する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            スケジュールイベント

        Returns
        -------
        str
            Googleカレンダー追加用のURL
        """
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
        """イベントに参加する

        ユーザーにイベント用カテゴリの閲覧・書き込み権限を付与する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            スケジュールイベント
        user : discord.User
            参加するユーザー
        """
        event = cls._get_event_by_scheduled_event_id(scheduled_event.id)
        await set_category_permissions(
            user=user,
            guild=scheduled_event.guild,
            category_id=event.category_id,
            is_visible=True,
        )

    @classmethod
    async def leave_event(
        cls, scheduled_event: discord.ScheduledEvent, user: discord.User
    ):
        """イベントから退出する

        ユーザーのイベント用カテゴリの閲覧・書き込み権限を削除する。

        Parameters
        ----------
        scheduled_event : discord.ScheduledEvent
            スケジュールイベント
        user : discord.User
            退出するユーザー
        """
        event = cls._get_event_by_scheduled_event_id(scheduled_event.id)
        await set_category_permissions(
            user=user,
            guild=scheduled_event.guild,
            category_id=event.category_id,
            is_visible=False,
        )


class EventUIView(discord.ui.View):
    """イベントUIビュー

    イベントチャンネルへの参加・退出ボタンを提供するUIコンポーネント。
    """

    def __init__(self):
        """イベントUIビューを初期化する"""
        super().__init__(timeout=None)

    @discord.ui.button(
        label="ライブ用チャンネルを見る",
        style=discord.ButtonStyle.green,
        custom_id="persistent_view:join",
    )
    async def join(self, interaction: discord.Interaction, _: discord.ui.Button):
        """ライブ用チャンネル参加ボタンの処理

        Parameters
        ----------
        interaction : discord.Interaction
            Discordのインタラクション
        _ : discord.ui.Button
            押されたボタン（未使用）
        """
        message_id = interaction.message.id

        event = EventService._get_event_by_message_id(message_id)
        await set_category_permissions(
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
    async def leave(self, interaction: discord.Interaction, _: discord.ui.Button):
        """ライブ用チャンネルからの退出ボタンの処理

        Parameters
        ----------
        interaction : discord.Interaction
            Discordのインタラクション
        _ : discord.ui.Button
            押されたボタン（未使用）
        """
        message_id = interaction.message.id

        event = EventService._get_event_by_message_id(message_id)
        await set_category_permissions(
            user=interaction.user,
            guild=interaction.guild,
            category_id=event.category_id,
            is_visible=False,
        )

        await interaction.response.send_message(
            "ライブ用チャンネルから抜けました", ephemeral=True
        )


async def set_category_permissions(
    user: discord.User,
    guild: discord.Guild,
    category_id: int,
    is_visible: bool,
):
    """カテゴリの権限を操作する

    指定されたユーザーのカテゴリへのアクセス権限を設定する。

    Parameters
    ----------
    user : discord.User
        権限を設定するユーザー
    guild : discord.Guild
        Discordサーバー
    category_id : int
        カテゴリID
    is_visible : bool
        Trueの場合は閲覧・書き込み可能、Falseの場合は不可
    """
    category = discord.utils.get(guild.categories, id=category_id)
    await category.set_permissions(
        target=user, read_messages=is_visible, send_messages=is_visible
    )
