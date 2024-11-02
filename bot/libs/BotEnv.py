import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN: str = os.getenv("DISCORD_BOT_TOKEN")
LW_API_20_CLIENT_ID: str = os.getenv("LW_API_20_CLIENT_ID")
LW_API_20_CLIENT_SECRET: str = os.getenv("LW_API_20_CLIENT_SECRET")
LW_API_20_SERVICE_ACCOUNT_ID: str = os.getenv("LW_API_20_SERVICE_ACCOUNT_ID")
LW_API_20_PRIVATEKEY: str = os.getenv("LW_API_20_PRIVATEKEY")
LW_API_20_BOT_ID: str = os.getenv("LW_API_20_BOT_ID")
LW_API_20_BOT_SECRET: str = os.getenv("LW_API_20_BOT_SECRET")
LW_API_20_CHANNEL_ID: str = os.getenv("LW_API_20_CHANNEL_ID")
DISCORD_CHANNEL_ID: str = os.getenv("DISCORD_CHANNEL_ID")
CHANNEL_LIST: str = os.getenv("CHANNEL_LIST")
