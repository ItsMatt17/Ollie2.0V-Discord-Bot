import json
from typing import Tuple, Union

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from config import ISSLocatorInfo, MY_ID, current_time


class ISSLocator(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.embeds = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self._check_data()

    def _check_data(self) -> None:
        with open(ISSLocatorInfo.ISSEmbedPath, "r+") as file:
            self.embeds = json.load(file)

    @staticmethod
    async def _get_location() -> Union[Tuple[str, str], None]:
        async with aiohttp.ClientSession() as session:
            data = await session.get(url=ISSLocatorInfo.COORD_API)
            if data.status != 200:
                print(f"[Request Error] {data.status}")
                return
            json_info = await data.json()
            lat_pos = json_info["iss_position"]["latitude"]
            long_pos = json_info["iss_position"]["longitude"]
            return lat_pos, long_pos

    async def _tracker_embed(self) -> discord.Embed:
        x_coord, y_coord = await self._get_location()
        embed = discord.Embed(title="ISS Tracker", color=discord.Color.blue(),
                              description=f"Currently orbiting over {x_coord}, {y_coord}") \
            .set_image(
            url=f"https://maps.googleapis.com/maps/api/staticmap?center={x_coord},{y_coord}&style=visibility:on&zoom=1&maptype=hybrid&markers=size:tiny%7Cicon:https://i.imgur.com/pV2X2DJ.png%7C{x_coord},{y_coord}&size=600x400&sensor=false&key={ISSLocatorInfo.GOOGLE_MAPS}"
            )

        return embed

    @staticmethod
    async def _create_tracker_file(channel_id: int, guild_id: str, message_id: int) -> None:
        print(channel_id, guild_id, message_id)
        with open(ISSLocatorInfo.ISSEmbedPath, "r+") as file:
            data = json.load(file)
            data['embeds'][str(guild_id)] = {"channel": channel_id, "message": message_id}

            file.seek(0)
            json.dump(data, file)
            file.truncate()

    @app_commands.command(name="tracker", description="Create a tracker embed for ISS location")
    async def tracker(self, interaction: discord.Interaction):
        self._check_data()

        if str(interaction.guild_id) in self.embeds["embeds"]:
            guild_info = self.embeds["embeds"][f"{interaction.guild_id}"]
            embed_channel = int(guild_info["channel"])
            embed_message = int(guild_info["message"])

            message = await self.bot.get_channel(embed_channel).fetch_message(embed_message)
            print(message.type)
            if message is None or message.type != discord.MessageType.default or message.author.id != self.bot.user.id:
                print('here')
                response_embed = await interaction.response.send_message(embed=self._tracker_embed())
                await self._create_tracker_file(channel_id=interaction.channel_id, guild_id=str(interaction.guild_id),
                                                message_id=response_embed.id)
                await interaction.response.send_message("ok", delete_after=0.01)
                return

            # TODO Make it so interaction doesn't time out
            await message.reply(f"{interaction.user.mention}, this is already your tracker...")
            await interaction.response.send_message("ok", delete_after=0.01)
            return

        message = await self.bot.get_channel(interaction.channel_id).send(embed=await self._tracker_embed())
        await self._create_tracker_file(channel_id=interaction.channel_id, guild_id=str(interaction.guild_id),
                                        message_id=message.id)

    @app_commands.command(name="update", description="Update tracker")
    @commands.is_owner()
    async def update(self, interaction: discord.Interaction):
        if interaction.user.id != MY_ID:
            return

        self._check_data()
        embed_info = self.embeds["embeds"].get(f"{interaction.guild_id}")
        if not embed_info:
            await interaction.response.send_message("You don't have a tracker embed...")
            return

        time = current_time()

        channel_id = embed_info["channel"]
        message_id = embed_info["message"]
        guild = interaction.guild
        channel: discord.TextChannel = await guild.fetch_channel(channel_id)
        message: discord.Message = await channel.fetch_message(message_id)
        if not channel or not message or message.author.id != self.bot.user.id:
            await interaction.response.send_message(
                "You are either missing your tracker channel or message... Try to create a new one!")
            return

        embed: discord.Embed = await self._tracker_embed()
        embed.set_footer(icon_url=interaction.user.avatar.url, text=f"{interaction.user.name} | {time}")
        await message.edit(embed=embed)
        await interaction.response.send_message("ok", delete_after=0.01)

    @tracker.error
    async def tracker_error(self, interaction: discord.Interaction, error):
        self._check_data()
        if isinstance(error.__cause__, discord.errors.NotFound):
            message = await self.bot.get_channel(interaction.channel_id).send(embed=await self._tracker_embed())
            await self._create_tracker_file(channel_id=interaction.channel_id, guild_id=str(interaction.guild_id),
                                            message_id=message.id)
        else:
            print(error)


async def setup(bot):
    await bot.add_cog(ISSLocator(bot))
