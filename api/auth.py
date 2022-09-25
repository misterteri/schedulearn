import jwt
from pydantic import EmailStr, BaseModel
from config import SECRET
from fastapi import HTTPException
from starlette.responses import JSONResponse
from datetime import datetime, timedelta
from passlib.context import CryptContext

from dotenv import load_dotenv
load_dotenv('.env')

class NewUser(BaseModel):
    email: EmailStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encode_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload['email']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")