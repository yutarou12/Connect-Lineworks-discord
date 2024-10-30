import os
import discord
from discord.ext import commands
from logging import getLogger, StreamHandler, DEBUG
import bot.libs.env as env

logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


extensions_list = [f[:-3] for f in os.listdir("cogs") if f.endswith(".py")]


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    async def setup_hook(self):
        await bot.load_extension('jishaku')
        for ext in extensions_list:
            await bot.load_extension(f'cogs.{ext}')

    async def get_context(self, message, *args, **kwargs):
        return await super().get_context(message, *args, **kwargs)


intents = discord.Intents.default()
intents.message_content = True

bot = MyBot(
    command_prefix=commands.when_mentioned_or('lineworks.'),
    intents=intents,
    allowed_mentions=discord.AllowedMentions(replied_user=False, everyone=False),
    help_command=None
)

if __name__ == '__main__':
    bot.run(env.DISCORD_BOT_TOKEN)
