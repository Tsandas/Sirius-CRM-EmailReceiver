from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class EmailMessage:
    uid: int
    message_id: str
    sender: str
    subject: str
    body: str
    received_at: Optional[datetime]
