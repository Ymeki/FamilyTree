# FILE: /FamilyTree/FamilyTree/docs/need.md

# 🌳 轻量级族谱系统 (Lightweight Family Tree)

**技术栈**：FastAPI (Python) + Vue 3 + Pinia + Vite + PostgreSQL/SQLite  
**开发模式**：Vibe Coding（分阶段 Prompt 驱动、AI 结对编程）

## 1. 项目概述
轻量级族谱系统旨在提供一个用户友好的平台，帮助用户创建和管理他们的家族树。系统支持用户注册、登录、创建族谱、添加成员、查看族谱图谱等功能。

## 2. 核心架构与数据流
```
前端 (Vue3) ↔ REST API ↔ FastAPI (异步) ↔ SQLAlchemy 2.0 ↔ DB
权限拦截：FastAPI Depends + Vue Router Guards
图谱渲染：前端 D3.js / ECharts / GoJS（推荐 D3-force 或 ECharts-graph）
导出引擎：后端生成 JSON 图数据 → 前端 Canvas 截图 / 后端 WeasyPrint/Graphviz 生成 PDF/PNG
```

## 3. 核心数据模型 (轻量级设计)
> 💡 Vibe Coding 建议：先实现核心字段，自定义字段统一使用 `JSON` 类型扩展。

| 表名 | 字段 | 类型 | 说明 |
|------|------|------|------|
| `users` | `id`, `username`, `email`, `password_hash`, `created_at` | PK, UUID/VARCHAR | 基础用户表 |
| `family_trees` | `id`, `name`, `creator_id`, `visibility` (`public`/`private`), `invite_code`, `created_at` | PK, FK, ENUM | 族谱主表 |
| `tree_members` | `id`, `tree_id`, `name`, `gender`, `birth_date`, `death_date`, `bio`, `custom_data` (JSON), `father_id`, `mother_id`, `created_by` | PK, FK, Nullable | 成员表（自关联父母） |
| `tree_roles` | `id`, `tree_id`, `user_id`, `role` (`owner`/`manager`/`member`) | PK, Composite UK | 权限分配表 |
| `member_assets` | `id`, `member_id`, `url`, `type` (`image`/`doc`), `caption` | PK, FK | 附件/成就图片 |

## 4. 功能模块与迭代路线 (Vibe Coding 阶段)
| 阶段 | 目标 | 交付物 | AI 提示词关键词 |
|------|------|--------|----------------|
| `Phase 1` | 基础脚手架 & 用户认证 | FastAPI+Vue 项目结构、JWT 登录注册、基础路由 | `scaffold fastapi vue3 jwt pinia` |
| `Phase 2` | 族谱管理 & 权限控制 | 创建/加入族谱、邀请码逻辑、可见性控制、角色分配 | `family_tree crud invite_code rbac` |
| `Phase 3` | 成员管理 & 详情 | 增删改查成员、父母关联、JSON 自定义字段、图片上传 | `member form parent_link json_custom upload` |
| `Phase 4` | 图谱渲染 & 导出 | 图数据 API、前端可视化、PDF/PNG/JSON 导出 | `d3_graph export pdf png networkx` |

## 5. 关键 API 路由设计
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

## 6. 前端组件结构 (Vue 3)
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

## 7. 权限与可见性逻辑
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