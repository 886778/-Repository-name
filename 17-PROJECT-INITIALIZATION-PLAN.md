# AI 八字命理分析平台：项目初始化计划

**文档编号：** 17  
**文档类型：** Project Initialization Plan  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md` 至 `16-GLOSSARY-AND-APPENDIX.md`（按当前正式决策均已 Approved）  
**适用阶段：** Architecture Baseline 完成后、任何项目初始化或业务编码开始前  
**目标读者：** CTO、架构师、工程负责人、前后端开发、测试、数据、安全、AI、平台与项目负责人

---

## Version 0.9 Change Log

- 首次将 Architecture Baseline 转换为项目初始化、工程骨架和首批 Backlog 方案。
- 推荐 Monorepo 作为初始仓库形态，但保留正式 Repository Topology 决策 Gate。
- 定义前端、后端、DDD 模块、数据库、异步、测试、CI 和本地环境初始化顺序。
- 将未决 ADR、命理专家、产品、安全、法律与运营事项分为初始化、模块、Beta 和 GA Gate。
- 给出 32 项首批可执行任务；任务仅描述工作，不在本轮执行。
- 本文件未初始化项目、Git 或目录，未生成代码、配置、脚本、数据库或迁移资产，也未修改 01～16。

---

## 1. Purpose and Scope

### 1.1 目标

本文档定义平台从“架构已批准”进入“工程可开工”所需的初始化顺序、责任、交付物和门禁。它把已有架构约束转化为可执行的项目准备任务，但不替代任何 Product、Domain、Data、Application、API、Technology、Security、AI、Testing 或 ADR Baseline。

### 1.2 范围

本文覆盖：

- Repository Topology 推荐与逻辑 Workspace；
- Python/FastAPI 与 TypeScript/Next.js 的初始化顺序；
- 模块化单体和 DDD 物理映射原则；
- PostgreSQL、Redis、Migration、Worker、Outbox/Inbox 的启动计划；
- 本地开发、测试结构和 CI Gate；
- 第一批工程里程碑和 Backlog；
- ADR Candidate、专家输入和发布 Gate 分类；
- 当前明确不得正式实现的范围。

### 1.3 不包含内容

本文不包含：

- 业务代码或测试代码；
- 实际 Git/Repository 初始化；
- 目录、虚拟环境、数据库、Schema 或服务创建；
- 依赖清单、锁文件、环境变量文件、Migration 或 CI 配置；
- Provider SDK、Prompt、AI 调用或命理算法实现；
- 对 01～16 的任何修改；
- 未经 ADR 批准的技术候选最终选择。

### 1.4 计划的权威边界

当本文与 01～16 存在差异时，以上游 Approved Baseline 为准。本文中的“推荐”需要在对应 Gate 获批后才能变为初始化动作；实现过程中发现重大架构变化时，先回到 ADR 流程。

### 1.5 No-Code Boundary

本轮只生成初始化计划。执行 M0、创建仓库、安装依赖、生成配置或开始编码，均需要后续明确授权。

---

## 2. Preconditions

### 2.1 已完成且可作为开工输入

- 产品愿景、SRS、系统架构、领域模型和数据模型已形成正式基线；
- Roadmap、Application、API、Technology 和 Engineering 约束已明确；
- Deployment、Security/Privacy、AI、Testing 和 ADR 治理已建立；
- Chart 已统一为确定性 Aggregate，RuleRun、EvidenceBundle、AIAnalysis、Report 生命周期独立；
- AnalysisProgress 已确认为只读 Projection；
- 后端技术方向为 Python、FastAPI、PostgreSQL、Redis、模块化单体、DDD 分层和异步 Worker；
- 前端技术方向为 TypeScript、Next.js、移动端优先、简体中文正式质量并预留 i18n/RTL；
- AI 正式调用必须经过 Model Gateway，业务模块不得直连 Provider；
- 测试金字塔、Release Gate、Security/Privacy 和 Immutable History 要求已明确；
- 当前项目目录为空白与否不构成本文件假设，本轮不进行初始化检查或变更。

### 2.2 待确认但不阻止纯工程规划

- Authentication Protocol、Token Strategy 和 MFA 具体机制；
- Restricted Sensitive 字段的字段级加密范围；
- AI Provider、Primary Model、Embedding 和 Reranker；
- Prompt Registry 的物理存储；
- Production Orchestration、Observability 和 Object Storage Vendor；
- 正式 SLO、RPO、RTO 和跨区域策略；
- 旺衰、格局、调候、用神、起运、神煞等专家规则；
- 黄金命例、边界命例和发布阈值；
- 高风险主题最终法律与产品边界。

### 2.3 初始化前必须关闭的工程决策

- Repository Topology：批准 Monorepo 或选择其他形态；
- Python/Node 支持版本和依赖管理方式；
- 测试框架与基础测试报告方式；
- ORM、Alembic/迁移、Repository 和 Unit of Work 组合；
- Worker/Broker 的初始开发模式与正式可靠消息边界；
- 最小 Secret、环境变量和本地服务隔离规则；
- Code Ownership 和首批模块 Owner。

这些决策只需满足工程初始化，不得顺带决定 AI Provider、生产云或未经确认的业务规则。

### 2.4 Definition of Ready for M0

M0 只有在 Repository Topology、工具链 Owner、代码审查规则、测试框架选择流程和无 Secret 原则获得批准后才可执行。

---

## 3. Repository Strategy

### 3.1 推荐方案：Monorepo

推荐第一阶段采用 Monorepo，作为待批准的 Repository Topology 方案。正式初始化前应通过对应 ADR/Triage Gate，不在本文件中把推荐冒充为已批准事实。

### 3.2 推荐原因

- MVP 是模块化单体，API 与 Worker 共享同一后端领域和应用基线；
- Web、API、Worker、Contracts、Tests 和 Docs 需要原子化兼容变更；
- 单一变更可以同时更新 API Contract、前端 Client、测试和文档；
- 统一 Lint、Type、Security、Dependency 和 Architecture Gate 更易建立；
- 团队和发布规模尚不足以证明多仓库协调成本合理；
- 未来拆分 Context 时，模块边界、制品边界和 Owner 已可作为迁移依据。

### 3.3 为什么当前不推荐多仓库

多仓库会提前引入 Contract 发布、跨仓版本、联调环境、Release Coordination 和权限管理复杂度。当前没有独立团队、独立发布节奏、合规隔离或规模证据要求这样做。

### 3.4 Monorepo 约束

- Monorepo 不等于共享业务模型；
- API 与 Worker 是 Runtime Entry Point，不是独立 Bounded Context；
- Context 私有代码不得因同仓库而被其他 Context 直接导入；
- 前端不得复制后端命理规则；
- `shared` 仅容纳稳定、无业务所有权的最小能力；
- 每个顶层区域和 Context 必须有 Owner；
- 制品可独立构建，但版本兼容由同一 Release Manifest 管理。

### 3.5 顶层区域

| Area | Purpose | Forbidden Content |
|---|---|---|
| `apps` | 可运行入口：Web、API、Worker | 共享领域实现、生产 Secret |
| `packages` | 后端核心、公共 Contract、UI/i18n 等受控 Package | 无边界业务杂物 |
| `docs` | 01～17、未来 ADR、模块说明与运行文档 | 未批准设计冒充基线 |
| `infrastructure` | 后续获授权的环境与基础设施声明 | 业务领域规则 |
| `tests` | 跨应用 Contract、Architecture、E2E、Performance 测试 | 真实生产敏感数据 |
| `scripts` | 后续获授权的非业务开发工具入口 | 绕过应用的数据修改工具 |

### 3.6 Repository Decision Gate

批准 Monorepo 时应记录：Owner、制品边界、权限、版本、构建影响、未来拆分触发条件和回退成本。若未批准，保留 10 中逻辑 Workspace，不执行物理初始化。

---

## 4. Proposed Directory Structure

以下目录树仅为建议，不在本轮创建：

- `apps/`
  - `web/`：Next.js 第一方 Web Runtime 与 Composition；
  - `api/`：FastAPI HTTP Runtime、Router 装配和进程生命周期入口；
  - `worker/`：异步 Worker Runtime、Consumer 与 Scheduler 入口。
- `packages/`
  - `backend/`
    - `src/bootstrap/`：Composition Root、依赖装配、运行生命周期；
    - `src/modules/`：按 Bounded Context 组织的模块化单体核心；
    - `src/projections/`：AnalysisProgress 等只读 Projection Builder；
    - `src/platform/`：配置、日志、错误、数据库、Redis、消息和 Observability Adapter；
  - `contracts/`：API、Event、Problem/Error Registry 等稳定契约源；
  - `shared-kernel/`：极小的 Identity、Version、Clock、Correlation 等批准共享原语；
  - `ui/`：跨页面、无业务规则的 UI 基础组件；
  - `i18n/`：语言资源契约、术语和 RTL 基础能力。
- `docs/`
  - `architecture/`：已批准架构文档的逻辑归属；
  - `adr/`：未来获授权后的正式 ADR；
  - `modules/`：模块边界和公共契约说明；
  - `runbooks/`：后续运行手册。
- `infrastructure/`
  - `local/`：后续本地环境声明；
  - `environments/`：后续环境差异与部署声明；
  - `observability/`：后续日志、指标、追踪声明。
- `tests/`
  - `architecture/`：层次、Context、依赖和禁用导入；
  - `contract/`：API、Event、Repository、Provider Contract；
  - `integration/`：跨 Runtime/Adapter 验证；
  - `e2e/`：关键用户旅程；
  - `performance/`：容量与性能基线；
  - `security/`：安全与隐私专项测试资产。
- `scripts/`
  - `development/`：后续无业务语义的本地辅助入口；
  - `quality/`：后续质量检查入口；
  - `operations/`：后续受控运维辅助入口，不包含直接生产数据修改。

### 4.1 Context 内部建议结构

每个后端 Context Module 采用：

- `domain/`：Aggregate、Entity、Value Object、Domain Service、Factory、Repository Port、Domain Event；
- `application/`：Command、Query、Handler、Policy、Process Port 和应用结果；
- `infrastructure/`：Persistence、Cache、Message、Search、Object、Provider Adapter；
- `interface/`：HTTP/Event/Scheduler Adapter；
- `tests/`：该 Context 的 Unit、Domain、Application 和 Adapter Test。

### 4.2 Directory Is Not Domain

目录只是物理组织方式，不自动形成 Bounded Context、Aggregate 或事务边界。领域边界以 04、05、07 为准；不得为适配目录树而合并或拆分 Context。

### 4.3 Shared-Kernel Gate

共享原语必须稳定、无具体业务状态、由至少两个真实用例证明。Chart、RuleFinding、Evidence、Consent、AI 内容和 Report 不得进入共享内核。

---

## 5. Backend Initialization Plan

### 5.1 初始化顺序总览

1. 锁定 Python 支持版本、依赖管理和 Package Boundary；
2. 建立后端核心 Package 与 API/Worker Composition Root；
3. 建立配置 Schema 和 Secret Reference 边界；
4. 建立依赖注入与 Port/Adapter 装配规则；
5. 建立结构化日志、Correlation 和敏感数据过滤；
6. 建立 Problem/Error Registry 与异常映射；
7. 建立 PostgreSQL 连接、事务和 Health Port；
8. 建立 Redis Adapter 与非 Source-of-Truth 约束；
9. 建立 Migration 框架与检查流程；
10. 建立 Worker、Broker Port、Outbox/Inbox 和幂等骨架；
11. 建立 Liveness、Readiness、Dependency Health；
12. 建立测试目录、Fixture、隔离和首个 Architecture Test；
13. 才允许进入首个纵向业务 Slice。

### 5.2 Python Environment

- 选择受支持且安全维护的 Python 版本并在所有环境锁定；
- 明确依赖管理、锁定、虚拟环境和升级 Owner；
- Runtime、Development、Test 依赖分层；
- 禁止全局环境或未锁定依赖作为团队标准；
- 版本改变需兼容、性能与安全验证。

本计划不选择具体依赖管理工具，也不生成环境。

### 5.3 FastAPI Project

- `apps/api` 仅作为 HTTP Runtime 和 Composition Entry；
- Router 按 Context Interface Adapter 显式注册；
- Route 只解析协议、建立安全/追踪上下文、调用应用用例并映射结果；
- Domain 不依赖 FastAPI、HTTP、ORM 或 Provider 类型；
- API Version、Problem Details、Idempotency 和 Security Header 继承 08/12。

### 5.4 Configuration Management

- 使用类型化、分层、可验证的配置 Schema；
- 区分 Build-time、Deploy-time、Secret 和动态 Policy；
- 默认值只允许用于安全本地场景，生产必需配置缺失时 Fail Closed；
- Config 不承载命理规则、Prompt 正文或未审计权限；
- 启动日志只记录安全配置摘要和版本，不记录 Secret。

### 5.5 Dependency Injection

- Composition Root 是 Adapter 装配的唯一入口；
- Domain/Application 依赖 Port，不依赖容器或框架；
- 生命周期明确区分 Singleton、Process、Request、Transaction 和 Task Scope；
- 禁止 Service Locator、隐式全局容器和跨 Context Repository 注入；
- 具体 DI 工具保持 Candidate，先批准再配置。

### 5.6 Logging

- 从第一天采用结构化日志；
- 标准字段包含 Time、Level、Service/Runtime、Environment、RequestId、CorrelationId、TraceId、Operation、ErrorCode 和安全主体摘要；
- 默认不记录 BirthInput、Conversation、Prompt、AI Raw Output、Token、Secret 或完整报告；
- 日志与 AuditEvent 分离；
- Redaction 失败按安全缺陷处理。

### 5.7 Error Handling

- 建立平台错误分类、Problem Details 映射和稳定错误码 Registry；
- 区分 Validation、Authorization、Conflict、Retryable Dependency、Non-Retryable、Rate、Privacy 和 Internal；
- 不暴露堆栈、SQL、Provider Raw Error 或内部路径；
- Worker 与 API 共享错误语义但不共享传输表现；
- 未映射异常进入安全默认错误并产生关联证据。

### 5.8 Database Connection and Transaction

- 连接池、Timeout、Read/Write 与事务范围显式；
- 一个 Command 默认修改一个 Aggregate Root；
- Repository 按 Context/Root 隔离；
- ORM 类型不得进入 Domain；
- 权限/Consent 关键读取不依赖允许延迟的副本；
- 启动不得自动执行生产 Migration。

### 5.9 Redis

- 首期用于 Cache、Rate Limit、短期协调和可丢状态；
- Key 必须包含环境、Tenant/User/Chart、用途和版本边界；
- Redis 不保存唯一正式业务状态；
- Redis 不可用时回源、限流或降级，不放宽授权；
- AI 私人 Context 不跨用户复用。

### 5.10 Alembic and Migration

推荐以 Alembic 作为 Python/PostgreSQL Migration 候选默认方案，最终选择需与 ORM、Repository 和 Unit of Work 组合一并批准。初始化计划要求：

- Migration 独立执行，不作为 API 启动副作用；
- 采用 Expand–Migrate–Contract 原则；
- 每个 Migration 有 Owner、风险、兼容、验证和回退/前滚计划；
- 禁止修改 Frozen/Published/Completed 历史语义；
- 危险操作在 CI 和 Staging 演练中阻断；
- 不允许直接手工修改生产 Schema。

### 5.11 Worker

- `apps/worker` 只提供 Runtime Entry，不复制业务逻辑；
- Worker 调用同一 Application/Domain Package；
- Broker、Scheduler 与 Task Framework 通过 Port/Adapter；
- 任务 Payload 只携带稳定 Identity、Version、Purpose 和 Correlation；
- Worker 重载权威状态并重验授权/前置条件；
- Retry、Timeout、Circuit、DLQ、幂等和并发预算显式；
- AI/Report 等正式长任务不得依赖进程内临时任务。

### 5.12 Health Checks

- Liveness 只判断进程是否应重启；
- Readiness 判断是否可接受相应正式流量；
- Dependency Health 分别报告 PostgreSQL、Redis、Broker、Object、AI 等状态；
- AI Provider 不可用不应让确定性排盘 Runtime 整体 Not Ready；
- Health 不返回 Secret、拓扑或敏感业务数据。

### 5.13 Test Framework Gate

首日必须建立测试结构，但具体 Python 测试框架、Fixture、并发和报告组合属于 `ADR-CANDIDATE-TEST-001`。批准前可以完成测试目录与测试策略，不创建工具配置或正式 Runner。

---

## 6. Frontend Initialization Plan

### 6.1 初始化顺序

1. 锁定 Node/TypeScript/Next.js 支持版本和依赖管理；
2. 建立 App Router/路由边界和全局 Layout；
3. 建立 Design Token、移动端断点和可访问性基础层；
4. 建立受控 API Client 与 Correlation/Error 处理；
5. 建立 Server/Client State 边界；
6. 建立表单、验证、时间精度和不确定性组件；
7. 建立简体中文资源与术语；
8. 建立 Locale/RTL 方向抽象；
9. 建立 Component、Contract 和 E2E 测试结构；
10. 才进入首次用户旅程页面实现。

### 6.2 Next.js and TypeScript

- Next.js 是第一方 Web Framework；TypeScript 用于前端类型安全；
- Framework 不承载命理规则或后端领域真相；
- Server/Client Boundary 明确，Secret 不进入浏览器 Bundle；
- Route 与 Feature 按用户旅程组织，不复制 Bounded Context 内部模型；
- 版本升级遵守兼容、安全、性能和构建门禁。

### 6.3 Routing

首期路由按公开入口、匿名排盘、结果、对话、报告、账户、数据权利和后台入口分区。路由只表达导航和授权入口，不等同 API Resource 或 Aggregate。

### 6.4 UI Foundation

- 移动端优先；
- 提供键盘、焦点、语义、对比度、Reduced Motion 和辅助技术基础；
- Chart/Timeline 可视化必须有等价文本；
- 不只靠颜色表达 EvidenceStatus、Risk 或错误；
- 专业依据可展开，普通用户首屏保持通俗。

### 6.5 API Client

- 单一受控 Client 层管理 Base URL、API Version、RequestId、Correlation、认证、超时和 Problem Details；
- 不直接拼接内部数据库或 Aggregate 字段；
- Command 与 Query 方法语义分开；
- 重试只针对批准的安全/幂等请求；
- Client 不缓存权限为永久事实。

### 6.6 Error Handling

- 统一映射稳定错误码到本地化、安全、可恢复的用户消息；
- 明确区分输入错误、处理中、投影延迟、限流、AI 降级、无权限和系统故障；
- 不显示堆栈、Provider 或内部路径；
- Error Boundary 不掩盖未保存表单和隐私提示。

### 6.7 State Management

- Server State、Form Draft、UI State、Session View 和 Async Operation 分离；
- 正式 Chart、Evidence、AIAnalysis、Report、Consent 状态来自 API；
- AnalysisProgress 只用于展示，不成为写入决定来源；
- 不引入全局可变业务 Store；
- 新状态库需真实跨 Feature 需求和 Owner。

### 6.8 Forms

- 表单支持时间精度、不确定性、地点歧义、时区、真太阳时和换日说明；
- 客户端验证用于体验，服务端始终重验；
- 不自动补造出生信息；
- 敏感字段不进入 URL、Analytics、错误或浏览器长期存储；
- 保存前明确用户确认和 Purpose。

### 6.9 i18n and RTL

- MVP 正式语言为简体中文；
- 从第一天使用 Locale Key，而非把中文散落为不可替换常量；
- 日期、数字、时区、术语和错误消息通过本地化边界；
- 布局使用逻辑方向属性，为 RTL 预留；
- 英文/阿拉伯语在人工和专业复核前不标记正式质量。

### 6.10 Frontend Testing

建立纯函数/组件、可访问性、API Contract、Form Boundary、状态、路由和关键 E2E 的测试位置。具体工具需 Test Framework Gate，不在本计划选型。

---

## 7. DDD Module Bootstrap

### 7.1 Bootstrap 原则

- Module 依照 Bounded Context，不依照页面或数据库表随意拆分；
- 每个 Module 先建立 Ownership、Public Contract 和依赖规则；
- 骨架仅包含稳定身份、Port、层次和禁止依赖，不填充未批准业务规则；
- API/Worker Runtime 不成为新的业务 Module；
- Operations/AnalysisProgress 是应用/查询能力，不成为跨 Context Aggregate。

### 7.2 首阶段模块清单

| Module | Context Mapping | Bootstrap Scope | 可立即实现 | 必须等待 |
|---|---|---|---|---|
| Identity / Account | Identity | User/Actor 边界、Port、生命周期骨架 | 模块、Identity 原语、授权 Port | Authentication Protocol、Token/MFA |
| Consent | Consent | SubjectConsent、追加记录与 Purpose/Scope Port | 聚合不变量和接口骨架 | 法律文案、Retention 细节 |
| Subject / BirthProfile | Birth | BirthProfile/BirthInput 边界、精度模型 | 容器与确认流程骨架 | Field Encryption、最终时间口径 |
| Chart Calculation | Calendar & Time + Chart Calculation | Chart/Snapshot/Algorithm Port、确定性生命周期 | Aggregate 骨架、状态与版本约束 | 权威算法、黄金命例、边界口径 |
| Rule Evaluation | Rule Evaluation | RuleSet/RuleRun/Finding Port 与生命周期 | 版本、发布、Run 骨架 | 旺衰、格局、用神、神煞等规则 |
| Evidence | Evidence | Bundle/Evidence/策略 Port 与冻结不变量 | 冻结、版本和引用骨架 | 证据等级判定、首批规则映射 |
| Knowledge | Knowledge | Article/Version/Rights/Query Port | 发布生命周期和 Rights 骨架 | 首批来源、Embedding/Reranker |
| AI Analysis | AI | Gateway Port、Analysis/Conversation 边界 | Gateway/Registry/Validation 接口骨架 | Provider、Model、Prompt Storage、正式逻辑 |
| Report | Report | Report/VersionManifest/Freeze Port | 生命周期与不可变骨架 | 正式内容模板、AI/规则输入 |
| Audit | Audit | AuditEvent Port、最小字段、追加约束 | 可立即实现基础审计能力 | 正式存储/归档与法律期限 |
| Operations / AnalysisProgress | Application/Operations | Operation、Projection、Correlation、Health | 可立即实现只读骨架 | Broker/Orchestration 具体实现 |

### 7.3 Recommended Bootstrap Order

1. Shared primitives：Identity、Version、Clock、Correlation；
2. Audit 与 Platform Error；
3. Identity/Consent/Birth Module Shell；
4. Chart Calculation Shell；
5. Outbox/Inbox、Operation、AnalysisProgress；
6. Rule/Evidence/Knowledge Shell；
7. AI Gateway/Analysis Shell；
8. Report Shell；
9. 首个允许的纵向 Slice。

### 7.4 Immediate Implementation Boundary

“可立即实现”仅表示获得下一轮编码授权后可实施，不表示本轮执行。立即范围限于架构骨架、稳定不变量和通用平台能力；任何正式命理结论、模型绑定或高风险输出继续阻断。

### 7.5 Module Dependency Guard

初始化时即建立 Architecture Test：Domain 不依赖 Framework；Context 不导入他 Context 私有代码；API/Worker 只经 Application；Projection 不写 Aggregate；AI 业务模块不直连 Provider。

---

## 8. Database Bootstrap

### 8.1 PostgreSQL Initialization

项目执行阶段先建立本地与测试 PostgreSQL，生产实例不属于 M0。数据库 Bootstrap 必须可重复、可销毁、无真实用户数据，并记录数据库版本和扩展需求。

### 8.2 Schema and Ownership Principles

- 一个 PostgreSQL 实例可以承载多个 Context，但逻辑所有权必须清晰；
- 每个 Context 只通过自己的 Repository/Adapter 读写所属数据；
- 禁止跨 Context ORM Relation、直接写表或共享 God Repository；
- Projection 使用独立读模型语义，不拥有源状态；
- Audit、Outbox、Inbox 具有独立访问和保留边界；
- Schema/Namespace 具体映射由 ORM/Migration 决策确认。

### 8.3 Migration Rules

- 所有 Schema 变化只通过已批准 Migration 流程；
- Migration 文件不可在已部署后原地修改；
- 每次变更包含升级、兼容验证和回退/前滚说明；
- 先 Expand，再数据迁移，最后 Contract；
- 长回填分批、限速、幂等并可中断；
- 生产 Migration 独立执行并受审批，不随应用启动；
- 禁止直接手工修改生产 Schema。

### 8.4 Identity and Version

- Identity 全局唯一、无业务含义、不可重用；
- Identity 不编码时间、地区、状态或 Version；
- SnapshotId 与 SnapshotSequence、ReportId 与 ReportOrdinal、RuleSetId 与 RuleSetVersion 分离；
- Published/Frozen/Completed 内容不原地更新；
- Version Manifest 能追踪所有影响正式结果的版本。

### 8.5 Initial Migration Order

建议只描述依赖顺序，实际 Migration 需后续生成：

1. 平台 Identity/Version/Correlation 基础类型与必要约束；
2. Context 所属 Aggregate Root 最小持久化结构；
3. AuditEvent 追加式结构与权限边界；
4. Outbox 可靠事件记录；
5. Inbox 消费去重记录；
6. Operation/Process 状态与 Projection Checkpoint；
7. 各业务 Context 按已批准里程碑逐步增加；
8. Index、Search/Vector Projection 在来源稳定后建立。

### 8.6 Audit and Outbox Order

Audit 与 Outbox 必须在第一个可改变正式状态的业务 Command 之前可用。关键操作的业务提交、Audit 意图和待发布 Event 采用批准的本地事务策略，不能后补为不可靠日志。

### 8.7 Test Database Strategy

- Unit/Domain Test 不依赖数据库；
- Repository/Integration Test 使用隔离、可重置的真实 PostgreSQL 语义环境；
- 每个测试运行使用独立数据库或逻辑 Namespace；
- Migration 从空库执行，并验证升级和必要回退；
- Fixture 全部合成，黄金命例另行版本治理；
- 生产数据不得复制到本地或普通 CI。

### 8.8 Database Gate

ORM/Migration/UoW 决策、首个 Schema Review、字段级加密范围和测试隔离方案批准后，才可创建正式持久化实现。

---

## 9. Local Development Environment

### 9.1 必需软件类别

- 受支持的 Python Runtime 和依赖管理工具；
- 受支持的 Node Runtime 和前端依赖管理工具；
- PostgreSQL Client/Server 或批准的隔离运行方式；
- Redis Client/Server 或批准的隔离运行方式；
- Git Client（仅在获得初始化授权后使用）；
- 编辑器与格式/类型/测试工具；
- 可选本地容器运行能力，但本计划不生成容器配置；
- 证书、Secret 或云 CLI 只在对应环境和批准后引入。

### 9.2 Environment Variables

- 定义变量名称、类型、必需性、环境范围和 Secret 分类；
- 示例只使用无效占位符；
- 本地 Secret 存在未跟踪、受权限保护的 Secret Store 或环境；
- 禁止提交 `.env` 实值、Token、Key 或生产连接；
- 启动时验证缺失/冲突，生产不使用不安全默认值；
- 变量命名不复用系统保留或通用敏感变量。

### 9.3 Local PostgreSQL and Redis

- 使用与目标生产语义兼容的版本；
- 每个开发者/工作区隔离数据库、缓存前缀和端口；
- 数据可销毁、可重建，不含真实命例；
- Redis 清空不得破坏正式本地数据库状态；
- Migration 是创建 Schema 的唯一入口。

### 9.4 Worker

本地 Worker 以独立进程运行，使用开发队列/Adapter；必须能测试重启、重复消息、失败和幂等。不能以 API 进程内后台任务替代正式 Worker 语义。

### 9.5 Recommended Start Order

1. 验证本地配置与 Secret；
2. 启动 PostgreSQL；
3. 执行已批准本地 Migration；
4. 启动 Redis 和开发 Broker/Adapter；
5. 启动 API；
6. 启动 Worker；
7. 启动 Web；
8. 运行 Health/Contract Smoke；
9. 加载允许的合成 Seed。

### 9.6 One-Command Start

后续可以提供一个统一开发入口，负责前置检查、服务启动、Health 等待和安全退出。它不得：自动创建生产资源、写入 Secret、执行未批准危险 Migration、下载真实数据或隐藏失败。具体脚本/工具本轮不生成。

### 9.7 Seed Data Boundary

- 只使用合成用户、Subject、BirthInput 和最小生命周期数据；
- 不含真实姓名、联系方式、详细地址、命例、Prompt 或 Provider 输出；
- 专家黄金命例由独立受控 Dataset 引入，不作为普通 Seed；
- Seed 具有版本并可重复；
- 禁止 Seed 创建 Frozen/Published 事实以绕过正式流程，除非为明确测试 Fixture。

### 9.8 Secret Management

- 本地、CI、Staging、Production Credential 完全隔离；
- Secret 最小权限、可轮换、有 Owner；
- 不进入代码、日志、Prompt、测试报告或浏览器；
- Provider 尚未批准前不创建正式 Provider Credential；
- 泄漏时立即撤销并按 Incident 流程处理。

---

## 10. Testing Bootstrap

### 10.1 Day-One Rule

测试结构、Fixture 原则、Architecture Boundary 和最小 Gate 与项目骨架同时建立，不能等业务完成后补测试。

### 10.2 Test Layers

| Layer | Initialization Deliverable | First Scope |
|---|---|---|
| Unit | 快速隔离测试位置与命名规则 | Error、Version、Clock、Config Validation |
| Domain | 每 Context Domain Test 结构 | Identity、Value Object、状态不变量 |
| Application | Command/Query/Policy/Saga 测试结构 | 授权 Port、事务结果、幂等 |
| Integration | PostgreSQL/Redis/Message Adapter Harness | 连接、事务、Repository、Cache Miss |
| Contract | API/Event/Repository/Provider Contract 区域 | Problem Details、Event Envelope |
| API | FastAPI Test Boundary | Health、错误、Correlation、Version |
| Frontend | Component/State/API Client 测试结构 | 错误、i18n、Form Primitive |
| E2E | 最小关键旅程框架 | Health 与匿名入口 Smoke；不实现命理旅程 |
| Architecture | 依赖和禁用规则 | Layer、Context、Provider Direct Call 禁令 |
| Security | Secret/Dependency/权限负向结构 | 无 Secret、默认拒绝、敏感日志 |

### 10.3 Unit and Domain

不访问网络、数据库或当前系统时钟。领域对象不被 Mock；Clock、Identity 和外部 Port 可控。每个稳定不变量至少有正向、负向和边界场景。

### 10.4 Integration and Contract

真实 PostgreSQL/Redis 语义验证不能由 Mock 替代。API/Event/Provider Contract 与实现分离；Provider 未选型前测试 Model Gateway Port 和受控 Simulator，不调用真实模型。

### 10.5 Frontend and E2E

首日覆盖移动端基础、i18n Key、RTL Direction、Problem Details 和 API Client。完整匿名排盘 E2E 必须等待允许的确定性计算 Slice 和专家样例。

### 10.6 Architecture Tests

最低规则：

- Domain 不依赖 Application/Infrastructure/Interface；
- Application 不依赖 Adapter 实现；
- Context 不访问其他 Context 私有 Module；
- API/Worker 不含领域规则；
- ORM/Provider SDK 不进入 Domain；
- AI 调用只能经 Model Gateway；
- AnalysisProgress 不写任何 Aggregate；
- Frontend 不实现正式命理规则。

### 10.7 Test Framework Decision

框架选型需比较语言生态、并行、异步、Fixture、报告、IDE、维护和安全。决策应在 M0 关闭；未关闭前可设计结构与 Acceptance，但不生成框架配置。

---

## 11. CI Bootstrap

### 11.1 CI 原则

CI 从第一个可合并变更起生效。具体供应商和配置格式不在本文选择或生成；所有 Gate 必须在本地可复现，CI Credential 最小权限且不接触生产数据。

### 11.2 Initial Pipeline Stages

| Gate | Purpose | Blocking Rule |
|---|---|---|
| Repository Hygiene | 禁止 Secret、生成物和临时文件 | 违规阻断 |
| Format | 统一格式来源 | 差异阻断 |
| Lint | 常见缺陷、复杂度和禁用模式 | 新违规阻断 |
| Type Check | Python/TypeScript 公共边界与空值安全 | 关键错误阻断 |
| Architecture Test | Layer、Context、Provider Boundary | 任一违规阻断 |
| Unit/Domain Test | 核心逻辑与不变量 | 失败阻断 |
| Migration Check | 空库升级、Head 一致、危险操作 | 失败或未批准风险阻断 |
| Security Scan | Secret、静态风险和敏感输出 | 高风险阻断 |
| Dependency Scan | 漏洞、许可证、过期与锁文件 | 未接受高风险阻断 |
| Build | Web/API/Worker 可重复制品 | 构建失败阻断 |
| Contract Test | API/Event/Repository Compatibility | Breaking 未治理则阻断 |
| Integration Smoke | PostgreSQL/Redis/Worker 基础语义 | 关键失败阻断 |

### 11.3 Pipeline Evolution

后续按里程碑增加 Golden、AI Evaluation、RAG、E2E、Accessibility、Performance、Recovery 和 Supply Chain Gate。未存在相应业务能力时不得用空测试制造假绿。

### 11.4 CI Data and Secrets

只使用合成 Fixture、短期 Credential 和隔离服务。CI 日志/Artifact 不含 Secret、PII、Prompt 或完整 AI 输出；失败证据按 Retention 和访问控制保存。

### 11.5 Migration Gate

每次 Schema 变更验证单一 Head、从空库升级、从当前基线升级、回退/前滚说明和不可变历史影响。CI 不连接生产数据库。

---

## 12. First Implementation Milestones

### M0 — Repository Bootstrap

- **目标：** 建立可审查、可构建、可测试的物理 Workspace。
- **输入：** Approved Architecture Baseline；Repository Topology、工具链和 Owner 决策。
- **输出：** 仓库、逻辑目录、Ownership、基础文档入口、依赖管理和最小质量 Gate。
- **完成标准：** Web/API/Worker 空 Runtime 可独立构建；Architecture Test、Format、Lint、Type、Unit Gate 可运行；无业务功能和 Secret。
- **专家依赖：** 否。
- **阻断：** Monorepo/Polyrepo、Test Framework、Python/Node 工具链未批准。

### M1 — Platform Foundation

- **目标：** 建立 Config、DI、Error、Log、Health、PostgreSQL、Redis 和 Migration 基础。
- **输入：** M0；ORM/Migration/UoW、配置与本地隔离决定。
- **输出：** Platform Port/Adapter、连接与事务边界、Health、空库 Migration、测试数据库 Harness。
- **完成标准：** API/Worker 启动与关闭可验证；数据库/Redis 故障行为明确；日志无敏感信息；Migration Gate 通过。
- **专家依赖：** 否。
- **阻断：** ORM/Migration 组合、Field Encryption 对首批敏感字段的决定。

### M2 — Identity and Consent

- **目标：** 建立账户、Actor/Subject、Purpose/Scope、Consent 追加历史和授权 Port。
- **输入：** M1；Authentication/Token 设计 Gate；Consent 基线。
- **输出：** Identity/Consent Module、Audit 事件、最小 API/Application Contract 和测试。
- **完成标准：** 默认拒绝、同一 Purpose/Scope 单一当前决定、追加历史、撤回传播意图和审计可验证。
- **专家依赖：** 否；需要产品、法律、安全输入。
- **阻断：** 正式认证流程依赖 Authentication Protocol/Token；纯 Domain Shell 可先行。

### M3 — BirthProfile and Chart Skeleton

- **目标：** 建立 BirthProfile、BirthInput、Chart、CalculationSnapshot 的边界与确定性状态机骨架。
- **输入：** M1/M2；Chart Baseline Correction；TimePrecision 与数据保护规则。
- **输出：** Module/Port、生命周期、不变量、Repository Contract、合成 Fixture 和 Architecture Test。
- **完成标准：** Chart 只含 Draft→Validating→Validated→Calculating→Calculated→Archived；下游状态不能写回；尚不产生正式命盘事实。
- **专家依赖：** 骨架否；正式 Calculation 是。
- **阻断：** 敏感字段持久化需 Field Encryption 决定；算法行为需专家口径。

### M4 — Operations and Async Foundation

- **目标：** 建立 Audit、Outbox/Inbox、Operation、Worker、幂等、Correlation 和 AnalysisProgress 骨架。
- **输入：** M1；Broker/Worker 初始实现决定。
- **输出：** 可靠事件 Port、消费去重、任务状态、Projection Checkpoint、故障测试结构。
- **完成标准：** 重复/乱序/重启不产生重复正式效果；AnalysisProgress 只读且不驱动流程；AI/Report 仍为接口骨架。
- **专家依赖：** 否。
- **阻断：** Broker/Task Framework 选型；本地可使用批准的 Simulator 验证语义。

### M5 — Deterministic Calculation Preparation

- **目标：** 在不实现未批准规则的情况下，完成算法 Port、版本、黄金 Dataset 流程和交叉验证 Harness。
- **输入：** M3/M4；专家算法范围、权威数据、黄金命例和边界口径。
- **输出：** AlgorithmVersion 发布流程、Calculation Adapter Contract、Golden/Boundary Test Harness 和 VerificationBlocked 流程。
- **完成标准：** 所有样例具备来源、版本、期望和专家批准；尚未批准算法不会进入 Published 或正式计算。
- **专家依赖：** 是，强依赖。
- **阻断：** 命理算法口径和黄金命例未批准。

### 12.1 Milestone Dependency

`M0 → M1 → M2/M3 → M4 → M5`。M2 与 M3 的非持久化 Shell 可部分并行；M4 依赖 M1 事务基础；M5 不得绕过专家 Gate。

---

## 13. Development Gate Classification

### 13.1 Gate 定义

| Gate | Meaning |
|---|---|
| 项目初始化前阻断 | 未关闭则不得创建正式仓库/工具配置或首个合并基线 |
| 模块启动前阻断 | 不阻止 M0/M1，但阻止相应模块正式实现或持久化 |
| Beta 阻断 | 可开发和内部验证，但不得开放 Beta 用户 |
| GA 阻断 | 可进入受控 Beta/RC 条件流程，但不得正式公开发布 |

### 13.2 Candidate Classification

| Topic | Classification | Blocks | Does Not Block | Required Decision/Evidence |
|---|---|---|---|---|
| Repository Topology | 项目初始化前阻断 | M0 物理初始化 | 本计划评审 | Monorepo/Polyrepo ADR/Triage |
| Test Framework Selection | 项目初始化前阻断 | 正式测试 Runner/CI 配置 | 测试结构设计 | Framework Evaluation |
| Python/Node Dependency Tooling | 项目初始化前阻断 | 锁文件与依赖安装 | 逻辑目录计划 | 支持版本、Owner、Security |
| Authentication Protocol | 模块启动前阻断 | Identity 登录/恢复实现 | Identity Domain Shell | Security/Identity ADR |
| Token Strategy | 模块启动前阻断 | Session/Token/API Auth 实现 | Authorization Port | JWT/Opaque/Hybrid ADR |
| Field Encryption | 模块启动前阻断 | Restricted Sensitive 字段正式持久化 | 无敏感数据骨架 | Threat/Data/Performance Review |
| ORM/Migration/UoW | 模块启动前阻断 | 正式 Repository/Migration | Domain/Application Shell | Implementation ADR/Triage |
| Worker/Broker Framework | 模块启动前阻断 | 可靠异步 Adapter | Port、Simulator、Operation Model | Reliability/Operations Review |
| AI Provider | 模块启动前阻断 | 正式 Provider Adapter/调用 | Model Gateway Port | Provider Security/Privacy/Cost Review |
| Primary Model | 模块启动前阻断 | 正式 AI Route | Registry/Analysis Shell | Evaluation + Compatibility |
| Embedding Model | 模块启动前阻断 | 正式 Vector Index/RAG | Knowledge/Retrieval Port | Retrieval/Privacy Evaluation |
| Prompt Registry Storage | 模块启动前阻断 | 正式 Prompt 持久化/发布 | Registry Contract | AI/Security/Operations Decision |
| 命理算法口径 | 模块启动前阻断 | 正式 Calculation/Rule Logic | Chart/Rule Shell | 专家批准与版本定义 |
| 黄金命例 | 模块启动前阻断 | Published Algorithm/Rule Gate | Test Harness | 来源、版权、专家预期 |
| 高风险主题边界 | Beta 阻断 | 对外 AI/Report 高风险主题 | 低风险骨架与拒绝默认 | Product/Legal/Security Policy |
| AI Provider Legal Terms | Beta 阻断 | 真实用户数据调用 | 去标识 Simulator | Region/Retention/Training/Contract |
| Production Orchestration | Beta 阻断 | Staging/Beta 运行平台 | 本地 Runtime | Platform ADR、Security、Cost |
| Observability/Object Vendor | Beta 阻断 | Beta 运行与 Incident 能力 | 本地结构化 Telemetry | Vendor/Region/Retention Review |
| Data Retention Values | Beta 阻断 | 真实用户持久化策略 | 可配置生命周期骨架 | Product/Legal/Privacy Approval |
| Formal SLO / RPO / RTO | GA 阻断 | 正式服务承诺与 DR Gate | 已批准测试基线 | Baseline Window + Joint Approval |
| Cross-Region Deployment | GA 阻断；当前默认不做 | 多区域 GA | 单区域 MVP | Legal/Data/Cost/DR ADR |
| English/Arabic Content Review | 对应语言上线阻断 | 英/阿正式发布 | 简体中文 MVP | 人工术语与法律复核 |

### 13.3 Gate Escalation

一个 Candidate 可以因数据、供应商或范围变化升级到更早 Gate，但不能由实现人员自行降级。任何“临时默认”都有 Owner、期限、限制和禁止生产使用说明。

---

## 14. First Backlog

以下 32 项是项目初始化获授权后的首批候选任务，不在本轮执行。

| ID | Task | Owner Role | Dependency | Acceptance Criteria | Blocking Status |
|---|---|---|---|---|---|
| INIT-001 | 批准 Repository Topology | CTO / Architecture | 17 Review | 明确 Monorepo/Polyrepo、制品、Owner、拆分触发 | 初始化阻断 |
| INIT-002 | 确认 Code Ownership | Engineering Lead | INIT-001 | 顶层区域与 Context 均有主/备 Reviewer | 初始化阻断 |
| INIT-003 | 锁定 Python/Node 支持版本 | Backend/Frontend Leads | INIT-001 | 支持期、安全、升级和开发环境一致 | 初始化阻断 |
| INIT-004 | 决定依赖管理与锁定方式 | Engineering Lead | INIT-003 | Runtime/Dev/Test 分层，锁文件可审查 | 初始化阻断 |
| INIT-005 | 决定测试框架组合 | QA / Engineering | INIT-003 | 覆盖异步、Fixture、报告、IDE、维护评估 | 初始化阻断 |
| INIT-006 | 建立 Monorepo 物理骨架 | Engineering Lead | INIT-001～005 | 仅批准目录和入口，无业务代码/Secret | 待授权可执行 |
| INIT-007 | 建立 Architecture Boundary 规则 | Architect / QA | INIT-006 | Layer、Context、Provider 禁令可自动验证 | 待授权可执行 |
| INIT-008 | 建立 Format/Lint/Type 基线 | Engineering Leads | INIT-006 | 本地可复现，首个变更即阻断违规 | 待授权可执行 |
| INIT-009 | 建立 CI 最小 Gate | Platform / QA | INIT-005～008 | Format、Lint、Type、Unit、Architecture、Build 可运行 | 待授权可执行 |
| INIT-010 | 定义配置 Schema 与环境层级 | Backend / Security | INIT-006 | 缺失 Fail Closed，无 Secret 默认值 | 待授权可执行 |
| INIT-011 | 定义 Secret 本地/CI 边界 | Security / Platform | INIT-010 | 无真实 Secret 入库，轮换/隔离规则明确 | 待授权可执行 |
| INIT-012 | 建立结构化日志字段规范 | Operations / Security | INIT-006 | Correlation 完整，敏感正文禁止 | 待授权可执行 |
| INIT-013 | 建立 Error/Problem Registry 骨架 | API / Backend | INIT-006 | 稳定分类、本地化 Key、安全映射 | 待授权可执行 |
| INIT-014 | 建立 API Composition Root | Backend Lead | INIT-006、010、013 | Runtime 可启动，Domain 不依赖 Framework | 待授权可执行 |
| INIT-015 | 建立 Worker Composition Root | Backend / Platform | INIT-006、010 | 与 API 共享核心，不含重复业务逻辑 | 待授权可执行 |
| INIT-016 | 决定 ORM/Migration/UoW 组合 | Data / Backend | INIT-003 | 事务、映射、Alembic 候选、测试与回退明确 | 模块阻断 |
| INIT-017 | 建立 PostgreSQL 本地/测试 Harness | Data / QA | INIT-016 | 隔离、可重建、从空库 Migration 通过 | 模块阻断 |
| INIT-018 | 建立 Redis Adapter Contract | Backend / Platform | INIT-006 | 非真相源、隔离、失效和降级测试明确 | 待授权可执行 |
| INIT-019 | 建立 Health Contract | Operations / Backend | INIT-014、015、017、018 | Liveness/Readiness/Dependency 分离 | 待授权可执行 |
| INIT-020 | 建立 Audit 基础 Module | Audit / Security | INIT-016、017 | 追加式、最小正文、不可普通更新 | 待授权可执行 |
| INIT-021 | 建立 Outbox/Inbox 基础 | Application / Data | INIT-016、017、020 | 本地事务、去重、重放与审计可测试 | 待授权可执行 |
| INIT-022 | 决定 Worker/Broker 开发实现 | Platform / Application | INIT-015、021 | Delivery、Retry、DLQ、幂等、退出明确 | 模块阻断 |
| INIT-023 | 建立 Operation/AnalysisProgress 骨架 | Application / Operations | INIT-021、022 | Projection 只读、可重建、不驱动流程 | 待授权可执行 |
| INIT-024 | 建立 Web/TypeScript/Next.js 骨架 | Frontend Lead | INIT-003～006 | 移动端 Layout、无 Secret、可构建 | 待授权可执行 |
| INIT-025 | 建立 API Client/Error 基础 | Frontend / API | INIT-013、024 | Version、Correlation、Problem Details 统一 | 待授权可执行 |
| INIT-026 | 建立 i18n/RTL 基础 | Frontend / Content | INIT-024 | 简中 Key、Locale 边界、RTL 方向测试 | 待授权可执行 |
| INIT-027 | 建立 Identity/Consent Module Shell | Domain / Security | INIT-007、016、020 | Root/Port/不变量存在，无认证方案绑定 | 待授权可执行 |
| INIT-028 | 建立 BirthProfile/Chart Module Shell | Domain / Data | INIT-007、016、020 | 确定性 Chart 生命周期，无正式算法 | 待授权可执行 |
| INIT-029 | 完成 Authentication/Token ADR | Security / Identity | INIT-027 | Protocol、Token、撤销、MFA、测试已批准 | 模块阻断 |
| INIT-030 | 完成 Field Encryption 决策 | Security / Data | INIT-028 | 字段、Key、查询、迁移、恢复和性能明确 | 模块阻断 |
| INIT-031 | 建立 Algorithm/Golden Dataset Harness | Calculation / QA | INIT-028 | 版本、来源、期望、差异与阻断结构就绪 | 专家阻断 |
| INIT-032 | 取得首批算法口径与黄金命例批准 | 命理专家 / Product | INIT-031 | 范围、边界、来源、预期、版本和签核完整 | M5 阻断 |

### 14.1 Backlog Execution Rule

`待授权可执行` 表示架构和依赖允许，但仍需用户明确授权开始项目初始化/编码。`初始化阻断`、`模块阻断` 和 `专家阻断` 必须先关闭相应 Gate。

### 14.2 Suggested First Sprint Boundary

首个获授权 Sprint 建议只处理 INIT-001～015 中已关闭决策的部分，不实现业务规则、数据库业务 Schema、真实认证、真实 AI 或命理算法。

---

## 15. Do Not Start List

当前不得正式实现或绑定：

1. 未经专家批准的历法、四柱、起运或其他命理算法；
2. 旺衰、格局、调候、用神、喜神、忌神、首批神煞等正式规则；
3. 未经专家批准的证据等级判定和多流派优先级；
4. 未批准黄金命例的“通过即发布”流程；
5. 正式 AI Provider、Primary Model、Embedding 或 Reranker 绑定；
6. 业务 Module 直接调用任何 Provider SDK；
7. 具体 Prompt 内容、生产 Prompt 发布或未版本化 Prompt；
8. 将 RAG/Vector Index 作为事实或 Evidence Source of Truth；
9. Model-as-Judge 作为唯一发布门禁；
10. AI Tool Calling 或外部动作执行；
11. 健康、婚姻、投资、法律、自伤、死亡等高风险主题正式输出；
12. 真实支付、结算、退款或套餐扣费；
13. 第三方动态插件或第三方代码执行；
14. V2 Developer API 的外部开放；
15. 正式 PDF、公开分享和完整 0～100 岁时间轴，除非进入批准版本；
16. GA 级跨区域、Active-Active 或多区域数据复制；
17. 微服务拆分、分库分表或独立 Search Engine；
18. 直接手工修改生产数据库或 Schema；
19. 使用真实用户命例作为本地、CI 或普通 Seed；
20. 将 AnalysisProgress、Cache、Dashboard 或 Queue 状态作为领域真相源；
21. 把 RuleRun、EvidenceBundle、AIAnalysis 或 Report 状态重新写入 Chart；
22. 在 Authentication/Token/Field Encryption 未决时形成不可逆安全实现；
23. 在正式 SLO/RPO/RTO 未批准时作外部服务承诺；
24. 未经下一轮明确授权创建项目、Git、目录、代码或配置。

### 15.1 Allowed Preparation

允许继续进行 ADR、专家样例准备、Threat Model、测试计划、接口边界评审、Backlog 拆分和用户原型研究，只要不把未决结果实现为正式能力。

---

## 16. Review Checklist

### 16.1 Baseline and Scope

- [ ] 是否严格继承 01～16 Approved Architecture Baseline。
- [ ] 是否未修改任何现有架构文档。
- [ ] 是否只生成 17 本身。
- [ ] 是否没有业务代码、测试代码、配置或脚本。
- [ ] 是否没有初始化 Git、项目、目录、数据库或依赖。
- [ ] 是否未把本计划变成新的 Domain/API/Technology Baseline。

### 16.2 Repository and Structure

- [ ] 是否明确推荐 Monorepo，并标记为待批准 Repository Decision。
- [ ] 是否解释不推荐 Polyrepo 的当前原因。
- [ ] 顶层是否包含 apps/web、apps/api、apps/worker、packages/shared、docs、infrastructure、tests、scripts。
- [ ] Runtime、Package、Context 和 Aggregate 是否没有混为一体。
- [ ] 模块化单体是否保持 Context 私有边界和单一发布兼容基线。
- [ ] Shared Kernel 是否最小且不包含业务状态。

### 16.3 Backend and Frontend

- [ ] Python、FastAPI、PostgreSQL、Redis、Worker、Outbox/Inbox 是否覆盖。
- [ ] 配置、DI、日志、错误、Health、Migration 和测试顺序是否明确。
- [ ] Alembic 是否仅作为待组合批准的推荐迁移候选，未生成配置。
- [ ] Next.js、TypeScript、移动端、API Client、Form、i18n、RTL 和测试是否覆盖。
- [ ] 前端是否不复制命理规则或持有领域真相。

### 16.4 DDD, Data and AI

- [ ] Identity、Consent、Birth、Chart、Rule、Evidence、Knowledge、AI、Report、Audit、Operations 模块是否覆盖。
- [ ] 是否区分立即可做的 Skeleton 与专家/ADR 阻断的正式逻辑。
- [ ] Chart 是否只负责确定性生命周期。
- [ ] AnalysisProgress 是否只读、不拥有状态、不驱动流程。
- [ ] PostgreSQL Ownership、Identity、Version、Audit 和 Migration 顺序是否明确。
- [ ] AI 是否仅允许 Gateway/Registry/Validation 接口骨架，禁止直接 Provider 调用。

### 16.5 Testing and CI

- [ ] Unit、Domain、Application、Integration、Contract、API、Frontend、E2E、Architecture 是否从第一天规划。
- [ ] Test Framework Candidate 是否未被静默决定。
- [ ] CI 是否至少覆盖 Lint、Format、Type、Unit、Migration、安全、依赖、Build、Contract。
- [ ] CI 是否不连接生产或使用真实敏感数据。
- [ ] 未实现能力是否没有用空测试制造假绿。

### 16.6 Milestones and Gates

- [ ] M0～M5 是否包含目标、输入、输出、完成标准和专家依赖。
- [ ] Repository/Test Tool 是否分类为初始化阻断。
- [ ] Authentication、Token、Encryption、AI、Migration、算法是否分类为模块阻断。
- [ ] Production Orchestration、Provider Legal、Retention 是否分类为 Beta 阻断。
- [ ] 正式 SLO/RPO/RTO 和 Cross-Region 是否分类为 GA 阻断。
- [ ] 命理算法和黄金命例是否明确阻断 M5 正式行为。

### 16.7 Backlog and Final Gate

- [ ] 32 项 Backlog 是否具备 ID、Task、Owner、Dependency、Acceptance 和 Blocking Status。
- [ ] 第一批任务是否可在对应 Gate 关闭后执行。
- [ ] Do Not Start List 是否覆盖所有未批准能力。
- [ ] 是否没有静默选定任何 ADR Candidate。
- [ ] 是否继续要求下一轮明确授权才可初始化或编码。

本文件完成后立即停止。不得执行 Backlog，不得创建其他文件，不得初始化项目或进入业务编码。
