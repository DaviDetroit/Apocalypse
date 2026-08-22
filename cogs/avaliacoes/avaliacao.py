import re

import discord
from discord.ext import commands

from utils.logger import setup_logger


logger = setup_logger()

CLIPES_JOGOS = 751088200742862968

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

        # Ignora mensagens enviadas por bots
        if message.author.bot:
            return

        # Só processa o canal de clipes
        if message.channel.id != CLIPES_JOGOS:
            return

        # Verifica links
        urls = self.get_urls(message.content)

        # Verifica vídeos anexados
        video_attachments = self.get_video_attachments(message)

        # Se não tiver link nem vídeo, ignora
        if not urls and not video_attachments:
            return

        try:
            await message.add_reaction("⭐")

            logger.info(
                "Avaliação disponível | autor=%s | canal=%s | "
                "mensagem=%s | links=%s | anexos=%s",
                message.author.id,
                message.channel.id,
                message.id,
                len(urls),
                len(video_attachments),
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
                "Erro ao adicionar reação | "
                "mensagem=%s | erro=%s",
                message.id,
                error,
            )

    @staticmethod
    def get_urls(content: str) -> list[str]:

        return URL_REGEX.findall(content)

    @staticmethod
    def get_video_attachments(
        message: discord.Message,
    ) -> list[discord.Attachment]:

        videos = []

        for attachment in message.attachments:

            if attachment.content_type:
                if attachment.content_type.startswith("video/"):
                    videos.append(attachment)
                    continue

            if attachment.filename.lower().endswith(VIDEO_EXTENSIONS):
                videos.append(attachment)

        return videos


async def setup(bot: commands.Bot):
    await bot.add_cog(Avaliacao(bot))