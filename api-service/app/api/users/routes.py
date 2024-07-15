from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from .dto import PublicUser
from app.services.user_service import UserService

router = APIRouter(prefix="/users/v1")

def get_user_service(req: Request) -> UserService:
    return req.app.state.user_service

####################
## Create

class CreateUserRequest(BaseModel):
    name: str

@router.post("", response_model=PublicUser)
async def create_user(data: CreateUserRequest, user_service: UserService = Depends(get_user_service)):
    user_entity = await user_service.create_user(data.name)
    
    return PublicUser(id=user_entity.id, name=user_entity.name)

####################
## Get Many

@router.get("", response_model=List[PublicUser])
async def get_users(user_service: UserService = Depends(get_user_service)):
    user_entities = await user_service.get_users()

    return [PublicUser(id=user.id, name=user.name) for user in user_entities]
    
####################
## Get One

@router.get("/{id}", response_model=PublicUser)
async def get_user(id: int, user_service: UserService = Depends(get_user_service)):
    user_entity = await user_service.get_user(id)
    if user_entity is None:
        raise HTTPException(status_code=404, detail="User not found")

    return PublicUser(id=user_entity.id, name=user_entity.name)
