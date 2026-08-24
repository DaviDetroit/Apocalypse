import re

import discord

from discord.ext import commands

from utils.logger import setup_logger
from config.constants import (
    CLIPES_JOGOS,
    EMOJI_AVALIACAO,
)

logger = setup_logger()

#Canal
<<<<<<< HEAD
CLIPES_JOGOS = 1427044546973405184

EMOJI = "<:1280pxUmbrella_Corporation_logo:1540878040354000966>"

=======
>>>>>>> dev
URL_REGEX = re.compile(r"https?://[^\s<>]+")

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
    ".avi",
)


class Avaliacao(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Ignora mensagens de bots
        if message.author.bot:
            return

        if message.channel.id != CLIPES_JOGOS:
            return

        has_url = bool(
            self.get_urls(message.content)
        )

        # Verifica se possui vídeo anexado
        has_video = self.has_video_attachment(message)

        # Não é uma publicação avaliável
        if not has_url and not has_video:
            return

        try:

            await message.add_reaction(EMOJI_AVALIACAO)

            logger.info(
                "Avaliação disponível | "
                "autor=%s | canal=%s | mensagem=%s",
                message.author.id,
                message.channel.id,
                message.id,
            )

        except discord.Forbidden:

            logger.warning(
                "Sem permissão para adicionar reação | "
                "mensagem=%s | canal=%s",
                message.id,
                message.channel.id,
            )

        except discord.HTTPException as error:

            logger.error(
                "Erro ao adicionar reação :( | "
                "mensagem=%s | erro=%s",
                message.id,
                error,
            )

    @staticmethod
    def get_urls(content: str) -> list[str]:

        return URL_REGEX.findall(content)

    @staticmethod
    def has_video_attachment(
        message: discord.Message,
    ) -> bool:

        for attachment in message.attachments:

            if attachment.content_type:
                if attachment.content_type.startswith("video/"):
                    return True

            if attachment.filename.lower().endswith(
                VIDEO_EXTENSIONS
            ):
                return True

        return False


async def setup(bot: commands.Bot):
    await bot.add_cog(Avaliacao(bot))