import discord
from discord.ui import View, Button

from utils.logger import setup_logger



class LojaView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Cargos",
        emoji="<:8681shoppmx:1541450494382448831>",
        style=discord.ButtonStyle.primary,
        custom_id="loja_cargos"
    )
    async def cargos(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content=(
                "## <:8681shoppmx:1541450494382448831> Loja de Cargos\n\n"
                "Compre cargos especiais usando seus pontos.\n\n"
                "🔴 **Crimson Head** — 200 pontos\n"
                "🟣 **Verdugo** — 400 pontos"
            ),
            view=CargosView()
        )

    @discord.ui.button(
        label="Pranks",
        emoji="🤡",
        style=discord.ButtonStyle.secondary,
        custom_id="loja_pranks"
    )
    async def pranks(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content=(
                "## 🤡 Loja de Pranks\n\n"
                "Use seus pontos para comprar brincadeiras "
                "e interações para zoar outros membros.\n\n"
                "🔇 **Em breve...**"
            ),
            view=PranksView()
        )

class CargosView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Crimson Head",
        emoji="🔵",
        style=discord.ButtonStyle.danger,
        custom_id="loja_crimson_head"
    )
    async def crimson_head(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content=(
                "## 🔵 Crimson Head\n\n"
                "**Preço:** 200 pontos\n"
                "**Duração:** 12 horas\n\n"
                "**Vantagens:**\n"
                "• 🩸 Acesso ao **chat geral do Licker**;\n"
                "• 📻 Permissão para **transmitir no chat de rádio**."
            ),
            view=CrimsonHeadView()
        )

    @discord.ui.button(
        label="Verdugo",
        emoji="🟣",
        style=discord.ButtonStyle.secondary,
        custom_id="loja_verdugo"
    )
    async def verdugo(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content=(
                "## 🟣 Verdugo\n\n"
                "**Preço:** 400 pontos\n"
                "**Duração:** 3 dias\n\n"
                "**Vantagens:**\n"
                "• 🩸 Acesso ao **chat geral do Licker**;\n"
                "• 📻 Permissão para **transmitir no chat de rádio**;\n"
                "• 🎤 Permissão para **usar o microfone no chat de músicas**."
            ),
            view=VerdugoView()
        )

    @discord.ui.button(
        label="Voltar",
        emoji="<:755819back:1541451089239343104>",
        style=discord.ButtonStyle.secondary,
        custom_id="loja_voltar"
    )
    async def voltar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content=(
                "## <:8681shoppmx:1541450494382448831> Loja do Licker\n\n"
                "**Cargo especial para...**\n\n"
                "Escolha um dos cargos abaixo ou confira nossas brincadeiras."
            ),
            view=LojaView()
        )


class CrimsonHeadView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Comprar",
        emoji="<a:855247doginaldollar:1541451321549258792>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_crimson_head"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.send_message(
            "💰 O sistema de compra será implementado na próxima etapa.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Voltar",
        emoji="<:755819back:1541451089239343104>",
        style=discord.ButtonStyle.secondary,
        custom_id="voltar_crimson_head"
    )
    async def voltar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content="## <:8681shoppmx:1541450494382448831> Loja de Cargos\n\nEscolha um cargo:",
            view=CargosView()
        )


class VerdugoView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Comprar",
        emoji="<a:855247doginaldollar:1541451321549258792>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_verdugo"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.send_message(
            "<a:855247doginaldollar:1541451321549258792> O sistema de compra será implementado na próxima etapa.",
            ephemeral=True
        )

    @discord.ui.button(
        label="Voltar",
        emoji="<:755819back:1541451089239343104>",
        style=discord.ButtonStyle.secondary,
        custom_id="voltar_verdugo"
    )
    async def voltar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content="## <a:855247doginaldollar:1541451321549258792> Loja de Cargos\n\nEscolha um cargo:",
            view=CargosView()
        )


class PranksView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Voltar",
        emoji="<:755819back:1541451089239343104>",
        style=discord.ButtonStyle.secondary,
        custom_id="voltar_pranks"
    )
    async def voltar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.edit_message(
            content=(
                "## <:8681shoppmx:1541450494382448831> Loja do Licker\n\n"
                "**Cargo especial para...**\n\n"
                "Escolha uma categoria abaixo."
            ),
            view=LojaView()
        )