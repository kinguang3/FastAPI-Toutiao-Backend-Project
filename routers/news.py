#导包
from fastapi import APIRouter, Depends,Query
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_database
from curd import news
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
    categories = await news.get_categories(db, skip, limit)
    return {"categories": categories}


@router.get("/list")
async def get_news_list(
     category_id: int = Query(..., alias="categoryId"),
     page: int = 1,
     page_size: int = Query(10, alias="pageSize",max_length=100), 
     db: AsyncSession = Depends(get_database)
     ):
    news_list = await news.get_news_list(db, category_id, page, page_size)
    total = await news.get_news_count(db, category_id)
    '''
    思路：处理分页->查询新闻列表->计算总量->计算是否还有更多
    '''
    has_more = total > page * page_size
    return {
        "news_list": news_list,
        "total": total,
        "has_more": has_more
    }

@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="Id"),#alias是自己定义的别名
    db: AsyncSession = Depends(get_database)
    ):
    news_detail = await news.get_news_detail(db, news_id)
    return {"news_detail": news_detail}

