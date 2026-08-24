import os

import aiomysql
from dotenv import load_dotenv

from utils.logger import setup_logger


load_dotenv()

logger = setup_logger()

_pool = None


async def init_database():
    global _pool

    _pool = await aiomysql.create_pool(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        minsize=1,
        maxsize=5,
        autocommit=False,
        charset="utf8mb4",
    )

    logger.info("Pool MySQL conectado")


def get_pool():
    if _pool is None:
        raise RuntimeError(
            "Pool do MySQL ainda não foi inicializado."
        )

    return _pool


async def close_database():
    global _pool

    if _pool is not None:
        _pool.close()
        await _pool.wait_closed()

        _pool = None

        logger.info("Pool MySQL encerrado")