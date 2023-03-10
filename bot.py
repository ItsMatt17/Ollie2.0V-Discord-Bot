""""     -----------------------
        +     @ItsMatt17        +
        +   Ollie-Discord-Bot   +
        +                       +
         -----------------------

"""
import os
import platform

import discord
from discord.ext import commands

import config


class OllieV2(commands.Bot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)

    async def on_ready(self) -> None:
        """
        Start up messages for when clients is ready
        :return `None`

        """
        print("-------------------")
        print(f"Logged in as {self.user.name}")
        print(f"Discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("Go for launch!")
        print("-------------------")

    async def setup_hook(self) -> None:
        """
        Loads all cogs during setup hook
        :return: `None`

        """

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                print(
                    f"[COG] Loaded bot extension", f"/{filename.replace('.', '/')}.py"
                )
                await bot.load_extension(f"cogs.{filename[:-3]}")


bot: commands.Bot = OllieV2(command_prefix="!", intents=discord.Intents.all())


@bot.tree.command(
    name="sync",
    description="Sync tree commands ",
    guild=discord.Object(id=982514587742142545),
)
async def sync(interaction: discord.Interaction) -> None:
    """
    The sync function is used to sync the commands from the bot's tree to a database.
    It will return a list of all synced commands.

    :param interaction:discord.Interaction: Get information about the interaction, such as the message
    :return: None
    :doc-author: Trelent
    """

    if interaction.user.id == 188779992585469952:  # My ID
        synced = await bot.tree.sync()
        await interaction.response.send_message(f"Synced {len(synced)} synced commands")
        print(f"Synced {len(synced)} synced commands")

    else:
        await interaction.response.send_message(
            content="You must be the owner to use this command!"
        )


if __name__ == "__main__":
    bot.run(config.AUTH_KEY)
