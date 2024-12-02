#para trabajar como una sola api
#from fastapi import FastAPI, HTTPException 
#para trabajar como router
from fastapi import APIRouter, HTTPException
#

from pydantic import BaseModel

# como API
# app = FastAPI()

# como Router
router = APIRouter()

#inicia el server: uvicorn users:app --reload
#salir del server: Ctrl + C

#url local: http://127.0.0.1:8000

######################### ESTO ES LO QUE SERIA UN GET DE USUARIOS DE LA BASE DE DATOS ###########################

# crear entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

#Users base de datos imaginaria
users_list = [User(id=1,name="Eddy",surname= "Hernandez", url= "https://moure.dev",age= "28"),
              User(id=2,name= "Endry",surname= "Manuel",url= "https://Endry.dev",age= "25"),
              User(id=3,name= "Rocky",surname= "Starr",url=  "https://Drimio.dev",age= "28")]

@router.get("/users_json")
async def users_json():
    return [{"name":"Eddy", "surname": "Hernandez", "url": "https://moure.dev", "age":"28"},
            {"name":"Endry", "surname": "Engeneering", "url": "https://Endry.dev", "age": "25"},
            {"name":"Rocky", "surname": "Starr", "url": "https://Drimio.dev", "age":"28"}]

#para api
#@app.get("/users")
#async def users():
   # return users_list

@router.get("/users")
async def users():
    return users_list

##parametros del path
@router.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id == id ,users_list) #Filter busca el id en users_list
    try:                                                      #Tratar para no obtener errores
        return list(users)[0]                                    # Obtiene el id pedido 
    except:
        return {"error":"No se ha encontrado el usuario"}        #Mensaje de error

## uso del query
## http://127.0.0.1:8000/userquery/?id=1 para buscar usuario



### uso de post    (Trabajo con el JSON de body en Thunder Client)
@router.post("/user/", response_model= User, status_code=201)  ## Http response status code por defecto 201, response model es para la documentacion
async def user(user: User):
    if type(search_user(user.id)) == User:   #TYPE se utiliza porque se comparan tipos de objetos
        raise HTTPException(status_code=404, detail="El usuario ya existe") ##raise te interrumpe la ejecucion con el error status code 404
        return {"error":"El usuario existe"}
    else:
        users_list.append(user)              #append: añade un objeto al final de la lista
        return  user              


### uso del put #### vamos a actualizar el usuario completo
@router.put("/user/") 
async def user(user: User):
    
    found = False


    for index,saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index,saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]  # del: comando que elimina
            found = True
            return {"Se elimino el usuario"}
    
    if not found:
        return {"No se encontro el usuario"}

    

                 
    

def search_user(id: int):
    users = filter(lambda user: user.id == id ,users_list) #Filter busca el id en users_list
    try:                                                      #Tratar para no obtener errores
        return list(users)[0]                                    # Obtiene el id pedido 
    except:
        return {"error":"No se ha encontrado el usuario"}

