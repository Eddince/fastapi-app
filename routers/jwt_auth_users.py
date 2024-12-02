from fastapi import FastAPI, HTTPException # depends es para el trabajo con datos y autorizacion
from fastapi import Depends
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm  #modulo de autenticacion, el segundo es para capturarusuario y password
# import jwt
from jose import jwt, JWTError
from passlib.context import CryptContext #contexto de encriptacion
from datetime import datetime, timedelta #datetime para fecha del sistema y timedelta para calcular con fecha

#inicia el server: uvicorn jwt_auth_users:app --reload
#url local: http://127.0.0.1:8000

ALGORITHM = "HS256"     #algoritmo de encriptacion
ACCESS_TOKEN_DURATION = 1 #duracion del token de autenticacion
SECRET = "bab211d51bec278ba5064737db31dfd95936b88525e0facdf681a39f3aaa1cfb" #esta forma es una especie de semilla que sola conozca el BACKEND
crypt = CryptContext(schemes=["bcrypt"])  #contexto de encriptacion

#app = FastAPI()
router = APIRouter(prefix="/jwt",
                   tags=["jwt"]
                   )

oauth2 = OAuth2PasswordBearer(tokenUrl="login_crypt")  #criterio de autenticacion


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

#la contraseña encriptada se guarda en la base de datos
users_db = {
    "eddy": {
        "username": "eddy",
        "full_name": "Eddy Hdez",
        "email": "eddy@gmail.com" ,
        "disabled": False,
        "password": "$2a$12$ZhS.QiZ1Qu5rEoXgTkWTG.ZdIEZr9GkiacwJJRboi9UmeoMqoFbGi" 
    },
    "eddy2": {
        "username": "eddy2",
        "full_name": "Eddy castro",
        "email": "eddy@gmail.com" ,
        "disabled": True,
        "password": "$2a$12$S.Drq4KjJWddbZy9vuW1.eoCwblBLOJJAsE7C9Zq6jErEqb3/poaS"
    }
}

def search_userdb(username: str): #operacion para buscar el usuario en la base de datos
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user(username: str): 
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    
    try:
      
        username = jwt.decode(token, SECRET, algorithms= ALGORITHM).get("sub") #el sub guardado en el access token del post abajo
        if username  is None:
            raise  HTTPException(status_code=401, detail="Credenciales de autenticacion invalida", headers= {"WWW-Authenticate": "Bearer"}) 
        

    except:
        JWTError
        raise HTTPException(status_code=401, detail="Credenciales de autenticacion invalida", headers= {"WWW-Authenticate": "Bearer"})

    return search_user(username)    
    

async def current_user(user: User = Depends(auth_user)): #criterio de dependencia
    if user.disabled:
         raise HTTPException(status_code=400, detail="Usuario inactivo")
    return user    

@router.post("/login_crypt", status_code= 202)
async def login_crypt(form:OAuth2PasswordRequestForm = Depends()):
      user_db_1 = users_db.get(form.username)
      if not user_db_1:
          raise HTTPException(status_code=400, detail= "El usuario no existe")
      else:
          user = search_userdb(form.username)
          
          if crypt.verify(form.password, user.password):   #verificacion de la contraseña de la form con la encriptada
              access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
              expire = datetime.utcnow() + access_token_expiration
              access_token = {"sub": user.username, "exp": expire}
              #return {"access_token": access_token,"token_type": "bearer" } #para ver el resultado del token con expiracion
              return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM) ,"token_type": "bearer" }
          else:
               raise HTTPException(status_code=400, detail= "Contraseña incorrecta")

@router.get("/users/yo") #depende este get de que este autenticado el usuario
async def me(user: User = Depends(current_user)):
    return user      
