from database.connection import Conexion
from models.eventsModel import Salida
from models.usersModel import Usuario, UsuarioLogin, Token, UsuarioSalida
from fastapi import status,HTTPException
from security.hash_password import PaswordHash
from sqlmodel import select
from security.jwt_handler import create_access_token
class UsuarioDAO:
    def __init__(self,conexion:Conexion):
        self.conexion=conexion
    def agregar(self,user:Usuario):
        salida=Salida(estatus=False,mensaje="")
        try:
            hp = PaswordHash()
            password=hp.create_hash(user.password)
            user.password = password
            self.conexion.get_session().add(user)
            self.conexion.get_session().commit()
            self.conexion.cerrar()
            salida.estatus=True
            salida.mensaje="Usuario creado con exito."
        except Exception as ex:
            print(f"Error:{ex}")
            salida.mensaje="Error al crear el usuario, contacta al administrador."
        return salida
    def login(self,userLogin:UsuarioLogin):
        salida=UsuarioSalida(estatus=False, mensaje="", usuarios=None)
        try:
            hp=PaswordHash()
            statement=select(Usuario).where(Usuario.email==userLogin.email)
            user=self.conexion.get_session().exec(statement).first()
            if user:
                if user.estatus and hp.verify_hash(userLogin.password,user.password):
                    salida.estatus=True
                    salida.mensaje="Usuario autenticado"
                    salida.usuario=user
                else:
                    salida.mensaje="Datos incorrectos"
            else:
                salida.mensaje="Usuario no encontrado"
        except Exception as ex:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                    detail=ex)
        return salida
    def getUser(self,email,password):
        try:
            statement=select(Usuario).where(Usuario.email==email)
            user=self.conexion.get_session().exec(statement).first()
            if user:
                hp=PaswordHash()
                if hp.verify_hash(password,user.password) and user.estatus:
                    return user
            else:
                return False
        except Exception as ex:
            print(f"Error:{ex}")
        return None
    def autenticate(self,login:UsuarioLogin):
        salida=Token(access_token="",token_type="")
        try:
            user=self.getUser(login.email,login.password)
            if user:
                token=create_access_token(user.json())
                salida.access_token=token
                salida.token_type="Bearer"
        except Exception as ex:
            print(f"Error:{ex}")
        return salida