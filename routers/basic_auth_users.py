from fastapi import FastAPI, HTTPException # depends es para el trabajo con datos y autorizacion
from fastapi import Depends
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  #modulo de autenticacion, el segundo es para capturarusuario y password


#inicia el server: uvicorn basic_auth_users:app --reload
#url local: http://127.0.0.1:8000

#app = FastAPI()
router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")  #criterio de autenticacion


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "eddy": {
        "username": "eddy",
        "full_name": "Eddy Hdez",
        "email": "eddy@gmail.com" ,
        "disabled": False,
        "password": "123456"
    },
    "eddy2": {
        "username": "eddy2",
        "full_name": "Eddy castro",
        "email": "eddy@gmail.com" ,
        "disabled": True,
        "password": "654321"
    }
}


def search_userdb(username: str): #operacion para buscar el usuario en la base de datos
    if username in users_db:
        return UserDB(**users_db[username])
    
#como podemos transfomar el usuario de base de datos a tipo usuario
def search_user(username: str): 
    if username in users_db:
        return User(**users_db[username])


async def current_user(token:str = Depends(oauth2)): #criterio de dependencia
    user = search_user(token)              # el token es el que se devuelve en el login, y se pone en Auth/bearer Token porque es de tipo bearer, todo en thunder client
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales de autenticacion invalida", headers= {"WWW-Authenticate": "Bearer"})
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario inactivo")
    
    return user
    
    

@router.post("/login", status_code= 202)
async def login(form:OAuth2PasswordRequestForm = Depends()):
      user_db_1 = users_db.get(form.username)
      if not user_db_1:
          raise HTTPException(status_code=400, detail= "El usuario no existe")
      else:
          user = search_userdb(form.username)
          if form.password == user.password:
              return {"access_token": user.username,"token_type": "bearer" }
          else:
               raise HTTPException(status_code=400, detail= "Contraseña incorrecta")
      
@router.get("/users/me") #depende este get de que este autenticado el usuario
async def me(user: User = Depends(current_user)):
    return user