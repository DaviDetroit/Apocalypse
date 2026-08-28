import discord

from discord import app_commands
from discord.ext import commands

from services.message_ranking_service import (
    MessageRankingService
)


class MessageRanking(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="gerar_ranking_mensagens",
        description="Gera o ranking semanal."
    )
    @app_commands.default_permissions(
        administrator=True
    )
    async def gerar_ranking_mensagens(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer()

        ranking = await MessageRankingService.reward_ranking()

        if not ranking:

            await interaction.followup.send(
                "Nenhuma mensagem encontrada."
            )
            return

        embed = discord.Embed(
            title="<:1477336895452348537:1542918892416929893> Ranking Semanal",
            color=discord.Color.gold()
        )

        medals = {
            1: "<:1480287911785005146:1542918668768251995>",
            2: "🥈",
            3: "🥉",
            4: "🏅",
            5: "🏅"
        }

        description = []

        for item in ranking:

            description.append(
                f"{medals[item['position']]} "
                f"<@{item['discord_id']}> • "
                f"{item['messages']} mensagens • "
                f"+{item['reward']} pesetas"
            )

        embed.description = "\n".join(description)

        await interaction.followup.send(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(
        MessageRanking(bot)
    )