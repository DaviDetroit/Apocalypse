from database.connection import get_pool


class LojaService:

    @staticmethod
    async def comprar_item(
        discord_id: int,
        store_item_id: int
    ):
        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    CALL sp_purchase_store_item(%s, %s)
                    """,
                    (
                        str(discord_id),
                        store_item_id
                    )
                )

                result = await cursor.fetchone()

                if not result:
                    while await cursor.nextset():
                        pass

                    return {
                        "success": False,
                        "error": "unknown_error"
                    }

                # IMPORTANTE:
                # Pegamos description ANTES de chamar nextset()
                columns = [
                    column[0]
                    for column in cursor.description
                ]

                result = dict(
                    zip(columns, result)
                )

                # Agora podemos limpar os result sets restantes
                while await cursor.nextset():
                    pass

                if result["result"] == "USER_NOT_FOUND":
                    return {
                        "success": False,
                        "error": "user_not_found"
                    }

                if result["result"] == "ITEM_NOT_FOUND":
                    return {
                        "success": False,
                        "error": "item_not_found"
                    }

                if result["result"] == "INSUFFICIENT_POINTS":
                    return {
                        "success": False,
                        "error": "insufficient_points",
                        "points": result["current_points"],
                        "cost": result["required_points"]
                    }

                if result["result"] == "ALREADY_OWNED":
                    return {
                        "success": False,
                        "error": "already_owned"
                    }

                if result["result"] == "SUCCESS":
                    return {
                        "success": True,
                        "user_id": result["user_id"],
                        "role_id": result["role_id"],
                        "discord_role_id": result["discord_role_id"],
                        "item_name": result["item_name"],
                        "points_cost": result["points_cost"],
                        "duration_seconds": result["duration_seconds"],
                        "expires_at": result["expires_at"],
                        "remaining_points": result["remaining_points"]
                    }

                return {
                    "success": False,
                    "error": "unknown_error"
                }