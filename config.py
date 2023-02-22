import os
import typing
from datetime import datetime

import pytz
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
SPOTIFY_CLIENT_ID: str = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_API: str = os.environ.get("SPOTIFY_API")
AUTH_KEY: str = os.environ.get("DISCORD_KEY")
NASA_PHOTO: str = os.environ.get("NASA_PHOTO")
GUILD: int = 982514587742142545
TESTING_CHANNEL: int = 1037278984410517504
MY_ID: int = 188779992585469952
CHLOE_ID: typing.Final[int] = 396098786520334338
SANDRA_ID: typing.Final[int] = 620357491355549715


class GuildInfo:
    DEFAULT_ROLE: int = 982531286616899634  # The Unwanted Role


class VoiceFunny:
    assets = "assets"
    executable = "./ffmpeg.exe"


class ISSLocatorInfo:
    GOOGLE_MAPS: str = os.environ.get("GOOGLE_MAPS")
    ISSEmbedPath: str = "storage/ISSEmbedData.json"
    COORD_API: str = "http://api.open-notify.org/iss-now.json"


class MusicTracker:
    SONG_COUNTER_PATH: typing.Final[str] = "storage/song_counter.json"
    MUSIC_CHANNEL: int = 1071272760099209237


def current_time() -> str:
    now = datetime.now()
    timez = pytz.timezone('US/Eastern')
    now = now.astimezone(timez)  #
    ftime: str = now.strftime("%I:%M %p")

    return ftime
