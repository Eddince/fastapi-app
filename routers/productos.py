from fastapi import APIRouter 
 # el tags es para agrupar el router en la documentacion a parte
router = APIRouter(prefix="/products",tags=["products"], responses= {404:{"Mensaje":"Mala mia"}}) # me mantiene la direcion inicial del router por defecto

products_list = {"Producto 1", "Producto 2", "Producto 3", "Producto 4"}

@router.get("/")
async def productos():
    return products_list

@router.get("/{id}")
async def productos(id: int):
    return products_list(id)

