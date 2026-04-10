# FamilyTree Lightweight Family Tree System

## 项目概述
轻量级族谱系统是一个基于FastAPI和Vue 3的全栈应用，旨在帮助用户创建和管理他们的家族树。该系统支持用户注册、登录、创建族谱、添加成员以及可视化族谱图谱。

## 技术栈
- **后端**：FastAPI (Python)
- **前端**：Vue 3 + Pinia + Vite
- **数据库**：PostgreSQL/SQLite
- **图谱渲染**：D3.js / ECharts
- **导出引擎**：WeasyPrint / Graphviz

## 项目结构
```
FamilyTree
├── backend
│   ├── app
│   │   ├── main.py
│   │   ├── api
│   │   │   └── v1
│   │   │       ├── auth.py
│   │   │       ├── trees.py
│   │   │       └── members.py
│   │   ├── core
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db
│   │   │   ├── base.py
│   │   │   ├── models.py
│   │   │   ├── crud.py
│   │   │   └── session.py
│   │   ├── schemas
│   │   │   └── pydantic_models.py
│   │   ├── services
│   │   │   └── auth_service.py
│   │   └── tests
│   │       └── test_auth.py
│   ├── alembic
│   │   ├── env.py
│   │   └── versions
│   ├── Dockerfile
│   ├── requirements.txt
│   └── docker-compose.yml
├── frontend
│   ├── src
│   │   ├── main.ts
│   │   ├── App.vue
│   │   ├── router
│   │   │   └── index.ts
│   │   ├── views
│   │   │   ├── Auth
│   │   │   │   ├── Login.vue
│   │   │   │   └── Register.vue
│   │   │   ├── Dashboard
│   │   │   │   └── TreeList.vue
│   │   │   └── Tree
│   │   │       ├── GraphView.vue
│   │   │       ├── MemberDetail.vue
│   │   │       └── InvitePage.vue
│   │   ├── components
│   │   │   ├── MemberForm.vue
│   │   │   ├── ImageUploader.vue
│   │   │   ├── GraphRenderer.vue
│   │   │   └── ExportModal.vue
│   │   ├── stores
│   │   │   ├── auth.ts
│   │   │   └── tree.ts
│   │   └── api
│   │       └── index.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
├── docs
│   └── need.md
├── .env.example
├── README.md
├── .gitignore
└── LICENSE
```

## 环境配置
### 后端
1. 安装依赖：
   ```
   pip install -r backend/requirements.txt
   ```
2. 数据库迁移：
   ```
   alembic upgrade head
   ```
3. 启动后端服务：
   ```
   uvicorn app.main:app --reload
   ```

### 前端
1. 安装依赖：
   ```
   npm install
   ```
2. 启动前端开发服务器：
   ```
   npm run dev
   ```

## 功能模块
- **用户认证**：支持用户注册和登录。
- **族谱管理**：创建、查看和管理族谱。
- **成员管理**：添加、查看和管理族谱成员。
- **图谱可视化**：展示族谱图谱，支持导出为PDF/PNG/JSON格式。

## API 路由
- **认证**
  - `POST /api/v1/auth/register`：用户注册
  - `POST /api/v1/auth/login`：用户登录

- **族谱管理**
  - `POST /api/v1/trees`：创建族谱
  - `GET /api/v1/trees`：获取用户族谱列表
  - `POST /api/v1/trees/{id}/join`：通过邀请码加入族谱
  - `PUT /api/v1/trees/{id}/settings`：修改族谱设置
  - `GET /api/v1/trees/{id}/members`：获取族谱成员列表
  - `POST /api/v1/trees/{id}/members`：添加成员

- **成员管理**
  - `GET /api/v1/members/{member_id}`：获取成员详细信息
  - `GET /api/v1/trees/{id}/graph`：获取族谱图谱数据
  - `GET /api/v1/trees/{id}/export`：导出族谱数据

## 开发注意事项
- 确保在开发过程中遵循最佳实践，保持代码整洁和可维护。
- 使用版本控制系统管理代码变更，确保团队协作顺畅。

## 许可证
本项目遵循MIT许可证，详细信息请查看LICENSE文件。