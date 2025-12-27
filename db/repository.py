from db.postgres import get_conn, release_conn
from email_reader.model import EmailMessage

def find_last_email_in_db():
    conn = get_conn()
    try:
        row = conn.run(
            """
            SELECT *
            FROM emails
            ORDER BY uid DESC
            LIMIT 1
            """
        )
        print(row)
        return row[0] if row else None
    finally:
        release_conn(conn)

def insert_emails_to_db(emails: list[EmailMessage]) -> None:
    if not emails:
        return

    conn = get_conn()
    try:
        for e in emails:
            conn.run(
                """
                INSERT INTO emails (
                    uid,
                    message_id,
                    sender,
                    subject,
                    body,
                    received_at
                )
                VALUES (:uid, :message_id, :sender, :subject, :body, :received_at)
                """,
                uid=e.uid,
                message_id=e.message_id,
                sender=e.sender,
                subject=e.subject,
                body=e.body,
                received_at=e.received_at
            )
    finally:
        release_conn(conn)