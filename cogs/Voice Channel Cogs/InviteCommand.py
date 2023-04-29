from typing import Union

import discord
from discord import Forbidden, StageChannel, VoiceChannel, VoiceState
from discord import app_commands
from discord.app_commands import CommandOnCooldown
from discord.ext import commands

from Utils.channel_utils import ChannelUtils
from Utils.embeds import no_vc, successful_invite
from Utils.user_utils import UserUtils
from config import current_time


class InviteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    async def send_channel_invite(self, interaction: discord.Interaction, user: discord.Member,
                                  voice_channel: VoiceState):
        time = current_time()
        invite_obj = await self.bot.get_channel(voice_channel.channel.id).create_invite(
            reason="Auto Creation"
        )

        invite = invite_obj.url
        await user.send(
            embed=successful_invite(
                channel_link=invite, user=interaction.user
            ).set_footer(
                icon_url=interaction.guild.icon.url,
                text=f"{user.name} invited you a to [{voice_channel.channel.name}] at {time}", ))

    @app_commands.checks.cooldown(rate=3, per=30)
    @app_commands.command(
        name="invite", description="Invite users to channel through command"
    )
    async def invite(self, interaction: discord.Interaction, user: discord.Member):
        user_voice_state = interaction.user.voice

        if not user_voice_state:
            await interaction.response.send_message(embed=no_vc())
            return

        if not user:
            return

        user_channel_obj: Union[VoiceChannel, StageChannel] = user_voice_state.channel

        await self.send_channel_invite(interaction, user, user_voice_state)

        if UserUtils.is_channel_owner(interaction, user_channel_obj) and ChannelUtils.is_channel_locked(interaction,
                                                                                                        user_channel_obj):
            await user_channel_obj.set_permissions(target=user, connect=True, view_channel=True)
        await interaction.response.send_message("Invite Sent!", ephemeral=True)

    @invite.error
    async def invite_error(self, interaction: discord.Interaction, error) -> None:
        if isinstance(error.__cause__, Forbidden):
            await interaction.response.send_message(
                "You can't send invites to that user!", ephemeral=True
            )

        elif isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"You're on cooldown for {error.retry_after:.2f}s", ephemeral=True
            )
    
        elif isinstance(error, discord.app_commands.errors.CommandInvokeError):
             await interaction.response.send_message(
                f"Don't invite bots, silly", ephemeral=True)
        else:
            await interaction.response.send_message(
                f"Something went wrong...", ephemeral=True
            )
            print(error)


async def setup(bot: commands.Bot):
    await bot.add_cog(InviteCommand(bot))
