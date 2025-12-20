import imaplib
import os
from dotenv import load_dotenv
from email_reader.parseEmail import parse_email
from email_reader.model import EmailMessage

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

def fetch_latest_email() -> EmailMessage | None:
    imap = imaplib.IMAP4_SSL(IMAP_SERVER)
    imap.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    imap.select("INBOX")

    status, data = imap.uid("search", None, "ALL")
    uids = data[0].split()

    if not uids:
        imap.logout()
        return None

    latest_uid = uids[-1].decode()  # UID is bytes
    status, data = imap.uid("fetch", latest_uid, "(RFC822)")

    imap.close()
    imap.logout()

    return parse_email(
        raw_bytes=data[0][1],
        uid=int(latest_uid)
    )