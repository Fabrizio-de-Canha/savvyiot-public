from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import engine, Base
from ..models import user
from ..schemas import user as UserSchema
from . import auth, database

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=UserSchema.Token)
def login_for_access_token(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # type: ignore
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}