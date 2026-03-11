'''
用来写用户注册的请求体:放请求体参数的地方
'''



from pydantic import BaseModel



#数据库的email,phone字段都是必填的,所以在请求体中必需要写
#必填项没填会报错(只有自带自增的属性才可以不填)
class UserRequest(BaseModel):
    username: str
    password: str
    email: str = None
    phone: str = None