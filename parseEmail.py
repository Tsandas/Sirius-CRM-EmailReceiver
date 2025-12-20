import email
from email.header import decode_header
from model import EmailMessage

def parse_email(raw_bytes: bytes, uid: int) -> EmailMessage:
    msg = email.message_from_bytes(raw_bytes)

    subject, encoding = decode_header(msg.get("Subject", ""))[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="replace")

    sender = msg.get("From", "")

    date_raw = msg.get("Date")
    received_at = None
    if date_raw:
        try:
            received_at = email.utils.parsedate_to_datetime(date_raw)
        except Exception:
            pass

    body = ""
    for part in msg.walk():
        if part.get_content_type() == "text/plain" and not part.get_filename():
            charset = part.get_content_charset() or "utf-8"
            body = part.get_payload(decode=True).decode(charset, errors="replace")
            break

    return EmailMessage(
        uid=uid,
        message_id=msg.get("Message-ID", ""),
        sender=sender,
        subject=subject,
        body=body.strip(),
        received_at=received_at
    )
