import re

import discord
from discord.ext import commands

from app.entity.user_idol_preference_entity import UserIdolPreferencesEntity
from app.repository.user_idol_preference_repository import UserIdolPreferencesRepository


class PreferencesService:
    @classmethod
    async def set_idol_preferences(cls, interaction: discord.Interaction):
        user_id = interaction.user.id
        preferences_entity = UserIdolPreferencesRepository.get_by_user_id(user_id)
        await interaction.response.send_modal(
            IdolPreferences(preferences_entity, cls.update_idol_preferences)
        )

    @classmethod
    async def search_idol_preferences(
        cls, bot: commands.Bot, interaction: discord.Interaction, search_name
    ):
        await interaction.response.defer()

        tantou_preferences = UserIdolPreferencesRepository.get_by_tantou(search_name)
        favorite_preferences = UserIdolPreferencesRepository.get_by_favorite(
            search_name
        )

        tantou_users = [
            bot.get_user(preference.user_id).mention
            for preference in tantou_preferences
        ]
        favorite_users = [
            bot.get_user(preference.user_id).mention
            for preference in favorite_preferences
        ]

        preferences = discord.Embed(title=f"{search_name}での検索結果")
        preferences.add_field(
            name="担当のユーザー", value=" ".join(tantou_users), inline=False
        )
        preferences.add_field(name="", value="", inline=False)
        preferences.add_field(
            name="推しのユーザー", value=" ".join(favorite_users), inline=False
        )

        await interaction.followup.send(embed=preferences)

    @classmethod
    async def search_user_preferences(
        cls, interaction: discord.Interaction, member: discord.Member
    ):
        await interaction.response.defer()
        preferences_entity = UserIdolPreferencesRepository.get_by_user_id(member.id)
        preferences = discord.Embed()

        icon_url = (
            member.avatar is None and member.default_avatar.url or member.avatar.url
        )
        preferences.set_author(name=member.display_name, icon_url=icon_url)

        if preferences_entity is None:
            preferences.description = "登録情報がありません"
            await interaction.followup.send(embed=preferences)
            return

        preferences.add_field(
            name="担当アイドル",
            value=",".join(preferences_entity.tantou_idols),
            inline=False,
        )
        preferences.add_field(name="", value="", inline=False)
        preferences.add_field(
            name="推しのアイドル",
            value=",".join(preferences_entity.favorite_idols),
            inline=False,
        )
        await interaction.followup.send(embed=preferences)

    @classmethod
    def update_idol_preferences(
        cls, is_new_row: bool, preferences_entity: UserIdolPreferencesEntity
    ):
        if is_new_row:
            return UserIdolPreferencesRepository.create(preferences_entity)
        else:
            return UserIdolPreferencesRepository.update(preferences_entity)


class IdolPreferences(discord.ui.Modal):
    def __init__(
        self,
        preferences_entity: UserIdolPreferencesEntity,
        callback_func: callable,
    ):
        super().__init__(
            title="好きなアイドルを設定してください",
        )

        self.is_new_data = preferences_entity is None

        self.tantou_input = Input(
            "担当アイドル",
            "" if self.is_new_data else "\n".join(preferences_entity.tantou_idols),
        )
        self.favorite_input = Input(
            "推しのアイドル",
            "" if self.is_new_data else "\n".join(preferences_entity.favorite_idols),
        )

        self.add_item(self.tantou_input)
        self.add_item(self.favorite_input)
        self.callback_func = callback_func

    async def on_submit(self, interaction: discord.Interaction) -> None:
        tantou_idols = re.split("[\n,、]", self.tantou_input.value)
        favorite_idols = re.split("[\n,、]", self.favorite_input.value)

        self.callback_func(
            self.is_new_data,
            UserIdolPreferencesEntity(
                user_id=interaction.user.id,
                tantou_idols=tantou_idols,
                favorite_idols=favorite_idols,
            ),
        )

        await interaction.response.send_message(
            f"好きなアイドルを設定しました\n{', '.join(tantou_idols)}\n{', '.join(favorite_idols)}",
            ephemeral=True,
        )


class Input(discord.ui.TextInput):
    def __init__(self, label: str, default: str):
        super().__init__(
            label=label,
            default=default,
            style=discord.TextStyle.long,
            placeholder=",、改行で区切ってください",
        )
