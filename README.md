# 头条新闻后端（FastAPI Toutiao Backend）

基于 **FastAPI + SQLAlchemy（异步）+ SQLite** 开发的新闻资讯类后端接口服务，模拟「今日头条」类 App 的核心数据接口：新闻分类、新闻列表分页、新闻详情与浏览量统计、同类新闻推荐，以及用户注册与 Token 签发。

接口遵循 RESTful 风格，并自动生成 Swagger / ReDoc 交互式接口文档，可直接用于前后端联调。

---

## 功能特性

- 🗂 **新闻分类**：查询分类列表（内置科技、娱乐、体育、财经等 8 个默认分类）
- 📰 **新闻列表**：按分类分页查询，返回总数与是否还有更多（`has_more`）
- 🔍 **新闻详情**：查询详情的同时自动累加浏览量，并返回同类热门新闻推荐
- 🔥 **相关推荐**：同分类下排除当前新闻，按浏览量、发布状态排序
- 👤 **用户注册**：校验用户名唯一性，密码使用 bcrypt 哈希存储
- 🔑 **登录凭证**：注册后生成 UUID Token，有效期 7 天并持久化到数据库
- 🌐 **跨域支持**：内置 CORS 中间件，方便本地前端联调
- ⚡ **全异步**：异步引擎 + 异步会话，接口非阻塞处理请求

---

## 技术栈

| 分类 | 技术 |
| --- | --- |
| Web 框架 | FastAPI |
| ASGI 服务器 | Uvicorn |
| ORM | SQLAlchemy 2.0（异步） |
| 数据库 | SQLite（aiosqlite 驱动，可切换 MySQL / PyMySQL） |
| 数据校验 | Pydantic |
| 密码加密 | Passlib + bcrypt |
| 配置管理 | python-dotenv |

---

## 项目结构

```text
toutiao_backend/
├── main.py                 # 应用入口：创建 FastAPI 实例、注册 CORS 与路由
├── requirements.txt        # 依赖清单
├── .gitignore
├── config/
│   ├── db_conf.py          # 异步数据库引擎、会话工厂、get_database 依赖
│   ├── init_db.py          # 建表脚本
│   └── init_data.py        # 初始化默认新闻分类
├── models/                 # SQLAlchemy 数据模型（表结构）
│   ├── news.py             # User / Category / News
│   └── users.py            # User / UserToken
├── schemas/                # Pydantic 请求/响应模型
│   └── user.py             # 用户注册请求体 UserRequest
├── curd/                   # 数据库操作层（增删改查）
│   ├── news.py             # 分类、列表、详情、浏览量、相关推荐
│   ├── users.py            # 用户查询、创建、Token 生成
│   └── category.py         # 分类查询与创建
├── routers/                # 路由层（接口定义）
│   ├── news.py             # /api/news/*
│   └── user.py             # /api/user/*
├── utils/
│   └── security.py         # 密码哈希工具
└── test.db                 # SQLite 数据库文件（已被 .gitignore 忽略）
```

**分层思路**：`routers`（接口）→ `schemas`（入参校验）→ `curd`（数据库操作）→ `models`（表结构），职责分离，便于扩展与维护。

---

## 快速开始

### 1. 环境要求

- Python 3.10+
- pip

### 2. 克隆项目并安装依赖

```bash
git clone https://github.com/kinguang3/FastAPI-Toutiao-Backend-Project.git
cd FastAPI-Toutiao-Backend-Project

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
# 密码哈希库（curd/users.py 依赖，未包含在 requirements.txt 中）
pip install "passlib[bcrypt]"
```

### 3. 初始化数据库与默认数据

```bash
python -m config.init_db     # 创建数据表
python -m config.init_data   # 写入默认新闻分类
```

> 数据库默认使用项目根目录下的 `test.db`。如需改用 MySQL，修改 `config/db_conf.py` 中的连接串即可，例如：
> `mysql+aiomysql://user:password@127.0.0.1:3306/toutiao`

### 4. 启动服务

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

| 地址 | 说明 |
| --- | --- |
| http://127.0.0.1:8000/ | 服务首页（健康检查） |
| http://127.0.0.1:8000/docs | Swagger UI 交互式文档 |
| http://127.0.0.1:8000/redoc | ReDoc 文档 |

---

## 接口一览

### 新闻模块 `/api/news`

| 方法 | 路径 | 说明 | 主要参数 |
| --- | --- | --- | --- |
| GET | `/api/news/categories` | 获取新闻分类列表 | `skip`、`limit` |
| GET | `/api/news/list` | 按分类分页获取新闻列表 | `categoryId`（必填）、`page`、`pageSize` |
| GET | `/api/news/detail` | 获取新闻详情，浏览量 +1 | `Id`（新闻 ID，必填） |

**请求示例**

```http
GET /api/news/list?categoryId=1&page=1&pageSize=10
```

```json
{
  "news_list": [
    {
      "id": 1,
      "title": "新闻标题",
      "content": "新闻内容",
      "category_id": 1,
      "author_id": 1,
      "views": 128,
      "is_published": true,
      "created_at": "2026-01-01T10:00:00"
    }
  ],
  "total": 42,
  "has_more": true
}
```

```http
GET /api/news/detail?Id=1
```

```json
{
  "news_detail": { "id": 1, "title": "新闻标题", "views": 128 },
  "views": 128,
  "related_news": [
    { "id": 3, "title": "同类新闻标题", "views": 96 }
  ]
}
```

### 用户模块 `/api/user`

| 方法 | 路径 | 说明 | 请求体 |
| --- | --- | --- | --- |
| POST | `/api/user/register` | 用户注册并签发 Token | `username`、`password`、`email`、`phone` |

**请求示例**

```json
{
  "username": "testuser",
  "password": "123456",
  "email": "test@example.com",
  "phone": "13800000000"
}
```

用户名已存在时返回 `400`：

```json
{ "detail": "用户名已存在" }
```

---

## 数据模型

- **User**：`id`、`username`、`email`、`password`、`phone`、`is_active`、`created_at`
- **UserToken**：`id`、`user_id`、`token`、`expires_at`、`created_at`（Token 有效期 7 天）
- **Category**：`id`、`name`、`description`
- **News**：`id`、`title`、`content`、`category_id`、`author_id`、`is_published`、`views`、`created_at`、`updated_at`

`news` 表在 `category_id`、`author_id` 上建立索引以提升高频查询性能。

---

## 待完善（TODO）

- [ ] 统一数据模型定义，避免 `models/news.py` 与 `models/users.py` 中重复的 `User` / `Base`
- [ ] 修正 SQLAlchemy 查询方法名（`scalars_one` → `scalar_one`、`scalars_one_or_none` → `scalars().one_or_none()`）
- [ ] 注册接口返回体不应包含密码字段
- [ ] 补全 `create_user_token` 的实现，并统一 Token 校验（依赖注入）逻辑
- [ ] 增加新闻发布 / 编辑 / 删除等管理接口
- [ ] 增加 Token 校验中间件与登录接口
- [ ] 引入 Alembic 管理数据库迁移
- [ ] 补充单元测试与 CI

---

## 说明

- `allow_origins=["*"]` 仅适用于开发环境，生产环境请改为具体的前端域名。
- `test.db`、`venv/`、`__pycache__/` 等已在 `.gitignore` 中忽略，不会提交到仓库。

## License

本项目仅用于学习与交流，可自由 fork 与修改。
