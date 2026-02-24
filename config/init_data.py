from config.db_conf import AsyncSessionLocal
from curd.category import create_category
import asyncio


async def init_default_data():
    """初始化默认数据"""
    print("正在初始化默认数据...")
    
    # 默认分类列表
    default_categories = [
        {"name": "科技", "description": "科技新闻和资讯"},
        {"name": "娱乐", "description": "娱乐新闻和明星八卦"},
        {"name": "体育", "description": "体育赛事和运动员信息"},
        {"name": "财经", "description": "财经新闻和市场分析"},
        {"name": "教育", "description": "教育资讯和学习资源"},
        {"name": "健康", "description": "健康知识和医疗资讯"},
        {"name": "旅游", "description": "旅游攻略和景点介绍"},
        {"name": "汽车", "description": "汽车新闻和评测"}
    ]
    
    async with AsyncSessionLocal() as session:
        try:
            for cat_data in default_categories:
                await create_category(
                    session, 
                    name=cat_data["name"], 
                    description=cat_data["description"]
                )
            await session.commit()
            print(f"成功添加 {len(default_categories)} 个默认分类")
        except Exception as e:
            await session.rollback()
            print(f"添加默认分类时出错: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(init_default_data())
