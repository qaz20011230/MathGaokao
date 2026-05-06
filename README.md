# mathgaokao.top 高考数学试题档案馆

<h2 align="center">1905 — 2025 &nbsp;·&nbsp; 跨越一百二十年的数学教育记忆</h2>

<p align="center">
  <strong>中文</strong> &nbsp;|&nbsp; <a href="#english">English</a>
</p>

---

## 项目概述

**mathgaokao.top** 收录科举制度废除（1905年）至今一切高考数学试卷、答题卡及相关文档，是中国高考数学试题最完整的数字档案馆。

清光绪三十一年，延续一千三百余年的科举制度正式废除。从民国时期的大学独立招生，到1952年全国统一高考的建立，再到1977年恢复高考至今——数学试题的变迁，本身就是一部浓缩的中国近现代教育史。

本站致力于系统性地收录、保存和展示这些承载了无数青春记忆与命运转折的数学试卷，为中国的数学教育史留下完整、可追溯的数字档案。

### 收录范围

| 时期 | 年份 | 内容 |
|------|------|------|
| **大学独立招生期** | 1905—1951 | 北京大学、清华大学、燕京大学、交通大学等校自命题数学试卷 |
| **统一高考初期** | 1952—1965 | 新中国全国统一高考数学试卷（理工类 / 文史类） |
| **恢复高考至今** | 1977—2025 | 全国卷、各省自主命题卷、新高考卷等全类型试卷 |

### 文档类型

- **试卷** — 正式考试使用的数学试卷原题
- **答题卡** — 标准化考试答题卡样式
- **参考答案** — 官方或权威来源的参考答案与评分标准
- **其他文档** — 考纲、命题说明、统计分析等辅助材料

---

## 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Next.js 14 + React 18 + TypeScript + Tailwind CSS | App Router, SSG/SSR |
| 后端 | FastAPI + SQLAlchemy + Pydantic | 异步 REST API |
| 数据库 | SQLite (开发) / MySQL 8.0 (生产) | utf8mb4 |
| PDF 渲染 | PyMuPDF + 自研虚拟滚动查看器 | 180 DPI 高清 |
| 认证 | JWT (HS256) | 管理员独占 |
| 部署 | Docker Compose + Nginx | 单机 / 集群 |

### 技术亮点

- **PDF 保护** — PDF 文件通过后端流式传输，浏览器端不暴露文件路径
- **虚拟滚动** — 1218 页自研 HTML 查看器，仅渲染可见区域页码
- **系统字体** — 零外部依赖，离线可用
- **安全沙箱** — 访客仅可在线浏览，管理员 JWT 认证后可下载上传

---

## 项目结构

```
mathgaokao/
├── frontend/                        # Next.js 14 前端
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx           # 全局布局 + 元数据
│   │   │   ├── layout-wrapper.tsx   # 文档页全屏切换
│   │   │   ├── page.tsx             # 首页（搜索 + 统计 + 年份轴）
│   │   │   ├── browse/page.tsx      # 浏览页（待选 + 筛选 + 卡片）
│   │   │   ├── doc/[id]/page.tsx    # 文档页（图片/PDF 双模式）
│   │   │   ├── region/[name]/page.tsx  # 按命题单位浏览
│   │   │   ├── about/page.tsx       # 关于本站
│   │   │   └── admin/page.tsx       # 管理后台（上传/编辑/删除）
│   │   └── lib/
│   │       ├── api.ts               # API 客户端封装
│   │       └── utils.ts             # 工具函数
│   ├── next.config.js               # API 代理 + 构建配置
│   └── tailwind.config.ts           # 学术风格主题
├── backend/                         # FastAPI 后端
│   ├── app/
│   │   ├── main.py                  # 应用入口 + 路由注册
│   │   ├── config.py                # 配置（数据库/JWT/路径）
│   │   ├── database.py              # SQLAlchemy 引擎
│   │   ├── models/document.py       # Document + Admin ORM
│   │   ├── schemas/document.py      # Pydantic 请求/响应模型
│   │   ├── services/document.py     # 业务逻辑（CRUD + 统计）
│   │   ├── api/documents.py         # 公开 API（浏览/查看/搜索）
│   │   ├── api/admin.py             # 管理 API（上传/编辑/删除/下载）
│   │   ├── api/auth.py              # JWT 认证中间件
│   │   └── utils/file_handler.py    # 文件上传/MD5/命名
│   ├── seeds/
│   │   ├── seed_1977_2025.py        # 1977-2025 真题种子数据
│   │   └── convert_pdf.py           # PDF → HTML 查看器转换脚本
│   └── requirements.txt
├── nginx/default.conf               # 反向代理 + 文件保护
├── docker-compose.yml               # 一键生产部署
└── setup.sh                         # 本地开发一键安装
```

---

## 快速开始

### 本地开发

```bash
# 1. 安装依赖
cd mathgaokao
bash setup.sh

# 2. 启动后端（端口 8000）
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 3. 启动前端（端口 3000）
cd frontend
npm run dev

# 4. 访问
open http://localhost:3000
```

### 生产部署

```bash
# 配置环境变量
cp .env.example .env
# 编辑 .env：修改 JWT_SECRET、ADMIN_PASSWORD
# 切换 database_url 为 MySQL 连接串

# 一键启动
docker compose up -d

# 服务端口
# Nginx → :80/:443
# 前端 → :3000 （内部）
# 后端 → :8000 （内部）
# MySQL → :3306 （内部）
```

---

## 安全模型

| 角色 | 在线浏览 | 下载 | 上传 | 编辑 | 删除 |
|------|:-------:|:----:|:----:|:----:|:----:|
| 访客（所有人） | ✓ | ✗ | ✗ | ✗ | ✗ |
| 超级管理员 | ✓ | ✓ | ✓ | ✓ | ✓ |

- **PDF 保护** — 文件不在 Nginx 静态目录，仅通过 FastAPI 流式传输
- **JWT 认证** — 管理员登录获得 token，存储于 localStorage
- **沙箱隔离** — 前端 iframe 使用 `sandbox` 属性限制下载行为
- **路径隐藏** — `/data/documents/` 不对外暴露

---

## API 文档

### 公开端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats` | 文档统计总览 |
| GET | `/api/years` | 年份分布 |
| GET | `/api/provinces` | 命题单位列表 |
| GET | `/api/documents` | 文档列表（分页 + 筛选 + 搜索） |
| GET | `/api/documents/:id` | 文档详情 |
| GET | `/api/documents/:id/view` | PDF 在线查看 |
| GET | `/api/documents/:id/viewer` | HTML 图片查看器 |
| GET | `/api/documents/:id/pages/*` | 查看器页面图片 |

### 管理端点（需 JWT）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/admin/login` | 管理员登录 |
| POST | `/api/admin/documents` | 上传新文档 |
| PUT | `/api/admin/documents/:id` | 编辑文档元数据 |
| DELETE | `/api/admin/documents/:id` | 删除文档及其文件 |
| GET | `/api/admin/documents/:id/download` | 下载文档文件 |

启动后端后访问 `http://localhost:8000/docs` 查看 Swagger 交互文档。

---

## 贡献指南

本站为永久性数字档案项目，欢迎通过以下方式贡献：

- **提供历史资料** — 如您拥有本站尚未收录的历史试卷（尤其是 1905—1951 年时期资料），欢迎提交
- **修正错误** — 如发现元数据错误或文档问题，请提交 Issue
- **技术支持** — 欢迎提交 PR 改进代码

---

<a name="english"></a>

## English

### mathgaokao.top — The Gaokao Mathematics Archive

A comprehensive digital archive of all Chinese college entrance examination (Gaokao) mathematics papers, answer sheets, and related documents from the abolition of the Imperial Examination System (1905) to the present day (2025).

### Overview

In 1905, the 1,300-year-old Chinese Imperial Examination System was officially abolished. From the independent university entrance exams of the Republican era, to the establishment of the national unified Gaokao in 1952, to its resumption in 1977 — the evolution of mathematics examination papers chronicles the history of modern Chinese education.

mathgaokao.top is dedicated to systematically collecting, preserving, and displaying these mathematics papers — bearing witness to the aspirations and turning points of generations — creating a complete, traceable digital archive for the history of Chinese mathematics education.

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 + React 18 + TypeScript + Tailwind CSS |
| Backend | FastAPI + SQLAlchemy + Pydantic |
| Database | SQLite (dev) / MySQL 8.0 (production) |
| PDF Viewer | PyMuPDF + custom virtual-scroll HTML viewer (180 DPI) |
| Auth | JWT (HS256) |
| DevOps | Docker Compose + Nginx |

### Key Features

- **7 Pages** — Home, Browse, Document Viewer, Region, About, Admin
- **111 Documents** — Seeded with 1977—2025 national exam data
- **1,218-page Viewer** — Custom HTML viewer with virtual scrolling, zoom, and keyboard shortcuts
- **Dual Mode** — Switch between high-resolution image viewer and embedded PDF
- **Security** — Public browsing only; download/upload restricted to JWT-authenticated admins
- **Offline-ready** — Zero external font dependencies; fully functional without internet

### Quick Start

```bash
bash setup.sh                        # Install dependencies
cd backend && uvicorn app.main:app --port 8000 --reload
cd frontend && npm run dev           # Then visit http://localhost:3000
```

### Production

```bash
cp .env.example .env                 # Configure secrets
docker compose up -d                 # Nginx + Frontend + Backend + MySQL
```

### License

This project is maintained by 广州菲娜睿特人工智能科技有限责任公司 (Guangzhou Finaret AI Technology Co., Ltd.). All collected examination papers belong to their respective copyright holders. This digital archive serves academic research and historical preservation purposes only. Commercial use of the archived materials is not permitted.

---

<p align="center">
  <sub>© 2025 广州菲娜睿特人工智能科技有限责任公司 &nbsp;·&nbsp; mathgaokao.top</sub>
</p>
