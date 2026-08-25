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

        # Precisa ter pelo menos um anexo
        if not message.attachments:
            return

        attachment = message.attachments[0]

        # Só aceita imagens
        if not (attachment.content_type or "").startswith("image/"):
            return

        # Guarda a URL da imagem original
        image_url = attachment.url

        try:
            # Cria o embed
            embed = discord.Embed(
                title=f"🐾 Pet de {message.author.name}"
            )

            embed.set_image(url=image_url)

            # Envia a mensagem do bot
            pet_message = await message.channel.send(
                embed=embed
            )

            # Salva o pet no banco
            await PetService.criar_pet(
                discord_message_id=pet_message.id,
                discord_author_id=message.author.id,
                image_url=image_url
            )

            # Adiciona o botão de Curtir
            await pet_message.edit(
                view=PetLikeView(pet_message.id)
            )

            # Só apaga a mensagem original depois
            # que tudo deu certo
            await message.delete()

        except discord.Forbidden:
            print(
                f"Sem permissão para processar o pet "
                f"da mensagem {message.id}"
            )

        except discord.HTTPException as error:
            print(
                f"Erro do Discord ao processar o pet "
                f"{message.id}: {error}"
            )

        except Exception as error:
            print(
                f"Erro ao processar o pet {message.id}: {error}"
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Pet(bot))