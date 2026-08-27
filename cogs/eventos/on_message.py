import discord

from discord.ext import commands

from services.user_service import UserService
from services.message_service import MessageService


class OnMessage(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        await UserService.get_or_create_user(
            discord_id=message.author.id,
            username=message.author.name
        )

        # Registra a mensagem
        await MessageService.registrar_mensagem(
            discord_message_id=message.id,
            discord_author_id=message.author.id,
            guild_id=message.guild.id if message.guild else 0,
            channel_id=message.channel.id,
            content=message.content,
            has_attachment=bool(message.attachments),
            has_embed=bool(message.embeds)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessage(bot)
    )