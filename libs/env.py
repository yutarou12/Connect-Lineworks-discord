import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN : str = os.getenv("DISCORD_BOT_TOKEN")