import datetime

import discord

from zoneinfo import ZoneInfo

from discord.ext import tasks

from config.constants import MENSAGEM_SEMANAL
from services.message_ranking_service import MessageRankingService
from utils.logger import setup_logger


logger = setup_logger()


class WeeklyMessageRanking:

    def __init__(self, bot):
        self.bot = bot
        self.ranking_loop.start()

    @tasks.loop(
        time=datetime.time(
            hour=15,
            minute=0,
            tzinfo=ZoneInfo("America/Sao_Paulo")
        )
    )
    async def ranking_loop(self):

        now = datetime.datetime.now(
            ZoneInfo("America/Sao_Paulo")
        )

        if now.weekday() != 6:
            return

        try:

            result = await (
                MessageRankingService.reward_ranking()
            )

            if not result["success"]:

                if result["error"] == "already_rewarded":
                    logger.info(
                        "Ranking semanal já foi premiado."
                    )
                    return

                if result["error"] == "empty_ranking":
                    logger.info(
                        "Nenhuma mensagem encontrada "
                        "para o ranking semanal."
                    )
                    return

                logger.warning(
                    "Erro ao gerar ranking: %s",
                    result["error"]
                )
                return

            ranking = result["ranking"]

            channel = self.bot.get_channel(
                MENSAGEM_SEMANAL
            )

            if channel is None:
                logger.error(
                    "Canal do ranking semanal não encontrado: %s",
                    MENSAGEM_SEMANAL
                )
                return

            medals = {
                1: "<:1480287911785005146:1542918668768251995>",
                2: "🥈",
                3: "🥉",
                4: "🏅",
                5: "🏅"
            }

            lines = []

            for item in ranking:

                position = item["position"]
                discord_id = item["discord_id"]
                messages = item["messages"]
                reward = item["reward"]

                medal = medals.get(
                    position,
                    "🏅"
                )

                lines.append(
                    f"{medal} <@{discord_id}> "
                    f"**{messages} mensagens** "
                    f"• <:pesetasmediumPhotoroom:1541499172467908678> "
                    f"**{reward} Pesetas**"
                )

            embed = discord.Embed(
                title=(
                    "<:1477336895452348537:1542918892416929893> "
                    "Os usuários mais ativos da semana"
                ),
                description="\n".join(lines),
                color=discord.Color.dark_red()
            )

            embed.set_footer(
                text="Faça /pesetas para ver quantas você possui."
            )

            await channel.send(
                embed=embed
            )

            logger.info(
                "Ranking semanal publicado no canal %s.",
                MENSAGEM_SEMANAL
            )

        except Exception:

            logger.exception(
                "Erro ao gerar ranking semanal de mensagens."
            )

    @ranking_loop.before_loop
    async def before_ranking_loop(self):

        await self.bot.wait_until_ready()

        logger.info(
            "Ranking semanal automático iniciado. "
            "Execução: domingos às 15:00 (Brasília)."
        )

async def setup(bot):
    WeeklyMessageRanking(bot)