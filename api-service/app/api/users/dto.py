from pydantic import BaseModel

class PublicUser(BaseModel):
  id: int
  name: str
