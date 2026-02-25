from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category
from sqlalchemy import select

from models.news import News

#查询方法

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

#新闻列表
async def get_news_list(db: AsyncSession, category_id: int, page: int = 1, page_size: int = 10):
    skip = (page - 1) * page_size
    query = select(News).filter(News.category_id == category_id).offset(skip).limit(page_size)
    result = await db.execute(query)
    return result.scalars().all()
