from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ...models import user as UserModel
from ...schemas import user as UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str):
    return db.query(UserModel.User).filter(UserModel.User.username == username).first()

def create_user(db: Session, user: UserSchema.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserModel.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user