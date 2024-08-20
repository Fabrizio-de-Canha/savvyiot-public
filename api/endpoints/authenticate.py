import bcrypt
from datetime import datetime, timedelta
from jose import jwt
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Header, HTTPException, Depends
from typing import Optional

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Serialize the private key to a PEM-encoded string
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize the public key to a PEM-encoded string
pem_public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

JWT_ALGORITHM = "RS256"
JWT_EXPIRATION_TIME_MINUTES = 30

# Load the private key from the PEM-encoded string
private_key = serialization.load_pem_private_key(
    pem_private_key,
    password=None,
)

# Load the public key from the PEM-encoded string
public_key = serialization.load_pem_public_key(pem_public_key)

def hash_password(password: str):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password.encode('utf-8'))


def create_jwt_token(user_id: str, admin: bool, superuser: bool):
    expire = datetime.now() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    to_encode = {"sub": user_id, "exp": expire, "admin": admin, "superuser":superuser}
    encoded_jwt = jwt.encode(to_encode, pem_private_key, algorithm=JWT_ALGORITHM)
    return encoded_jwt

async def get_token_header(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    try:
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, pem_public_key, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id

async def get_admin_header(authorization: Optional[str] = Header(None), user_id: str = Depends(get_token_header)):
    try:
        token = authorization.split("Bearer ")[1]
        print(token)
        payload = jwt.decode(token, pem_public_key, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        admin = payload.get("admin")
        print(admin)
        if not admin:
            raise HTTPException(status_code=403, detail="User doesn't have admin roles")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id
    
async def get_superuser_header(authorization: Optional[str] = Header(None), user_id: str = Depends(get_token_header)):
    try:
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, pem_public_key, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        admin = payload.get("superuser")
        if not admin:
            raise HTTPException(status_code=403, detail="User doesn't have superuser roles")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_id