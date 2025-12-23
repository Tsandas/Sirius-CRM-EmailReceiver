from db.postgres import get_conn, release_conn

def find_last_email_in_db():
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT *
                FROM emails
                ORDER BY uid DESC
                LIMIT 1
            """)
            row = cur.fetchone()
            return row
    finally:
        release_conn(conn)
