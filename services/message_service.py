from database.connection import get_pool


class MessageService:

    @staticmethod
    async def registrar_mensagem(
        discord_message_id: int,
        discord_author_id: int,
        guild_id: int,
        channel_id: int,
        content: str | None,
        has_attachment: bool,
        has_embed: bool
    ):

        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    CALL sp_register_message(
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        str(discord_message_id),
                        str(discord_author_id),
                        str(guild_id),
                        str(channel_id),
                        content,
                        int(has_attachment),
                        int(has_embed)
                    )
                )
                while await cursor.nextset():
                    pass

                await conn.commit()