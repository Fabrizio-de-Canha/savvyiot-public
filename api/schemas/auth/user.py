from typing import List, Optional, Dict
import uuid
from datetime import datetime

from schemas.base import BaseModel

class UserBase(BaseModel):
    id: uuid.UUID
    email: str
    name:  Optional[str]
    surname:  Optional[str]
    last_login: Optional[datetime]
    login_count: Optional[int]
    created_on: Optional[datetime]
    verified: bool
    active: bool
    admin: bool
    super_user: bool

class ForgottenPasswordBase(BaseModel):
    email: str

class AddUserBase(BaseModel):
    email: str
    password: str

class LoginBase(BaseModel):
    email: str
    password: str