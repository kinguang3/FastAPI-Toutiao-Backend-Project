from sqlalchemy.ext.asyncio import AsyncSession
from models.news import Category
from sqlalchemy import select





async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Category).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()