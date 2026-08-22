import discord

from discord.ext import commands

from database.evaluations import (
    process_evaluation,
    count_daily_evaluations,
)

from utils.logger import setup_logger


logger = setup_logger()


CLIPES_JOGOS = 751088200742862968
EMOJI = "<:778612sigmaleonkennedy:1540797776038989884>"

POINTS_PER_EVALUATION = 1
DAILY_REWARD_MILESTONE = 5


class ReactionEvents(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self,
        payload: discord.RawReactionActionEvent,
    ):

        # Ignora bots
        if payload.member is not None and payload.member.bot:
            return

        if payload.channel_id != CLIPES_JOGOS:
            return

        if str(payload.emoji) != EMOJI:
            return

        evaluator_id = payload.user_id

        try:
            channel = self.bot.get_channel(payload.channel_id)

            if channel is None:
                logger.warning(
                    "Canal %s não encontrado.",
                    payload.channel_id,
                )
                return

            try:
                message = await channel.fetch_message(
                    payload.message_id
                )
            except discord.NotFound:
                logger.warning(
                    "Mensagem %s não encontrada.",
                    payload.message_id,
                )
                return

            author_id = message.author.id

            if evaluator_id == author_id:
                await self._remove_reaction(payload)

                logger.info(
                    "Usuário %s tentou avaliar a própria publicação %s.",
                    evaluator_id,
                    payload.message_id,
                )

                return

            # Processa avaliação no banco
            created = await process_evaluation(
                message_id=payload.message_id,
                author_discord_id=author_id,
                evaluator_discord_id=evaluator_id,
                points=POINTS_PER_EVALUATION,
            )

            if not created:
                await self._remove_reaction(payload)

                logger.info(
                    "Usuário %s já avaliou a mensagem %s.",
                    evaluator_id,
                    payload.message_id,
                )

                return

            logger.info(
                "Avaliação registrada: %s avaliou %s | +%s pontos.",
                evaluator_id,
                author_id,
                POINTS_PER_EVALUATION,
            )

            # Verifica quantidade de avaliações recebidas hoje
            daily_count = await count_daily_evaluations(
                author_id
            )

            if daily_count == DAILY_REWARD_MILESTONE:
                await self._send_milestone_message(
                    channel,
                    message.author,
                )

                logger.info(
                    "Usuário %s atingiu %s avaliações hoje.",
                    author_id,
                    DAILY_REWARD_MILESTONE,
                )

        except Exception:
            logger.exception(
                "Erro ao processar reação na mensagem %s.",
                payload.message_id,
            )

    async def _remove_reaction(
        self,
        payload: discord.RawReactionActionEvent,
    ):

        channel = self.bot.get_channel(payload.channel_id)

        if channel is None:
            return

        try:
            message = await channel.fetch_message(
                payload.message_id
            )

            await message.remove_reaction(
                payload.emoji,
                discord.Object(id=payload.user_id),
            )

        except discord.NotFound:
            pass

        except discord.Forbidden:
            logger.warning(
                "Sem permissão para remover reação da mensagem %s.",
                payload.message_id,
            )

        except discord.HTTPException as error:
            logger.error(
                "Erro ao remover reação: %s",
                error,
            )

    async def _send_milestone_message(
        self,
        channel: discord.TextChannel,
        member: discord.User,
    ):

        embed = discord.Embed(
            title="<:11639rebeccasalute:1540797532354125975> Parabéns!",
            description=(
                f"{member.mention} recebeu **5 avaliações** "
                "hoje pelas suas jogadas!"
            ),
        )

        await channel.send(
            embed=embed,
            allowed_mentions=discord.AllowedMentions(
                users=True
            ),
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionEvents(bot))