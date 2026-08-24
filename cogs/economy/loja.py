import discord
from discord import app_commands
from discord.ext import commands

from views.loja.loja_view import LojaView
from config.constants import (
    CANAL_COMANDOS,
)

class Loja(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="loja",
        description="Abra a loja do Licker."
    )
    async def loja(self, interaction: discord.Interaction):
        if interaction.channel_id != CANAL_COMANDOS:
            await interaction.response.send_message(
                f"Por favor, use este comando no canal <#{CANAL_COMANDOS}>.",
                ephemeral=True,
            )
            return

        embed = discord.Embed(
            title="🛒 Loja do Licker",
            description=(
                "**Cargo especial para...**\n\n"
                "Compre cargos especiais usando seus pontos "
                "ou confira nossas brincadeiras.\n\n"
                "Escolha uma categoria abaixo."
            ),
            color=discord.Color.dark_red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=LojaView()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Loja(bot))