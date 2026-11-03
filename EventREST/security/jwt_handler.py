from datetime import datetime
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException,status
from models.usersModel import Usuario
from dotenv import load_dotenv
import time
import os
def create_access_token(user:Usuario):
    load_dotenv()
    secret_key=os.getenv("SECRET_KEY")
    algorithm=os.getenv("ALGORITHM")
    timeExp=int(os.getenv("TIME"))
    payload={
        "user":user,
        "expire":time.time()+timeExp
    }
    token=jwt.encode(payload,secret_key,algorithm=algorithm)
    return token
def verify_access_token(token:str):
    try:
        load_dotenv()
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pueden validar las credenciales"
        )
        secret_key = os.getenv("SECRET_KEY")
        algorithm =os.getenv("ALGORITHM")
        data=jwt.decode(token,secret_key,algorithms=[algorithm])
        expire=data.get('expire')
        if expire is None:
            raise credentials_exception
        if datetime.utcnow()>datetime.utcfromtimestamp(expire):
            raise credentials_exception
        return data
    except InvalidTokenError as ex:
        raise credentials_exception


