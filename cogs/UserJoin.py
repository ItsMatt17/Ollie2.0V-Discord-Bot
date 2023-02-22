import discord
from discord.ext import commands

from config import GUILD, GuildInfo


class UserJoin(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        user_guild = member.guild
        if user_guild != GUILD:  # Foster Home
            return

        role = user_guild.get_role(GuildInfo.DEFAULT_ROLE)
        await member.add_roles(role)


async def setup(bot: commands.Bot):
    await bot.add_cog(UserJoin(bot))
