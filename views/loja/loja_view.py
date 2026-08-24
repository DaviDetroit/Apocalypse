import discord

from discord.ui import View, Button

from services.loja import LojaService


COR_PADRAO = discord.Color.dark_red()
COR_CARGOS = discord.Color.blurple()
COR_PRANKS = discord.Color.orange()
COR_CRIMSON = discord.Color.from_rgb(220, 20, 60)
COR_VERDUGO = discord.Color.purple()

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
            name="🔴 Crimson Head — 200 pontos",
            value=(
                "• Garante **12 horas** de duração do cargo\n"
                "• Acesso ao **chat geral do Licker**\n"
                "• Permissão para **transmitir no chat de rádio**"
            ),
            inline=False
        )

        embed.add_field(
            name="🟣 Verdugo — 400 pontos",
            value=(
                "• Garante **3 dias** de duração do cargo\n"
                "• Acesso ao **chat geral do Licker**\n"
                "• Permissão para **transmitir no chat de rádio**\n"
                "• Permissão para **usar o microfone no chat de músicas**"
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
                "Use seus pontos para comprar brincadeiras "
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
        emoji="🔴",
        style=discord.ButtonStyle.danger,
        custom_id="loja_crimson_head"
    )
    async def crimson_head(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        embed = discord.Embed(
            title="🔴 Crimson Head",
            color=COR_CRIMSON
        )

        embed.add_field(
            name="Preço",
            value="200 pontos",
            inline=True
        )

        embed.add_field(
            name="Duração",
            value="12 horas",
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

        embed.add_field(
            name="Preço",
            value="400 pontos",
            inline=True
        )

        embed.add_field(
            name="Duração",
            value="3 dias",
            inline=True
        )

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
        emoji="<:532883cash:1541463231699226695>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_crimson_head"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await processar_compra(
            interaction=interaction,
            store_item_id=1,
            nome_item="Crimson Head"
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
        emoji="<:532883cash:1541463231699226695>",
        style=discord.ButtonStyle.success,
        custom_id="comprar_verdugo"
    )
    async def comprar(
        self,
        interaction: discord.Interaction,
        button: Button
    ):
        await processar_compra(
            interaction=interaction,
            store_item_id=2,
            nome_item="Verdugo"
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
        name="🔴 Crimson Head — 200 pontos",
        value=(
            "• Garante **12 horas** do cargo\n"
            "• Acesso ao **chat geral do Licker**\n"
            "• Permissão para **transmitir no chat de rádio**"
        ),
        inline=False
    )

    embed.add_field(
        name="🟣 Verdugo — 400 pontos",
        value=(
            "• Garante **3 dias** do cargo\n"
            "• Acesso ao **chat geral do Licker**\n"
            "• Permissão para **transmitir no chat de rádio**\n"
            "• Permissão para **usar o microfone no chat de músicas**"
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
        name="🔴 Crimson Head — 200 pontos",
        value="Duração: **12 horas**",
        inline=False
    )

    embed.add_field(
        name="🟣 Verdugo — 400 pontos",
        value="Duração: **3 dias**",
        inline=False
    )

    aplicar_padrao(embed)

    return embed


# ============================================================
# PROCESSAMENTO DA COMPRA
# ============================================================

async def processar_compra(
    interaction: discord.Interaction,
    store_item_id: int,
    nome_item: str
):

    # Evita que o usuário fique esperando sem resposta
    await interaction.response.defer(ephemeral=True)

    try:

        resultado = await LojaService.comprar_item(
            discord_id=interaction.user.id,
            store_item_id=store_item_id
        )

    except Exception as error:

        print(
            f"Erro ao comprar {nome_item}: {error}"
        )

        await interaction.followup.send(
            "❌ Ocorreu um erro ao processar sua compra.",
            ephemeral=True
        )

        return

    # ========================================================
    # ERROS
    # ========================================================

    if not resultado["success"]:

        if resultado["error"] == "user_not_found":

            mensagem = (
                "❌ Você ainda não possui uma conta registrada "
                "no sistema de economia."
            )

        elif resultado["error"] == "item_not_found":

            mensagem = (
                "❌ Este item não está disponível na loja."
            )

        elif resultado["error"] == "insufficient_points":

            mensagem = (
                "❌ Você não possui pontos suficientes.\n\n"
                f"💰 Seus pontos: **{resultado['points']}**\n"
                f"💵 Preço: **{resultado['cost']}**"
            )

        elif resultado["error"] == "already_owned":

            mensagem = (
                f"❌ Você já possui o cargo **{nome_item}** "
                "ativo."
            )

        else:

            mensagem = (
                "❌ Não foi possível realizar a compra."
            )

        await interaction.followup.send(
            mensagem,
            ephemeral=True
        )

        return

    # ========================================================
    # SUCESSO
    # ========================================================

    discord_role_id = resultado.get("discord_role_id")

    if not discord_role_id:

        await interaction.followup.send(
            "⚠️ A compra foi registrada, mas não consegui "
            "identificar o cargo no Discord. Avise um administrador.",
            ephemeral=True
        )

        return

    role = interaction.guild.get_role(
        int(discord_role_id)
    )

    if role is None:

        await interaction.followup.send(
            "⚠️ A compra foi registrada, mas o cargo não foi "
            "encontrado no servidor. Avise um administrador.",
            ephemeral=True
        )

        return

    try:

        await interaction.user.add_roles(
            role,
            reason=f"Compra na loja: {nome_item}"
        )

    except discord.Forbidden:

        await interaction.followup.send(
            "⚠️ A compra foi registrada, mas o bot não possui "
            "permissão para adicionar esse cargo.",
            ephemeral=True
        )

        return

    except discord.HTTPException:

        await interaction.followup.send(
            "⚠️ A compra foi registrada, mas ocorreu um erro "
            "ao adicionar o cargo.",
            ephemeral=True
        )

        return

   

    pontos_restantes = resultado["remaining_points"]

    await interaction.followup.send(
        (
            "<:532883cash:1541463231699226695> "
            f"**Compra realizada com sucesso!**\n\n"
            f"🩸 Cargo: **{nome_item}**\n"
            f"⏱️ Duração: **{formatar_duracao(resultado['duration_seconds'])}**\n"
            f"💰 Pontos restantes: **{pontos_restantes}**"
        ),
        ephemeral=True
    )


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