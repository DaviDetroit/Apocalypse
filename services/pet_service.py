from database.connection import get_pool
from config.constants import PESETAS_PET


class PetService:

    @staticmethod
    async def criar_pet(
        discord_message_id,
        discord_author_id,
        image_url
    ):
        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                await cursor.execute(
                    """
                    INSERT INTO pets (
                        discord_message_id,
                        discord_author_id,
                        image_url
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        discord_message_id,
                        discord_author_id,
                        image_url
                    )
                )

                await conn.commit()


    @staticmethod
    async def dar_like(
        discord_message_id,
        discord_user_id
    ):
        pool = get_pool()

        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:

                # Busca o pet pela mensagem do Discord
                await cursor.execute(
                    """
                    SELECT id, discord_author_id
                    FROM pets
                    WHERE discord_message_id = %s
                    AND is_active = 1
                    """,
                    (discord_message_id,)
                )

                pet = await cursor.fetchone()

                if not pet:
                    return {
                        "success": False,
                        "error": "pet_not_found"
                    }


                pet_id = pet[0]
                owner_id = pet[1]


                # Verifica se já curtiu
                await cursor.execute(
                    """
                    SELECT id
                    FROM pet_likes
                    WHERE pet_id = %s
                    AND discord_user_id = %s
                    """,
                    (
                        pet_id,
                        discord_user_id
                    )
                )

                already_liked = await cursor.fetchone()

                if already_liked:
                    return {
                        "success": False,
                        "error": "already_liked"
                    }


                # Registra o like
                await cursor.execute(
                    """
                    INSERT INTO pet_likes (
                        pet_id,
                        discord_user_id
                    )
                    VALUES (%s, %s)
                    """,
                    (
                        pet_id,
                        discord_user_id
                    )
                )


                # Atualiza contador do pet
                await cursor.execute(
                    """
                    UPDATE pets
                    SET
                        likes_count = likes_count + 1,
                        pesetas_received = pesetas_received + %s
                    WHERE id = %s
                    """,
                    (
                        PESETAS_PET,
                        pet_id
                    )
                )


                # Dá as pesetas para o dono
                await cursor.execute(
                    """
                    UPDATE users
                    SET points = points + %s
                    WHERE discord_id = %s
                    """,
                    (
                        PESETAS_PET,
                        owner_id
                    )
                )


                await conn.commit()


                return {
                    "success": True,
                    "owner_id": owner_id,
                    "reward": PESETAS_PET
                }