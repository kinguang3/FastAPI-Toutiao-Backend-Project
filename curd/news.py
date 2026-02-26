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
    #where->筛选出指定分类的新闻(但是每条新闻都有News里面的属性)
    query = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


#获取分类下的新闻数量总数方法
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


#增加点击量方法
async def increase_views(db: AsyncSession, news_id: int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)#自己更新
    result =await db.execute(stmt)
    await db.commit()#数据库的更新->检查数据库是否真的命中了数据
    #拓展
    return result.rowcount>0#返回受影响的行数


#获取同类推荐新闻方法
async def get_related_news(db: AsyncSession, news_id: int, category_id: int, skip: int = 1, limit: int = 10):#响应的数据是有限的,默认返回10条数据
    skip = (skip - 1) * limit
    #order_by排序->根据点击量进行排序(降序desc(),默认是升序asc())
    # 查询同一分类下、排除当前新闻本身，并按点击量降序排序，分页返回相关新闻
    query = select(News).where(News.category_id == category_id, News.id != news_id).order_by(News.views.desc(),News.is_published.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    # return result.scalars().all()
    #拓展
    #列表推导式->筛选出is_published为True的新闻
    related_news = [{"id": news.id, "title": news.title, "views": news.views} for news in result.scalars().all() if news.is_published]
    return related_news#返回相关新闻的id,title,views


