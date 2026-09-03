from datetime import datetime
from zoneinfo import ZoneInfo

import discord
from discord.ext import commands, tasks

from database.evaluations import get_monthly_top_evaluations
from utils.logger import setup_logger
from config.constants import DESTAQUE_CHANNEL_ID


logger = setup_logger()


HORA_DESTAQUE = 20


class DestaqueMensal(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ultimo_destaque = None
        self.verificar_destaque.start()

    def cog_unload(self):
        self.verificar_destaque.cancel()

    @tasks.loop(minutes=1)
    async def verificar_destaque(self):

        agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

        if agora.day != 1:
            return

        if agora.hour < HORA_DESTAQUE:
            return

        chave = agora.strftime("%Y-%m")

        if self.ultimo_destaque == chave:
            return

        self.ultimo_destaque = chave

        logger.info(
            "Horário do destaque atingido | data=%s",
            agora.strftime("%d/%m/%Y %H:%M:%S"),
        )

        try:
            await self.enviar_destaque()

        except Exception:
            logger.exception(
                "Erro ao enviar destaque mensal."
            )

    @verificar_destaque.before_loop
    async def antes_de_verificar(self):

        await self.bot.wait_until_ready()

    async def enviar_destaque(self):

        canal = self.bot.get_channel(DESTAQUE_CHANNEL_ID)

        if canal is None:
            logger.warning(
                "Canal de destaques %s não encontrado.",
                DESTAQUE_CHANNEL_ID,
            )
            return

        agora = datetime.now(
            ZoneInfo("America/Sao_Paulo")
        )

        # Pega o mês anterior
        if agora.month == 1:
            ano = agora.year - 1
            mes = 12
        else:
            ano = agora.year
            mes = agora.month - 1

        logger.info(
            "Buscando ranking mensal | período=%02d/%d",
            mes,
            ano,
        )

        ranking = await get_monthly_top_evaluations(
            year=ano,
            month=mes,
            limit=3
        )

        if not ranking:
            logger.info(
                "Nenhuma avaliação encontrada para %02d/%d.",
                mes,
                ano,
            )
            return

        embed = discord.Embed(
            title="🏆 Destaques do Mês",
            description=(
                "Os jogadores que mais se destacaram "
                f"em **{mes:02d}/{ano}**!"
            ),
            color=discord.Color.dark_red()
        )

        medalhas = ["🥇", "🥈", "🥉"]

        for index, jogador in enumerate(ranking):

            discord_id = jogador["discord_id"]
            total = jogador["total"]

            member = canal.guild.get_member(
                int(discord_id)
            )

            if member:
                nome = member.mention
            else:
                nome = f"<@{discord_id}>"

            embed.add_field(
                name=f"{medalhas[index]} {nome}",
                value=(
                    "<:487747ladydimitrescuez:1540868042517651547> "
                    f"**{total} avaliações recebidas**"
                ),
                inline=False
            )

        embed.set_footer(
            text="Apocalypse • Ranking mensal"
        )

        await canal.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions(
                users=True
            ),
        )

        logger.info(
            "Destaque mensal enviado | período=%02d/%d | "
            "participantes=%s",
            mes,
            ano,
            len(ranking)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(DestaqueMensal(bot))