from sqlmodel import Session, create_engine
from sqlalchemy import URL
from dotenv import load_dotenv
import os
load_dotenv()
class Conexion:
   def __init__(self):
      self.DATABASE_URL = URL.create(
         drivername="mysql+pymysql",
         username=os.getenv("DB_USER"),
         password=os.getenv("DB_PASSWORD"),
         host=os.getenv("DB_HOST", "db"),
         port=int(os.getenv("DB_PORT", 3306)),
         database=os.getenv("DB_NAME")
      )
      print(self.DATABASE_URL)
      self.engine=create_engine(self.DATABASE_URL,pool_pre_ping=True)
      self.session=Session(self.engine)
   def get_session(self) -> Session:
      return  self.session
   def cerrar(self):
      self.session.close()

def getConexion()->Conexion:
   conexion=Conexion()
   return conexion