import json

import discord
from discord import app_commands
from discord.ext import commands

from config import MY_ID


class ClearSongCount(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.SONG_COUNTER_PATH: str = "storage/song_counter.json"

    @app_commands.command(name='clear', description="Clear user's data")
    async def clear(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.user.id != MY_ID:
            return

        user_id: int = user.id
        with open(self.SONG_COUNTER_PATH, "r+") as file:
            data = json.load(file)
            if not str(user_id) in data["User"]:  # If user's id not in file
                await interaction.response.send_message("User doesn't have any data")
                return

            data["User"][f"{user_id}"] = 0  # Set counter to 0
            file.seek(0)
            json.dump(data, file)
            file.truncate()

            await interaction.response.send_message(f"{user.display_name}'s data has been reset")

    @app_commands.command(name="clear_all", description="Clear all user's data")
    async def clear_all(self, interaction: discord.Interaction):
        if interaction.user.id != MY_ID:
            return

        with open(self.SONG_COUNTER_PATH, "r+") as file:
            data = json.load(file)
            data["basic_songs"] = 0

            for key, value in data["User"].items():
                data["User"][f"{key}"] = 0

            file.seek(0)
            json.dump(data, file)
            file.truncate()
        await interaction.response.send_message("Cleared all users")


async def setup(bot: commands.Bot):
    await bot.add_cog(ClearSongCount(bot))
