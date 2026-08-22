import io
import re

import aiohttp
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

# Discord tem limite de upload por arquivo (padrão 25MB, servidores boost
# podem chegar a 50MB/100MB). Ajuste conforme o boost level do seu servidor.
MAX_UPLOAD_BYTES = 25 * 1024 * 1024


class AvaliacaoView(discord.ui.View):

    def __init__(self, autor_id: int):
        super().__init__(timeout=None)

        self.autor_id = autor_id

    @discord.ui.button(
        label="Avaliar jogada",
        emoji="⭐",
        style=discord.ButtonStyle.secondary,
        custom_id="avaliar_jogada",
    )
    async def avaliar_jogada(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button,
    ):
        await interaction.response.send_message(
            "Avaliação recebida!",
            ephemeral=True,
        )

        logger.info(
            "Avaliação iniciada | avaliador=%s | autor=%s | mensagem=%s",
            interaction.user.id,
            self.autor_id,
            interaction.message.id,
        )


class Avaliacao(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._session: aiohttp.ClientSession | None = None

    async def cog_load(self):
        self._session = aiohttp.ClientSession()

    async def cog_unload(self):
        if self._session:
            await self._session.close()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Ignora mensagens enviadas por bots
        if message.author.bot:
            return

        # Ignora outros canais
        if message.channel.id != CLIPES_JOGOS:
            return

        # Procura links
        urls = self.get_urls(message.content)

        # Procura vídeos anexados
        video_attachments = self.get_video_attachments(message)

        # Se não tiver link nem vídeo anexado, ignora
        if not urls and not video_attachments:
            return

        autor_id = message.author.id

        logger.info(
            "Vídeo detectado | autor=%s | canal=%s | mensagem=%s | "
            "links=%s | anexos=%s",
            autor_id,
            message.channel.id,
            message.id,
            len(urls),
            len(video_attachments),
        )

        try:

            texto = message.content

            # Baixa os bytes de cada vídeo anexado ANTES de deletar a
            # mensagem original (a URL do attachment pode ficar
            # inválida depois que a mensagem é apagada).
            files = await self.download_attachments(video_attachments)

            await message.delete()

            logger.info(
                "Mensagem original removida | autor=%s | mensagem=%s",
                autor_id,
                message.id,
            )

            conteudo = texto if texto else None

            nova_mensagem = await message.channel.send(
                content=conteudo,
                files=files if files else None,
                view=AvaliacaoView(autor_id),
                allowed_mentions=discord.AllowedMentions.none(),
            )

            logger.info(
                "Publicação republicada | autor=%s | "
                "mensagem_original=%s | mensagem_nova=%s | canal=%s",
                autor_id,
                message.id,
                nova_mensagem.id,
                message.channel.id,
            )

        except discord.Forbidden:

            logger.warning(
                "Sem permissão para processar publicação | "
                "autor=%s | mensagem=%s | canal=%s",
                autor_id,
                message.id,
                message.channel.id,
            )

        except discord.HTTPException as error:

            logger.error(
                "Erro HTTP ao republicar publicação | "
                "autor=%s | mensagem=%s | erro=%s",
                autor_id,
                message.id,
                error,
            )

    async def download_attachments(
        self,
        attachments: list[discord.Attachment],
    ) -> list[discord.File]:
        """Baixa cada attachment e devolve como discord.File pronto
        para reenvio. Attachments maiores que MAX_UPLOAD_BYTES são
        ignorados (nesse caso, cai de volta pra reenviar só o link)."""

        files = []

        for attachment in attachments:

            if attachment.size and attachment.size > MAX_UPLOAD_BYTES:
                logger.warning(
                    "Anexo muito grande para reenvio direto | "
                    "arquivo=%s | tamanho=%s",
                    attachment.filename,
                    attachment.size,
                )
                continue

            try:
                data = await attachment.read()
            except discord.HTTPException as error:
                logger.error(
                    "Falha ao baixar anexo | arquivo=%s | erro=%s",
                    attachment.filename,
                    error,
                )
                continue

            files.append(
                discord.File(
                    io.BytesIO(data),
                    filename=attachment.filename,
                )
            )

        return files

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