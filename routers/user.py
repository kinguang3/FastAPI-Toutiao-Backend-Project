from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_database
from schemas.user import UserRequest
from curd.users import get_user_by_username, create_user

'''
#注册逻辑:验证用户是否存在->如果存在,返回错误信息->如果不存在,创建用户->生成token ->响应结果
'''

router = APIRouter(prefix="/api/user", tags=["user"])


#一般数据库查询都是异步操作
@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_database)):
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    #注册逻辑:验证用户是否存在->如果存在,返回错误信息->如果不存在,创建用户->生成token ->响应结果
    user = await create_user(db, user_data)
    return {"username": user.username, "password": user.password, "id": user.id}
#可能bcrypt要降等级