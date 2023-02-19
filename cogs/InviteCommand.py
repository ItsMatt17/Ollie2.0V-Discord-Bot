import logging

import discord
from discord import Forbidden
from discord import app_commands
from discord.app_commands import CommandOnCooldown
from discord.ext import commands

from Utils.embeds import no_vc, successful_invite
from config import current_time


class InviteCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @app_commands.checks.cooldown(rate=3, per=30)
    @app_commands.command(
        name="invite", description="Invite users to channel through command"
    )
    async def invite(self, interaction: discord.Interaction, user: discord.Member):
        user_voice_state = interaction.user.voice

        if not user_voice_state:
            await interaction.response.send_message(embed=no_vc())
            return

        if user:
            user_channel_obj = user_voice_state.channel
            user_channel_id = user_voice_state.channel.id
            time = current_time()

            users_dm = await self.bot.create_dm(user)
            if isinstance(users_dm, discord.DMChannel):
                invite_obj = await self.bot.get_channel(user_channel_id).create_invite(
                    reason="Auto Creation"
                )

                invite = invite_obj.url
                await users_dm.send(
                    embed=successful_invite(
                        channel_link=invite, user=interaction.user
                    ).set_footer(
                        icon_url=interaction.guild.icon.url,
                        text=f"{user.name} invited you a to [{user_voice_state.channel.name}] at {time}",
                    )
                )
                if not user_channel_obj.overwrites_for(interaction.guild.default_role).view_channel:
                    await user_channel_obj.set_permissions(target=user, connect=True, view_channel=True)
                await interaction.response.send_message("Invite Sent!", ephemeral=True)

    @invite.error
    async def invite_error(self, interaction: discord.Interaction, error) -> None:
        logging.critical(error.__cause__, type(error))
        if isinstance(error.__cause__, Forbidden):
            logging.error("Not allowed to message that user!")
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
