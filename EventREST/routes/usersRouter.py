from fastapi import APIRouter,Depends
from fastapi.security import OAuth2PasswordRequestForm
#from fastapi.security import HTTPBasic,HTTPBasicCredentials
from database.connection import Conexion,getConexion
from database.userDAO import UsuarioDAO
from models.usersModel import Usuario, UsuarioLogin,Token,UsuarioSalida

usuariosRouter=APIRouter(prefix="/usuarios",tags=["Usuarios"])
@usuariosRouter.post("")
def agregar(user:Usuario,conexion:Conexion=Depends(getConexion)):
    dao=UsuarioDAO(conexion)
    return dao.agregar(user)
@usuariosRouter.post("/login",response_model=UsuarioSalida)
def login(user:UsuarioLogin,conexion:Conexion=Depends(getConexion))->UsuarioSalida:
    dao=UsuarioDAO(conexion)
    return dao.login(user)

@usuariosRouter.post('/token',response_model=Token)
def login_token(credenciales:OAuth2PasswordRequestForm=Depends())->Token:
    conexion=Conexion()
    userLogin=UsuarioLogin(email=credenciales.username,password=credenciales.password)
    usuarioDAO = UsuarioDAO(conexion)
    token=usuarioDAO.autenticate(userLogin)
    return token
