from config.db_conf import engine
from models.models import Base
import asyncio


async def init_database():
    """初始化数据库，创建所有表"""
    print("正在初始化数据库...")
    
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("数据库初始化完成！")


if __name__ == "__main__":
    asyncio.run(init_database())
