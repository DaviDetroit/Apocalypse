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

        if message.author.bot:
            return

        if message.channel.id != CANAL_PET:
            return

        if not message.attachments:
            return


        attachment = message.attachments[0]


        if not (attachment.content_type or "").startswith("image/"):
            return


        try:

            file = await attachment.to_file(
                filename=attachment.filename
            )


            embed = discord.Embed(
                title=f"🐾 Pet de {message.author.name}"
            )

            embed.set_image(
                url=f"attachment://{attachment.filename}"
            )


            pet_message = await message.channel.send(
                embed=embed,
                file=file
            )


            # busca a mensagem novamente para garantir attachment
            pet_message = await message.channel.fetch_message(
                pet_message.id
            )


            if not pet_message.attachments:
                print(
                    "Erro: Discord não retornou o attachment"
                )
                return


            bot_image_url = pet_message.attachments[0].url


            pet_id = await PetService.criar_pet(
                discord_message_id=pet_message.id,
                discord_author_id=message.author.id,
                image_url=bot_image_url
            )


            await pet_message.edit(
                view=PetLikeView(pet_id)
            )


            await asyncio.sleep(2)

            await message.delete()


        except discord.Forbidden:
            print(
                f"Sem permissão para processar {message.id}"
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