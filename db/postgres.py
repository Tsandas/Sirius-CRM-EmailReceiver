import pg8000.native
import os

def get_conn():
    conn = pg8000.native.Connection(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DBNAME")
    )
    return conn

def release_conn(conn):
    conn.close()
