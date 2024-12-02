
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    #id: str | None #El none hace que puede que el id no llegue, cuando se introduce un user
    id: Optional[str]
    username: str
    email: str
    
