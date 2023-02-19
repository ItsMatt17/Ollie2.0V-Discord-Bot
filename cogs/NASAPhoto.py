import typing

import aiohttp
from discord.ext import commands

from config import NASA_PHOTO


class NASAPhoto(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    async def _get_undated_photo() -> typing.Union[tuple[str, str, str], None]:
        """
        The _get_undated_photo function returns a tuple of three strings. The first string is the URL to an image,
        the second string is the title of that image, and the third string is a description of that image. If there
        is no photo for today's date, then None will be returned instead.

        :return: A tuple of the url, title and explanation
        :doc-author: Trelent
        """
        async with aiohttp.ClientSession as session:
            response = await session.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_PHOTO}")
            if response.status != 200: return None
            data = await response.json()

        return data['url'], data['title'], data["explanation"]


async def setup(bot: commands.Bot):
    await bot.add_cog(NASAPhoto(bot))
