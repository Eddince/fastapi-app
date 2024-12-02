from pymongo import MongoClient

#base de datos local#
#db_client = MongoClient().local #si esta vacio la url es en el local host

#base de datos en servidor internacional o remota#
db_client = MongoClient(
    "mongodb+srv://EddyHernandez:Rock@cluster0.mxtjd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    ).base_datos




