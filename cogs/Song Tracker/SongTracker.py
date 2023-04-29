import discord
from discord import app_commands
from discord.ext import commands

from Utils.stack import Stack
from Utils.user_utils import UserUtils
from bot import OllieV2
from config import MusicTracker, current_time
from request.spotify import get_popularity_rating

SUFFIXES = {
    "1": "",
    "2": " & ",
    "3": ", "
}


class SongTracker(commands.Cog):
    def __init__(self, bot: OllieV2):
        self.bot = bot
        self.disabled = False
        self.stack = Stack(5)

    @commands.is_owner()
    @app_commands.command(name="pause", description="pause counter for songs")  # TODO: Refactor to alternative class
    async def pause(self, interaction: discord.Interaction):
        self.disabled = not self.disabled
        await interaction.response.send_message(f"Sound tracking is set to {not self.disabled}")
        return

    @staticmethod
    def error_embed() -> discord.Embed:
        embed = discord.Embed(color=discord.Color.red(), title="An Error Occurred"
                              ).add_field(name="Error", value="Something went wrong")
        return embed

    async def _update_total_song_data(self) -> None:
        await self.bot.db.execute("update public.song_counter set count = count + 1 where id = $1", 0)

    async def _add_popularity_counter(self, user_id: int) -> int:
        """
        Returns number of genaric song offenses & adds 1 to the JSON file.

        :return: Numbe of genaric songs
        :rtype: `int`
        """
        response = await self.bot.db.execute(
            "update public.users set song_tracker = song_tracker + 1 where discord_id = $1", user_id)
        if response == -1:
            raise pg.NoData()

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

    @staticmethod
    def embed_title(populatiry: int):
        if populatiry <= 75:
            return "Music Tracker"
        return "Basic Music Tracker"

    def _is_duplicate(self, user_id, song_name):
        song_data = (user_id, song_name)
        for items in self.stack.items:
            if song_data != items:
                continue
            return True
        return False

    @staticmethod
    def _artist_string_formatting(num_of_artists: int, artists: list) -> str:
        if not str(num_of_artists) in SUFFIXES:
            return ", ".join(artists)

        suffix: str = SUFFIXES.get(str(num_of_artists))
        return suffix.join(artists)

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        """Checks if a user is listening to a song, and if it is a basic song, it will send a message to the channel."""
        current_user: discord.Member = after
        if not current_user.activities or self.disabled:
            return

        song_activity = discord.utils.get(current_user.activities, type=discord.ActivityType.listening)

        if not song_activity:
            return

        if after.is_on_mobile() is True or after.web_status.value != "offline" and after.desktop_status.value != "offline":  # To prevent duplicates | on multiple clients can cause duplicate responses
            return

        print(after.is_on_mobile(), after.web_status.value, after.desktop_status.value)

        user_id: int = current_user.id
        song_id: int = song_activity.track_id

        if (m := self._is_duplicate(user_id, song_id)):  # Jumps from here to top of func
            return

        # -----Embed Vars-----
        popularity = await get_popularity_rating(song_id)
        song_name = song_activity.title
        album_photo = song_activity.album_cover_url
        embed_title = self.embed_title(popularity)
        offenses = await self.bot.db.get_total_song_offenses()
        time: str = current_time()
        artists = self._artist_string_formatting(len(song_activity.artists), song_activity.artists)
        avatar = await UserUtils.get_user_avatar(after)

        # -----Update Data-----
        if popularity >= 75:
            await self._add_popularity_counter(user_id)
            await self._update_total_song_data()

        await self.bot.get_channel(MusicTracker.MUSIC_CHANNEL).send(
            embed=self._song_tracker_embed(
                user=current_user.id, title=embed_title)
            .add_field(name="Song", value=f"{song_name} by **{artists}**", inline=False)
            .set_thumbnail(url=f"{album_photo}")
            .set_footer(text=f"{current_user.name} | Basic Song Counter: {offenses} | {time} EST",
                        icon_url=avatar)
            .add_field(name="Popularity", value=f"{popularity}")
        )

        self.stack.push((user_id, song_id))  # Keep track of duplicates


async def setup(bot: OllieV2):
    await bot.add_cog(SongTracker(bot))
