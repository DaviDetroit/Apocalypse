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

        # Ignora mensagens do próprio bot
        if message.author.bot:
            return

        # Só funciona no canal de pets
        if message.channel.id != CANAL_PET:
            return

        # Precisa ter imagem
        if not message.attachments:
            return

        attachment = message.attachments[0]

        # Aceita apenas imagens
        if not (attachment.content_type or "").startswith("image/"):
            return

        image_url = attachment.url

        try:
            embed = discord.Embed(
                title=f"🐾 Pet de {message.author.name}"
            )

            embed.set_image(url=image_url)

            # Envia a imagem do bot
            pet_message = await message.channel.send(
                embed=embed
            )

            # Salva no banco e pega ID do pet
            pet_id = await PetService.criar_pet(
                discord_message_id=pet_message.id,
                discord_author_id=message.author.id,
                image_url=image_url
            )

            # Coloca botão usando ID correto do banco
            await pet_message.edit(
                view=PetLikeView(pet_id)
            )

            # Aguarda antes de apagar original
            await asyncio.sleep(2)

            await message.delete()

        except discord.Forbidden:
            print(
                f"Sem permissão para processar o pet {message.id}"
            )

        except discord.HTTPException as error:
            print(
                f"Erro Discord ao processar pet {message.id}: {error}"
            )

        except Exception as error:
            print(
                f"Erro ao processar o pet {message.id}: {error}"
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Pet(bot))