import imaplib
import os
from dotenv import load_dotenv

from db.repository import find_last_email_in_db
from email_reader.parseEmail import parse_email
from email_reader.model import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = "imap.gmail.com"


def get_mailbox_max_uid(imap) -> int:
    status, data = imap.uid("search", None, "ALL")
    if status != "OK" or not data[0]:
        return 0
    return int(data[0].split()[-1])


def fetch_new_emails(start_uid: int) -> list[EmailMessage]:
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    imap.select("INBOX")

    max_uid = get_mailbox_max_uid(imap)

    if start_uid >= max_uid:
        imap.close()
        imap.logout()
        return []

    search_range = f"{start_uid + 1}:{max_uid}"
    status, data = imap.uid("search", None, search_range)

    if status != "OK" or not data[0]:
        imap.close()
        imap.logout()
        return []

    uids = [int(uid) for uid in data[0].split()]
    emails = []

    for uid in uids:
        status, msg_data = imap.uid("fetch", str(uid), "(RFC822)")
        if status != "OK":
            continue

        emails.append(
            parse_email(
                raw_bytes=msg_data[0][1],
                uid=uid
            )
        )

    imap.close()
    imap.logout()
    return emails


def get_last_uid_from_db() -> int:
    row = find_last_email_in_db()
    return row[0] if row else 0


def fetch_and_push_new_emails():
    last_uid = get_last_uid_from_db()
    ## insert to db
    return fetch_new_emails(last_uid)
