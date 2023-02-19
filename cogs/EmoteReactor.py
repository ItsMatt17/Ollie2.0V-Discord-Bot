import random
import typing

import discord
from discord import app_commands
from discord.ext import commands

from config import CHLOE_ID, MY_ID, SANDRA_ID

responses = [
    "Please stfu kindly",
    "You're going to make me have a joker moment",
    "Making me end it soon",
    "This is why Hue is better",
    "Just shut up, I beg",
    "Here comes the art major",
]

EMOJIS = ["😡", "🍓", "🍇", "🍉", "🥺", "🤐", '😎']


class EmoteReactor(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.channel_id = None
        self.chloe_reactor = True
        self.sandra_reactor = True

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id:
            return
        if message.author.id == SANDRA_ID and self.sandra_reactor is True:
            emoji = random.choice(EMOJIS)
            await message.add_reaction(emoji)

        if message.author.id == CHLOE_ID and self.chloe_reactor is True:
            emoji = "🤓"
            await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, interaction: discord.RawReactionActionEvent):

        reaction = interaction.emoji
        if interaction.user_id == CHLOE_ID and reaction.name == "🤓" and self.chloe_reactor:
            self.channel_id = interaction.channel_id
            random_response = random.choice(responses)

            await self.bot.get_channel(self.channel_id).send(
                content=f"{random_response} <@{CHLOE_ID}> ")

    @app_commands.command(name="emote", description="Turns on and off reactions to users")
    async def emote(self, interaction: discord.Interaction, user: typing.Literal["chloe", "sandra"]):
        if interaction.user.id != MY_ID:
            return

        if user == "chloe":
            if self.chloe_reactor is False:
                self.chloe_reactor = True
                await interaction.response.send_message("Chloe auto reaction is now true")
                return

            self.chloe_reactor = False
            await interaction.response.send_message("Chloe auto reaction is now false")
            return

        if user == "sandra":
            if not self.sandra_reactor:
                self.sandra_reactor = True
                await interaction.response.send_message("Sandra's auto reaction is now true")
                return

            self.sandra_reactor = False
            await interaction.response.send_message("Sandra's auto reaction is now false")
            return


async def setup(bot: commands.Bot):
    await bot.add_cog(EmoteReactor(bot))
