
from fastapi import APIRouter, status, HTTPException
from db.models.user import User
from db.schemas.user import user_schema, users_all_schemas
from db.client import db_client
from bson import ObjectId #para importar un objeto con la estructura id del JSon


router = APIRouter(prefix="/userdb",
                   tags=["userdb"], 
                   responses= {status.HTTP_404_NOT_FOUND:{"Mensaje":"No encontrado"}})





@router.get("/", response_model=list[User]) #quiero una lista de todos los usuarios
async def users():
    return users_all_schemas(db_client.users.find())

@router.get("/{id}")
async def user(id: str):
    
    return search_user("_id", ObjectId(id))  # para que id tenga la estructura correcta   

    
@router.post("/", response_model= User, status_code=status.HTTP_201_CREATED)  
async def user(user: User):
   
   if type(search_user("email", user.email)) == User:   
        raise HTTPException(status_code=404, detail="El email ya existe")
   if type(search_user("username", user.username)) == User:   
        raise HTTPException(status_code=404, detail="El username ya existe") 
        
   user_dict = dict(user)  #convertir user en tipo dict que es tipo JSON
   del user_dict["id"]  #borrar el campo Id, solo inserta el username y el email
   id = db_client.users.insert_one(user_dict).inserted_id   #insertar usuario
   new_user = user_schema(db_client.users.find_one({"_id":id})) #buscar usuario
   return  User(**new_user)              


@router.put("/", response_model= User) 
async def user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
       db_client.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id)) 
    

@router.delete("/{id}")
async def user(id: str):

    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    
    
    if not found:
        return {"No se encontro el usuario"}
      else:
        return {"Se borro el usuario deseado"}

    

def search_user_email(email: str):
     
    try:                                                      
        user = user_schema (db_client.users.find_one({"email": email})) #buscar el email  
        return User(**user)                                
    except:
        return {"error":"No se ha encontrado el usuario"}

def search_user_username(username: str):
     
    try:                                                      
        user = user_schema (db_client.users.find_one({"username": username})) #buscar el email  
        return User(**user)                                
    except:
        return {"error":"No se ha encontrado el usuario"}

def search_user(field: str , key): #buscador generico
     
    try:                                                      
        user = user_schema (db_client.users.find_one({field : key})) #buscar el email  
        return User(**user)                                
    except:
        return {"error":"No se ha encontrado el usuario"}
