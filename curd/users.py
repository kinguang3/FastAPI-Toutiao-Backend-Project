# 根据用户名查询数据库用户
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User
from utils.security import get_hash_possword
from schemas.user import UserRequest


# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()  # 用户一般只有一条


# 创建用户功能
async def create_user(db: AsyncSession, user: UserRequest):
    # 先密码加密(下载哈希密码库)->再commit
    hash_pwd = get_hash_possword(user.password)
    new_user = User(username=user.username, password=hash_pwd)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # 拓展:返回数据库中的最新的用户信息
    return new_user
