
# 🌳 轻量级族谱系统 (Lightweight Family Tree)
**技术栈**：FastAPI (Python) + Vue 3 + Pinia + Vite + PostgreSQL/SQLite  
**开发模式**：Vibe Coding（分阶段 Prompt 驱动、AI 结对编程）

## 1. 核心架构与数据流
```
前端 (Vue3) ↔ REST API ↔ FastAPI (异步) ↔ SQLAlchemy 2.0 ↔ DB
权限拦截：FastAPI Depends + Vue Router Guards
图谱渲染：前端 D3.js / ECharts / GoJS（推荐 D3-force 或 ECharts-graph）
导出引擎：后端生成 JSON 图数据 → 前端 Canvas 截图 / 后端 WeasyPrint/Graphviz 生成 PDF/PNG
```

## 2. 核心数据模型 (轻量级设计)
> 💡 Vibe Coding 建议：先实现核心字段，自定义字段统一使用 `JSON` 类型扩展。

| 表名 | 字段 | 类型 | 说明 |
|------|------|------|------|
| `users` | `id`, `username`, `email`, `password_hash`, `created_at` | PK, UUID/VARCHAR | 基础用户表 |
| `family_trees` | `id`, `name`, `creator_id`, `visibility` (`public`/`private`), `invite_code`, `created_at` | PK, FK, ENUM | 族谱主表 |
| `tree_members` | `id`, `tree_id`, `name`, `gender`, `birth_date`, `death_date`, `bio`, `custom_data` (JSON), `father_id`, `mother_id`, `created_by` | PK, FK, Nullable | 成员表（自关联父母） |
| `tree_roles` | `id`, `tree_id`, `user_id`, `role` (`owner`/`manager`/`member`) | PK, Composite UK | 权限分配表 |
| `member_assets` | `id`, `member_id`, `url`, `type` (`image`/`doc`), `caption` | PK, FK | 附件/成就图片 |

## 3. 功能模块与迭代路线 (Vibe Coding 阶段)
| 阶段 | 目标 | 交付物 | AI 提示词关键词 |
|------|------|--------|----------------|
| `Phase 1` | 基础脚手架 & 用户认证 | FastAPI+Vue 项目结构、JWT 登录注册、基础路由 | `scaffold fastapi vue3 jwt pinia` |
| `Phase 2` | 族谱管理 & 权限控制 | 创建/加入族谱、邀请码逻辑、可见性控制、角色分配 | `family_tree crud invite_code rbac` |
| `Phase 3` | 成员管理 & 详情 | 增删改查成员、父母关联、JSON 自定义字段、图片上传 | `member form parent_link json_custom upload` |
| `Phase 4` | 图谱渲染 & 导出 | 图数据 API、前端可视化、PDF/PNG/JSON 导出 | `d3_graph export pdf png networkx` |

## 4. 关键 API 路由设计
```bash
# 认证
POST   /api/v1/auth/register
POST   /api/v1/auth/login

# 族谱管理
POST   /api/v1/trees                     # 创建 (自动成为 owner)
GET    /api/v1/trees                     # 我的族谱列表
POST   /api/v1/trees/{id}/join           # 通过 invite_code 加入
PUT    /api/v1/trees/{id}/settings       # 修改可见性/邀请码/管理者
GET    /api/v1/trees/{id}/members        # 成员列表
POST   /api/v1/trees/{id}/members        # 添加成员
GET    /api/v1/members/{member_id}       # 详情（含自定义字段/图片）
GET    /api/v1/trees/{id}/graph          # 图谱数据 (节点+边)
GET    /api/v1/trees/{id}/export         # ?format=pdf|png|json|gedcom
```
> 🔒 权限中间件：所有 `/api/v1/trees/*` 接口需校验 `user` 是否属于该树，且 `visibility=private` 时非成员拒绝访问。

## 5. 前端组件结构 (Vue 3)
```
src/
├── views/
│   ├── Auth/           # Login.vue, Register.vue
│   ├── Dashboard/      # TreeList.vue (我的族谱)
│   ├── Tree/           # GraphView.vue (图谱), MemberDetail.vue, InvitePage.vue
│   └── Settings/       # RoleManager.vue, TreeSettings.vue
├── components/
│   ├── MemberForm.vue  # 动态表单 (基础字段 + JSON 自定义字段渲染器)
│   ├── ImageUploader.vue
│   ├── GraphRenderer.vue # 封装 D3/ECharts
│   └── ExportModal.vue
├── stores/             # auth.js, tree.js, ui.js
└── api/                # 按模块拆分 axios 请求
```

## 6. 权限与可见性逻辑
```python
# FastAPI Depends 伪代码
async def check_tree_access(tree_id: UUID, current_user: User, required_role: str = "member"):
    tree = await get_tree(tree_id)
    if tree.visibility == "private" and not await is_tree_member(tree_id, current_user.id):
        raise HTTPException(403, "Private tree, invite required.")
    if required_role == "manager" and not await has_role(tree_id, current_user.id, ["owner", "manager"]):
        raise HTTPException(403, "Manager access required.")
    return tree
```

## 7. 🤖 Vibe Coding 提示词工作流 (直接复制使用)
> 建议配合 Cursor / Windsurf 使用，每次只喂一个 Phase，保留上下文。

### Phase 1 Prompt
```text
使用 FastAPI + Vue 3 + Vite + Pinia 搭建基础项目。
后端：异步 SQLAlchemy 2.0 + PostgreSQL/SQLite，实现 JWT 注册/登录接口，返回 access_token。
前端：配置 Vue Router、Pinia、Axios 拦截器（自动附加 Token）。
要求：提供完整目录结构、环境变量配置示例、基础 Dockerfile 或启动脚本。代码需符合现代 Python/Vue 最佳实践，添加必要类型注解。
```

### Phase 2 Prompt
```text
基于现有项目，实现族谱管理模块。
后端：
1. 创建 /api/v1/trees 接口，创建者自动为 owner。
2. 生成 8 位字母数字 invite_code，支持 POST /trees/{id}/join 验证并加入。
3. 实现 visibility 字段 (public/private)，私有树需校验成员身份。
4. 实现角色分配接口 /trees/{id}/roles (owner/manager/member)。
前端：
1. Dashboard 展示用户创建/加入的族谱列表。
2. 树设置页：切换公开/私有、重置邀请码、添加管理者（搜索用户名）。
提供数据库迁移脚本 (Alembic) 和完整路由守卫。
```

### Phase 3 Prompt
```text
实现族谱成员管理模块。
后端：
1. 成员表包含：姓名、性别、生日、简介、自定义字段(JSON)、父亲ID、母亲ID。
2. 实现 CRUD 接口，关联父母时需校验同属一个族谱。
3. 图片上传接口 /members/{id}/assets，返回可访问 URL。
前端：
1. MemberForm.vue：动态渲染基础字段 + JSON 自定义字段（支持 key-value 增删）。
2. MemberDetail.vue：展示信息、图片画廊、成就时间线。
3. 使用 Element Plus / Naive UI 保持 UI 一致。
```

### Phase 4 Prompt
```text
实现族谱图谱生成与导出。
后端：
1. /trees/{id}/graph 返回标准 JSON：{ nodes: [{id, name, gender}], links: [{source, target, relation: "parent"}] }
2. 实现 /trees/{id}/export?format=pdf|png|json。PDF 使用 WeasyPrint 或 Playwright 渲染图谱截图；PNG 使用 NetworkX+Graphviz；JSON 直接返回 graph 数据。
前端：
1. GraphRenderer.vue 使用 ECharts 或 D3 渲染力导向图，支持拖拽、缩放、点击跳转详情。
2. ExportModal.vue 触发导出，显示进度/下载链接。
要求：图数据需处理循环引用，导出时包含族谱标题、生成时间水印。
```

## 8. 开发注意事项 & 避坑指南
1. **父母关联设计**：轻量级建议直接在成员表加 `father_id` 和 `mother_id`，避免复杂的关系表。导出时可通过 BFS/DFS 遍历生成层级。
2. **自定义字段**：前端使用 `v-for` 遍历 `custom_data` 对象渲染，后端用 Pydantic `Json` 类型自动序列化。
3. **图谱性能**：成员 >500 时 D3 会卡顿。建议前端开启 `forceSimulation` 的 `alpha` 衰减，或改用 ECharts `graph` 类型（WebGL 渲染）。
4. **导出一致性**：PDF 导出建议后端用 `playwright` 无头浏览器访问图谱页截图，比纯后端生成排版更准。
5. **Vibe Coding 心法**：
   - 每次只让 AI 生成一个模块，跑通测试后再进入下一步。
   - 使用 `@workspace` 或项目上下文索引，避免 AI 幻觉。
   - 关键逻辑要求 AI 写单元测试（`pytest` + `vitest`），提升重构信心。

---
✅ **下一步建议**：复制 `Phase 1 Prompt` 到你的 AI 编程助手，生成基础脚手架并本地运行 `uvicorn main:app --reload` + `npm run dev`。跑通后依次执行 Phase 2~4。需要我为你生成某个 Phase 的完整初始代码模板吗？