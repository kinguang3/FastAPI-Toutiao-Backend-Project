
#创建分类,数据库没有分类,需要手动创建
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Boolean
from datetime import datetime

#基本时间
class Base(AsyncAttrs, DeclarativeBase):
    create_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
        )
    update_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
        )





class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)


class News(Base):
    __tablename__ = "news"
    #高频查询场景,创建索引，提升速度
    __table_args__ = (
        Index("idx_news_category_id", "category_id"),
        Index("idx_news_author_id", "author_id"),
    )



    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True,comment="新闻id")
    title: Mapped[str] = mapped_column(String(200), index=True,comment="新闻标题")
    content: Mapped[str] = mapped_column(Text,comment="新闻内容")
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"),comment="分类id")
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"),comment="作者id")
    is_published: Mapped[bool] = mapped_column(Boolean, default=False,comment="是否发布")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    views: Mapped[int] = mapped_column(Integer, default=0,comment="浏览量")

