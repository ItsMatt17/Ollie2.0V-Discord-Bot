import random
from datetime import datetime

import discord
from discord.ext import commands
import json

from request.spotify import popularity_rating

CHLOE_ID = 396098786520334338
MY_ID = 188779992585469952
responses = [
    "Please stfu kindly",
    "You're going to make me have a joker moment",
    "Making me end it soon",
    "This is why Hue is better",
    "Just shut up, I beg",
    "Here comes the art major",
]

POPULARITY_PHOTOS = {

}


class SongHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel_id = 1012526325401145374

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, interaction: discord.RawReactionActionEvent):

        reaction = interaction.emoji
        if interaction.user_id == CHLOE_ID and reaction.name == "🤓":
            self.channel_id = interaction.channel_id
            random_response = random.choice(responses)

            await self.bot.get_channel(self.channel_id).send(
                content=f"{random_response} <@{CHLOE_ID}> ")

    @staticmethod
    def error_embed() -> discord.Embed:
        embed = discord.Embed(color=discord.Color.red(), title="An Error Occurred"
                              ).add_field(name="Error", value="Something went wrong")
        return embed

    @staticmethod
    def _get_offenses() -> int:
        """Returns number of offenses within song_counter.json, but does not add 1

        :param: `None`

        :return: `int` of number of times a generaic song has been captured
        """

        with open("storage/song_counter.json", "r+") as file:
            data = json.load(file)

        return data["basic_songs"]

    @staticmethod
    def _get_update_offenses() -> int:
        """
        Returns number of genaric song offenses & adds 1 to the JSON file.

        :return: Numbe of genaric songs
        :rtype: `int`
        """

        with open("storage/song_counter.json", "r+") as file:
            data = json.load(file)
            data["basic_songs"] += 1

            file.seek(0)
            json.dump(data, file)
            file.truncate()
        return data["basic_songs"]

    @staticmethod
    def _song_tracker_embed(user: int, title: str) -> discord.Embed:
        """Initializes discord embed to be sent in a channel

         :param: `discord.Embed` embed to be sent
         """
        photo_embed = (
            discord.Embed(title=f"{title}", color=discord.Color.red())
            .add_field(name="User", value=f"<@{user}>", inline=False)
        )
        return photo_embed

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        # TODO make it so the bot doesn't log stop and starts of songs
        # TODO Make a a way to save data on who makes the bot activiate the most amount of times
        """Checks if a user is listening to a song, and if it is a basic song, it will send a message to the channel."""

        if not after.activities or not isinstance(after.activity,
                                                  discord.activity.Spotify):  # Confirm they didn't remove their activity
            print(
                f"Activity Spotify Not Found: | Type: | User: {after.name} | after_activity: {type(after.activity)} | Returned")

            return

        song_activity = None
        for activity in after.activities:  # Sort through list of numerous activities i.e game, streaming, listening
            print(activity, type(activity))

            if isinstance(activity, discord.activity.Spotify):
                print(
                    f"Activity Chosen: {activity} | Type:{type(activity)} | User: {after.name} | after_activity: {type(after.activity)}")
                song_activity = activity
                break

        if not song_activity:  # If there's not a song in their activity, return | Might not need?
            print("[No Song Activity] No song activity found")
            return

        message_history = self.bot.get_channel(1071272760099209237).history(limit=5)
        async for message in message_history:  # Intended to prevent duplicate/spam messages. Checks what last message was, if it was the same as current, song then return.
            embeds: list[discord.Embed] = message.embeds
            embed: discord.Embed
            for embed in embeds:
                embed_dict: dict = embed.to_dict()
                # print(embed_dict)
                user_id: str = embed_dict["fields"][0]["value"].strip("<@>")
                song_name: str = embed_dict["fields"][1]["value"].replace("*", "")
                index: int = song_name.index("by")
                song_name = song_name[:index - 1]
                print(
                    f"user_id: {int(user_id)} | after_id: {after.id} | after_activity: {after.activity.title} | song_name: {song_name}")
                if int(user_id) == after.id and after.activity.title == song_name:
                    print("[Duplicate] Song found duplicated")
                    return

        song_id = song_activity.track_id
        popularity = await popularity_rating(song_id)
        print(type(song_activity))
        song_name = song_activity.title
        album_photo = song_activity.album_cover_url
        embed_title = "Music Tracker"
        offenses = None
        now = datetime.now()
        ftime = now.strftime("%H:%M")

        if not popularity:
            await self.bot.get_channel(1071272760099209237).send(embed=self.error_embed())
            return

        if int(popularity) >= 75:
            offenses = self._get_update_offenses()

            embed_title = "Basic Music Tracker"

        else:
            offenses = self._get_offenses()

        artist_len = len(song_activity.artists)
        if artist_len >= 3:
            artist = ", ".join(song_activity.artists)
        elif artist_len == 2:
            artist = " & ".join(song_activity.artists)
        else:
            artist = "".join(song_activity.artists)

        await self.bot.get_channel(1071272760099209237).send(
            embed=self._song_tracker_embed(
                user=after.id, title=embed_title)
            .add_field(name="Song", value=f"{song_name} by **{artist}**", inline=False)
            .set_thumbnail(url=f"{album_photo}")
            .set_footer(text=f"{after.name} | Global Occurrence Number: {offenses} | {ftime}",
                        icon_url=after.avatar.url)
            .add_field(name="Popularity", value=f"{popularity}")
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(SongHandler(bot))
