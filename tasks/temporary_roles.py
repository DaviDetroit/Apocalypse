import discord
from discord.ext import tasks, commands

from database.connection import get_pool
from utils.logger import setup_logger


logger = setup_logger()


class TemporaryRolesTask(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_expired_roles.start()

    def cog_unload(self):
        self.check_expired_roles.cancel()

    @tasks.loop(minutes=1)
    async def check_expired_roles(self):

        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    SELECT
                        id,
                        discord_id,
                        discord_role_id,
                        name
                    FROM vw_expired_temporary_roles
                    """
                )

                expired_roles = await cursor.fetchall()

                for (
                    temporary_role_id,
                    discord_id,
                    discord_role_id,
                    role_name
                ) in expired_roles:

                    try:
                        discord_id = int(discord_id)
                        discord_role_id = int(discord_role_id)

                        member = None
                        guild = None

                        # Procura o usuário no servidor
                        for current_guild in self.bot.guilds:

                            try:
                                member = await current_guild.fetch_member(
                                    discord_id
                                )

                                guild = current_guild
                                break

                            except discord.NotFound:
                                continue

                        if member is None:
                            logger.warning(
                                "Usuário %s não encontrado nos servidores.",
                                discord_id
                            )

                            continue

                        role = guild.get_role(discord_role_id)

                        if role is None:
                            logger.warning(
                                "Cargo %s não encontrado no servidor.",
                                discord_role_id
                            )

                            continue

                        # Remove o cargo
                        if role in member.roles:

                            await member.remove_roles(
                                role,
                                reason="Cargo temporário expirado"
                            )

                            logger.info(
                                "Cargo %s removido de %s.",
                                role_name,
                                member
                            )

                        # Envia DM
                        try:

                            await member.send(
                                f"⏱<:11639rebeccasalute:1540797532354125975> Seu cargo **{role_name}** "
                                f"expirou e foi removido."
                            )

                        except discord.Forbidden:

                            logger.warning(
                                "Não foi possível enviar DM para %s.",
                                discord_id
                            )

                        # Remove do banco
                        await cursor.execute(
                            """
                            CALL sp_remove_temporary_role_by_id(%s)
                            """,
                            (temporary_role_id,)
                        )

                        while await cursor.nextset():
                            pass

                    except discord.Forbidden:

                        logger.warning(
                            "Sem permissão para acessar o usuário %s.",
                            discord_id
                        )

                    except Exception:

                        logger.exception(
                            "Erro ao processar cargo temporário %s.",
                            temporary_role_id
                        )

                await conn.commit()

    @check_expired_roles.before_loop
    async def before_check_expired_roles(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(
        TemporaryRolesTask(bot)
    )