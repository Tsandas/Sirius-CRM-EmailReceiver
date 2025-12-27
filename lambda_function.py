from email_reader.emailReader import fetch_and_push_new_emails

def lambda_handler(event, context):
    emails = fetch_and_push_new_emails()
    return {
        "statusCode": 200,
        "body": f"Fetched {len(emails)} emails"
    }
