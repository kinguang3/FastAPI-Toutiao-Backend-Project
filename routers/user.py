from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_database
from schemas.user import UserRequest







router = APIRouter(prefix="/api/user",tags=["user"])

@router.post("/register")
async def register(user: UserRequest, db: AsyncSession = Depends(get_database)):
    return {"username": user.username, "password": user.password}