from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Category


async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取分类列表"""
    result = await db.execute(
        select(Category).offset(skip).limit(limit)
    )
    categories = result.scalars().all()
    return [
        {
            "id": cat.id,
            "name": cat.name,
            "description": cat.description
        }
        for cat in categories
    ]


async def create_category(db: AsyncSession, name: str, description: str = None):
    """创建分类"""
    db_category = Category(name=name, description=description)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return {
        "id": db_category.id,
        "name": db_category.name,
        "description": db_category.description
    }
