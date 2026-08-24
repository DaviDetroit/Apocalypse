from database.connection import get_pool


class EconomyService:

    @staticmethod
    async def transferir_pesetas(
        sender_discord_id: int,
        receiver_discord_id: int,
        amount: int
    ):

        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    CALL sp_transfer_points(%s, %s, %s)
                    """,
                    (
                        str(sender_discord_id),
                        str(receiver_discord_id),
                        amount
                    )
                )

                result = await cursor.fetchone()

                while await cursor.nextset():
                    pass

                if not result:
                    return {
                        "success": False,
                        "error": "unknown_error"
                    }

                if result[0] == "SENDER_NOT_FOUND":
                    return {
                        "success": False,
                        "error": "sender_not_found"
                    }

                if result[0] == "RECEIVER_NOT_FOUND":
                    return {
                        "success": False,
                        "error": "receiver_not_found"
                    }

                if result[0] == "SELF_TRANSFER":
                    return {
                        "success": False,
                        "error": "self_transfer"
                    }

                if result[0] == "INSUFFICIENT_POINTS":
                    return {
                        "success": False,
                        "error": "insufficient_points",
                        "points": result[1]
                    }

                if result[0] == "SUCCESS":
                    return {
                        "success": True,
                        "amount": result[1]
                    }

                return {
                    "success": False,
                    "error": "unknown_error"
                }