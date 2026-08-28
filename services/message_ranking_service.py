from database.connection import get_pool

from config.constants import REWARDS_WEEK


class MessageRankingService:

    @staticmethod
    async def get_weekly_ranking():

        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    CALL sp_get_weekly_message_ranking()
                    """
                )

                ranking = await cursor.fetchall()

                while await cursor.nextset():
                    pass

                return ranking

    @staticmethod
    async def reward_ranking():

        ranking = await MessageRankingService.get_weekly_ranking()

        pool = get_pool()

        results = []

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                for position, row in enumerate(ranking, start=1):

                    discord_author_id = row[0]
                    total_messages = row[1]

                    reward = REWARDS_WEEK.get(position, 0)

                    await cursor.execute(
                        """
                        UPDATE users
                        SET points = points + %s
                        WHERE discord_id = %s
                        """,
                        (
                            reward,
                            str(discord_author_id)
                        )
                    )

                    await cursor.execute(
                        """
                        INSERT INTO weekly_message_rewards (
                            discord_author_id,
                            position,
                            messages_count,
                            reward_points
                        )
                        VALUES (%s, %s, %s, %s)
                        """,
                        (
                            str(discord_author_id),
                            position,
                            total_messages,
                            reward
                        )
                    )

                    results.append({
                        "position": position,
                        "discord_id": discord_author_id,
                        "messages": total_messages,
                        "reward": reward
                    })

                await conn.commit()

        return results