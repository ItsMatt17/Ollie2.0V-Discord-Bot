import random
import logging

import discord
from discord.ext import commands

from config import TESTING_CHANNEL


EMOJIS = ["😊", "😂", "😁", "😍", "😘", "😒", "😜", "👏", "💋", "😃", "🤢", "🤔", "😆"]
logging.basicConfig(level=0)

class VCChannelCreator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.channel_obj: discord.VoiceChannel = []
        self.channel_creator = None

    async def empty_checker(self, guild: discord.Guild) -> None:
        channel: discord.VoiceChannel
        if len(self.channel_obj) <= 0:  # If channel doesn't have nothing in it
            return

        for channel in self.channel_obj:
            # Iterates through channels created by bot/auto create


            if len(channel.members) == 0:
                print(f"[DELETED] Channel named: {channel.name} was deleted")
                self.channel_obj.remove(channel)
                await guild.get_channel(channel.id).delete()
                await self.bot.get_channel(TESTING_CHANNEL).send(
                    content="Channel deleted, thank god!"
                )

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        guild: discord.Guild = member.guild
        
        await self.empty_checker(guild)

        if not after.channel:  # Check if both are not equal to None | Why does this work now........

            return

        # await self.empty_checker(guild)  # Not sure why this throws an error if this above this statement... 


        if (
            after.channel.name != "[+] Create Channel"
        ):  # Check if user join is in a certain channel TODO:(Will make dynamic)

            return
        if self.bot.is_ws_ratelimited():
            await self.bot.get_channel(1012526325401145374).send(
                content=f"Bot is currently ratelimited"
            )  # Makes sure it's not ratelimited
            return

        channel_name: str = member.display_name  # Get user's name/nick for channel name
        catagory = after.channel.category  # Get's catagory channel creator is in
        overwrites = {member: discord.PermissionOverwrite(priority_speaker=True)}
        position = len(guild.voice_channels)
        channel_emoji = random.choice(EMOJIS)
        channel_name = f"{channel_name}'s Channel {channel_emoji}"

        created_channel: discord.VoiceChannel = await guild.create_voice_channel(
            name=channel_name, position=position, category=catagory, overwrites=overwrites
        )  # Creates channel


        await member.move_to(
            channel=created_channel, reason="Auto Bot Move"
        )  # Moves user
        await self.bot.get_channel(1037278984410517504).send("Successful Interaction")
        self.channel_obj.append(
            created_channel
        )  # Adds to list to keep track of channel objects


async def setup(bot: commands.Bot):
    await bot.add_cog(VCChannelCreator(bot))
