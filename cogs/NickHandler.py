import random
import logging

import discord
from discord.ext import commands
from discord import app_commands

MY_ID = 188779992585469952

DAVID_GOGGINS = [
    "https://www.youtube.com/watch?v=Y7F2RirF9Zc",
    "https://www.youtube.com/watch?v=75TUcoMsYHY",
    "https://www.youtube.com/watch?v=dshOfFnDYY0",
    "https://www.youtube.com/watch?v=6ikwfkLb68I",
    "https://www.youtube.com/watch?v=qspyXo3z0_8",
]


class NickHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def user_dm(self, user: discord.Member):
        await user.edit(nick="DAVID GOGGINS")
        dm = await user.create_dm()
        await dm.send(
            content=f"You are david goggins, and nothing but him, embrace it!\n{random.choice(DAVID_GOGGINS)}"
        )


    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if not before.nick or before.nick.lower() != "david goggins": #If no user nickname or nickname was never 'David Goggins' :return:
            return

        if after.nick and after.nick.lower() == "david goggins": # If the user has a nickname and it equals 'David Goggins' :return:
            return

        
        logging.warning("david goggins detected") 
        await self.user_dm(after)

    @app_commands.command(name="nick", description="Does a funny little hahaha")
    async def nick(self, interaction: discord.Interaction, nick_user: discord.Member):
        if interaction.user.id != MY_ID: #User is not me, don't do anything
            await interaction.response.send_message("No you can't do this...")
            return

        await nick_user.edit(nick="DAVID GOGGINS")
        await self.user_dm(nick_user)
        await interaction.response.send_message(
            content="https://media.tenor.com/e725ChiJpTMAAAAd/nerd-cube.gif"
        )

            
    @nick.error
    async def nick_error(self, interaction : discord.Interaction, error):
        if isinstance(error.__cause__, discord.errors.Forbidden):
            await interaction.response.send_message("Can't change this user's name :weary:")

async def setup(bot: commands.Bot):
    await bot.add_cog(NickHandler(bot))
