import random

import discord
from discord.ext import commands

EMOJIS = ["😊", "😂", "😁", "😍", "😘", "😒", "😜", "👏", "💋", "😃", "🤔", "😆"]

class VCChannelCreator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.channel_obj: list[discord.VoiceChannel] = []

    async def empty_checker(self, guild: discord.Guild) -> None:
        channel: discord.VoiceChannel
        if len(self.channel_obj) <= 0:  # If there are no custom channels
            return

        for channel in self.channel_obj:  # Iterates through a list of custom channels
            if len(channel.members) == 0:
                self.channel_obj.remove(channel)
                await channel.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: discord.Member,
            before: discord.VoiceState,
            after: discord.VoiceState,
    ):
        guild: discord.Guild = member.guild

        await self.empty_checker(guild)

        if not after.channel:  # Why does this work now........
            return

        if (
                after.channel.name != "[+] Create Channel"
        ):  # Check if user does not join channel creator
            return

        channel_name: str = member.display_name  # Get user's name/nick for channel name
        category: discord.CategoryChannel = after.channel.category  # Gets category channel creator is in
        overwrites: dict[discord.Member, discord.PermissionOverwrite] = {
            member: discord.PermissionOverwrite(priority_speaker=True, view_channel=True, connect=True),
            guild.default_role: discord.PermissionOverwrite(stream=True, send_messages=True)}
        position: int = len(guild.voice_channels)
        channel_emoji = random.choice(EMOJIS)

        channel_name: str = f"{channel_name}'s Channel {channel_emoji}"

        created_channel: discord.VoiceChannel = await guild.create_voice_channel(
            name=channel_name, position=position, category=category, overwrites=overwrites
        )  # Creates channel

        await member.move_to(
            channel=created_channel, reason="Auto Bot Move"
        )  # Moves user

        self.channel_obj.append(
            created_channel
        )  # Adds to list to keep track of channel objects


async def setup(bot: commands.Bot):
    await bot.add_cog(VCChannelCreator(bot))
