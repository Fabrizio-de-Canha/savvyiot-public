from db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, text, Float
from sqlalchemy.dialects.postgresql import JSONB, UUID, BYTEA
from sqlalchemy.sql import func
from uuid import uuid4

class Device(Base):
    __tablename__ = "devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    mac_id = Column('mac_id', Text, index=True)
    active = Column('active', Boolean, server_default=text("false"))
    name = Column('name', Text)
    last_reported = Column('last_reported', DateTime())
    created_on = Column('created_on', DateTime(), server_default=func.now())
    device_type = Column('device_type', Text)