
from pydantic import BaseModel


class User(BaseModel):
    id: str | None #El none hace que puede que el id no llegue, cuando se introduce un user
    username: str
    email: str
    