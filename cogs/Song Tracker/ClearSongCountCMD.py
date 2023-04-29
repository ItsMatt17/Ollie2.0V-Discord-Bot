import discord
from discord import app_commands
from discord.ext import commands

from bot import OllieV2
from config import MY_ID


class ClearSongCount(commands.Cog):
    def __init__(self, bot: OllieV2):
        self.bot: OllieV2 = bot

    @app_commands.command(name='clear', description="Clear user's data")
    @commands.is_owner()
    async def clear(self, interaction: discord.Interaction, user: discord.Member):
        user_id: int = user.id
        response = await self.bot.db.execute("update public.users set song_tracker = 0 where discord_id = $1", user_id)
        if response == -1:
            return await interaction.response.send_message(f"{user.display_name} has no data data")
        await interaction.response.send_message(f"{user.display_name}'s data has been reset")

    @app_commands.command(name="clear_all", description="Clear all user's data")
    async def clear_all(self, interaction: discord.Interaction):
        if interaction.user.id != MY_ID:
            return

        await interaction.response.send_message("Cleared all users")


async def setup(bot: OllieV2):
    await bot.add_cog(ClearSongCount(bot))
