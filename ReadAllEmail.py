import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime


def lambda_handler(event, context):
    currentTime = datetime.now()
    print("Hello World! It's currently " + str(currentTime))


email_address = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")
imap_server = "imap.gmail.com"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_address, password)

imap.select("Inbox")

_, msgnums = imap.search(None, "ALL")
msg_ids = msgnums[0].split()

if msg_ids:
    latest_msg_id = msg_ids[-1]
    _, data = imap.fetch(latest_msg_id, "(RFC822)")
    message = email.message_from_bytes(data[0][1])

    subject, encoding = decode_header(message.get("Subject"))[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")

    sender = message.get("From")
    date = message.get("Date")

    body = ""
    for part in message.walk():
        if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition")):
            charset = part.get_content_charset() or "utf-8"
            body = part.get_payload(decode=True).decode(charset, errors="replace")
            break

    print(f"From: {sender}")
    print(f"Date: {date}")
    print(f"Subject: {subject}")
    print("\nContent:\n")
    print(body.strip())

else:
    print("No messages found.")

imap.close()
imap.logout()
