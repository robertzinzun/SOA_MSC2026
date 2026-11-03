from fastapi import FastAPI,Depends
from sqlmodel import Session

from routes.eventsRoute import eventsRouter
import uvicorn
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from routes.usersRouter import usuariosRouter
# imports slowapi
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler

app=FastAPI(title="MS Eventos",description="Microservicio de Eventos",root_path="/mseventos/api/v1")
app.include_router(eventsRouter,prefix="/eventos")
app.include_router(usuariosRouter)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)

security=HTTPBasic()
@app.get("/")

def home():
    return {"mensaje":"Welcome to MSEventos"}




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",host="0.0.0.0",port=8080,reload=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
