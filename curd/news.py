from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category
from sqlalchemy import select,func,update

from models.news import News

#查询方法

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

#新闻列表
async def get_news_list(db: AsyncSession, category_id: int, skip: int = 1, limit: int = 10):
    skip = (skip - 1) * limit
    query = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()



async def get_news_count(db:AsyncSession, category_id: int):
    #查询指定分类的新闻数量
    query = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(query)
    return result.scalars_one()#只能有一个结果，否则就报错


#新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    query = select(News).where(News.id == news_id)
    result = await db.execute(query)
    return result.scalars_one_or_none()#防止不存在报错



async def increase_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)#自己更新
    result =await db.execute(stmt)
    await db.commit()#数据库的更新->检查数据库是否真的命中了数据
    #拓展
    return result.rowcount>0#返回受影响的行数




