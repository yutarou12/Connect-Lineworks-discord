import time
import uvicorn
import requests

from logging import getLogger, StreamHandler, DEBUG

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from requests.structures import CaseInsensitiveDict

from fastapi import FastAPI, Request

import libs.lineworks as lineworks
import libs.env as env

BASE_API_URL = "https://www.worksapis.com/v1.0"
BASE_AUTH_URL = "https://auth.worksmobile.com/oauth2/v2.0"
BASE_DISCORD_API_URL = "https://discord.com/api/v10"
SCOPE = "bot bot.message bot.read user.read"


global_data = {}
RETRY_COUNT_MAX = 5

app = FastAPI()
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


def load_privkey(filename):
    with open(filename, 'rb') as fpr:
        privkey = serialization.load_pem_private_key(
            fpr.read(),
            password=None,
            backend=default_backend()
        )
    return privkey


@app.post("/callback")
async def callback(request: Request):
    body_raw = await request.body()
    body_json = await request.json()
    headers = CaseInsensitiveDict(request.headers)

    logger.info(body_json)
    logger.info(headers)

    header_bot_id = headers.get("x-works-botid", "dummy")

    # Load parameters
    bot_id = env.LW_API_20_BOT_ID
    bot_secret = env.LW_API_20_BOT_SECRET
    client_id = env.LW_API_20_CLIENT_ID
    client_secret = env.LW_API_20_CLIENT_SECRET
    service_account_id = env.LW_API_20_SERVICE_ACCOUNT_ID
    privatekey = load_privkey("./key/private_20241030132604.key")

    # Validation
    signature = headers.get("x-works-signature")
    if header_bot_id != bot_id or not lineworks.validate_request(body_raw, signature, bot_secret):
        logger.warning("Invalid request")
        return

    user_id = body_json["source"]["userId"]
    content = body_json["content"]

    if "access_token" not in global_data:
        # Get Access Token
        logger.info("Get access token")
        res = lineworks.get_access_token(client_id,
                                         client_secret,
                                         service_account_id,
                                         privatekey,
                                         SCOPE)
        global_data["access_token"] = res["access_token"]

    logger.info("reply")

    discord_header = {
        'Authorization': f"Bot {env.DISCORD_BOT_TOKEN}"
    }
    res = requests.get(f"{BASE_DISCORD_API_URL}/channels/{env.DISCORD_CHANNEL_ID}/webhooks", headers=discord_header)
    if res.json():
        webhook_data = res.json()[0]
        webhook_id = webhook_data.get("id")
        webhook_token = webhook_data.get("token")

        user_data = lineworks.get_user(user_id, global_data["access_token"])
        user_name = f"{user_data.get('userName').get('lastName')} {user_data.get('userName').get('lastName')}"
        res_get_access_token = lineworks.get_access_token(client_id, client_secret, service_account_id, privatekey, "user.profile.read")
        user_photo = lineworks.get_user_photo(user_id, res_get_access_token["access_token"])
        logger.info(user_photo)

        discord_content = {
            "username": user_name,
            "content": str(content)
        }

        res = requests.post(f"{BASE_DISCORD_API_URL}/webhooks/{webhook_id}/{webhook_token}", json=discord_content)
        logger.info(res.json())

    return {}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8085, log_level="debug")
