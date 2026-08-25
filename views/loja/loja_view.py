import discord

from discord.ui import View, Button

from services.loja_service import LojaService


COR_PADRAO = discord.Color.dark_red()
COR_CARGOS = discord.Color.blurple()
COR_PRANKS = discord.Color.orange()
COR_CRIMSON = discord.Color.yellow()
COR_VERDUGO = discord.Color.green()

# Footer padrão
FOOTER_TEXT = "Loja do Licker"


def aplicar_padrao(embed: discord.Embed) -> discord.Embed:
    embed.set_footer(text=FOOTER_TEXT)
    return embed


# ============================================================
# LOJA PRINCIPAL
# ============================================================

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
            description="Confira os cargos disponíveis para compra.",
            color=COR_CARGOS
        )

        embed.add_field(
            name="<:1477335586221199612:1541493141201227856> Crimson Head — 250 pesetas",
            value=(
                "• Garante **24 horas** de duração do cargo\n"
                "• Acesso ao **chat geral do Licker**\n"
                "• Permissão para **transmitir no chat de rádio**"
            ),
            inline=False
        )

        embed.add_field(
            name="<:1477335499277602992:1541493231538274375> Verdugo — 400 pesetas",
            value=(
                "• Garante **2 dias** de duração do cargo\n"
                "• Imune a cooldown nos chats"
            ),
            inline=False
        )

        aplicar_padrao(embed)

        await interaction.response.edit_message(
            content=None,
            embed=embed,
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
        embed = discord.Embed(
            title="🤡 Loja de Pranks",
            description=(
                "Use suas pesetas para comprar brincadeiras "
                "e interações para zoar outros membros."
            ),
            color=COR_PRANKS
        )

        embed.add_field(
            name="🔇 Em breve...",
            value="Novas brincadeiras estarão disponíveis aqui.",
            inline=False
        )

        aplicar_padrao(embed)

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=PranksView()
        )


# ============================================================
# CARGOS
# ============================================================

class CargosView(View):

    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Crimson Head",
        emoji="<:1477335586221199612:1541493141201227856>",
        style=discord.ButtonStyle.danger,
        custom_id="loja_crimson_head"
    )
    async def crimson_head(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        embed = discord.Embed(
            title="<:1477335586221199612:1541493141201227856> Crimson Head",
            color=COR_CRIMSON
        )

        embed.add_field(
            name="Preço",
            value="250 pesetas",
            inline=True
        )

        embed.add_field(
            name="Duração",
            value="24 horas",
            inline=True
        )

        embed.add_field(
            name="Vantagens",
            value=(
                "🩸 Acesso ao **chat geral do Licker**\n"
                "📻 Permissão para **transmitir no chat de rádio**"
            ),
            inline=False
        )

        aplicar_padrao(embed)

        await interaction.response.edit_message(
            content=None,
            embed=embed,
            view=CrimsonHeadView()
        )

    @discord.ui.button(
        label="Verdugo",
        emoji="<:1477335499277602992:1541493231538274375>",
        style=discord.ButtonStyle.secondary,
        custom_id="loja_verdugo"
    )
    async def verdugo(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        embed = discord.Embed(
            title="<:1477335499277602992:1541493231538274375> Verdugo",
            color=COR_VERDUGO
        )

        embed.add_field(
            name="Preço",
            value="400 pesetas",
            inline=True
        )

        embed.add_field(
            name="Duração",
            value="2 dias",
            inline=True
        )

        embed.add_field(
            name="Vantagens",
            value="⏱️ Imune a cooldown nos chats",
            inline=False
        )

        aplicar_padrao(embed)

        await interaction.response.edit_message(
            content=None,
            embed=embed,
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
            content=None,
            embed=criar_embed_loja(),
            view=LojaView()
        )


# ============================================================
# CRIMSON HEAD
# ============================================================

class CrimsonHeadView(View):

    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Comprar",
        emoji="<:pesetasmediumPhotoroom:1541499172467908678>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_crimson_head"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        result = await LojaService.comprar_item(
            discord_id=interaction.user.id,
            store_item_id=1
        )

        if not result["success"]:

            if result["error"] == "user_not_found":
                await interaction.response.send_message(
                    "❌ Você ainda não possui uma conta registrada.",
                    ephemeral=True
                )
                return

            if result["error"] == "item_not_found":
                await interaction.response.send_message(
                    "❌ Este item não está disponível na loja.",
                    ephemeral=True
                )
                return

            if result["error"] == "insufficient_points":
                await interaction.response.send_message(
                    f"❌ Você não possui pesetas suficientes.\n\n"
                    f"**Você tem:** {result['points']} pesetas\n"
                    f"**Necessário:** {result['cost']} pesetas",
                    ephemeral=True
                )
                return

            if result["error"] == "already_owned":
                await interaction.response.send_message(
                    "❌ Você já possui este cargo temporário.",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "❌ Não foi possível realizar a compra.",
                ephemeral=True
            )
            return

        # Compra aprovada pelo banco
        role = interaction.guild.get_role(
            int(result["discord_role_id"])
        )

        if role is None:
            await interaction.response.send_message(
                "⚠️ A compra foi registrada, mas não consegui encontrar "
                "o cargo no servidor. Avise a administração.",
                ephemeral=True
            )
            return

        try:
            await interaction.user.add_roles(role)
        except discord.Forbidden:
            await interaction.response.send_message(
                "⚠️ A compra foi registrada, mas não tenho permissão "
                "para adicionar este cargo.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"<:pesetasmediumPhotoroom:1541499172467908678>"
            f"**Compra realizada com sucesso!**\n\n"
            f"Você recebeu o cargo **{role.name}**.\n"
            f"⏱️ Duração: **24 horas**\n"
            f"💰 pesetas restantes: **{result['remaining_points']}**",
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
            content=None,
            embed=criar_embed_cargos(),
            view=CargosView()
        )


# ============================================================
# VERDUGO
# ============================================================

class VerdugoView(View):

    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Comprar",
        emoji="<:pesetasmediumPhotoroom:1541499172467908678>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_verdugo"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        result = await LojaService.comprar_item(
            discord_id=interaction.user.id,
            store_item_id=2
        )

        if not result["success"]:

            if result["error"] == "user_not_found":
                await interaction.response.send_message(
                    "<:654404secret:1540852720263626872> Você ainda não possui uma conta registrada.",
                    ephemeral=True
                )
                return

            if result["error"] == "item_not_found":
                await interaction.response.send_message(
                    "<:11639rebeccasalute:1540797532354125975> Este item não está disponível na loja.",
                    ephemeral=True
                )
                return

            if result["error"] == "insufficient_points":
                await interaction.response.send_message(
                    f"❌ Você não possui pesetas suficientes.\n\n"
                    f"**Você tem:** {result['points']} pesetas\n"
                    f"**Necessário:** {result['cost']} pesetas",
                    ephemeral=True
                )
                return

            if result["error"] == "already_owned":
                await interaction.response.send_message(
                    "❌ Você já possui este cargo temporário.",
                    ephemeral=True
                )
                return

            await interaction.response.send_message(
                "❌ Não foi possível realizar a compra.",
                ephemeral=True
            )
            return

        # Compra aprovada pelo banco
        role = interaction.guild.get_role(
            int(result["discord_role_id"])
        )

        if role is None:
            await interaction.response.send_message(
                "⚠️ A compra foi registrada, mas não consegui encontrar "
                "o cargo no servidor. Avise a administração.",
                ephemeral=True
            )
            return

        try:
            await interaction.user.add_roles(role)
        except discord.Forbidden:
            await interaction.response.send_message(
                "⚠️ A compra foi registrada, mas não tenho permissão "
                "para adicionar este cargo.",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"<:pesetasmediumPhotoroom:1541499172467908678>"
            f"**Compra realizada com sucesso!**\n\n"
            f"Você recebeu o cargo **{role.name}**.\n"
            f"⏱️ Duração: **2 dias**\n"
            f"💰 pesetas restantes: **{result['remaining_points']}**",
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
            content=None,
            embed=criar_embed_cargos(),
            view=CargosView()
        )


# ============================================================
# PRANKS
# ============================================================

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
            content=None,
            embed=criar_embed_loja(),
            view=LojaView()
        )


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def criar_embed_loja() -> discord.Embed:

    embed = discord.Embed(
        title="<:8681shoppmx:1541450494382448831> Loja do Licker",
        description="**Cargos especiais disponíveis:**",
        color=COR_PADRAO
    )

    embed.add_field(
        name="<:1477335586221199612:1541493141201227856> Crimson Head — 250 pesetas",
        value=(
            "• Garante **24 horas** do cargo\n"
            "• Acesso ao **chat geral do Licker**\n"
            "• Permissão para **transmitir no chat de rádio**"
        ),
        inline=False
    )

    embed.add_field(
        name="<:1477335499277602992:1541493231538274375> Verdugo — 400 pesetas",
        value=(
            "• Garante **2 dias** do cargo\n"
            "• Imune a cooldown nos chats"
        ),
        inline=False
    )

    aplicar_padrao(embed)

    return embed


def criar_embed_cargos() -> discord.Embed:

    embed = discord.Embed(
        title="<:8681shoppmx:1541450494382448831> Loja de Cargos",
        description="Escolha um cargo para visualizar os detalhes.",
        color=COR_CARGOS
    )

    embed.add_field(
        name="<:1477335586221199612:1541493141201227856> Crimson Head — 250 pesetas",
        value="Duração: **24 horas**",
        inline=False
    )

    embed.add_field(
        name="<:1477335499277602992:1541493231538274375> Verdugo — 400 pesetas",
        value="Duração: **2 dias**",
        inline=False
    )

    aplicar_padrao(embed)

    return embed


def formatar_duracao(segundos: int) -> str:

    if segundos >= 86400:

        dias = segundos // 86400
        restante = segundos % 86400

        if restante == 0:
            return f"{dias} dia{'s' if dias != 1 else ''}"

    if segundos >= 3600:

        horas = segundos // 3600

        if horas == 1:
            return "1 hora"

        return f"{horas} horas"

    minutos = segundos // 60

    return f"{minutos} minutos"