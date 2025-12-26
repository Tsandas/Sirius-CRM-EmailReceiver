from db.postgres import get_conn, release_conn
from email_reader.model import EmailMessage

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

def insert_emails_to_db(emails: list[EmailMessage]) -> None:
    if not emails:
        return

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO emails (
                    uid,
                    message_id,
                    sender,
                    subject,
                    body,
                    received_at
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    (
                        e.uid,
                        e.message_id,
                        e.sender,
                        e.subject,
                        e.body,
                        e.received_at
                    )
                    for e in emails
                ]
            )
        conn.commit()
    finally:
        release_conn(conn)
