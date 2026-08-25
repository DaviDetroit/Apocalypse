from database.connection import get_pool


class UserService:

    @staticmethod
    async def get_or_create_user(
        discord_id: int,
        username: str = None
    ):

        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    SELECT id
                    FROM users
                    WHERE discord_id = %s
                    """,
                    (
                        str(discord_id),
                    )
                )

                user = await cursor.fetchone()

                if user:
                    return user[0]


                await cursor.execute(
                    """
                    INSERT INTO users (
                        discord_id,
                        username
                    )
                    VALUES (%s, %s)
                    """,
                    (
                        str(discord_id),
                        username
                    )
                )

                await conn.commit()

                return cursor.lastrowid