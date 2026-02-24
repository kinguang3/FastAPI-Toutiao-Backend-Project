from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

# 创建数据库引擎
engine = create_async_engine(
    "sqlite+aiosqlite:///./test.db",
    echo=True,  # 可选，输出SQL日志
    pool_size=10,  # 设置连接池活跃的连接数
    max_overflow=20  # 允许额外的连接数
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后不过期，保持会话状态
)

# 依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 回滚
            raise  # 重新抛出异常
        finally:
            await session.close()  # 关闭会话
