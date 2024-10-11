import models
from deps import get_session

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from endpoints.authenticate import get_admin_header, get_token_header, hash_password
from schemas.auth.user import UserBase, ForgottenPasswordBase, AddUserBase
from random import randbytes
import hashlib
from datetime import datetime
from sqlalchemy.orm import Session, Query

router = APIRouter()

@router.get("")
def read_users(
    user_id: str = Depends(get_admin_header),
    db: Session = Depends(get_session),
) -> list[UserBase]:
    """
    Retrieve users.
    """

    results = db.query(models.User).all()
    users: list[UserBase] = [UserBase.from_orm(user) for user in results]
    return users


@router.post("")
def add_new_user(
    input: AddUserBase,
    # user_id: str = Depends(get_admin_header),
    db: Session = Depends(get_session),
):
    existingUser: models.User = db.query(models.User).filter(models.User.email == input.email).first()
    if not existingUser:
        hashed_password = hash_password(input.password)
        user: models.User = models.User(email=input.email, password=hashed_password.decode('utf-8'))
        try:
            db.add(user)
            db.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=e)
    else:
        raise HTTPException(status_code=404, detail="User already exists")

    return {'status': 'success', 'message': 'User added'}

@router.delete("/{id}")
def delete_user_by_id(
    id: str,
    user_id: str = Depends(get_admin_header),
    db: Session = Depends(get_session),
):
    query_object: Query = db.query(models.User).filter(models.User.id == id)
    user = query_object.first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query_object.delete()
    db.commit()

    return {'status': 'success', 'message': 'User deleted'}