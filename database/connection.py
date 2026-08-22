import os

import mysql.connector
from mysql.connector import pooling


db_pool = pooling.MySQLConnectionPool(
    pool_name="apocalypse_pool",
    pool_size=5,
    pool_reset_session=True,

    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

def get_connection():
    return db_pool.get_connection()