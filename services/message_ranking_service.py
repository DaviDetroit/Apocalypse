import math
from datetime import date, timedelta

from database.connection import get_pool
from config.constants import (
    BASE_REWARDS,
    MAX_REWARDS
)



class MessageRankingService:

    @staticmethod
    def get_week_reference():

        today = date.today()

        # Domingo = 6
        days_since_sunday = (today.weekday() + 1) % 7

        return today - timedelta(days=days_since_sunday)

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

        week_reference = (
            MessageRankingService.get_week_reference()
        )

        pool = get_pool()

        results = []

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    SELECT id
                    FROM weekly_message_reward_runs
                    WHERE week_reference = %s
                    """,
                    (
                        week_reference,
                    )
                )

                already_rewarded = await cursor.fetchone()

                if already_rewarded:
                    return {
                        "success": False,
                        "error": "already_rewarded"
                    }

                # Busca o ranking
                ranking = await MessageRankingService.get_weekly_ranking()

                if not ranking:
                    return {
                        "success": False,
                        "error": "empty_ranking"
                    }

                # Registra a execução antes da premiação
                await cursor.execute(
                    """
                    INSERT INTO weekly_message_reward_runs (
                        week_reference
                    )
                    VALUES (%s)
                    """,
                    (
                        week_reference,
                    )
                )

                # Premia o Top 5
                for position, row in enumerate(
                    ranking,
                    start=1
                ):

                    discord_author_id = row[0]
                    total_messages = row[1]

                    base_reward = BASE_REWARDS.get(
                        position,
                        0
                    )

                    max_reward = MAX_REWARDS.get(
                        position,
                        base_reward
                    )

                    reward = min(
                        max_reward,
                        base_reward + int(
                            math.sqrt(total_messages) * 2
                        )
                    )

                    # Adiciona as pesetas
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

        return {
            "success": True,
            "week_reference": week_reference,
            "ranking": results
        }