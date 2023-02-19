import json

import discord
from discord import app_commands
from discord.ext import commands

from config import MY_ID, MusicTracker, current_time
from request.spotify import popularity_rating


class SongHandler(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.disabled = False

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
        with open(MusicTracker.SONG_COUNTER_PATH, "r+") as file:
            data = json.load(file)

        return data["basic_songs"]

    @staticmethod
    def _get_update_offenses(user_id: int) -> int:
        """
        Returns number of genaric song offenses & adds 1 to the JSON file.

        :return: Numbe of genaric songs
        :rtype: `int`
        """
        with open(MusicTracker.SONG_COUNTER_PATH, "r+") as file:
            data = json.load(file)

            data["basic_songs"] += 1
            if str(user_id) not in data["User"]:
                data["User"][f"{user_id}"] = 1  # Track user song popularity
                print("[Not Found] Adding user to JSON file")
            else:
                data["User"][f"{user_id}"] += 1
                print("[Found User] Found user add one to their counter")

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

    @app_commands.command(name="pause", description="pause counter for songs")
    @commands.is_owner()
    async def pause(self, interaction: discord.Interaction):
        if not self.disabled:
            self.disabled = True
            print("Song tracking disabled")
            await interaction.response.send_message("Sound tracking disabled")
            return

        self.disabled = False
        print("Song tracking enabled")
        await interaction.response.send_message("Sound tracking enabled")

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        """Checks if a user is listening to a song, and if it is a basic song, it will send a message to the channel."""

        if not after.activities or self.disabled:
            return

        song_activity = discord.utils.get(after.activities, type=discord.ActivityType.listening)

        if not song_activity:
            return

        message_history = self.bot.get_channel(MusicTracker.MUSIC_CHANNEL).history(limit=5)
        async for message in message_history:  # Intended to prevent duplicate/spam messages. Checks what last message was, if it was the same as current, song then return.
            embeds: list[discord.Embed] = message.embeds
            embed: discord.Embed
            for embed in embeds:
                embed_dict: dict = embed.to_dict()

                try:
                    user_id: str = embed_dict["fields"][0]["value"].strip("<@>")
                    song_name: str = embed_dict["fields"][1]["value"].replace("*", "")
                    index: int = song_name.index("by")
                    song_name = song_name[:index - 1]
                except IndexError as e:
                    continue

                # print(
                #    f"[EMBED LOOP] user_id: {int(user_id)} | after_id: {after.id} | after_activity: {song_activity.title} | song_name: {song_name} ||| {int(user_id) == after.id} {song_activity.title == song_name}")
                if int(user_id) == after.id and song_activity.title == song_name:
                    return

        song_id: int = song_activity.track_id
        popularity = await popularity_rating(song_id)
        song_name = song_activity.title
        album_photo = song_activity.album_cover_url
        embed_title = "Music Tracker"
        offenses = None

        if popularity is None:
            me = await self.bot.fetch_user(MY_ID)
            me.send("Popularity issue...")
            return

        if int(popularity) >= 75:
            offenses = self._get_update_offenses(after.id)  # User's ID
            embed_title = "Basic Music Tracker"

        else:
            offenses = self._get_offenses()

        time: str = current_time()

        artist_len = len(song_activity.artists)
        # Dealing with suffixes to make it somewhat nice. There's probably a better way to do this.
        if artist_len >= 3:
            artist = ", ".join(song_activity.artists)
        elif artist_len == 2:
            artist = " & ".join(song_activity.artists)
        else:
            artist = "".join(song_activity.artists)

        await self.bot.get_channel(MusicTracker.MUSIC_CHANNEL).send(
            embed=self._song_tracker_embed(
                user=after.id, title=embed_title)
            .add_field(name="Song", value=f"{song_name} by **{artist}**", inline=False)
            .set_thumbnail(url=f"{album_photo}")
            .set_footer(text=f"{after.name} | Basic Song Counter: {offenses} | {time} EST",
                        icon_url=after.avatar.url)
            .add_field(name="Popularity", value=f"{popularity}")
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(SongHandler(bot))
