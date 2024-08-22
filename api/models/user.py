from db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, DateTime, Boolean, ForeignKey, text, Float
from sqlalchemy.dialects.postgresql import JSONB, UUID, BYTEA
from sqlalchemy.sql import func
from uuid import uuid4

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    verified = Column('verified', Boolean, server_default=text("false"))
    active = Column('active', Boolean, server_default=text("false"))
    admin = Column('admin', Boolean, server_default=text("false"))
    super_user = Column('super_user', Boolean, server_default=text("false"))
    email = Column('email', Text, unique=True)
    name = Column('name', Text)
    surname = Column('surname', Text)
    password = Column('password', Text, nullable=True)
    last_login = Column('last_login', DateTime())
    password_reset = Column('password_reset', DateTime())
    login_count = Column('login_count', Integer)
    created_on = Column('created_on', DateTime(), server_default=func.now())