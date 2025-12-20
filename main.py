from db.repository import find_last_email_in_db
from email_reader.emailReader import fetch_latest_email

email_obj = fetch_latest_email()

if not email_obj:
    print("No messages found.")
else:
    find_last_email_in_db()
    print(f"\n")
    print(f"UID: {email_obj.uid}")
    print(f"ID: {email_obj.message_id}")
    print(f"From: {email_obj.sender}")
    print(f"Date: {email_obj.received_at}")
    print(f"Subject: {email_obj.subject}")
    print("Content:")
    print(email_obj.body)
