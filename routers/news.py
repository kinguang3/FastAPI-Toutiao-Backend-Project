#导包
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_database
from curd import category
'''
创建APIrouter实例
prefix: 路由前缀
tags: 分组标签

'''
router = APIRouter(
    prefix="/api/news",
    tags=["news"],
)

'''
接口实现流程
1.API接口规范文档 -> 模块化路由
2.数据库表(数据库设计文档) -> 定义模型类
3.在curd文件夹下定义数据库操作的方法
4.在路由处理函数里面调用curd方法,响应结果
'''



@router.get("/categories")
async def get_news_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_database)):
    categories = await category.get_categories(db, skip, limit)
    return {"categories": categories}
