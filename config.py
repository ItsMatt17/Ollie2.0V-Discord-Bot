import os
import platform
import typing
from datetime import datetime

import pytz
from dotenv import load_dotenv

# ~~~~~~API KEYS~~~~~~#
load_dotenv(dotenv_path=r"C:\Users\matts\OneDrive\Desktop\Discord-Bot\.env")
SPOTIFY_CLIENT_ID: str = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_API: str = os.environ.get("SPOTIFY_API")
AUTH_KEY: str = os.environ.get("DISCORD_KEY")
NASA_PHOTO: str = os.environ.get("NASA_PHOTO")
DATA_BASE_PASS: str = os.environ.get("DATA_BASE_PASSWORD")

folder_root: str = "MattBot/"

if platform.system() == "Windows":
    folder_root: str = ""
    database: str = "discord"
    db_user: str = "postgres"

# ~~~~~GUILD INFO~~~~~~
GUILD: int = 982514587742142545
TESTING_CHANNEL: int = 1037278984410517504

# ~~~~~~USERS~~~~~~
SHADYS_ID = 212353187523330048
MY_ID: int = 188779992585469952
CHLOE_ID: typing.Final[int] = 396098786520334338
SANDRA_ID: typing.Final[int] = 620357491355549715

COGS_FOLDER: typing.Final[str] = f"{folder_root}cogs"


class VCLeveling:
    XP_RATE = 250
    VC_FILE_PATH = f"{folder_root}storage/voice_channel_data.json"


class GuildInfo:
    DEFAULT_ROLE: int = 982531286616899634  # The Unwanted Role
    GUILD_ID: int = 982514587742142545


class VoiceFunny:
    assets = f"{folder_root}assets"
    executable = f"{folder_root}ffmpeg.exe"


class ISSLocatorInfo:
    GOOGLE_MAPS: str = os.environ.get("GOOGLE_MAPS")
    ISSEmbedPath: str = f"{folder_root}storage/ISSEmbedData.json"
    COORD_API: str = "http://api.open-notify.org/iss-now.json"


class MusicTracker:
    SONG_COUNTER_PATH: typing.Final[str] = f"{folder_root}storage/song_counter.json"
    MUSIC_CHANNEL: int = 1071272760099209237


def current_time() -> str:
    now = datetime.now()
    timez = pytz.timezone('US/Eastern')
    now = now.astimezone(timez)  #
    ftime: str = now.strftime("%I:%M %p")

    return ftime
