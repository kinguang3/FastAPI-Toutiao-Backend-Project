#utils:工具文件
#security:安全py文件



from passlib.context import CryptContext

#创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


#密码加密
def get_hash_possword(password:str):
    return pwd_context.hash(password)

