from sqlalchemy import Column, Integer, String, Boolean, text, DateTime, Text
from ..auth_api.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import JSONB, UUID, BYTEA
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column('name', Text)
    active = Column('active', Boolean, server_default=text("false"))
    created_on = Column('created_on', DateTime(), server_default=func.now())