import re

import discord
from discord.ext import commands

CLIPES_JOGOS = 1427044546973405184


class AvaliacaoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(
        label="Avaliar jogada",
        emoji="⭐",
        style=discord.ButtonStyle.secondary,
        custom_id="avaliar_jogada"
    )
    async def avaliar_jogada(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "Avaliação recebida!",
            ephemeral=True
        )  

class Avaliacao(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.channel.id != CLIPES_JOGOS:
            return
        if not self.is_video(message):
            return
        await message.edit(
            view=AvaliacaoView()
        )
    @staticmethod
    def is_video(message: discord.Message) -> bool:
        for attachment in message.attachments:
            if attachment.content_type:
                if attachment.content_type.startswith("video/"):
                    return True

            if attachment.filename.lower().endswith(
                (".mp4", ".mov", ".webm", ".mkv", ".avi")
            ):
                return True

            urls = re.findall(
                r"https?://[^\s<>]+",
                message.content
            )

            for url in urls:
                url = url.lower().split("?")[0]

                if url.endswith(
                    (".mp4", ".mov", ".webm", ".mkv", ".avi")
                ):
                    return True
            return False
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Avaliacao(bot))


    