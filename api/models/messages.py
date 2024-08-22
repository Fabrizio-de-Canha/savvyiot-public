from db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, text, Float, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB, UUID, BYTEA
from sqlalchemy.sql import func
from uuid import uuid4

class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    device_mac = Column('device_mac', Text)
    tenant = Column('tenant', Text)
    timestamp = Column('timestamp', TIMESTAMP(), nullable=False)
    message = Column('message', JSONB)
    time_received = Column('time_received', DateTime(), server_default=func.now())
    