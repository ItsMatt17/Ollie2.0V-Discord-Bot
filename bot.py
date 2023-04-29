""""     -----------------------
        +     @ItsMatt17        +
        +   Ollie-Discord-Bot   +
        +                       +
         -----------------------

"""

import Utils.database

"""
TODO Fixes:
    Migrate cogs to proper folders ✓
    Leaderboard command ✓
    Lock Hide command
    Fix Untalking Stick message
    Tracker embed imagine fix 
    Voice fix idk 
    Leveling embed photo
    Migrate to proper database
    Use proper data structure like stack.py to track duplicate songs.
"""

import os
import platform
import logging
import logging.handlers

import asyncio
import discord
from discord.ext import commands
from pathlib import Path
import asyncpg as pg

import config
from config import AUTH_KEY


class OllieV2(commands.Bot):
    OllieInstance: commands.Bot | None = None

    def __init__(self, db_pool: pg.Pool, command_prefix, logger: logging.Logger, **options):
        super().__init__(command_prefix=command_prefix, **options)
        OllieV2.OllieInstance = self
        self.owner_id: int = config.MY_ID
        self.db_pool = db_pool
        self.db = Utils.database.Database(self.db_pool, self)
        self.log: logging.Logger = logger

    @staticmethod
    def get_bot() -> commands.Bot:
        return OllieV2.OllieInstance

    # async def close(self) -> None:
    #     print("disconnecting")

    async def on_ready(self) -> None:
        """
        Start up messages for when clients is ready
        :return `None`

        """
        print("ready")
        self.log.info("-------------------")
        self.log.info(f"Logged in as {self.user.name}")
        self.log.info(f"Discord.py API version: {discord.__version__}")
        self.log.info(f"Python version: {platform.python_version()}")
        self.log.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.log.info("Go for launch!")
        self.log.info("-------------------")

    async def setup_hook(self) -> None:
        """
        Loads all cogs during setup hook
        :return: `None`

        """
        path = Path("cogs")
        for file in list(path.rglob("*.py*")):
            if file.suffix == ".pyc":  # Pycache being annoying
                continue

            file_str: str = file.__str__()
            file_str = file_str.replace("\\", ".")
            file_str = file_str.removesuffix(".py")
            self.log.info(
                f"[COG] Loaded bot extension {file_str.replace('.', '/')}.py"
            )
            await self.load_extension(file_str)


async def main():
    log = logging.getLogger("discord")
    logging.basicConfig(level=logging.INFO)

    async with pg.create_pool(database="discord", user="postgres", password=config.DATA_BASE_PASS) as db:
        async with OllieV2(command_prefix="!", db_pool=db, intents=discord.Intents.all(), logger=log) as bot:
            await bot.start(AUTH_KEY)

        database: pg.Pool = db


if __name__ == "__main__":
    asyncio.run(main())
