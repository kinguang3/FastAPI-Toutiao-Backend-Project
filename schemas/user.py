'''
用来写用户注册的请求体:放请求体参数的地方
'''



from pydantic import BaseModel



#数据库的email,phone字段都是可选的,所以在请求体中也可以不写
class UserRequest(BaseModel):
    username: str
    password: str
