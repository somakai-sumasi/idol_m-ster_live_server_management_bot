import discord
from discord import app_commands
from discord.ext import commands

from app.cogs.base_cog import BaseUserCog
from app.service.preferences_service import PreferencesService


class Preferences(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.command(description="好きなアイドルを設定出来ます")
    async def set_idol_preferences(self, interaction: discord.Interaction):
        await PreferencesService.set_idol_preferences(interaction)

    @app_commands.command(
        description="他のユーザーの好きなアイドルを検索出来ます(前方後方一致)"
    )
    @app_commands.rename(search_name="検索するアイドル名")
    async def search_idol_preferences(
        self, interaction: discord.Interaction, search_name: str
    ):
        await PreferencesService.search_idol_preferences(
            self.bot, interaction, search_name
        )

    @app_commands.command(description="ユーザーの好きなアイドルを検索出来ます")
    @app_commands.rename(member="検索するユーザー")
    async def search_user_preferences(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
    ):
        await PreferencesService.search_user_preferences(interaction, member)


async def setup(bot: commands.Bot):
    await bot.add_cog(Preferences(bot))
