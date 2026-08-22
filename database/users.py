from database.connection import get_pool


async def get_user_by_discord_id(discord_id: int):

    pool = get_pool()

    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:

            await cursor.execute(
                """
                SELECT id, discord_id, points
                FROM users
                WHERE discord_id = %s
                """,
                (str(discord_id),)
            )

            return await cursor.fetchone()


async def add_points(
    connection,
    user_id: int,
    points: int
):

    async with connection.cursor() as cursor:

        await cursor.execute(
            """
            UPDATE users
            SET points = points + %s
            WHERE id = %s
            """,
            (
                points,
                user_id
            )
        )