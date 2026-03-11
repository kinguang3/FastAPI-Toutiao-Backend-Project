from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_database
from schemas.user import UserRequest
from curd.users import get_user_by_username, create_user, create_user_token

'''
#注册逻辑:验证用户是否存在->如果存在,返回错误信息->如果不存在,创建用户->生成token ->响应结果
'''

router = APIRouter(prefix="/api/user", tags=["user"])


#一般数据库查询都是异步操作
#在路由中使用Depends(get_database)来获取数据库会话
@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_database)):
    existing_user = await get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    #注册逻辑:验证用户是否存在->如果存在,返回错误信息->如果不存在,创建用户->生成token ->响应结果
    user = await create_user(db, user_data)
    token = await create_user_token(db, user.id)
    return {"username": user.username, "password": user.password, "id": user.id, "token": token}
#可能bcrypt要降等级,因为默认是2a,而2b是最新的版本

'''
Token:Tocken服务器发给客户端,客户端后续请求在header中携带token,服务器验证token是否有效 
作用:解决无状态的http协议,服务器无法记住客户端的状态,每次请求都需要客户端重新登录
过程:用户登入->服务器验证用户信息->如果验证通过,服务器(后端)生成token->返回token给客户端(前端)->客户端后续请求在header中携带token->服务器验证token是否有效
'''

