from discord.ext import commands


class Pontos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(Pontos(bot))