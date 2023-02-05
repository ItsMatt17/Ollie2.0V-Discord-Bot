import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
SPOTIFY_CLIENT_ID : str = os.environ.get("SPOTIFY_CLIENT_ID")
SPOTIFY_API : str = os.environ.get("SPOTIFY_API")
AUTH_KEY: str = os.environ.get("DISCORD_KEY")
GUILD: int = 982514587742142545
TESTING_CHANNEL: int = 1037278984410517504
MY_ID: int = 188779992585469952

