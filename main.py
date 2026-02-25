from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#中间体，解决跨域问题，cors
#同源的三个条件：协议、域名、端口号都相同
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,  #是否允许发送cookie
    allow_methods=["*"],  #允许的HTTP方法
    allow_headers=["*"],   #允许的请求头
)




@app.get("/")
async def root():
    return {"message": "Hello World"}


#挂载路由/注册路由
app.include_router(news.router)
