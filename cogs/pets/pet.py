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

        if message.author.bot or message.channel.id != CANAL_PET:
            return

        if not message.attachments:
            return


        attachment = message.attachments[0]

        if not (attachment.content_type or "").startswith("image/"):
            return


        embed = discord.Embed(
            title=f"🐾 Pet de {message.author.name}"
        )

        embed.set_image(
            url=attachment.url
        )


        # Cria a mensagem do bot primeiro
        pet_message = await message.channel.send(
            embed=embed
        )


        # Salva no banco e pega o ID do pet
        pet_id = await PetService.criar_pet(
            pet_message.id,
            message.author.id,
            attachment.url
        )


        # Adiciona o botão depois que possui o ID
        await pet_message.edit(
            view=PetLikeView(pet_id)
        )


        await message.delete()



async def setup(bot: commands.Bot):
    await bot.add_cog(Pet(bot))