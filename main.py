from fastapi import FastAPI
from routers import productos # busco donde esta el router productos
from routers import users     # busco donde esta el router users 
from routers import basic_auth_users
from routers import jwt_auth_users
from routers import users_db
from fastapi.staticfiles import StaticFiles # importacion para trabajar con recursos estaticos

app = FastAPI()

# Routers
app.include_router(productos.router) #importo productos router 
app.include_router(users.router) #importo users router
app.include_router(basic_auth_users.router) #importo basic_auth_users router
app.include_router(jwt_auth_users.router) #importo jwt_auth_users router
app.include_router(users_db.router)

# para un recurso estatico se pone primero el path, directorio de la carpeta y el nombre del path
app.mount("/static", StaticFiles(directory="static_images"), name= "static" ) #http://127.0.0.1:8000/static/che.jpg

#inicia el server: uvicorn main:app --reload
#salir del server: Ctrl + C

#url local: http://127.0.0.1:8000
@app.get("/")
async def raiz_servidor():
    return "HOLA MUNDO BACKEND"

#url local: http://127.0.0.1:8000/url
@app.get("/url")
async def url():
    return {"url_curso":"https://mouredev.com/python"}

#Documentacion de Swagger: http://127.0.0.1:8000/docs
#Documentacion de Redocly: http://127.0.0.1:8000/redoc







