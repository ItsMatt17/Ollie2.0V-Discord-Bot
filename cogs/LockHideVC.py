import discord
from discord.ext import commands
from discord import app_commands


class LockHideVC(commands.Cog):

    def __init__(self, bot):
        self.bot : commands.Bot = bot

    @app_commands.command(name="lh", description="Lock and hide channels that you own")
    async def lh(self, interaction : discord.Interaction):
        voice_channel : discord.VoiceState = interaction.user.voice
        if not voice_channel:  # Check if user is in a voice channel on command send
            await interaction.response.send_message("You're not in a voice channel...")
            return
            
        owns_channel : bool = voice_channel.channel.overwrites_for(interaction.user).priority_speaker  # Way to check if user owns channel (giving specific perm on channel creation)
        #print(owns_channel)

        if not owns_channel:  # Checks is user owns channel
            await interaction.response.send_message("You don't own this channel... Try in a channel you created yourself!")
            return 
        
        locked = voice_channel.channel.permissions_for(interaction.guild.default_role)
        if not locked.view_channel:  # Checks if channel is already locked
            await interaction.response.send_message("Channel unlocked!", ephemeral=True)
            await voice_channel.channel.set_permissions(interaction.guild.default_role, view_channel=True, connect=True)
            return

        
        await voice_channel.channel.set_permissions(interaction.guild.default_role, view_channel=False, connect=False)
        await interaction.response.send_message("Channel Locked!", ephemeral=True)

        


async def setup(bot : commands.Bot):
    await bot.add_cog(LockHideVC(bot))
