import datetime
import typing

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks

import config
from bot import OllieV2
from config import NASA_PHOTO

daily_apod_api: datetime = datetime.time(hour=5, minute=30,
                                         second=0)  # 23:00 EDT | 22:00 EST == 11pm & 10pm | Not in class because of decorator conflicts


# daily_apod_api = datetime.time(hour=6, minute=1, second=0)
class NASAPhoto(commands.Cog):
    # TODO get max distance api goes back to
    non_dated_embed_fallback: discord.Embed = discord.Embed(color=discord.Color.red(),
                                                            title="An Error Occurred").add_field(
        name="Invalid Api Request",
        value=f"Trying to grab {config.current_time()}'s image resulted in an error. Try again later!")
    date_embed_fallback: discord.Embed = discord.Embed(color=discord.Color.red(), title="An Error Occurred").add_field(
        name="Request Was Invalid",
        value="Please try again requesting photo with proper date.\nUse a date format such as **YYYY-MM-DD** i.e (1996-12-31)")

    def __init__(self, bot: OllieV2):
        self.bot: OllieV2 = bot
        self.ANNOUNCE_CHANNEL: typing.Final[int] = 1074257478600110141
        self.daily_api_announce.start()

    # -----No Date Given-----
    @staticmethod
    async def _get_undated_nasa_request() -> typing.Union[tuple[str, str, str], None]:
        """
        The _get_undated_photo function returns a tuple of three strings. The first string is the URL to an image,
        the second string is the title of that image, and the third string is a description of that image. If there
        is no photo for today's date, then None will be returned instead.

        :return: A tuple of the url, title and explanation
        :doc-author: Trelent
        """
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_PHOTO}")
            if response.status != 200: return None
            data = await response.json()
        return data['url'], data['title'], data["explanation"]

    async def get_embed_no_date_given(self) -> discord.Embed:
        if not (api_response := await self._get_undated_nasa_request()):
            return NASAPhoto.non_dated_embed_fallback

        photo, title, paragraph = api_response
        if len(paragraph) >= 4096:
            paragraph = paragraph[:4093] + "..."

        return discord.Embed(color=discord.Color.red(), title=title, description=paragraph).set_image(url=photo)

    # -----Date Given-----
    @staticmethod
    async def _get_dated_nasa_request(date: str):
        async with aiohttp.ClientSession() as session:
            response = await session.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_PHOTO}&date={date}")
            if response.status != 200: return None
            data = await response.json()
            print(data['url'], data['title'])
        return data['url'], data['title'], data["explanation"]

    async def get_embed_date_given(self, date: str) -> discord.Embed:
        if (api_response := await self._get_dated_nasa_request(date=date)) is None:
            return NASAPhoto.date_embed_fallback

        photo, title, paragraph = api_response
        if len(paragraph) >= 4096:
            paragraph = paragraph[:4093] + "..."

        return discord.Embed(color=discord.Color.red(), title=title, description=paragraph).set_image(url=photo)

    # -----Daily Task-----
    @tasks.loop(time=daily_apod_api)
    async def daily_api_announce(self):
        announce_channel = await self.bot.fetch_channel(self.ANNOUNCE_CHANNEL)
        embed: discord.Embed = await self.get_embed_no_date_given()
        await announce_channel.send(embed=embed.set_footer(text=f"{config.current_time()}"))

    # -----Command-----
    @app_commands.checks.cooldown(3.0, 15)
    @app_commands.command(name="photo", description="Gives a dated photo")
    async def photo(self, interaction: discord.Interaction, yyyymmdd: str = None) -> None:
        if await self.bot.db.is_blacklisted(interaction.user.id) is True:
            await interaction.response.send_message("You are blacklisted :cry:")
            return

        user = interaction.user

        if yyyymmdd is None:
            embed: discord.Embed = await self.get_embed_no_date_given()
            await interaction.response.send_message(embed=embed.set_footer(icon_url=user.display_avatar.url,
                                                                           text=f"{config.current_time()} | {user.name}:{user.discriminator}"))
            return

        embed: discord.Embed = await self.get_embed_date_given(yyyymmdd)
        await interaction.response.send_message(embed=embed.set_footer(icon_url=user.display_avatar.url,
                                                                       text=f"{config.current_time()} | {user.name}:{user.discriminator}"))


async def setup(bot: OllieV2):
    await bot.add_cog(NASAPhoto(bot))
