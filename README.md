# AI 八字命理分析平台

这是 AI 八字命理分析平台的 M0 Monorepo 工程骨架。当前仅包含 Web、API、Worker、平台基础能力和质量门禁，不包含业务逻辑、命理算法、AI、认证、支付或业务数据库结构。

## 工具版本

- Python 3.14.6
- Node.js 24.18.0 LTS
- TypeScript 6.0.x（锁文件固定精确版本）
- uv 0.11.x
- pnpm 11.9.0

## Workspace

- `apps/web`：Next.js Web Runtime。
- `apps/api`：FastAPI Runtime，仅提供健康检查。
- `apps/worker`：独立 Worker Runtime，仅支持启动与关闭。
- `packages/backend`：后端平台、Bootstrap、模块边界和 Projection 边界。
- `packages/contracts`：跨应用契约的空骨架。
- `packages/shared-kernel`：最小共享内核空骨架。
- `packages/ui`：前端 UI Package 空骨架。
- `packages/i18n`：简体中文与 RTL 预留基础。
- `tests`：跨系统、架构、契约和 E2E 测试入口。
- `infrastructure`：后续基础设施声明入口；M0 不绑定云平台。

目录不是 Bounded Context。任何领域边界仍以已批准 Architecture Baseline 为准。

## 开发环境

1. 使用 `.nvmrc` 选择 Node.js。
2. 使用 `.python-version` 选择 Python。
3. 使用 pnpm 的 Frozen Lockfile 安装 Node 依赖。
4. 使用 uv 的 Locked 模式同步 Python 依赖。
5. 本地仅使用合成测试数据；当前不需要数据库、Redis、Broker 或 AI Provider。

常用命令记录在 `scripts/README.md`，验证入口为 `scripts/verify.sh`。

## No Secret Policy

- 不得提交 `.env`、私钥、Token、密码或生产连接串。
- 仓库只允许提交无敏感值的 `.env.example`。
- 客户端可见环境变量不得包含服务端 Secret。
- 发现 Secret 必须立即停止、撤销凭证并按安全流程处理，不能只删除 Git 最新版本。

## 当前明确不包含

- 命理算法、Rule Engine、Evidence、AI Analysis、Prompt 或 Provider SDK；
- 登录、Token、支付、报告和高风险主题输出；
- 业务数据库 Schema、Migration 或真实用户数据；
- Broker、云平台或生产部署绑定。
