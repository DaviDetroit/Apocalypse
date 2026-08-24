import discord
from discord import app_commands
from discord.ext import commands

from services.economy_service import EconomyService


class TransferirPesetas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="transferir_pesetas",
        description="Transfere Pesetas para outro membro."
    )
    @app_commands.describe(
        usuario="Membro que receberá as Pesetas",
        quantidade="Quantidade de Pesetas a transferir"
    )
    async def transferir_pesetas(
        self,
        interaction: discord.Interaction,
        usuario: discord.Member,
        quantidade: int
    ):

        if quantidade <= 0:
            await interaction.response.send_message(
                "<:whiskers:1541503209565200445> A quantidade precisa ser maior que 0.",
                ephemeral=True
            )
            return

        if usuario.id == interaction.user.id:
            await interaction.response.send_message(
                "<:whiskers:1541503209565200445> Você não pode transferir Pesetas para você mesmo.",
                ephemeral=True
            )
            return

        result = await EconomyService.transferir_pesetas(
            sender_discord_id=interaction.user.id,
            receiver_discord_id=usuario.id,
            amount=quantidade
        )

        if not result["success"]:

            if result["error"] == "sender_not_found":
                await interaction.response.send_message(
                    "<:whiskers:1541503209565200445> Você ainda não possui uma conta no sistema.",
                    ephemeral=True
                )
                return

            if result["error"] == "receiver_not_found":
                await interaction.response.send_message(
                    "<:whiskers:1541503209565200445> Esse usuário ainda não possui uma conta no sistema.",
                    ephemeral=True
                )
                return

            if result["error"] == "insufficient_points":
                await interaction.response.send_message(
                    f"<:whiskers:1541503209565200445> Você não possui Pesetas suficientes.\n\n"
                    f"<:pesetasmediumPhotoroom:1541499172467908678> Seu saldo: **{result['points']:,} Pesetas**\n"
                    f"💸 Valor da transferência: **{quantidade:,} Pesetas**"
                    .replace(",", "."),
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "❌ Ocorreu um erro ao realizar a transferência.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"<:pesetasmediumPhotoroom:1541499172467908678> **Transferência realizada!**\n\n"
            f"<:778612sigmaleonkennedy:1540797776038989884> Destinatário: {usuario.mention}\n"
            f"💸 Valor: **{quantidade:,} Pesetas**"
            .replace(",", ".")
        )


async def setup(bot):
    await bot.add_cog(
        TransferirPesetas(bot)
    )