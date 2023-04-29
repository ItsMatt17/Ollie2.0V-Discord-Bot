import discord
from discord import app_commands
from discord.ext import commands

from Utils.user_utils import UserUtils


class LockHideVC(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @app_commands.command(name="lh", description="Lock and hide channels that you own")
    async def lh(self, interaction: discord.Interaction):
        voice_channel: discord.VoiceState = interaction.user.voice

        if not voice_channel:
            # Check if user is in voice channel or not
            await interaction.response.send_message("You're not in a voice channel...")
            return

        voice_obj = voice_channel.channel
        if not UserUtils.is_channel_owner(interaction=interaction, channel=voice_obj):  # Checks is user owns channel
            await interaction.response.send_message(
                "You don't own this channel... Try in a channel you created yourself!")
            return

        if not ChannelUtils.is_channel_locked(interaction=interaction,
                                              voice_channel=voice_obj):  # Checks if channel is already locked
            await interaction.response.send_message("Channel unlocked!", ephemeral=True)
            await voice_channel.channel.set_permissions(interaction.guild.default_role, view_channel=True, connect=True)
            return

        await voice_channel.channel.set_permissions(interaction.guild.default_role, view_channel=False, connect=False)
        await interaction.response.send_message("Channel Locked!", ephemeral=True)




async def setup(bot : commands.Bot):
    await bot.add_cog(LockHideVC(bot))
