import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown

from config import MY_ID


class TalkingStick(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.checks.cooldown(1, 10)
    @app_commands.command(name="talking_stick", description="Make a channel a talking stick")
    async def talking_stick(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You're not in a voice channel!")
            return

        if interaction.user.id != MY_ID:
            await interaction.response.send_message("You don't have perms loser")
            return

        channel = interaction.user.voice
        for user in channel.channel.members:  # All users in voice channel
            if user.id == interaction.user.id:
                continue
            print(f'[TALKING STICK] Muted {user}')

            await user.edit(
                mute=True)  # I think server mutes for every channel. Could be problem when someone leaves without me unmuting them.

        await interaction.response.send_message(
            "https://media.discordapp.net/attachments/602603671875747844/799212528600612904/image0.png")

    @app_commands.checks.cooldown(1, 10)
    @app_commands.command(name='untalking_stick', description="Untalking stick a channel")
    async def untalking_stick(self, interaction: discord.Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("You're not in a voice channel!")
            return

        if interaction.user.id != MY_ID:
            await interaction.response.send_message("You don't have perms loser")
            return

        channel = interaction.user.voice
        for user in channel.channel.members:
            if user.id == interaction.user.id:
                continue
            print(f'[TALKING STICK] Unmuted {user}')
            await user.edit(mute=False)
        await interaction.response.send_message("Untalking sticked")

    @talking_stick.error
    async def talking_stick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"You're on cooldown for {error.retry_after:.2f}s", ephemeral=True
            )

    @untalking_stick.error
    async def untalking_stick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"You're on cooldown for {error.retry_after:.2f}s", ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(TalkingStick(bot))
