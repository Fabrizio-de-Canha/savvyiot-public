from typing import List, Optional, Dict
import uuid
from datetime import datetime

from schemas.base import BaseModel

class MessagesResponse(BaseModel):
    device_mac: str
    tenant: str
    value_type:  Optional[str]
    value: float
    message_timestamp: Optional[datetime]

class MessageQuery(BaseModel):
    device_mac: str
    value_type:  Optional[str]
    limit: int