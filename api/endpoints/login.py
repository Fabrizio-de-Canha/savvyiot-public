import models
from deps import get_session

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from endpoints.authenticate import verify_password, create_jwt_token
from schemas.auth.user import LoginBase

router = APIRouter()

@router.post("")
def login(
    credentials: LoginBase,
    db: Session = Depends(get_session)
    ):
    """
    Check user credentials and insert jwt token in cookies
    """
    user: models.User = db.query(models.User).filter(models.User.email == credentials.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Incorrect password")
    
    token = create_jwt_token(str(user.id), user.admin, user.super_user)
    return {"access_token": token, "userId": user.id, "email": user.email}