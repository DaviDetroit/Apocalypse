import discord

from services.pet_service import PetService


class PetLikeView(discord.ui.View):

    def __init__(self, pet_id: int):
        super().__init__(timeout=None)
        self.pet_id = pet_id

    @discord.ui.button(
        label="Curtir",
        emoji="❤️",
        style=discord.ButtonStyle.primary,
        custom_id="pet_like"
    )
    async def like(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        result = await PetService.dar_like(
            pet_id=self.pet_id,
            discord_user_id=interaction.user.id
        )

        if not result["success"]:

            if result["error"] == "own_pet":
                await interaction.response.send_message(
                    "<:whiskers:1541503209565200445> "
                    "Você não pode dar like no próprio pet.",
                    ephemeral=True
                )
                return

            if result["error"] == "already_liked":
                await interaction.response.send_message(
                    "❤️ Você já curtiu este pet.",
                    ephemeral=True
                )
                return

            if result["error"] == "pet_not_found":
                await interaction.response.send_message(
                    "❌ Este pet não está mais disponível.",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "❌ Não foi possível registrar o like.",
                ephemeral=True
            )
            return


        # Resposta para quem deu like
        await interaction.response.send_message(
            "❤️ Voto registrado! Obrigado por curtir este pet.",
            ephemeral=True
        )


        # Aviso para o dono do pet
        try:
            owner = await interaction.client.fetch_user(
                result["owner_id"]
            )

            await owner.send(
                f"❤️ Seu pet recebeu um novo like!\n"
                f"<:pesetasmediumPhotoroom:1541499172467908678> "
                f"Você ganhou **{result['points']} pesetas**."
            )

        except discord.Forbidden:
            pass