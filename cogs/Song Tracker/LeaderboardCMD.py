import discord
from discord import app_commands
from discord.app_commands import CommandOnCooldown
from discord.ext import commands

from Utils.user_utils import UserUtils
from bot import OllieV2
from config import current_time


class SongCounterManager(commands.Cog):
    def __init__(self, bot: OllieV2):
        self.bot: OllieV2 = bot

    @staticmethod
    def _leaderboard_embed() -> discord.Embed:
        embed = discord.Embed(
            colour=discord.Color.green(),
            title="Popular Song Counter"
        )
        return embed

    async def get_top_users(self, limit: int = 10) -> dict:
        response = await self.bot.db.fetch(
            "select discord_id, song_tracker from public.users order by song_tracker desc limit $1", limit)
        users = {}
        for user in response:
            users[user[0]] = user[1]
        return users

    @staticmethod
    async def _get_embed_avatar(interaction: discord.Interaction, top_ids: int):
        try:
            top_user: discord.Member = await interaction.guild.fetch_member(top_ids)
            return top_user.avatar.url
        except discord.NotFound as e:
            return interaction.user.default_avatar

    async def _get_user_average(self) -> int:
        response = await self.bot.db.fetch("select avg(song_tracker)::numeric(10, 2) from public.users")
        return response[0][0]

    @staticmethod
    def string_build(top_users: dict) -> str:
        message = ""
        for i, (user, value) in enumerate(top_users.items()):
            message += f"**{i + 1}**. <@{user}>: {value} \n"
        return message

    @app_commands.checks.cooldown(3, 10)
    @app_commands.command(name="leaderboard", description="Gets song popularity leaderboard")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        response = await self.get_top_users()
        avatar = await UserUtils.get_user_avatar(await self.bot.fetch_user(list(response.keys())[0]))
        average = await self._get_user_average()
        total_count = await self.bot.db.get_total_song_offenses()
        # Time
        time = current_time()
        await interaction.response.send_message(embed=self._leaderboard_embed()
                                                .add_field(name='Top users',
                                                           value=self.string_build(response))
                                                .set_thumbnail(url=avatar)
                                                .set_footer(icon_url=interaction.user.avatar.url,
                                                            text=f"{interaction.user.name} | {time} EST")
                                                .add_field(name="Other Data",
                                                           value=f" -> **User Average**: {average}\n-> **Total Count**: {total_count} "))
        # TODO Graph of increment for song counter

    @leaderboard.error
    async def leaderboard_error(self, interaction: discord.Interaction, error):
        print(error, type(error), error.__cause__)

        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"You're on cooldown for {error.retry_after:.2f}s", ephemeral=True
            )


async def setup(bot: OllieV2):
    await bot.add_cog(SongCounterManager(bot))
