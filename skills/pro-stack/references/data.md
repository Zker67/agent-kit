# 数据

本地与服务端的数据存储候选，按使用方式选择。

## 技术候选

| 领域 | 作者偏好 | 适用条件与例外 |
|---|---|---|
| 轻量数据 | JSON | 配置、静态数据、导入导出，以及读写可控的小规模单用户数据。按使用方式而非数据量判断：数据量小但需要关联查询、频繁修改、事务或一致性约束时改用数据库。 |
| 浏览器本地结构化数据 | IndexedDB | 网页离线数据、较多结构化数据与本地索引查询时使用；少量简单键值可用 Web Storage。跨设备同步另行设计。 |
| 应用本地结构化数据 | SQLite | 桌面与移动应用的本地持久化、查询与事务候选；多设备或多人同步需求需另外设计。 |
| 服务端共享结构化数据 | PostgreSQL，结合 Supabase / Drizzle | 网页、移动与桌面多客户端共享数据的主要候选，不限于网页。PostgreSQL 是数据库；Supabase 是围绕它提供认证、存储、API、实时等能力的托管平台；Drizzle 是 TypeScript 环境的数据访问、结构定义与迁移工具。三者分别判断、按需组合；Flutter 等非 TypeScript 客户端通过 Supabase 对应 SDK 或后端 HTTP API 接入，Drizzle 留在 TypeScript 后端。 |

## 官方入口

链接于 2026-10-20 核对可访问；失效或迁移时只更新本表。

| 领域 | 技术 | 官网 | 文档入口 | 备注 |
|---|---|---|---|---|
| 轻量数据 | JSON | [json.org](https://www.json.org/) | [json.org](https://www.json.org/) | |
| 浏览器本地结构化数据 | IndexedDB | [W3C 规范](https://www.w3.org/TR/IndexedDB/) | [MDN IndexedDB API](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API) | 用法见 [Using IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB)。 |
| 应用本地结构化数据 | SQLite | [sqlite.org](https://sqlite.org/) | [Documentation](https://sqlite.org/docs.html) | |
| 服务端共享结构化数据 | PostgreSQL | [postgresql.org](https://www.postgresql.org/) | [Documentation](https://www.postgresql.org/docs/) | |
| 服务端共享结构化数据 | Supabase | [supabase.com](https://supabase.com/) | [Docs](https://supabase.com/docs) | Flutter 客户端见 [Flutter Client Library](https://supabase.com/docs/reference/dart/introduction)。 |
| 服务端共享结构化数据 | Drizzle ORM | [orm.drizzle.team](https://orm.drizzle.team/) | [Overview](https://orm.drizzle.team/docs/overview) | |

[返回技术偏好入口](./preferences.md)
