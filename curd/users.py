# 根据用户名查询数据库用户
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.users import User
from routers import user
from utils.security import get_hash_possword
from schemas.user import UserRequest
from models.users import UserToken
import uuid
from datetime import datetime, timedelta



# 根据用户名查询数据库
async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()  # 用户一般只有一条


# 创建用户功能
async def create_user(db: AsyncSession, user: UserRequest):
    # 先密码加密(下载哈希密码库)->再commit
    #运行不了可能是因为哈希密码库版本过高->pip install passlib[bcrypt]
    hash_pwd = get_hash_possword(user.password)
    new_user = User(username=user.username, password=hash_pwd)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)  # 拓展:返回数据库中的最新的用户信息
    return new_user


#生成token
async def create_token(db: AsyncSession, user_id: int, token: str, expires_at: datetime):
    #生成Token + 设置过期时间 -> 查询数据库是否存在该token -> 如果存在,返回错误信息 -> 如果不存在,创建token
    # 生成一个全局唯一的随机字符串作为用户登录凭证（token）
    token = str(uuid.uuid4())
    #timedelta(days=7)表示时间长度
    expires_at = datetime.now() + timedelta(days=7)#设置过期时间为7天后
    query = select(UserToken).where(UserToken.user_id == user_id)#通过user_id查询是否存在该token
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()
    if user_token: 
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)#添加到数据库
    await db.commit()
    db.refresh(user_token)#刷新数据库中的user_token
    return token
