import discord
from discord import app_commands
from discord.ext import commands

from database.connection import get_pool


class Pesetas(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="pesetas",
        description="Veja quantas Pesetas você possui."
    )
    async def pesetas(self, interaction: discord.Interaction):

        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    SELECT points
                    FROM users
                    WHERE discord_id = %s
                    """,
                    (str(interaction.user.id),)
                )

                result = await cursor.fetchone()

        if not result:
            await interaction.response.send_message(
                "<:654404secret:1540852720263626872> Você ainda não possui uma conta registrada.",
                ephemeral=True
            )
            return

        points = result[0]

        embed = discord.Embed(
            title="🧟 Pesetas",
            description=(
                f"Você possui **{points:,} Pesetas**."
            ).replace(",", "."),
            color=discord.Color.dark_red()
        )

        embed.set_footer(
            text="Economia do Licker"
        )

        await interaction.response.send_message(
            embed=embed
        )


async def setup(bot):
    await bot.add_cog(Pesetas(bot))