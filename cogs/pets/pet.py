import discord

from discord.ext import commands

from config.constants import CANAL_PET

from services.pet_service import PetService

from cogs.pets.pet_view import PetLikeView


class Pet(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        if message.channel.id != CANAL_PET:
            return

        if not message.attachments:
            return

        attachment = message.attachments[0]

        if not (attachment.content_type or "").startswith("image/"):
            return

        # Baixa a imagem do Discord
        image = await attachment.to_file(
            filename=attachment.filename
        )

        embed = discord.Embed(
            title=f"🐾 Pet de {message.author.name}"
        )

        # A imagem será anexada na mensagem do bot
        embed.set_image(
            url=f"attachment://{attachment.filename}"
        )

        # Envia a nova mensagem
        pet_message = await message.channel.send(
            embed=embed,
            file=image,
            view=PetLikeView()
        )

        image_url = pet_message.attachments[0].url

        await PetService.criar_pet(
            pet_message.id,
            message.author.id,
            image_url
        )

        # Apaga a mensagem original
        await message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Pet(bot))