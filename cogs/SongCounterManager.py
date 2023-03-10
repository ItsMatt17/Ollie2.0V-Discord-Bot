import json
from operator import itemgetter

import discord
from discord import app_commands
from discord.app_commands import CommandOnCooldown
from discord.ext import commands

from config import MusicTracker, current_time


class SongCounterManager(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @staticmethod
    def _leaderboard_embed() -> discord.Embed:
        embed = discord.Embed(
            colour=discord.Color.green(),
            title="Popular Song Counter"
        )
        return embed

    @app_commands.checks.cooldown(3, 10)
    @app_commands.command(name="leaderboard", description="Gets song popularity leaderboard")
    async def leaderboard(self, interaction: discord.Interaction) -> None:
        with open(MusicTracker.SONG_COUNTER_PATH, "r") as file:
            data = json.load(file)
            res = dict(sorted(data["User"].items(), key=itemgetter(1), reverse=True)[:3])  # Fetch top 3 users
            top_ids = []
            top_count = []  # Most def a better way of doing this idk how yet

            for key, value in res.items():
                top_ids.append(key)
                top_count.append(value)

            top_user: discord.Member = await interaction.guild.fetch_member(int(top_ids[0]))
            avatar = top_user.avatar.url

            # Time
            time = current_time()

        await interaction.response.send_message(embed=self._leaderboard_embed()
                                                .add_field(name='Top users',
                                                           value=f"1.<@{top_ids[0]}> : {top_count[0]}\n2.<@{top_ids[1]}> : {top_count[1]}\n3.<@{top_ids[2]}> : {top_count[2]}")
                                                .set_thumbnail(url=avatar)
                                                .set_footer(icon_url=interaction.user.avatar.url,
                                                            text=f"{interaction.user.name} | {time} EST"))

    @leaderboard.error
    async def leaderboard_error(self, interaction: discord.Interaction, error):
        if isinstance(error, CommandOnCooldown):
            await interaction.response.send_message(
                f"You're on cooldown for {error.retry_after:.2f}s", ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(SongCounterManager(bot))
