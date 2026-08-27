from discord.ext import commands

from services.user_service import UserService


class OnMemberJoin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):

        await UserService.get_or_create_user(
            discord_id=member.id,
            username=member.name
        )


async def setup(bot):
    await bot.add_cog(
        OnMemberJoin(bot)
    )