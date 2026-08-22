from database.connection import get_pool


async def process_evaluation(
    message_id: int,
    author_discord_id: int,
    evaluator_discord_id: int,
    points: int,
) -> bool:

    if author_discord_id == evaluator_discord_id:
        return False

    pool = get_pool()

    async with pool.acquire() as connection:
        try:
            async with connection.cursor() as cursor:

                await cursor.execute(
                    """
                    CALL ensure_evaluation_users(%s, %s)
                    """,
                    (
                        str(author_discord_id),
                        str(evaluator_discord_id),
                    ),
                )

                while await cursor.nextset():
                    pass

                await cursor.execute(
                    """
                    SELECT id, discord_id
                    FROM users
                    WHERE discord_id IN (%s, %s)
                    FOR UPDATE
                    """,
                    (
                        str(author_discord_id),
                        str(evaluator_discord_id),
                    ),
                )

                rows = await cursor.fetchall()

                users = {
                    int(discord_id): user_id
                    for user_id, discord_id in rows
                }

                if author_discord_id not in users:
                    raise ValueError(
                        f"Autor não encontrado: {author_discord_id}"
                    )

                if evaluator_discord_id not in users:
                    raise ValueError(
                        f"Avaliador não encontrado: {evaluator_discord_id}"
                    )

                author_id = users[author_discord_id]
                evaluator_id = users[evaluator_discord_id]

                await cursor.execute(
                    """
                    SELECT 1
                    FROM evaluations
                    WHERE message_id = %s
                    AND evaluator_id = %s
                    LIMIT 1
                    """,
                    (
                        message_id,
                        evaluator_id,
                    ),
                )

                if await cursor.fetchone() is not None:
                    return False

                await cursor.execute(
                    """
                    CALL create_evaluation(%s, %s, %s, %s)
                    """,
                    (
                        message_id,
                        author_id,
                        evaluator_id,
                        points,
                    ),
                )

                
                while await cursor.nextset():
                    pass

                await cursor.execute(
                    """
                    CALL add_user_points(%s, %s)
                    """,
                    (
                        author_id,
                        points,
                    ),
                )

                # Consome os resultados da segunda procedure
                while await cursor.nextset():
                    pass

            await connection.commit()

            return True

        except Exception:
            await connection.rollback()
            raise


async def count_daily_evaluations(
    author_discord_id: int,
) -> int:

    pool = get_pool()

    async with pool.acquire() as connection:
        async with connection.cursor() as cursor:

            await cursor.execute(
                """
                SELECT COUNT(*)
                FROM evaluations e
                INNER JOIN users u
                    ON u.id = e.author_id
                WHERE u.discord_id = %s
                AND e.created_at >= CURDATE()
                """,
                (
                    str(author_discord_id),
                ),
            )

            result = await cursor.fetchone()

            return result[0] if result else 0