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

        # Ignora mensagens do bot
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

            # Faz download da imagem original
            file = await attachment.to_file(
                filename=attachment.filename
            )


            # Primeiro envia o arquivo puro
            pet_message = await message.channel.send(
                file=file
            )


            # Busca novamente a mensagem
            # para garantir que o Discord carregou o attachment
            pet_message = await message.channel.fetch_message(
                pet_message.id
            )


            if not pet_message.attachments:
                print("Discord não retornou attachment")
                return


            # URL definitiva do Discord CDN
            image_url = pet_message.attachments[0].url



            # Cria registro no banco
            pet_id = await PetService.criar_pet(
                discord_message_id=pet_message.id,
                discord_author_id=message.author.id,
                image_url=image_url
            )


            # Cria embed
            embed = discord.Embed(
                title=f"🐾 Pet de {message.author.name}"
            )

            embed.set_image(
                url=image_url
            )


            # Edita mensagem adicionando embed e botão
            await pet_message.edit(
                embed=embed,
                view=PetLikeView(pet_id)
            )


            # Aguarda para não apagar instantâneo
            await asyncio.sleep(2)


            # Apaga mensagem original
            await message.delete()



        except discord.Forbidden:

            print(
                f"Sem permissão para processar pet {message.id}"
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