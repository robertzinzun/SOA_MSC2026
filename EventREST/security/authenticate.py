from fastapi import HTTPException,status,Depends
from fastapi.security import OAuth2PasswordBearer
import json
from models.usersModel import Usuario
from security.jwt_handler import verify_access_token

security=OAuth2PasswordBearer(tokenUrl='/usuarios/token')

async def authenticate_user(token:str=Depends(security)):
    if not token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Sin autorizacion")
    data=verify_access_token(token)
    user=Usuario(**json.loads(data.get('user')))
    return user

class RoleChecker:
    def __init__(self,roles:list):
        self.roles_permitidos=roles
    def __call__(self, usuario:Usuario=Depends(authenticate_user)):
        if usuario is None or usuario.rol not in self.roles_permitidos:
            raise HTTPException(status.HTTP_403_FORBIDDEN,detail="Sin autorizacion.")
        return usuario