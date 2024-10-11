from db.session import Base
from sqlalchemy import Column, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

class Test(Base):
    __tablename__ = "test"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    verified = Column('verified', Boolean, server_default=text("false"))
    active = Column('active', Boolean, server_default=text("false"))
    admin = Column('admin', Boolean, server_default=text("false"))
