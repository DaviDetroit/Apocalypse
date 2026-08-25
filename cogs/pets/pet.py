import asyncio

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

        # Ignora bots
        if message.author.bot:
            return

        # Apenas canal de pets
        if message.channel.id != CANAL_PET:
            return

        # Precisa ter imagem
        if not message.attachments:
            return


        attachment = message.attachments[0]


        # Apenas imagens
        if not (attachment.content_type or "").startswith("image/"):
            return


        try:

            # Faz uma cópia do arquivo
            file = await attachment.to_file(
                filename=attachment.filename
            )


            # Cria embed usando o anexo do próprio bot
            embed = discord.Embed(
                title=f"🐾 Pet de {message.author.name}"
            )

            embed.set_image(
                url=f"attachment://{attachment.filename}"
            )


            # Envia imagem pelo bot
            pet_message = await message.channel.send(
                embed=embed,
                file=file
            )


            # Pega a URL verdadeira do bot
            bot_image_url = pet_message.attachments[0].url


            # Salva no banco
            pet_id = await PetService.criar_pet(
                discord_message_id=pet_message.id,
                discord_author_id=message.author.id,
                image_url=bot_image_url
            )


            # Adiciona botão
            await pet_message.edit(
                view=PetLikeView(pet_id)
            )


            # Espera e remove original
            await asyncio.sleep(2)

            await message.delete()


        except discord.Forbidden:

            print(
                f"Sem permissão para apagar/processar {message.id}"
            )


        except discord.HTTPException as error:

            print(
                f"Erro Discord no pet {message.id}: {error}"
            )


        except Exception as error:

            print(
                f"Erro ao processar pet {message.id}: {error}"
            )



async def setup(bot: commands.Bot):

    await bot.add_cog(Pet(bot))