from discord.ext import commands


class OnReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        pass


async def setup(bot):
    await bot.add_cog(OnReaction(bot))