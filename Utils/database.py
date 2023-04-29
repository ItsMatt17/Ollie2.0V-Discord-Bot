import asyncpg as pg
import discord
from discord.ext import commands


class Database:
    def __init__(self, db_pool: pg.Pool, bot: commands.Bot):
        self._db_pool: pg.Pool = db_pool
        self._bot: commands.Bot = bot

    async def create_new_user(self, discord_id: int, guild_id: int):
        try:
            if self._bot.get_user(discord_id).bot:
                return

            query = "insert into public.Users (discord_id, guild_id) values ($1, $2)"
            response = await self._db_pool.execute(query, discord_id, guild_id)
        except pg.UniqueViolationError:
            return

    async def is_blacklisted(self, user_id: int) -> bool | int:
        try:
            response = await self._db_pool.fetch("select bot_blacklisted from public.users where discord_id = $1 ",
                                                 user_id)
            return response[0][0]
        except pg.NoData:
            return -1

    async def is_blacklisted_check(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        response = await self._db_pool.fetch("select bot_blacklisted from public.users where discord_id = $1 ",
                                             user_id)
        return not response[0][0]  # Return opposite because checks want True for if they can run the command

    async def fetch(self, query, args=()):

        print(args == (), args)
        try:
            if args == ():
                return await self._db_pool.fetch(query)
            return await self._db_pool.fetch(query, args)
        except pg.NoData as e:
            return -1

    async def execute(self, query, *args):
        print(args)
        try:
            if len(args) == 0:
                return await self._db_pool.execute(query)

            return await  self._db_pool.execute(query, *args)
        except pg.NoData as e:
            return -1

    async def get_total_song_offenses(self) -> int:
        """Returns number of offenses within song_counter.json, but does not add 1

        :param: `None`

        :return: `int` of number of times a generaic song has been captured
        """
        response = await self._db_pool.fetch("select count from public.song_counter where id = 0")
        return response[0][0]

    async def is_double_exp(self, user_id: int) -> bool:
        response = await self._db_pool.fetch("select double_xp from public.users where discord_id = $1", user_id)
        return response[0][0]

    async def get_user_level(self, user_id: int) -> int:
        response = await self._db_pool.fetch("select user_level from public.users where discord_id = $1", user_id)
        print(response)
        return response[0][0]
