import discord

from services.pet_service import PetService


class PetLikeView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)


    @discord.ui.button(
        label="Curtir",
        emoji="❤️",
        style=discord.ButtonStyle.primary,
        custom_id="pet_like_button"
    )
    async def like(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        result = await PetService.dar_like(
            interaction.message.id,
            interaction.user.id
        )


        if not result["success"]:

            if result["error"] == "already_liked":
                await interaction.response.send_message(
                    "❌ Você já curtiu esse pet.",
                    ephemeral=True
                )
                return


            if result["error"] == "pet_not_found":
                await interaction.response.send_message(
                    "❌ Esse pet não existe mais.",
                    ephemeral=True
                )
                return


            await interaction.response.send_message(
                "❌ Não foi possível registrar o like.",
                ephemeral=True
            )
            return


        # envia DM para o dono do pet
        try:
            owner = await interaction.client.fetch_user(
                int(result["owner_id"])
            )

            await owner.send(
                f"❤️ **{interaction.user.name}** deu like no seu pet!\n\n"
                f"<:pesetasmediumPhotoroom:1541499172467908678> Você ganhou **{result['reward']} pesetas**.\n"
                f"Use `/pesetas` para ver seu saldo."
            )

        except discord.Forbidden:
            pass


        await interaction.response.send_message(
            f"<:whiskers:1541503209565200445> Like registrado!\n"
            f"Você deu **+1 like** nesse pet.",
            ephemeral=True
        )