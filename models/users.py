from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from sqlalchemy import String, Integer, Boolean, DateTime,Index
from datetime import datetime
from typing import Optional




class Base(DeclarativeBase):
    pass



class User(Base):
    __tablename__ = "users"


    #用户信息
    __table_args__ = (
        Index('username_UNIQUE', 'username'),
        Index('phone_UNIQUE', 'phone'),
    )


    #Optional的作用：表示该字段可以为空(根据业务逻辑判断是否必填)
    #Integer, primary_key=True实现自增
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="用户ID")
    username: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True, comment="用户名")
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, comment="邮箱")
    password: Mapped[str] = mapped_column(String(100), comment="密码")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否激活")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    phone: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment="手机号")



class UserToken(Base):
    __tablename__ = "user_tokens"

    __table_args__ = (
        Index('user_id_UNIQUE', 'user_id'),
        Index('token_UNIQUE', 'token'),
    )


    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, comment="用户令牌ID")
    user_id: Mapped[int] = mapped_column(Integer, comment="用户ID")
    token: Mapped[str] = mapped_column(String(255), comment="令牌")
    expires_at: Mapped[datetime] = mapped_column(DateTime, comment="过期时间")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
