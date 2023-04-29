import asyncpg
import discord
from discord import PublicUserFlags
from discord.ext import commands
from discord.ext.commands import command

import config
from bot import OllieV2


class AdminCMDS(commands.Cog):
    def __init__(self, bot: OllieV2):
        self.bot: OllieV2 = bot

    @command(
        name="sync",
        description="Sync tree commands ",
        guild=discord.Object(id=982514587742142545),
    )
    async def sync(self, interaction: discord.Interaction) -> None:
        """
        The sync function is used to sync the commands from the bot's tree to a database.
        It will return a list of all synced commands.

        :param interaction:discord.Interaction: Get information about the interaction, such as the message
        :return: None
        :doc-author: Trelent
        """

        if interaction.user.id == 188779992585469952:  # My ID
            synced = await self.bot.tree.sync()
            await interaction.response.send_message(f"Synced {len(synced)} synced commands")
            self.bot.log.info(f"Synced {len(synced)} synced commands")

        else:
            await interaction.response.send_message(
                content="You must be the owner to use this command!"
            )

    async def get_user_badges(self, user: int) -> PublicUserFlags | None:
        if isinstance(user, int) or isinstance(user, str):
            try:
                user = int(user)
                user = await self.bot.fetch_user(user)
            except discord.NotFound or discord.HTTPException as e:
                return
            user_flags: list = [flag[0] for flag in user.public_flags if flag[1]]
            if user.avatar and user.avatar.is_animated():
                user_flags.append("discord_nitro")
            return user_flags  # Return all flags user has

    @command("flag")
    async def flags(self, ctx: commands.Context) -> None:
        print(await self.get_user_badges(ctx.author.id)) \
 \
        @ command(
            name="add_user",
            description="",
            guild=discord.Object(id=982514587742142545),
        )

    @commands.is_owner()
    async def add_user(self, ctx: commands.Context, user: discord.Member | discord.User):
        if ctx.author.id != config.MY_ID:
            return
        if user is None and not isinstance(user, discord.Member) or not isinstance(user, discord.User):
            return

        try:
            await self.bot.db.create_new_user(user.id, ctx.guild.id)
        except asyncpg.UniqueViolationError as e:
            return

    @command(
        name="add_all_users",
        description="",
        guild=discord.Object(id=982514587742142545),
    )
    @commands.is_owner()
    async def add_all_users(self, ctx: commands.Context):
        member: discord.Member
        await ctx.send("Adding users...")
        async for member in ctx.guild.fetch_members(limit=100):
            await self.bot.db.create_new_user(member.id, ctx.guild.id)

    @command(
        name="blacklist",
        description="",
        guild=discord.Object(id=982514587742142545),
    )
    @commands.is_owner()
    async def blacklist(self, ctx: commands.Context, user: discord.Member):
        print(type(user))
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Incorrect params")
            return

        try:
            await self.bot.db.execute(
                "update public.users set bot_blacklisted = not bot_blacklisted where discord_id = $1",
                user.id)  # Set within list need to do double indexing
            await ctx.send(f"Still in progress...")
        except asyncpg.NoData:
            await ctx.send("User does not exist")


async def setup(bot: OllieV2):
    await bot.add_cog(AdminCMDS(bot))
