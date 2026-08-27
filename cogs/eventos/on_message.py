from discord.ext import commands

from services.user_service import UserService


class OnMessage(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        await UserService.get_or_create_user(
            discord_id=message.author.id,
            username=message.author.name
        )


async def setup(bot):
    await bot.add_cog(
        OnMessage(bot)
    )