import re

import discord
from discord.ext import commands


CLIPES_JOGOS = 1427044546973405184

URL_REGEX = re.compile(r"https?://[^\s<>]+")


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


class Avaliacao(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Ignora mensagens enviadas pelo próprio bot
        if message.author.bot:
            return

        if message.channel.id != CLIPES_JOGOS:
            return

        urls = self.get_urls(message.content)

        if not urls:
            return

        autor_id = message.author.id

        texto = message.content

        try:
            await message.delete()


            await message.channel.send(
                content=texto,
                view=AvaliacaoView(autor_id),
                allowed_mentions=discord.AllowedMentions.none(),
            )

        except discord.Forbidden:
            print(
                "O bot não possui permissão para apagar "
                "ou enviar mensagens."
            )

        except discord.HTTPException as error:
            print(f"Erro ao republicar mensagem: {error}")

    @staticmethod
    def get_urls(content: str) -> list[str]:
       

        return URL_REGEX.findall(content)


async def setup(bot: commands.Bot):
    await bot.add_cog(Avaliacao(bot))