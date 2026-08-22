import asyncio
import discord
import os

from discord.ext import commands
from utils.logger import setup_logger

logger = setup_logger()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    logger.info(f"Bot conectado como {bot.user}")


async def load_cogs():
    for root, _, files in os.walk("cogs"):
        for file in files:
            if file.endswith(".py"):
                module = os.path.join(root, file)
                module = module.replace("\\", ".").replace("/", ".")[:-3]

                await bot.load_extension(module)

                logger.info(f"Carregado: {module}")

TOKEN = os.getenv("DISCORD_TOKEN")


async def main():
    await load_cogs()
    await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())