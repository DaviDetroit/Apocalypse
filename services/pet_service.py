import discord

from services.pet_service import PetService


class PetLikeView(discord.ui.View):

    def __init__(self, discord_message_id):
        super().__init__(timeout=None)
        self.discord_message_id = discord_message_id


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
            discord_message_id=self.discord_message_id,
            discord_user_id=interaction.user.id
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


        await interaction.response.send_message(
            f"❤️ Like registrado!\n"
            f"Você deu **+{result['reward']} pesetas** para o dono do pet.",
            ephemeral=True
        )


        try:
            user = await interaction.client.fetch_user(
                result["owner_id"]
            )

            await user.send(
                f"❤️ **{interaction.user.name}** deu like no seu pet!\n"
                f"Você ganhou **{result['reward']} pesetas**."
            )

        except discord.Forbidden:
            pass