import asyncio
import os

import discord
from discord.ext import commands

from database.connection import (
    init_database,
    close_database,
)

from utils.logger import setup_logger


logger = setup_logger()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
)


@bot.event
async def on_ready():

    logger.info(
        "Bot conectado como %s",
        bot.user
    )


async def load_cogs():

    for root, _, files in os.walk("cogs"):

        for file in files:

            if not file.endswith(".py"):
                continue

            module = os.path.join(root, file)

            module = (
                module
                .replace("\\", ".")
                .replace("/", ".")
                [:-3]
            )

            await bot.load_extension(module)

            logger.info(
                "Carregado: %s",
                module
            )


async def main():

    await init_database()

    try:

        async with bot:

            await load_cogs()

            await bot.start(TOKEN)

    finally:

        await close_database()


if __name__ == "__main__":
    asyncio.run(main())