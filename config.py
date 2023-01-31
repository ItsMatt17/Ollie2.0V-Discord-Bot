import os


from dotenv import load_dotenv

load_dotenv(dotenv_path="OllieV2.0-master\.env")

AUTH_KEY=os.environ.get("DISCORD_KEY")
GUILD=982514587742142545
TESTING_CHANNEL=1037278984410517504