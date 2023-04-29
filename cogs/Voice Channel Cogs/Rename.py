import random
import typing

import discord
from discord import app_commands
from discord.ext import commands

from Utils.user_utils import UserUtils

EMOJIS = ["😊", "😂", "😁", "😍", "😘", "😒", "😜", "👏", "💋", "😃", "🤔", "😆"]


async def status_choice(interaction: discord.Interaction, message: str = None):
    message_change = ""

    game_activity = discord.utils.get(interaction.user.activities,
                                      type=discord.ActivityType.playing or discord.ActivityType.streaming)
    if not game_activity:
        await interaction.response.send_message("You don't have a game on right now!", ephemeral=True)
        return False

    emoji = random.choice(EMOJIS)
    if game_activity.type == discord.ActivityType.playing:
        message_change = f"Playing {game_activity.name} {emoji}"

    elif game_activity.type == discord.ActivityType.streaming:
        message_change = f"Streaming on {game_activity.platform} {emoji}"

    return message_change


async def text_choice(interaction: discord.Interaction, message):
    if not message:
        await interaction.response.send_message("You have no message to add", ephemeral=True)
        return

    await interaction.response.send_message(f"Changed your channel name to `{message}`", ephemeral=True)

    return message


options = {
    "status": status_choice,
    "text": text_choice
}


class Rename(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="rename", description="rename voice channel")
    async def rename(self, interaction: discord.Interaction, rename_type: typing.Literal["status", "text"],
                     message: str = None):

        channel: discord.VoiceState = interaction.user.voice
        if not channel:
            await interaction.response.send_message("You are currently not in a voice channel", ephemeral=True)
            return

        voice_obj: discord.VoiceChannel = channel.channel
        if not UserUtils.is_channel_owner(interaction=interaction, voice_channel=voice_obj):
            await interaction.response.send_message("You don't own this channel...", ephemeral=True)
            return

        option_func = options.get(rename_type)
        message_change = await option_func(interaction, message)
        if not message_change:
            return

        await voice_obj.edit(name=message_change)


async def setup(bot):
    await bot.add_cog(Rename(bot))
