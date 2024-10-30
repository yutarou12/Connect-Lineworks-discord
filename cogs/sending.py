import json
from urllib import parse
from datetime import datetime

import discord
import jwt
import requests
from discord.ext import commands
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from libs import env

BASE_API_URL = "https://www.worksapis.com/v1.0"
BASE_AUTH_URL = "https://auth.worksmobile.com/oauth2/v2.0"


class SendingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_list = [1301041772926996490]

    def load_privkey(self, filename):
        with open(filename, 'rb') as fpr:
            privkey = serialization.load_pem_private_key(
                fpr.read(),
                password=None,
                backend=default_backend()
            )
        return privkey

    def get_jwt(self, client_id, service_account_id, privatekey):
        """アクセストークンのためのJWT取得
        """
        current_time = datetime.now().timestamp()
        iss = client_id
        sub = service_account_id
        iat = current_time
        exp = current_time + (60 * 60)  # 1時間

        jws = jwt.encode(
            {
                "iss": iss,
                "sub": sub,
                "iat": iat,
                "exp": exp
            }, key=privatekey, algorithm="RS256")

        return jws

    def get_access_token(self, client_id, client_secret, scope, jws):
        """アクセストークン取得"""
        url = '{}/token'.format(BASE_AUTH_URL)
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "assertion": f"{jws}",
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "client_id": f"{client_id}",
            "client_secret": f"{client_secret}",
            "scope": scope
        }
        form_data = params
        r = requests.post(url=url, data=form_data, headers=headers)
        body = json.loads(r.text)
        return body

    def refresh_access_token(self, client_id, client_secret, refresh_token):
        """アクセストークン更新"""
        url = '{}/token'.format(BASE_AUTH_URL)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": client_id,
            "client_secret": client_secret,
        }
        form_data = params
        r = requests.post(url=url, data=form_data, headers=headers)
        body = json.loads(r.text)

        return body

    def send_message(self, content, bot_id, channel_id, access_token):
        """メッセージ送信"""
        url = "{}/bots/{}/users/{}/messages".format(BASE_API_URL, bot_id, channel_id)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(access_token)
        }
        params = content
        form_data = json.dumps(params)
        r = requests.post(url=url, data=form_data, headers=headers)
        r.raise_for_status()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.content:
            return

        if message.channel.id in self.channel_list:
            client_id = env.LW_API_20_CLIENT_ID
            client_secret = env.LW_API_20_CLIENT_SECRET
            service_account_id = env.LW_API_20_SERVICE_ACCOUNT_ID
            privatekey = self.load_privkey("./key/private_20241030132604.key")
            bot_id = env.LW_API_20_BOT_ID
            channel_id = env.LW_API_20_CHANNEL_ID
            scope = 'bot bot.message bot.read'

            # JWT生
            jwttoken = self.get_jwt(client_id, service_account_id, privatekey)
            # アクセストークン取得
            res = self.get_access_token(client_id, client_secret, scope, jwttoken)
            access_token = res["access_token"]

            # APIリクエスト (メッセージ送信)
            content = {
                "content": {
                    "type": "text",
                    "text": message.clean_content
                }
            }

            self.send_message(content, bot_id, channel_id, access_token)


async def setup(bot):
    await bot.add_cog(SendingCog(bot))