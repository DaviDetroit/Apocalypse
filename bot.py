from discord.ext import commands

def create_bot():
    bot = commands.Bot(
        command_prefix="!",
        intents=...
    )

    return bot

