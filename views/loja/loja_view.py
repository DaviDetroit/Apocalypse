import discord
from discord.ui import View, Button

from utils.logger import setup_logger


COR_PADRAO = discord.Color.dark_red()
COR_CARGOS = discord.Color.blurple()
COR_PRANKS = discord.Color.orange()
COR_CRIMSON = discord.Color.from_rgb(220, 20, 60)
COR_VERDUGO = discord.Color.purple()

# Footer padrão (só texto, sem ícone)
FOOTER_TEXT = "Loja do Licker"


def aplicar_padrao(embed: discord.Embed) -> discord.Embed:
    embed.set_footer(text=FOOTER_TEXT)
    return embed


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
        embed = discord.Embed(
            title="<:8681shoppmx:1541450494382448831> Loja de Cargos",
            description="Compre cargos especiais usando seus pontos.",
            color=COR_CARGOS
        )
        embed.add_field(name="🔴 Crimson Head", value="200 pontos", inline=True)
        embed.add_field(name="🟣 Verdugo", value="400 pontos", inline=True)
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=CargosView())

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
        embed = discord.Embed(
            title="🤡 Loja de Pranks",
            description=(
                "Use seus pontos para comprar brincadeiras "
                "e interações para zoar outros membros."
            ),
            color=COR_PRANKS
        )
        embed.add_field(name="🔇 Em breve...", value="\u200b", inline=False)
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=PranksView())


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
        embed = discord.Embed(
            title="🔵 Crimson Head",
            color=COR_CRIMSON
        )
        embed.add_field(name="Preço", value="200 pontos", inline=True)
        embed.add_field(name="Duração", value="12 horas", inline=True)
        embed.add_field(
            name="Vantagens",
            value=(
                "🩸 Acesso ao **chat geral do Licker**\n"
                "📻 Permissão para **transmitir no chat de rádio**"
            ),
            inline=False
        )
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=CrimsonHeadView())

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
        embed = discord.Embed(
            title="🟣 Verdugo",
            color=COR_VERDUGO
        )
        embed.add_field(name="Preço", value="400 pontos", inline=True)
        embed.add_field(name="Duração", value="3 dias", inline=True)
        embed.add_field(
            name="Vantagens",
            value=(
                "🩸 Acesso ao **chat geral do Licker**\n"
                "📻 Permissão para **transmitir no chat de rádio**\n"
                "🎤 Permissão para **usar o microfone no chat de músicas**"
            ),
            inline=False
        )
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=VerdugoView())

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
        embed = discord.Embed(
            title="<:8681shoppmx:1541450494382448831> Loja do Licker",
            description="**Cargo especial para...**\n\nEscolha um dos cargos abaixo ou confira nossas brincadeiras.",
            color=COR_PADRAO
        )
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=LojaView())


class CrimsonHeadView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Comprar",
        emoji="<:532883cash:1541463231699226695>",
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
        embed = discord.Embed(
            title="<:8681shoppmx:1541450494382448831> Loja de Cargos",
            description="Escolha um cargo:",
            color=COR_CARGOS
        )
        embed.add_field(name="🔴 Crimson Head", value="200 pontos", inline=True)
        embed.add_field(name="🟣 Verdugo", value="400 pontos", inline=True)
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=CargosView())


class VerdugoView(View):
    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Comprar",
        emoji="<:532883cash:1541463231699226695>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_verdugo"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await interaction.response.send_message(
            "<:532883cash:1541463231699226695> O sistema de compra será implementado na próxima etapa.",
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
        embed = discord.Embed(
            title="<:8681shoppmx:1541450494382448831> Loja de Cargos",
            description="Escolha um cargo:",
            color=COR_CARGOS
        )
        embed.add_field(name="🔴 Crimson Head", value="200 pontos", inline=True)
        embed.add_field(name="🟣 Verdugo", value="400 pontos", inline=True)
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=CargosView())


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
        embed = discord.Embed(
            title="<:8681shoppmx:1541450494382448831> Loja do Licker",
            description="**Cargo especial para...**\n\nEscolha uma categoria abaixo.",
            color=COR_PADRAO
        )
        aplicar_padrao(embed)

        await interaction.response.edit_message(content=None, embed=embed, view=LojaView())