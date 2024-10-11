from db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, NUMERIC, DateTime, Boolean, ForeignKey, text, Float
from sqlalchemy.dialects.postgresql import JSONB, UUID, BYTEA
from sqlalchemy.sql import func
from uuid import uuid4

class Device(Base):
    __tablename__ = "devices"

    mac_id = Column('mac_id', Text, primary_key=True, index=True, unique=True)
    tenant = Column('tenant', Text)
    active = Column('active', Boolean, server_default=text("false"))
    name = Column('name', Text)
    rssi = Column('rssi', Integer)
    firmware_version = Column('firmware_version', NUMERIC)
    last_reported = Column('last_reported', DateTime())
    last_firmware_upgrade = Column('last_firmware_upgrade', DateTime())
    last_booted = Column('last_booted', DateTime())
    created_on = Column('created_on', DateTime(), server_default=func.now())
    device_type = Column('device_type', Text)