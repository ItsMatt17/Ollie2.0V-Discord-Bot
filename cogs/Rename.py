import random
import typing

import discord
from discord import app_commands
from discord.ext import commands

from config import MY_ID

EMOJIS = ["😊", "😂", "😁", "😍", "😘", "😒", "😜", "👏", "💋", "😃", "🤔", "😆"]


class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="rename", description="rename voice channel")
    async def rename(self, interaction: discord.Interaction, rename_type: typing.Literal["status", "text"],
                     message: str = None):
        channel = interaction.user.voice
        if not channel:
            await interaction.response.send_message("You are currently not in a voice channel", ephemeral=True)
            return

        channel = channel.channel
        if not channel.overwrites_for(
                obj=interaction.user).priority_speaker and interaction.user.id != MY_ID:  # Not the one who created channel or not me
            await interaction.response.send_message("You don't own this channel...", ephemeral=True)
            return

        if rename_type == "text":
            if not message:
                await interaction.response.send_message("You have no message to add", ephemeral=True)
                return

            await interaction.response.send_message(f"Changed your channel name to `{message}`", ephemeral=True)
            await channel.edit(name=message)
            return

        if rename_type == "status":
            message_change = ""

            user = self.bot.get_guild(interaction.guild_id).get_member(interaction.user.id)

            game_activity = discord.utils.get(user.activities,
                                              type=discord.ActivityType.playing or discord.ActivityType.streaming)

            if not game_activity:
                await interaction.response.send_message("You don't have a game on right now!", ephemeral=True)
                return

            emoji = random.choice(EMOJIS)
            if game_activity.type == discord.ActivityType.playing:
                message_change = f"Playing {game_activity.name}"

            elif game_activity.type == discord.ActivityType.streaming:
                message_change = f"Streaming on {game_activity.platform} {emoji}"

            await channel.edit(name=message_change)


async def setup(bot):
    await bot.add_cog(Rename(bot))
