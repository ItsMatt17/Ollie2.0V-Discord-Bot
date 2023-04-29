import random

import discord
from discord import app_commands
from discord.ext import commands

from config import CHLOE_ID, MY_ID, SANDRA_ID, SHADYS_ID

responses = [
    "Please stfu kindly",
    "You're going to make me have a joker moment",
    "Making me end it soon",
    "This is why Hue is better",
    "Just shut up, I beg",
    "Here comes the art major",
]

SANDRA_EMOJIS = ["😡", "🍓", "🍇", "🍉", "🥺", "🤐", '😎']
SHADY_EMOJI = ["💯", "🔥"]

EMOTING_USERS = {
    CHLOE_ID: {"Emoji": "🤓", "State": True},  # State true == on
    SANDRA_ID: {"Emoji": SANDRA_EMOJIS, "State": True},
    SHADYS_ID: {"Emoji": SHADY_EMOJI, "State": True}
}

class EmoteReactor(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == self.bot.user.id or not message.author.id in EMOTING_USERS.keys():
            return

        emoji, state = EMOTING_USERS.get(message.author.id).values()

        if state is False:
            return

        if not isinstance(emoji, list):
            await message.add_reaction(emoji)
            return

        random_emoji = random.choice(emoji)
        await message.add_reaction(random_emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, interaction: discord.RawReactionActionEvent):
        if interaction.user_id != CHLOE_ID:
            return

        emoji, _ = EMOTING_USERS.get(interaction.user_id).values()
        reaction = interaction.emoji

        if reaction == emoji:
            random_response = random.choice(responses)
            await self.bot.get_channel(interaction.channel_id).send(random_response)

    @app_commands.command(name="emote", description="Turns on and off reactions to users")
    async def emote(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.user.id != MY_ID:
            return

        user_id = user.id
        if user_id not in EMOTING_USERS:
            await interaction.response.send_message("User doesn't have any reaction settings")
            return

        _, state = EMOTING_USERS.get(user_id).values()
        EMOTING_USERS[user_id]["State"] = not state

        await interaction.response.send_message(f"Changed <@{user_id}>'s reactions to {not state}")


async def setup(bot: commands.Bot):
    await bot.add_cog(EmoteReactor(bot))
