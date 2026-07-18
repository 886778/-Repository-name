# AI 八字命理分析平台：工程实现规范

**文档编号：** 10  
**文档类型：** Engineering Implementation Guide  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md`、`02-SRS.md`、`03-SYSTEM-ARCHITECTURE.md`、`04-DOMAIN-MODEL.md` 1.0、`05-DATA-MODEL.md` 1.0、`06-ROADMAP.md` 1.0、`07-APPLICATION-ARCHITECTURE.md` 1.0、`08-API-DESIGN.md` 1.0、`09-TECHNOLOGY-ARCHITECTURE.md` 1.0（均已 Approved）  
**目标读者：** 技术负责人、架构师、后端与前端工程师、测试工程师、安全工程师、平台工程师、代码审查者及技术项目负责人

---

## Version 0.9 Change Log

- 首次建立逻辑工程目录、后端与前端组织、DDD 映射和依赖规则。
- 定义 Dependency Injection、Configuration、Logging、Error、Validation、Repository、Domain Event 和 Transaction 实现规范。
- 定义 Testing、Code Style、Naming、Git、Branch、Commit、Pull Request 和 Code Review 规范。
- 定义 Static Analysis、Documentation、Development Workflow、Engineering Governance、ADR 和反模式。
- 本文件仅为 Engineering Guide，不包含业务代码、可运行代码或工程配置，不授权进入编码阶段。

---

## 1. Document Purpose

### 1.1 目标

本文档规定团队在未来获得编码授权后，应如何把 Approved Domain、Data、Application、API 和 Technology Architecture 映射为一致、可测试、可审查、可维护的工程结构。

它解决“代码应该放在哪里、依赖应指向哪里、一个用例如何经过各层、工程变更如何评审”等问题，不重新决定“业务是什么”或“架构边界是什么”。

### 1.2 适用范围

本规范覆盖：

- 前后端逻辑目录与模块组织；
- DDD 对象、用例和基础设施的工程映射；
- Dependency Injection、配置、日志、错误与校验；
- Repository、Domain Event、Transaction 和异步边界；
- 测试金字塔、静态分析与质量门禁；
- 命名、风格、Git、Commit、PR、Review 和文档；
- 日常开发、例外、技术债务与工程治理。

### 1.3 不包含内容

本文不包含：

- Python、TypeScript 或其他语言代码；
- FastAPI Controller、Next.js 页面、DTO 或业务 Service 实现；
- SQL、ORM Mapping、数据库迁移或数据种子；
- Dockerfile、Compose、Kubernetes、Terraform 或云配置；
- CI/CD Pipeline 配置或 GitHub Actions YAML；
- OpenAPI、GraphQL、gRPC、SDK 或可运行示例；
- 任何 Aggregate、Entity、Value Object、Domain Event、Data Model 或 API Contract 变更；
- 进入编码阶段的授权。

### 1.4 Baseline Conflict Rule

如果实现便利要求改变 Domain Model、Aggregate Boundary、Context Boundary、Data Model、Application Layer、API Contract 或 Technology Baseline，只能登记为 `ADR Candidate` 或 `Open Question`。工程团队不得先写成既成事实再请求追认。

### 1.5 当前授权状态

本文件描述未来实现标准。用户尚未明确回复“需求与架构评审通过，可以进入编码阶段”前，不得依据本指南创建项目骨架、业务代码、测试代码、配置、迁移或部署资产。

---

## 2. Engineering Principles

### ENG-001 Architecture Is Executable Policy

目录、依赖、测试和 Review Gate 必须持续证明 Approved Architecture，而不是只在文档中声明遵守。

### ENG-002 Domain First

领域行为、状态转换和不变量进入 Domain；Interface、Application 和 Infrastructure 不复制或替代领域规则。

### ENG-003 Use Case Oriented

Application 实现围绕批准的 Command、Query 和 Use Case；不以数据库表的通用 CRUD 作为工程主结构。

### ENG-004 Context Ownership

每个 Bounded Context 拥有自己的 Domain、Application、Infrastructure Adapter 和 Interface。跨 Context 不共享 Repository、ORM Model 或可变对象。

### ENG-005 Explicit Dependencies

依赖通过构造和明确 Port 传入。禁止 Service Locator、隐式全局状态和无法在测试中替换的运行时单例。

### ENG-006 Small Transaction Boundaries

一个写用例原则上只修改一个 Aggregate，事务不跨 Context、不等待外部网络。跨 Context 使用已批准 Event/Saga。

### ENG-007 Immutable History

实现必须保护 Valid Snapshot、Completed RuleRun、Frozen EvidenceBundle、Completed AIAnalysis、Published 定义和 Frozen Report，不能通过通用更新入口原地修改。

### ENG-008 Test at the Lowest Responsible Layer

领域规则在 Domain Unit Test 验证；应用编排在 Use Case Test 验证；Adapter 和契约在 Integration/Contract Test 验证；不把所有信心寄托于昂贵端到端测试。

### ENG-009 Secure and Private Defaults

认证、授权、Purpose、Consent、遮蔽、日志禁记和最小数据传输是默认工程行为，不依赖开发者临时记忆。

### ENG-010 Observable Outcomes

Command、Query、Task、Event、External Call 和关键失败具有稳定日志、指标和关联标识，但不记录敏感正文。

### ENG-011 Deterministic Core

确定性计算和规则执行固定输入与版本，避免系统时钟、网络、随机数或“最新版本”成为隐藏依赖。

### ENG-012 No Silent Failure

错误必须分类、传播、记录并映射为批准结果；禁止吞掉异常、返回空对象或把失败伪装为 Completed。

### ENG-013 Automated Quality

格式、类型、依赖方向、测试、安全、Secret、许可证和兼容性尽可能自动检查；人工 Review 聚焦语义与风险。

### ENG-014 Small Reversible Changes

变更保持单一目的、可审查、可回退或可前滚。大规模重构与业务变化不混在同一 Pull Request。

### ENG-015 No Premature Abstraction

共享抽象由至少两个真实、稳定且语义一致的用例证明。第二个术数模块出现前，不为假设场景建设动态插件框架。

### ENG-016 Documentation Travels with Change

代码、测试、契约、Runbook、ADR 和用户可见变化在同一变更中保持一致；文档不是发布后的补录任务。

---

## 3. Repository Structure

### 3.1 Physical Topology Boundary

`09-TECHNOLOGY-ARCHITECTURE.md` 尚未决定 Monorepo 或 Polyrepo。本文定义与物理仓库无关的逻辑 Workspace；最终仓库拓扑必须先通过 ADR。无论选择哪种拓扑，模块名、依赖方向和质量门禁保持一致。

### 3.2 Logical Workspace

逻辑 Workspace 至少包含以下区域：

- `backend`：Python/FastAPI 模块化单体的 Domain、Application、Infrastructure 和 Interface。
- `frontend`：Next.js/TypeScript 第一方 Web Interface。
- `quality`：跨应用 Contract、Architecture、Security、Performance 和端到端测试资产的逻辑归属。
- `docs`：Architecture Baseline、ADR、工程标准、模块说明和运行文档。
- `platform`：未来获授权后容纳 CI/CD、环境和基础设施声明；本阶段不得创建相关配置。
- `tools`：仅在获授权后容纳无业务语义的开发/验证工具，并有 Owner 和文档。

这些名称是逻辑约定，不要求本轮创建任何目录。

### 3.3 Top-Level Ownership

| Area | Primary Owner | Change Gate | Forbidden Content |
|---|---|---|---|
| backend | Backend / Context Owners | Architecture + Backend Review | 前端页面、生产 Secret |
| frontend | Frontend Owner | Frontend + API Contract Review | 后端领域规则、Server Secret 泄漏 |
| quality | QA / Architecture / Security | Test Owner Review | 真实生产敏感数据 |
| docs | Document Owners | 对应基线/ADR Review | 未批准的架构决定 |
| platform | Platform / Security | Platform + Security Approval | 业务领域规则 |
| tools | Tool Owner | Security / Dependency Review | 绕过正式流程的数据修改脚本 |

### 3.4 Repository Hygiene

- 根目录只保留全局治理和入口文档，不堆放临时脚本。
- 生成物、构建缓存、IDE 状态和本地 Secret 不进入版本库。
- 依赖锁定文件属于受审查制品，不能随意删除或重新生成。
- 大型二进制测试资产使用受控 Artifact 机制，不直接污染源仓库。
- 所有目录有明确 Owner；无人维护区域不得成为共享垃圾箱。

### 3.5 Code Ownership

每个 Bounded Context、公共工程能力、前端 Feature、测试域和平台能力至少有主 Owner 与备份 Reviewer。修改 Context Boundary、共享内核、安全、数据或发布流程需要相应 Owner 审批。

---

## 4. Backend Project Organization

### 4.1 Logical Backend Layout

后端逻辑结构如下，具体 Python Package 名称在项目初始化 ADR 中确认：

- `backend / source / bootstrap`：应用装配、Composition Root、运行入口和生命周期协调。
- `backend / source / modules / <context> / domain`：该 Context 的 Aggregate、Entity、Value Object、Domain Service、Factory、Repository Port 和正式 Domain Event。
- `backend / source / modules / <context> / application`：Command、Query、Handler、Application Service、Authorization Policy、Process Manager/Saga Port 和应用结果。
- `backend / source / modules / <context> / infrastructure`：Persistence、Cache、Message、Search、Object Storage 和外部 Provider Adapter。
- `backend / source / modules / <context> / interface`：FastAPI Route Adapter、Event Consumer Adapter 和 Scheduler Adapter。
- `backend / source / projections`：跨 Context 只读 Projection Builder，例如 AnalysisProgress；不得成为写模型。
- `backend / source / shared`：极小技术共享能力，不包含业务状态与命理规则。
- `backend / tests / unit`：Domain 和纯函数测试。
- `backend / tests / application`：Use Case、Policy、Saga 和事务边界测试。
- `backend / tests / integration`：数据库、消息、缓存、对象和 Provider Adapter 测试。
- `backend / tests / contract`：模块、API、Event 和 Provider Contract 测试。

该布局是设计说明，不代表本轮实际创建目录。

### 4.2 Context Package Rules

1. Context Package 是最主要的业务模块边界。
2. 其他 Context 只能依赖其公开 Application/Query/Event Contract。
3. `domain` 不依赖 `application`、`infrastructure` 或 `interface`。
4. `application` 可以依赖本 Context `domain` 与 Port，不依赖 Adapter 实现。
5. `infrastructure` 实现本 Context Port，不向 Domain 暴露 ORM/SDK 类型。
6. `interface` 只做协议适配、基础验证和应用调用。
7. 共享能力不得反向依赖任何业务 Context。

### 4.3 FastAPI Organization Rules

- FastAPI 实例、全局 Middleware 和 Router 注册集中在 Composition Root。
- 每个 Context 自己声明 Interface Adapter，由 Bootstrap 显式注册。
- Route Handler 保持薄：解析协议、建立安全/追踪上下文、调用 Command/Query、映射结果。
- Route Handler 不加载 ORM、不直接开启跨模块事务、不调用供应商 SDK。
- API Version、Problem Details、Header、Idempotency 和 Status Code 严格继承 `08-API-DESIGN.md`。
- Framework Dependency 机制只用于 Interface/Composition 装配，不渗透 Domain。
- Background Task 机制不能替代可靠 Broker；正式长任务必须先可靠受理。

### 4.4 Bootstrap and Composition Root

Composition Root 负责：

- 读取并验证环境配置引用；
- 构造 Infrastructure Adapter；
- 建立 Repository/Transaction/Message/Clock 等 Port Binding；
- 注册 Context Application Service、Route 和 Consumer；
- 配置日志、指标、追踪和健康检查；
- 管理启动、Readiness 和 Graceful Shutdown。

业务规则、环境分支和用例选择不得藏在 Bootstrap 中。

### 4.5 Worker Organization

- Worker Handler 按 Context/Use Case 归属，不建立“万能任务处理器”。
- Message 只携带稳定 Identity、Version、Correlation 和最小安全上下文。
- Worker 重新加载权威状态并重验前置条件，不信任陈旧 Payload。
- AI、Calculation、Report、Index 和 Data Rights 使用隔离的执行池或并发预算。
- Task 成功只在业务事务提交后确认；失败按 Retry 分类处理。

### 4.6 Scheduler Organization

Scheduler 只触发受批准、幂等的 Application Command，例如保留清理、索引重建或备份验证意图。禁止 Scheduler 直接运行任意 SQL 或修改 Aggregate 内部状态。

### 4.7 Shared Backend Code

允许共享：基础 Identity 包装、Clock/ID Port、通用 Result 类型、Tracing Context、无业务语义的 Serialization/Redaction 工具。禁止共享：Domain Entity、业务状态机、权限决定、Rule、Evidence、ORM Model 和“通用业务 Service”。

---

## 5. Frontend Project Organization

### 5.1 Logical Frontend Layout

前端逻辑结构如下，Next.js 具体 Router 模式仍需项目初始化决策：

- `frontend / source / app-shell`：路由入口、Layout、Provider 装配、错误边界和全局 Metadata。
- `frontend / source / features / <use-case>`：按用户任务组织的页面编排、状态和 API 调用。
- `frontend / source / components`：无业务状态的可复用 UI 组件。
- `frontend / source / design-system`：Token、主题、可访问性和 RTL 基础。
- `frontend / source / api-client`：遵循 Approved API Contract 的受控 Client Adapter。
- `frontend / source / i18n`：语言资源、格式化和 RTL 行为。
- `frontend / source / security`：CSRF、会话边界和安全导航辅助；不存 Server Secret。
- `frontend / source / observability`：去敏前端错误、性能和用户旅程信号。
- `frontend / source / test-support`：合成 Fixture、Mock Boundary 和可访问性辅助。
- `frontend / tests`：Component、Feature、Contract、Accessibility 和 End-to-End 测试。

该布局不要求本轮创建任何文件或页面。

### 5.2 Feature Organization

Feature 围绕用户旅程组织，例如出生输入、命盘查看、证据展开、AI 对话、报告和数据权利，而不是复制后端表或 Aggregate 结构。一个 Feature 可以读取多个已授权 API Resource，但不能在浏览器实现跨 Context 业务事务。

### 5.3 Server and Client Boundary

- Server-only 能力和 Secret 不进入浏览器 Bundle。
- Browser 状态不成为正式业务真相源。
- 权限隐藏用于体验，不替代后端授权。
- 敏感数据只在必要组件和生命周期内存在，不进入 URL、公共 Cache 或 Analytics。
- Streaming/Progress 必须区分 Accepted、Running、Completed 和 Projection Lag。

### 5.4 API Client Rules

- 只调用 `08-API-DESIGN.md` 批准的 Resource/Command/Query。
- 统一处理 RequestId、CorrelationId、Problem Details、Retry-After、Idempotency-Key 和 API Version。
- GET 不触发业务副作用；写操作由明确用户意图发起。
- Timeout 后先查询 Operation，不盲目生成新 Idempotency-Key。
- Client 不依赖本地化错误文本或未承诺字段顺序。
- 认证/授权失败不通过前端猜测资源存在性。

### 5.5 State Management

状态分为：Server State、Form Draft、UI State、Session View 和 Async Operation View。正式 Chart、Snapshot、Evidence、Report 与 Consent 状态来自 API；本地 Draft 可丢且不冒充已确认事实。引入全局状态库必须有真实跨 Feature 需求和 Owner。

### 5.6 Form and Uncertainty UX

- BirthInput Draft 保留用户输入精度和不确定性，不自动补成精确值。
- 跨时柱、节气、换日或时区歧义显示明确提示。
- 真太阳时与子时换日只展示批准的配置语义。
- 高风险内容和命理有效性文案保持克制。
- Form Validation 同时支持字段级提示与服务端最终裁决。

### 5.7 Internationalization and RTL

- 所有用户文本使用 i18n Resource，不在 Component 中散落硬编码文案。
- 简体中文为 MVP 正式质量语言；英文/阿拉伯语发布前需人工与术语复核。
- Layout、方向、图标、数字、日期和标点从第一天兼容 RTL。
- 错误码与业务状态不因语言变化而改变。

### 5.8 Accessibility

交互组件遵循键盘、焦点、语义、对比度、Reduced Motion 和辅助技术要求。Chart/Timeline 可视化提供等价文本，不能只靠颜色表达证据状态或风险。

### 5.9 Frontend Dependency Rule

页面与 Feature 可以依赖 Design System、API Client、i18n 和无业务 Utility；通用 Component 不反向依赖具体业务 Feature。禁止形成跨 Feature 循环依赖。

---

## 6. DDD Implementation Rules

### 6.1 Approved Model Only

实现只能映射 `04-DOMAIN-MODEL.md` Approved 1.0 中的对象和边界。新 Entity、Value Object、Aggregate Root、Domain Service 或 Domain Event 先走 Domain Review；不得由 ORM 或接口字段自动生成领域对象。

### 6.2 Entity

- Entity 以稳定 Identity 判断身份，不以全部属性值判断。
- Identity 不承载地区、时间、版本或顺序语义。
- Entity 状态只能经 Aggregate Root 允许的行为变化。
- Setter 不能绕过不变量；不提供通用“更新全部字段”。
- 删除、Archive、Anonymization 和 Legal Hold 遵循 Data Model。

### 6.3 Value Object

- Value Object 无独立生命周期，以完整值相等。
- 创建时完成格式与领域不变量验证。
- 对外表现为不可变；变更通过创建新值表达。
- 不包含 Repository、Clock、Network 或 Framework 依赖。
- 可安全共享不等于可以包含主体敏感信息的全局 Cache。

### 6.4 Aggregate

- Aggregate Root 是外部写入唯一入口。
- 一致性边界内状态在一次本地事务提交。
- 外部只保存其他 Aggregate Root Identity 或批准 Snapshot 引用。
- Aggregate 不直接调用 Repository、Broker、HTTP、AI 或其他 Aggregate。
- Aggregate 行为产生 Domain Event，但不自行发布网络消息。
- Aggregate 大小和加载范围严格遵循 Approved Domain/Data Model。

### 6.5 Domain Service

只有当一个无自然 Entity/Value Object Owner 的领域行为确实跨多个值协作时使用 Domain Service。Domain Service 保持无状态或显式输入，不成为“放不下代码”的杂物箱。

### 6.6 Factory

复杂创建使用已批准 Factory：ChartFactory、ReportFactory、EvidenceFactory 等。Factory 负责合法初始对象与不变量，不读取数据库或执行外部网络；所需引用由调用方准备。

### 6.7 Domain Event

Domain Event 表达已经发生的领域事实，使用过去时、不可变、带稳定 Event Identity 与发生时间。只有 Approved Domain Event 是正式事实；Application/Integration Event Candidate 不能静默升级为 Domain Event。

### 6.8 Application Service and Handler

Application Service/Handler 负责授权、幂等、加载 Aggregate、调用 Domain 行为、提交 Transaction、发布结果和触发 Audit。它不实现旺衰、格局、用神、Evidence 判断或 AI 事实校验规则。

### 6.9 Command and Query Separation

- Command 表达变更意图并返回明确 Application Result。
- Query 读取 Projection/Snapshot，不触发 Command 或修复。
- Command Model 不为 UI 便利返回无界查询图。
- Query Model 不被用作写入前唯一权威状态。

### 6.10 Process Manager / Saga

Saga 只保存协调进度、关联 Identity、尝试、超时与结果，不持有参与 Context 的业务状态。每一步发出独立 Command，并处理重复、乱序、失败和人工介入。

### 6.11 Anti-Corruption Layer

AI、地点、对象存储、身份、通知和未来第三方 API 通过防腐层转换。供应商枚举、错误、模型名和 Payload 不进入 Domain。

### 6.12 Determinism and Clock

确定性计算显式接收锁定输入、参数、Algorithm Version 和必要时间边界。系统时间通过 Clock Port 获取；测试可控制，生产不可由客户端覆盖。随机值通过受控 Port，不能改变同版本计算事实。

---

## 7. Dependency Injection Strategy

### 7.1 Principle

采用显式 Constructor Injection 为默认。依赖由 Composition Root 创建和连接，Domain Object 不知道 DI Container。

### 7.2 Injection Scope

| Scope | Typical Dependencies | Rule |
|---|---|---|
| Application Lifetime | 配置、Adapter Factory、无状态 Client | 必须线程/并发安全，不保存请求状态 |
| Request / Command | ActorContext、Unit of Work、Repository Port、Correlation | 请求结束释放，不跨用户共享 |
| Worker Task | TaskContext、Unit of Work、幂等、Trace | 每次尝试独立，不能遗留上次状态 |
| Transaction | 数据库 Session/Connection 与 Outbox | 不跨 Context、不跨外部等待 |

### 7.3 FastAPI Dependency Boundary

FastAPI Dependency 机制可以解析认证、请求上下文和 Interface Adapter，但不得成为 Domain Service Locator。Application Handler 的必需依赖仍通过清晰构造契约表达。

### 7.4 Dependency Rules

- 依赖接口/Port，而非 Infrastructure Concrete Type。
- 依赖必须是必需或显式可选；不通过 `None` 隐藏配置缺失。
- 不在方法内部从全局 Container 临时获取依赖。
- 不把 Repository、Transaction 或 RequestContext 注入 Entity/Value Object。
- 不为每个简单纯函数创建 Interface 和 Container Binding。
- 测试用 Fake/Stub 遵循相同 Port Contract。

### 7.5 Container Selection

是否使用独立 DI Container 尚未批准。若 FastAPI 原生装配和显式 Factory 足以满足需求，优先保持简单；引入 Container 需评估生命周期、异步 Scope、调试、类型支持和框架锁定。改变整体 DI 模型需 ADR。

### 7.6 Circular Dependency Prevention

Composition Root 可以知道所有 Adapter，业务模块之间不得因 DI 出现循环。发现循环时重新审查职责、Event/Query 边界或提取无业务的稳定 Port，而不是使用运行时延迟查找掩盖。

---

## 8. Configuration Implementation

### 8.1 Configuration Categories

继承技术架构，将配置分为 Static Runtime、Dynamic Operational、Feature Flag、Business Version Config 和 Secret。不同类别使用不同 Owner、存储、发布与审计；不得混用。

### 8.2 Typed Configuration

- 运行配置有明确类型、范围、必需性和安全默认值。
- 应用启动时完整校验；关键配置缺失时 Fail Fast。
- 配置名称不使用含糊缩写，明确单位和时区。
- Duration、Size、Rate、URL 和 Locale 不以无单位数字表达。
- 未知配置是否拒绝由兼容策略统一决定，不在各模块随意处理。

### 8.3 Environment Binding

同一制品通过环境化配置运行。配置层次、覆盖优先级和来源固定并可观测，避免“本地能跑但生产读取另一来源”。Production 不读取开发默认 Secret 或不安全回退。

### 8.4 Secret References

普通配置只保存 Secret Reference，不保存原值。日志只显示配置项是否存在、版本和安全引用，绝不显示 Secret 内容。

### 8.5 Dynamic Configuration

动态变化具备版本、Owner、批准、传播状态、回滚和 Audit。高风险配置使用双人审批或受控窗口。配置刷新失败保持最后一个已验证版本或关闭能力，不应用部分无效值。

### 8.6 Feature Flags

- Flag 有业务/技术 Owner、目标范围、到期和删除任务。
- Flag 不绕过授权、Consent、Risk、Evidence 或 Immutable Rules。
- Flag 评估结果进入必要的 Trace/Metric，而非敏感日志。
- 测试覆盖 On、Off 和关键组合；组合爆炸时缩小设计。
- 长期 Flag 转为正式配置或移除。

### 8.7 Business Version Configuration

Algorithm、RuleSet、Knowledge、Prompt、Model Route 和 Risk Policy 使用 Approved Governance/Version 流程，不通过环境变量或 Feature Flag 直接替换生产版本。

### 8.8 Configuration Testing

每个环境配置至少通过启动校验、缺失项、非法范围、旧版本兼容、Secret 不可见和安全默认测试。生产配置变更在预发布验证。

---

## 9. Logging Implementation

### 9.1 Structured Event

日志是结构化事件，不通过拼接自然语言承担机器查询。公共字段包括 Timestamp、Level、Environment、Release、Runtime、Module、EventName、RequestId、CorrelationId、TraceId、Actor/Resource 的安全引用、Result、Duration 和 Safe Error Code。

### 9.2 Event Naming

日志 EventName 使用稳定、可搜索的英文层级命名，表达技术动作与结果；不冒充 Domain Event。名称变更需兼容 Dashboard/Alert 和 Runbook。

### 9.3 Logging Boundaries

| Layer | Log Focus | Must Not Log |
|---|---|---|
| Interface | Method/Route Template、Status、Latency、RequestId | 完整 URL Query、Credential、Body |
| Application | Use Case、Actor Type、Result、Correlation | 完整 Command、出生/对话正文 |
| Domain | 关键规则结果的安全指标或 Event Identity | 敏感全对象 Dump、Infrastructure 细节 |
| Infrastructure | Dependency、Attempt、Timeout、Provider Ref | Secret、供应商原始敏感 Payload |
| Worker | Task、Queue、Attempt、Terminal State | 完整 Message Body |

### 9.4 Sensitive Data Redaction

统一 Redaction 规则覆盖 Authorization、Cookie、API Key、Secret、签名 URL、BirthInput、详细地址、姓名/联系方式、Conversation、Prompt、Model Context/Output 和完整 Report。禁止依赖 Engineer 手工删除敏感字段。

### 9.5 Exception Logging

- 异常只在拥有处置责任的边界记录一次完整内部诊断，避免每层重复。
- 对外响应使用 Safe Error；内部 Stack 受限访问。
- 已处理的业务拒绝不以系统错误级别污染告警。
- 未知错误生成稳定 Request/Correlation 引用。
- 记录异常不能把对象 `repr` 或序列化全文带入日志。

### 9.6 Audit Separation

普通日志不能替代 AuditEvent。需要回答谁、何时、基于何种权限、对何对象做何动作和结果的行为，走 Audit Port 与 Approved Audit Model。

### 9.7 Logging Tests

自动测试检查禁记字段、Redaction、关联 ID、Error Mapping 和重复日志。安全扫描验证源码与 Fixture 中不存在真实 Credential/个人信息。

---

## 10. Error Handling Strategy

### 10.1 Error Taxonomy by Layer

| Layer | Error Category | Handling Owner |
|---|---|---|
| Domain | 不变量、状态、规则适用、不可变冲突 | Domain/Application 形成明确失败结果 |
| Application | Authorization、Consent、Idempotency、Use Case Conflict、Partial | Handler/Process Manager |
| Infrastructure | Timeout、Dependency、Persistence、Message、Storage | Adapter 映射为稳定技术失败 |
| Interface | Protocol、Authentication、Header、Serialization | API Adapter 映射 Problem Details |
| Unknown | 未分类缺陷 | 顶层安全处理、关联、告警和缺陷修复 |

### 10.2 Error Mapping

Error 从内向外转换，保留原因链但不暴露内部类型。API 映射严格使用 `08-API-DESIGN.md` 的 HTTP Status、Problem Details、Error Prefix、retryable 和 Retry-After 语义。

### 10.3 Stable Errors

- Domain/Application 使用稳定、可测试的结果类型或受控异常，不依赖消息文本。
- 本地化只发生在 Interface/Presentation。
- 同一 Error Code 在同一 API Major 中不改变语义。
- Provider Error 先归类，再映射为平台错误。
- 未知错误不得静默转成空列表、默认命盘或安全成功。

### 10.4 Retryability

Retryability 是错误契约的一部分：Validation、Authorization、Consent、Immutable 和多数 Conflict 不自动重试；Transient Timeout/Dependency 可在预算内重试。Timeout 不证明原操作未提交，先通过 Idempotency/Operation 查询。

### 10.5 Exception Translation Boundaries

Repository、Message、Cache、Object 和 Provider Adapter 各自翻译底层错误；Application 不捕获所有异常后统一忽略。顶层 Catch-All 仅用于安全响应和诊断，不负责业务恢复。

### 10.6 Partial Failure

跨 Context Saga 记录每步结果、终态和人工处置。部分删除、导出、投影或通知失败保持明确 `Partial/Degraded`，不能返回完全成功。

---

## 11. Validation Strategy

### 11.1 Validation Layers

| Layer | Validates | Does Not Decide |
|---|---|---|
| Interface | 协议格式、大小、Header、基础类型 | 领域状态和命理规则 |
| Application | Actor、Purpose、Consent、Ownership、配额、用例前置 | Aggregate 内部不变量替代实现 |
| Domain | Value Object、Aggregate、状态转换和领域不变量 | HTTP Status、供应商协议 |
| Infrastructure | 外部 Payload、存储完整性、配置和依赖响应 | 正式领域结论 |
| AI Validation | 结构、事实、引用、冲突、风险与 Scope | 新建命盘事实或 Evidence |

### 11.2 Validation Order

优先执行低成本、安全且不泄露资源存在性的检查，再执行授权后的资源加载与领域验证。Validation 顺序不得形成枚举侧信道。

### 11.3 Input Normalization

Normalization 与 Validation 分离。出生日期、时间、地点、时区和精度按 Approved Calendar/Birth 语义处理；不确定输入不被自动“修正”为精确值。

### 11.4 Cross-Field Validation

跨字段或状态验证由最了解不变量的 Value Object/Aggregate 完成。Interface Schema 只能提供早期提示，不能成为唯一规则来源。

### 11.5 External Data Validation

地点、AI、Object Metadata 和 Message Payload 都视为不可信：验证格式、版本、来源、大小、签名/完整性和允许值。供应商成功响应仍需平台验证。

### 11.6 Validation Messages

内部使用稳定 Code/Path；用户消息可本地化且避免泄露敏感值。Field Issue 不回显完整自由文本、BirthInput 或 Credential。

### 11.7 Validation Tests

覆盖合法、缺失、边界、歧义、恶意、过大、旧版本、不兼容、重复和跨字段冲突。命理专家待确认规则不由工程测试擅自固定，只测试版本、发布和禁止行为。

---

## 12. Repository Implementation Rules

### 12.1 Port Location

Repository Port 按 Approved Domain Model 归属 Context；其接口位于不依赖 Infrastructure 的内层。具体代码位置可在 Domain 或 Application 边界内由项目标准统一，但不得由 ORM Package 拥有。

### 12.2 Aggregate Root Only

写 Repository 以 Aggregate Root 为单位，例如 User、Chart、Rule、Knowledge、EvidenceBundle 和 Report。内部 Entity 不获得跨 Context 公共 Repository。

### 12.3 Persistence Mapping

- ORM/Persistence Model 与 Domain Object 分离。
- Mapper 显式处理 Identity、Version、Lifecycle、Immutable 和内部集合。
- 不使用反射式“复制所有字段”绕过领域构造。
- 数据不完整或版本不兼容时返回明确错误，不构造半合法 Aggregate。
- Frozen/Valid 对象在 Persistence 层也有保护和并发验证。

### 12.4 Query Separation

复杂列表、搜索、Dashboard、Audit 和 AnalysisProgress 使用 Query Adapter/Read Model，不向写 Repository 增加任意过滤、排序和跨 Context Join。

### 12.5 Transaction Participation

Repository 不自行 Commit；由 Unit of Work/Transaction Manager 控制一次 Use Case 提交。禁止多个 Repository 隐式创建独立事务后伪装原子成功。

### 12.6 Optimistic Concurrency

对可变 Aggregate 使用明确 Version/Concurrency Token。冲突返回 Application/API 已批准 Conflict/Precondition 语义；不采用 Last Write Wins 覆盖未知变化。

### 12.7 Deletion

Repository 执行 Approved Physical Delete、Logical Delete、Archive、Anonymization 和 Legal Hold 策略，不提供通用 Hard Delete。删除失败参与 Data Rights Saga 并审计。

### 12.8 Batch Operations

批量读取/写入必须有上限、授权、事务和部分失败语义。批处理不绕过 Aggregate 行为；大规模维护使用受控 Application Use Case，而非公开通用 Repository。

### 12.9 No Cross-Context Access

一个 Context 的 Adapter 不导入或调用另一个 Context 的 Repository/ORM Model。需要数据时使用稳定 Snapshot、Query Contract 或 Event Projection。

### 12.10 Repository Contract Tests

每个 Adapter 通过统一 Contract 测试：Identity、Round Trip、Version、Concurrency、Immutable、Not Found、Delete/Archive、Transaction Rollback 和敏感字段处理。

---

## 13. Domain Event Implementation Rules

### 13.1 Event Creation

Domain Event 由 Aggregate 行为在领域事实发生时创建，内容最小、不可变，包含 EventId、Aggregate Root Identity、OccurredAt 和 Approved 事实。Event 不包含 ORM、HTTP、Queue 或 Provider 类型。

### 13.2 Collection and Publication

- Aggregate 收集尚未发布的 Domain Event。
- Application/Unit of Work 在业务提交中可靠记录 Event/Outbox。
- 事务提交后由 Publisher 转为内部 Integration Event 或触发同进程 Handler。
- 发布失败通过 Outbox 重试，不回滚已成功的外部网络调用来伪造原子性。
- Aggregate 不直接调用 Broker。

### 13.3 Domain vs Integration Event

Domain Event 是本 Context 的正式事实；Integration Event 是面向消费者的最小稳定契约。两者可以映射但不要求一比一。外部 API Event 仍遵循 `08-API-DESIGN.md` 的独立 Review。

### 13.4 Idempotency and Ordering

Consumer 按 EventId/MessageId 幂等。只在明确 Aggregate/Partition 范围内依赖顺序；乱序时等待前置、忽略陈旧或进入人工处理，不能直接改数据库“纠正”。

### 13.5 Event Handler Rules

- Handler 一次处理一个明确责任。
- Handler 的状态变化发出新 Command，不跨 Context 直接改 Aggregate。
- Handler 可失败、重试或 DLQ，并有日志、指标和 Correlation。
- Query Projection Handler 可重建，不成为 Source of Truth。
- Audit Handler 不复制敏感事件全文。

### 13.6 Event Versioning

Event Contract Version 与 Domain Object/API Version 分离。兼容扩展、Breaking Change、弃用和消费者迁移遵循 Approved Governance；不得静默改变既有事件含义。

### 13.7 Event Tests

测试 Event 产生条件、未产生条件、内容最小性、事务提交/回滚、重复、乱序、版本不支持、Retry、DLQ 和 Projection 重建。

---

## 14. Transaction Implementation

### 14.1 Ownership

Transaction Boundary 由 Application Use Case/Handler 拥有。Interface 不直接管理业务事务，Repository 不自行 Commit，Domain 不知道 Transaction。

### 14.2 Standard Write Flow

标准逻辑顺序：建立 Actor/Purpose 上下文 → 幂等检查 → 开启本地 Unit of Work → 加载目标 Aggregate → 调用 Domain 行为 → 记录 Event/Outbox 与必要 Audit → Commit → 发布/返回结果。

该顺序是设计描述，不是可运行代码。

### 14.3 Transaction Rules

1. 原则上一次只修改一个 Aggregate。
2. 不跨 Bounded Context。
3. 不在事务内等待 AI、地点、对象存储、Webhook 或 Broker 网络结果。
4. 事务尽量短，不包含用户交互或长计算等待。
5. 外部调用前后使用显式状态、Operation、Saga 和补偿。
6. Outbox/幂等/必要审计与业务提交保持可靠一致。
7. Frozen/Published/Completed 对象不会因重试回到可编辑状态。

### 14.4 Nested Transactions

禁止用嵌套事务掩盖多个独立 Use Case。内部函数共享调用方 Unit of Work；真正独立提交必须在 Application Flow 中明确，并接受部分失败语义。

### 14.5 Isolation and Locking

默认使用满足 Approved 一致性的最低充分 Isolation，结合 Optimistic Concurrency。悲观锁仅用于有证据的竞争窗口，设置超时并监控；分布式锁不能替代数据库唯一性或 Aggregate 不变量。

### 14.6 Retry

事务死锁、序列化冲突等可重试错误在有限预算内重新加载 Aggregate 并重放同一业务意图。不能复用已失效内存对象，不能重复外部副作用。

### 14.7 Read Transactions

Query 使用只读事务或一致性 Snapshot（如适用），不升级为写。权限/Consent 的关键判断不能从允许延迟的 Read Replica 获取。

### 14.8 Transaction Tests

覆盖 Commit、Rollback、并发冲突、重复请求、Outbox、Audit 失败、Provider Timeout、进程崩溃点和重试后唯一正式结果。

---

## 15. Testing Strategy

### 15.1 Test Objectives

测试证明：领域正确、边界不被绕过、版本可复现、AI 不编造事实、权限/隐私有效、失败可恢复、API 兼容、性能符合门禁、历史不被静默修改。

### 15.2 Test Categories

| Category | Primary Purpose | Typical Scope |
|---|---|---|
| Domain Unit | Value Object、Aggregate、Domain Service、Factory、不变量 | 无数据库/网络/Framework |
| Application Unit | Command/Query Handler、Policy、Saga、幂等和结果 | 使用 Fake Port |
| Adapter Integration | PostgreSQL、ORM、Redis、Broker、Object、Provider | 真实兼容测试环境 |
| Contract | Repository、Module、API、Event、Provider Adapter | 生产同语义 Contract |
| Component | 单 Context 通过 Interface 到 Adapter | 受控依赖 |
| End-to-End | 关键用户旅程与跨 Context Flow | 最少但高价值 |
| Golden Case | 排盘、边界、规则、Evidence | 命理专家批准样例 |
| AI Regression | 结构、事实、引用、冲突、风险与成本 | 锁定证据/版本与评估集 |
| Security | Auth、IDOR、注入、Secret、滥用、上传 | 自动 + 专项人工 |
| Privacy | 最小化、遮蔽、Consent、删除、导出、日志 | 跨存储与备份流程 |
| Performance | Baseline、Load、Stress、Soak、Backlog | Approved NFR |
| Recovery | Backup/Restore、DLQ、Projection Rebuild、Tombstone | DR 演练环境 |
| Accessibility / i18n | 键盘、语义、RTL、Locale、错误消息 | Component + E2E |

### 15.3 Test Data

- 默认使用合成数据。
- 黄金命例有来源、专家批准、版本和适用范围。
- 真实用户命例只有在单独授权、去标识化和受控环境下使用。
- 生产数据不进入本地、CI 或普通 Staging。
- Fixture 不包含真实 Credential、姓名、联系方式或详细地址。

### 15.4 Deterministic Tests

控制 Clock、Identity Generator、Random、External Provider、Algorithm/Rule/Knowledge/Prompt/Model Version。测试不依赖本地时区、执行顺序、真实网络或当前日期。

### 15.5 AI Testing

- Domain Fact、RuleFinding 和 Evidence 由锁定 Fixture 提供，AI 不参与计算。
- 验证结构、引用存在、事实一致、冲突表达、风险拒绝和 Scope。
- 区分模型波动与正式 Validation Result。
- 供应商真实调用测试有预算、去标识化和隔离，不作为所有 PR 的唯一门禁。
- 模型/Prompt/Route 升级通过固定评估集和人工抽检，不静默替换。

### 15.6 Security and Privacy Testing

覆盖跨用户/租户访问、对象 ID 猜测、Role/Scope、Purpose、Consent 撤回、Session、Rate Limit、CSRF/CORS、输入/输出注入、Webhook SSRF、日志泄漏、删除和备份复活。

### 15.7 Performance Testing

以 System/Technology Architecture 的 P95、并发、吞吐、长度和成本基线为准。测试 Cache Warm/Cold、数据库连接、Queue Backlog、Provider Slow、Redis Down 和 Rolling Deployment。

### 15.8 Flaky Test Policy

Flaky Test 是缺陷，不允许长期无条件重跑掩盖。临时隔离必须有 Owner、证据、期限和修复任务；关键安全/领域门禁不可因 Flaky 被跳过。

### 15.9 Coverage

Coverage 是风险信号，不是唯一目标。关键 Aggregate 状态、错误分支、权限、版本和不可变规则要求明确场景覆盖；不追求用低价值断言刷统一百分比。

---

## 16. Test Pyramid

### 16.1 Pyramid Shape

| Level | Relative Volume | Execution | Main Responsibility |
|---|---|---|---|
| Domain / Pure Unit | 最大 | 快速、每次变更 | 领域行为与边界条件 |
| Application / Policy | 较大 | 快速、每次变更 | 用例、授权、Saga、幂等 |
| Adapter / Contract | 中等 | CI 分层执行 | 数据库、消息、API、Provider 契约 |
| Component | 较少 | CI / Pre-Merge | Context 纵向行为 |
| End-to-End | 最少且关键 | Pre-Merge / Release | 核心用户旅程 |
| Performance / Security / DR | 风险驱动 | Nightly / Milestone / Release | 非功能与恢复门禁 |

不在本文件规定僵化百分比；每个模块按风险和故障成本配置。

### 16.2 Contract over Mock

Mock 只验证当前调用方行为，不能证明 Adapter 兼容。Repository、Broker、Object、AI/地点 Adapter 和 API Client 必须有真实 Contract Test，避免 Mock 与生产漂移。

### 16.3 End-to-End Scope

E2E 至少覆盖：匿名/注册首次排盘、时间不确定警告、规则与 Evidence、AI 受限分析、Report Frozen 历史、Consent 撤回、删除部分失败、管理员敏感访问拒绝和 i18n/RTL 骨架。

### 16.4 Release Test Suites

| Suite | Trigger | Blocking Scope |
|---|---|---|
| Fast | 每个 Commit/PR | Unit、类型、Lint、Architecture Boundary |
| Integration | PR / Merge | Adapter、DB、Message、API Contract |
| Domain Regression | PR / Nightly | 黄金命例、边界、规则、Evidence |
| AI Evaluation | Prompt/Model/Route 或相关变更 | 事实、引用、风险、成本 |
| Security / Privacy | PR 风险 + 定期 | 权限、Secret、删除、日志 |
| Performance | Milestone / RC | NFR 和容量基线 |
| Recovery | 定期 / RC | Backup、Restore、DLQ、Tombstone |

---

## 17. Code Style

### 17.1 General Rules

- 自动 Formatter 是唯一格式来源；不在 Review 争论个人排版偏好。
- 静态类型覆盖公开边界、Domain Model、Application Contract 和 Adapter Port。
- 函数/方法保持单一责任，控制嵌套和认知复杂度。
- 注释解释“为什么、约束、风险”，不重复代码表面行为。
- 禁止死代码、无 Owner TODO、调试输出和注释掉的大段实现进入主分支。
- 显式处理 Optional、错误、时区、单位、编码和 Locale。

### 17.2 Python Style Principles

- 遵循社区通行格式与命名，并由统一工具自动执行；具体工具链待项目初始化决定。
- Domain/Application 公共接口使用类型标注。
- 避免动态 Monkey Patch、隐藏导入副作用和运行时全局注册。
- 异步与同步边界清晰；不在异步请求路径执行无界阻塞操作。
- 数据结构选择以领域语义和不可变要求为先。

### 17.3 TypeScript Style Principles

- 启用严格类型方向，不用无约束动态类型逃避契约。
- Server/Client 模块边界显式，Server Secret 类型不得被 Client Import。
- UI Component 保持可组合、可访问、无隐藏网络副作用。
- API Error/State 使用判别明确的类型语义，不靠字符串包含判断。
- 不在前端复制 Python 领域规则。

### 17.4 Complexity

复杂度阈值由 Static Analysis 标准统一设置。超过阈值优先拆分职责、提取领域概念或简化分支，不通过关闭规则长期忽略。

### 17.5 Comments and Docstrings

公开 Port、复杂不变量、算法来源、风险边界和非直观失败语义需要文档说明。命理算法注释引用 Approved Algorithm Version/专家资料，不声称科学预测准确。

### 17.6 Generated Code

未来若出现生成代码，必须可重建、与源契约对应、明确禁止手改并接受安全扫描。生成物不得绕过 Review 或包含 Secret。本轮不生成任何代码。

---

## 18. Naming Convention

### 18.1 Ubiquitous Language

代码标识使用稳定英文 Ubiquitous Language，与 Approved Domain Model 一致；用户文案使用 i18n。禁止同一概念出现多套近义名称。

### 18.2 Type Suffixes

| Concept | Naming Rule | Prohibited Ambiguity |
|---|---|---|
| Aggregate / Entity / Value Object | 使用正式领域名 | `Data`、`Model`、`Info` 等泛名 |
| Command | 祈使业务意图 | 通用 `UpdateEverything` |
| Query | 读取意图 | 名为 Query 却触发写入 |
| Handler | Command/Query + Handler | `Manager`、`Helper` 万能类 |
| Repository Port | Aggregate + Repository | Table Repository 暴露内部 Entity |
| Adapter | Provider/Technology + Capability + Adapter | 供应商名进入 Domain Type |
| Domain Event | 已发生事实的过去时 | `DoXxxEvent` 命令式名称 |
| Integration Event | 稳定事实 + Contract Version 管理 | 直接复用数据库表名 |
| Error | 稳定语义 + Error | 仅用自然语言消息分类 |
| Test | Scenario + Expected Outcome | `test1`、`works` |

### 18.3 Identity and Version

使用 `UserId`、`ChartId`、`SnapshotId`、`RuleRunId`、`EvidenceBundleId`、`AIAnalysisId`、`ReportId` 等 Approved Identity。`SnapshotSequence`、`ReportOrdinal`、`RuleSetVersion` 等 Version/Order 名称独立，不混用。

### 18.4 Time and Units

时间名称明确 `OccurredAt`、`CreatedAt`、`LocalBirthTime`、`UtcOffset`、`TimeZone` 等语义；Duration/Size/Rate 包含单位或使用强类型。禁止无语义 `timestamp`/`timeout` 数字散落。

### 18.5 Boolean and State

Boolean 名称表达可判定问题，但复杂生命周期使用 Approved State，而不是多个互相冲突布尔值。禁止用 `isCompleted=true` 绕过正式状态机。

### 18.6 Abbreviations

只使用词汇表批准的通用缩写，如 API、AI、ID、UTC、RTL。内部新缩写先进入 Glossary，不以团队口头习惯传播。

---

## 19. Git Workflow

### 19.1 Workflow Model

默认采用受保护主分支、短生命周期变更分支和 Pull Request 的 Trunk-Oriented Workflow。长期 `develop` 分支不是默认；若发布模式需要改变，必须评审并走 ADR。

### 19.2 Main Branch

- 主分支始终保持可发布或明确受控状态。
- 禁止直接 Push、强制覆盖和绕过必需检查。
- Merge 需要 CI、Review、Ownership 和风险门禁通过。
- 主分支历史与 Release Tag 受保护。

### 19.3 Change Scope

一个变更对应明确 Issue/Requirement/ADR，尽量只解决一个目的。重构、依赖升级、格式化和业务变化分开提交/PR，除非不可分且在描述中说明。

### 19.4 Synchronization

分支保持短期并及时同步主分支，冲突由变更作者解决并重新运行门禁。禁止长期分支在发布前一次性合并大量不可审查变化。

### 19.5 Release

Release 由主分支上的已验证不可变 Commit/Tag 产生。环境晋级使用同一制品，不从临时分支直接生产部署。具体 Release Branch 是否需要列为 Open Question。

### 19.6 Hotfix

生产 Hotfix 从已知生产基线开始，走缩短但不取消的安全、测试、Review 和审计。修复随后合回主分支并补充根因/回归测试。

---

## 20. Branch Strategy

### 20.1 Branch Types

| Branch Type | Purpose | Lifetime | Merge Target |
|---|---|---|---|
| feature | 单一用户/工程能力 | 短 | main |
| fix | 非紧急缺陷修复 | 短 | main |
| refactor | 无行为变化的结构改善 | 短 | main |
| docs | 文档与 ADR | 短 | main |
| security | 受控安全修复 | 尽可能短、限制可见性 | main / Approved Hotfix Flow |
| release | 仅在确有稳定窗口需要时 | 有明确 Sunset | main + Tag |
| hotfix | 生产阻断修复 | 极短 | production baseline + main |

### 20.2 Naming

分支名包含类型、Issue/Requirement 标识和简短目的；不包含用户名敏感信息、Birth Data、客户名称或 Secret。自动化 Agent 分支遵循平台规定前缀。

### 20.3 Protection

Main、Release 和 Production Tag 受保护。删除合并后的短分支；不删除审计所需 Tag。强制 Push 仅限特殊恢复流程并审计。

### 20.4 Feature Flags vs Long-Lived Branches

未完成功能通过安全的 Feature Flag、接口兼容和小步合并管理，不用长期分支维持多个不可合并版本。Flag 不允许绕过授权或发布门禁。

---

## 21. Commit Convention

### 21.1 Commit Purpose

Commit 是可理解、可审查、可回退的最小变更单元。每个 Commit 构建/测试状态明确，不把临时调试和无关格式变化混入。

### 21.2 Message Structure

提交信息使用统一的“类型 + 可选范围 + 简短祈使摘要”，正文解释原因、约束和影响，Footer 关联 Issue、ADR 或 Breaking Change。本文只定义语义，不生成命令示例。

### 21.3 Allowed Types

| Type | Meaning |
|---|---|
| feat | 已批准的新能力 |
| fix | 缺陷修复 |
| refactor | 不改变外部行为的重构 |
| test | 测试新增或修正 |
| docs | 文档变化 |
| perf | 有证据的性能改善 |
| security | 安全修复或强化 |
| build | 构建/依赖变化 |
| ci | Pipeline 逻辑变化 |
| chore | 不影响产品行为的维护 |
| revert | 明确回退既有 Commit |

### 21.4 Commit Rules

- 摘要描述“做什么”，正文解释“为什么”。
- Breaking Change 必须显式标识并关联 Approved ADR；未批准不得提交。
- 不在 Commit Message 放 Secret、个人信息或安全漏洞可利用细节。
- 自动生成 Commit 必须标明工具/Agent 并由责任人 Review。
- Fix 必须尽可能包含回归测试。

### 21.5 History Strategy

Merge、Squash 或 Rebase 的团队默认策略需在仓库初始化时确认。无论方式如何，最终历史必须保留 Issue/ADR、Reviewer、检查和 Release 可追溯性；策略变化需 ADR。

---

## 22. Pull Request Process

### 22.1 Before Opening

作者确认需求/ADR 来源、范围、测试、静态检查、敏感数据、迁移、兼容和文档均已处理。Draft PR 可用于早期协作，但不能绕过 Ready 标准。

### 22.2 PR Description

每个 PR 至少说明：

- 问题与 Approved Requirement/ADR；
- 方案与不采用的关键替代；
- 影响模块、Context、API/Data/Transaction/Version；
- 安全、隐私、性能、成本与可观察性影响；
- 测试证据；
- 数据/配置/迁移和回退或前滚计划；
- 文档与 Runbook 变化；
- 未决风险和人工验证步骤。

### 22.3 PR Size

优先小型、单目的 PR。超过团队阈值时拆成行为不变准备、核心变化、迁移和清理步骤。无法拆分需在 PR 说明原因并增加 Review 时间。

### 22.4 Required Reviewers

| Change | Required Expertise |
|---|---|
| Domain/Context | Context Owner + Domain Architect |
| Data/Repository/Transaction | Data Owner + Backend Reviewer |
| API | API Owner + Consumer/Frontend Reviewer |
| Security/Identity/Secret | Security Owner |
| Privacy/Data Rights | Privacy/Legal Owner as applicable |
| Rule/Knowledge/Prompt | Domain Expert + Governance Reviewer |
| CI/CD/Deployment | Platform Owner + Security as applicable |
| User Experience/i18n | Product/Design + Frontend Reviewer |

### 22.5 Automated Gates

必需 Gate 按风险包含：Format、Lint、Type、Unit、Architecture、Integration、Contract、Golden、Security、Secret、Dependency、License、Migration、Accessibility 和 Performance Smoke。

### 22.6 Review Resolution

作者逐项回应 Comment。对 Architecture/Security/Correctness 的阻断意见不得仅以“已知”关闭；需要修正、证据或 Approved Exception/ADR。未解决讨论不进入 Merge。

### 22.7 Merge

只在必需 Approval、CI、基线同步和 Release 条件满足后 Merge。Merge 后监控主分支健康；发现回归优先停止扩散，再决定 Revert 或前滚修复。

---

## 23. Code Review Checklist

### 23.1 Correctness and Domain

- [ ] 变更是否对应 Approved Requirement/Use Case。
- [ ] 是否保持 Aggregate、Entity、Value Object 与状态机边界。
- [ ] Domain 规则是否只存在于正确层。
- [ ] 是否保护 Immutable/Frozen/Published/Completed 对象。
- [ ] 是否显式处理不确定出生时间和版本锁定。
- [ ] 是否未新增未经批准的 Domain Event。

### 23.2 Architecture and Dependencies

- [ ] Context 是否未访问其他 Context Repository/ORM Model。
- [ ] Domain 是否无 Framework/Infrastructure 依赖。
- [ ] Application Handler 是否薄且对齐 Command/Query。
- [ ] 是否无循环依赖、Service Locator 或共享可变状态。
- [ ] Process Manager 是否只协调、不成为 Domain Aggregate。
- [ ] Projection 是否只读且可重建。

### 23.3 Data and Transaction

- [ ] Repository 是否以 Aggregate Root 为边界。
- [ ] ORM 是否未泄漏到 Domain/Application Contract。
- [ ] Transaction 是否单 Context/单 Aggregate且足够短。
- [ ] 外部调用是否在数据库事务之外。
- [ ] 幂等、并发、Outbox、Rollback 和 Retry 是否正确。
- [ ] 删除、Archive、Anonymization、Legal Hold 是否符合 Data Model。

### 23.4 API and Errors

- [ ] 是否保持 API Resource、Method、Status、Version 与 Error Contract。
- [ ] GET/Query 是否无副作用。
- [ ] Idempotency-Key、RequestId、CorrelationId、Retry-After 是否正确。
- [ ] Error 是否安全、不泄露内部或敏感信息。
- [ ] Breaking Change 是否有 Approved ADR 和迁移计划。

### 23.5 Security and Privacy

- [ ] 服务端是否验证 Actor、Subject、Role、Scope、Ownership、Purpose、Consent。
- [ ] 是否最小收集、传输、缓存和记录敏感数据。
- [ ] Secret 是否未进入源码、日志、Fixture 或错误。
- [ ] 是否防止 IDOR、注入、SSRF、重放和批量枚举。
- [ ] 管理敏感访问是否有理由、期限和 Audit。
- [ ] 第三方 AI 是否只接收去标识化必要上下文。

### 23.6 Reliability and Observability

- [ ] Timeout、Retry、Circuit、Bulkhead 和降级是否有边界。
- [ ] 重试是否保持同一业务意图且有限。
- [ ] 日志、指标、Trace 是否足以调查且不含敏感正文。
- [ ] Queue 重复、乱序、DLQ 和人工处理是否覆盖。
- [ ] Health/Readiness 是否不会因可选依赖造成重启风暴。

### 23.7 Testing and Maintainability

- [ ] 测试是否位于最低责任层并覆盖失败分支。
- [ ] Fix 是否有回归测试。
- [ ] 是否使用合成/批准数据且测试可重复。
- [ ] 命名是否符合 Ubiquitous Language。
- [ ] 是否消除复制逻辑和无 Owner TODO。
- [ ] 文档、ADR、Runbook 和 Change Log 是否同步。

---

## 24. Static Analysis

### 24.1 Required Analysis Classes

| Analysis | Purpose | Blocking Principle |
|---|---|---|
| Formatter | 消除格式争议 | 自动修正后必须干净 |
| Linter | 常见缺陷、复杂度和风格 | 新违规阻断 |
| Type Checker | Python/TypeScript 边界和空值安全 | Domain/Application/API 边界严格 |
| Architecture Rule | Context/Layer 依赖 | 跨边界违规阻断 |
| Secret Scan | Credential、Key、Token | 命中阻断并启动轮换判断 |
| SAST | 注入、不安全 API、路径与反序列化 | 高风险阻断或批准例外 |
| Dependency Scan | 漏洞、恶意/过期包 | 按严重度 SLA |
| License Scan | 商业/分发兼容 | 未批准许可证阻断 |
| Supply Chain | Lock、来源、SBOM、制品完整性 | 发布门禁 |
| Migration Check | Schema 兼容、危险操作 | 风险变更需演练/审批 |
| Frontend Bundle | Secret、体积、Server/Client Boundary | 超预算或泄漏阻断 |

### 24.2 Architecture Tests

自动验证：Domain 不依赖 Infrastructure/Interface、Context 私有包不可跨模块导入、Repository 不共享、Frontend 通用组件不依赖 Feature、Server-only 模块不进入 Client Bundle。

### 24.3 Suppression Policy

禁止无理由全局关闭规则。单点 Suppression 包含原因、风险、Owner、Issue 和到期；安全、Secret 和 Architecture Boundary 规则原则上不允许永久忽略。

### 24.4 Baseline Existing Findings

首次启用工具若存在历史问题，可建立只读 Baseline 阻止新增，并制定清理计划。不能用 Baseline 隐藏 Critical 安全或数据完整性问题。

### 24.5 Tool Selection

具体 Formatter、Linter、Type Checker、SAST 和 Dependency 工具尚待项目初始化评审。工具变化若改变强制标准、开发流程或供应链信任，需 ADR。

---

## 25. Documentation Rules

### 25.1 Documentation Hierarchy

| Document | Authority |
|---|---|
| Architecture Baseline 01–10 | 产品、领域、数据、应用、API、技术和工程最高基线 |
| ADR | 重大决策、取舍和基线变更前置记录 |
| Module README | Context/模块入口、Owner、依赖、运行与测试说明 |
| Use Case / Contract Docs | Command、Query、Event 和 API 语义引用 |
| Runbook | 告警、故障、恢复、发布和人工处理 |
| Code Comments / Docstrings | 局部原因、不变量和非直观约束 |

### 25.2 Single Source of Truth

同一规则只有一个权威来源，其他文档通过链接引用。不要把 Domain、API 或配置说明复制到多个 README 后独立漂移。

### 25.3 Module Documentation

每个 Context Module 记录：职责、公开入口、禁止依赖、Owner、Aggregate/Repository 引用、事件、事务、配置、可观察性、测试和故障降级。

### 25.4 ADR Rules

ADR 包含状态、背景、决策、候选、取舍、影响、兼容、迁移、回退、风险、Owner 和链接。Rejected/Superseded ADR 保留历史，不删除或改写为“从未发生”。

### 25.5 Code Documentation

注释不声明未经批准的命理观点；算法说明引用正式 Version 和专家来源。公共错误、配置和指标使用稳定术语。文档示例不得包含真实用户数据或 Secret。

### 25.6 Change Synchronization

变更若影响文档，PR 必须同步更新。自动检查链接、术语、过期 Owner 和 ADR 状态；文档评审是 Definition of Done 的一部分。

---

## 26. Development Workflow

### 26.1 Standard Flow

1. **Intake：** 关联 Approved Requirement、缺陷、风险或技术债务。
2. **Clarify：** 明确 Actor、Outcome、Scope、Acceptance、Data、Security 与版本影响。
3. **Architecture Check：** 对照 01–10 基线和 ADR Matrix；冲突先停止并提 ADR。
4. **Design Slice：** 切分最小纵向用例，定义 Domain/Application/Interface/Infrastructure 责任。
5. **Test Plan：** 在编码前确定场景、黄金样例、契约、失败和非功能测试。
6. **Implement：** 仅在获得编码授权后按层次与小步变更实现。
7. **Local Verify：** 格式、类型、Unit、Architecture、Secret 和相关 Integration。
8. **Pull Request：** 提交影响、测试、风险、迁移与回退证据。
9. **Review and CI：** Owner 审查与自动门禁。
10. **Merge and Observe：** 合并后验证主分支与非生产环境。
11. **Release：** 按 Roadmap、CI/CD 和 Scope Freeze 晋级。
12. **Learn：** 监控、反馈、Incident 和债务回流。

### 26.2 Definition of Ready

工作开始前至少明确：需求/缺陷来源、范围、不做事项、Acceptance、Context/Owner、数据与权限、错误/版本、测试策略、依赖和是否需要 ADR。

### 26.3 Definition of Done

完成意味着：行为满足验收、测试通过、无新增高风险债务、日志/指标/审计可用、权限/隐私验证、文档同步、迁移/回退明确、Feature Flag 有清理计划、Owner 接受。

### 26.4 Spike / Proof of Concept

Spike 用于消除技术未知，不形成生产承诺。设置时间、问题、成功标准和删除/转化决定；PoC 代码不能未经重构、测试和 Review 直接进入生产。

### 26.5 Refactoring

重构保持外部行为与基线不变，通过测试保护。涉及 Boundary、Contract、Transaction 或 Version 的“重构”实际是架构变化，必须走 ADR。

### 26.6 Bug Workflow

先建立可复现证据和影响范围，再修复根因并增加回归测试。数据错误需评估历史对象、Audit、用户通知和再生成策略；禁止直接改生产数据库掩盖。

### 26.7 Incident Feedback

Incident 产生 Timeline、Root Cause、Detection Gap、Corrective Action、Owner 和期限。行动项进入正常 Issue/Review，不在事故后用全局绕过长期存在。

### 26.8 No-Code Authorization Gate

本指南获批不等于允许编码。只有用户明确回复“需求与架构评审通过，可以进入编码阶段”，工程流程的 Implement 步骤才可启动。

---

## 27. Engineering Governance

### 27.1 Baseline

01–09 Approved 文档与本文件未来 Approved 版本构成 Engineering Architecture Baseline。工程标准不能降低上游安全、隐私、领域、数据、API 或技术要求。

### 27.2 Ownership Model

| Asset | Owner Responsibility |
|---|---|
| Context Module | 边界、Ubiquitous Language、公开 Contract 和质量 |
| Shared Engineering | 最小范围、兼容、文档和升级 |
| Frontend Feature | 用户旅程、API、可访问性和 i18n |
| Test Suite | 信号质量、Flaky、Fixture 和门禁 |
| Dependency | 版本、安全、许可证和替代 |
| Pipeline / Tool | 可用性、权限、升级和故障 |
| Runbook / Alert | 准确性、演练和响应 |

### 27.3 Quality Gates

Gate 按风险分层，但以下不可因进度默认跳过：Architecture Boundary、Domain Regression、Authentication/Authorization、Secret Scan、Data Migration Safety、Immutable History 和 Critical Audit。

### 27.4 Exception

Exception 写明范围、理由、风险、补偿、Owner、到期和退出计划。涉及 ADR Matrix 的例外仍需 ADR；到期未关闭自动升级为阻断风险。

### 27.5 Technical Debt

债务按 Security/Privacy、Data Integrity、Recoverability、Architecture Boundary、Reliability、Performance 和 Maintainability 分类。每项有影响、Owner、期限和验证。安全、删除复活、版本不可复现和跨 Context 破坏为最高优先级。

### 27.6 Engineering Metrics

可以使用 Lead Time、Review Time、Change Failure Rate、Flaky Rate、Escaped Defects、Dependency Age、Architecture Violations 和 MTTR 等改进工程，不以行数、Commit 数或个人工时作为质量排名。

### 27.7 Dependency and Tool Governance

新增依赖说明用途、替代、许可证、安全、大小、运行影响和 Owner。无维护、重复、仅为微小功能或进入 Domain 的依赖优先拒绝。

### 27.8 AI-Assisted Engineering

AI 生成的变更与人工变更执行同样 Review、测试、许可证、Secret 和责任要求。不得把用户命例、生产日志、Secret 或受限代码发送给未批准工具。提交者对结果负责。

### 27.9 Governance Review Cadence

每个 Milestone 检查 Architecture Drift、Dependency、Debt、Flaky、Security、Performance 和 Documentation。Beta/RC/GA Scope Freeze 继续约束工程范围。

---

## 28. ADR Reference Matrix

| Topic | ADR Required | Trigger Example |
|---|---|---|
| Project / Repository Structure | Yes | Monorepo/Polyrepo、顶层边界或制品所有权改变 |
| DDD Layering | Yes | Domain 开始依赖 Framework/Infrastructure |
| Module / Context Packaging | Yes | 合并 Context Package 或共享内部 Entity |
| FastAPI Organization | Yes | Route/DI/Background Task 改变应用责任边界 |
| Next.js Organization | Yes | Router/Rendering 模型改变安全或 API 边界 |
| Repository Pattern | Yes | 通用 Repository、跨 Context Repository 或 Active Record 化 |
| ORM Strategy | Yes | ORM 渗透 Domain 或改变 Mapping/Unit of Work |
| Dependency Injection | Yes | 引入/替换 Container 或 Service Locator 模型 |
| Transaction Strategy | Yes | 改变单 Aggregate/Context原则或引入分布式事务 |
| Domain Event Implementation | Yes | 改变 Outbox、发布时点、幂等或 Event Contract |
| Configuration Strategy | Yes | 改变来源、动态传播、Flag 或 Business Config 边界 |
| Logging Strategy | Yes | 改变结构、敏感数据、聚合或 Audit 分工 |
| Error Handling | Yes | 改变错误分类、传播或 API 映射 |
| Validation Strategy | Yes | 将领域验证移到 Interface/Infrastructure |
| Testing Strategy | Yes | 改变 Test Pyramid、Golden/Contract 或 Release Gate |
| Static Analysis | Yes | 取消 Architecture/Type/Security 强制门禁 |
| Git Workflow | Yes | 从 Trunk-Oriented 改为其他长期集成模型 |
| Branch Strategy | Yes | 新增长期分支或改变保护/发布来源 |
| Commit / History Strategy | Yes | 改变 Merge/Squash/Rebase 与追溯要求 |
| Code Style / Naming | Yes | 改变自动格式、类型或 Ubiquitous Language 政策 |
| Pull Request Governance | Yes | 改变必需 Reviewer、CI 或审批门禁 |
| Generated Code Policy | Yes | 引入大规模生成并改变 Review/Ownership |
| Documentation Policy | Yes | 改变 ADR/Baseline 的权威或同步要求 |

任何涉及以上内容的修改，都不得直接修改本文档。必须先提交 ADR，说明背景、候选、影响、迁移、兼容、安全、回退、Owner 和退出条件；ADR 批准后才能更新 Engineering Baseline。

---

## 29. Implementation Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐做法 |
|---|---|---|---|
| Anemic Domain Model | Entity 只有数据，所有规则散落 Service | 不变量可被绕过、规则重复、状态失控 | 把合法行为和不变量放回 Aggregate/Value Object/Domain Service |
| Fat Controller | Controller 负责授权、事务、规则、Repository 和 Provider | 协议与业务耦合、难测试、API 漂移 | Controller 只适配协议并调用 Application Handler |
| Fat Repository | Repository 提供任意查询、业务判断和跨表操作 | 绕过 Aggregate、God Data Access、事务不清 | 以 Aggregate Root 最小持久化；复杂读取用 Query Adapter |
| Business Logic in Infrastructure | Adapter、ORM Hook、Trigger、Consumer 决定领域规则 | 规则隐藏、不可版本化、难复现 | Infrastructure 只执行技术能力，调用 Domain/Application 决策 |
| Business Logic in Controller | Interface 直接计算命盘、Evidence 或状态 | 多入口结果不一致、无法复用和审计 | 将业务行为放在 Domain，编排放 Application |
| Shared Mutable State | 请求、用户或 Context 共享可变全局对象 | 数据串扰、并发缺陷、隐私泄漏 | 不可变值、请求 Scope、持久权威状态和显式 Cache 隔离 |
| Cross Context Repository Access | 模块直接调用其他 Context Repository/ORM | 所有权消失、事务和迁移耦合 | 使用公开 Query、Snapshot、Command/Event 和 Saga |
| God Service | 一个 Service 管理所有 Context/Use Case | 依赖爆炸、难测试、修改影响全局 | 按 Context 与 Use Case 拆分 Application Service/Handler |
| Circular Dependency | 模块相互导入或运行时延迟查找 | 初始化脆弱、责任不清、无法独立测试 | 重审方向，使用 Event/Port 或最小稳定共享能力 |
| Hardcoded Configuration | 端点、阈值、保留期、Locale 或开关写死 | 环境漂移、不可审计、紧急变化需改代码 | Typed Config、环境绑定、版本和安全默认 |
| Copy-Paste Business Logic | 前后端或多个 Handler 复制同一规则 | 修复不一致、版本漂移 | 单一 Domain 能力；共享仅在语义稳定后提取 |
| Ignoring Domain Events | 状态变化不产生/处理 Approved Event | 下游投影、Audit、Saga 丢失 | Aggregate 产生 Event，Unit of Work + Outbox 可靠发布 |
| Ignoring Transaction Boundary | Repository 自行 Commit 或一个请求跨 Context | 半完成、重复、锁和恢复困难 | Application 持有单 Context Unit of Work，跨域最终一致 |
| Leaking ORM into Domain | Entity 继承 ORM 或返回 Session/Query | Domain 被 Persistence 锁定、Lazy Load 隐患 | 独立 Persistence Model/Mapper 和 Repository Port |
| Overusing Dependency Injection | 每个函数都建 Interface/Binding 或运行时查找 | 复杂度、调试成本和循环依赖 | 只注入有生命周期/外部边界的依赖，纯函数直接调用 |
| Generic CRUD Service | 用万能 CRUD 替代业务 Command | 绕过状态机、授权和不可变规则 | 暴露明确 Use Case 与领域行为 |
| Exception Swallowing | 捕获后返回空值/成功或只写日志 | 数据错误被掩盖、调用方错误决策 | 分类、传播稳定失败、必要告警和回归测试 |
| Mock-Only Testing | 所有外部能力只用 Mock | Contract 与生产漂移 | Mock 用于 Unit，Adapter 必须真实 Contract/Integration Test |
| Test Through UI Only | 所有规则只靠 E2E | 慢、脆弱、难定位、分支覆盖不足 | 领域/应用 Unit 为主体，少量关键 E2E |
| Feature Flag Without Sunset | 临时 Flag 永久存在 | 组合爆炸、不可测试产品变体 | Owner、到期、清理任务和正式化决定 |
| Utility Dumping Ground | `common`/`utils` 收纳任意业务函数 | 隐藏耦合、无人负责 | 放回 Context；共享需稳定语义和 Owner |
| Direct Production Data Fix | 手工 SQL 改状态绕过应用 | Audit/不变量/版本链破坏 | 受控修复 Use Case、审批、备份和验证 |
| Comments as Architecture | 只靠注释约束跨层访问 | 无自动执行、持续漂移 | Architecture Test、Package Boundary 和 Review Gate |
| Premature Plugin Framework | 无第二真实模块就建动态扩展 | 安全、兼容和延期风险 | 保持内部最小契约，真实需求后 ADR |

---

## 30. Review Checklist

### 30.1 Document and Authorization

- [ ] 文档状态是否为 Review、版本是否为 0.9。
- [ ] 是否严格继承 01–09 Approved 基线。
- [ ] 是否未改变 Domain、Aggregate、Entity、Value Object、API、Data 或 Technology Baseline。
- [ ] 是否没有 Python/TypeScript/SQL 或任何可运行代码。
- [ ] 是否没有 Controller、Page、OpenAPI、Docker、Kubernetes、Terraform 或 CI 配置。
- [ ] 是否未授权进入编码阶段。

### 30.2 Structure and DDD

- [ ] 逻辑目录是否兼容 Monorepo/Polyrepo 待决状态。
- [ ] Backend 是否按 Context + Layer 组织。
- [ ] Frontend 是否按用户 Feature 组织而非复制 Aggregate。
- [ ] Domain 是否无 Framework、ORM、HTTP、Queue 和 Provider 类型。
- [ ] Aggregate Root 是否为唯一写入口。
- [ ] Application Handler 是否只编排已批准用例。
- [ ] Saga/AnalysisProgress 是否未成为 Domain Aggregate。

### 30.3 Infrastructure Implementation

- [ ] DI 是否显式且无 Service Locator/循环依赖。
- [ ] Config、Secret、Flag 和 Business Version 是否分离。
- [ ] Logging 是否结构化、去敏并与 Audit 分离。
- [ ] Error 是否分层、稳定、安全且映射批准 API Contract。
- [ ] Validation 是否位于正确责任层。
- [ ] Repository 是否按 Context/Aggregate Root 隔离。
- [ ] ORM 是否未泄漏，Transaction 是否由 Application 拥有。
- [ ] Domain/Integration Event、Outbox/Inbox 和幂等是否正确。

### 30.4 Quality and Workflow

- [ ] Test Pyramid 是否以 Domain/Application Unit 为基础。
- [ ] 黄金命例、AI、安全、隐私、性能和恢复测试是否覆盖。
- [ ] 测试数据是否合成或经批准且无生产 Secret。
- [ ] Code Style、Naming 和 Static Analysis 是否可自动执行。
- [ ] Git/Branch/Commit/PR 是否支持小变更与可追溯发布。
- [ ] Code Review 是否覆盖领域、数据、API、安全和可靠性。
- [ ] Documentation、ADR、Runbook 是否随变更同步。
- [ ] Exception、Debt、Dependency 和 AI-Assisted Engineering 是否受治理。

### 30.5 ADR and Next Stage

- [ ] ADR Reference Matrix 是否覆盖重大工程变化。
- [ ] Monorepo/Polyrepo、ORM、DI、工具链等待决项是否未被擅自确定。
- [ ] Beta/RC/GA Scope Freeze 是否继续生效。
- [ ] 进入 11 前是否完成 Implementation Guide Review。

---

## 31. Open Questions

### 31.1 Repository and Project Setup

1. 采用 Monorepo 还是 Polyrepo，以及前端、后端、平台和文档的制品边界。
2. Python Package、TypeScript Workspace 和模块根命名的最终约定。
3. Next.js 使用哪种受支持 Router/Rendering 模式作为第一方标准。
4. Shared Kernel 的初始最小内容和审批 Owner。
5. 是否需要 Preview Environment 对应的临时测试资产目录。

### 31.2 Backend Tooling

1. Python ORM、Migration、DI、Task、HTTP Client 和配置工具的具体组合。
2. 同步/异步数据库访问模式及其 FastAPI/Worker 一致性。
3. Unit of Work 与 Repository Port 的具体 Package 归属标准。
4. Outbox/Inbox、Idempotency 和 Scheduler 的实现工具选择。
5. Architecture Dependency Test 的工具与规则表达方式。

### 31.3 Frontend Tooling

1. Design System、Component、Form、Server State 和测试工具选择。
2. API Client 是手工维护受控 Adapter，还是未来由批准契约生成部分类型。
3. i18n/RTL、Accessibility 和 Visual Regression 工具链。
4. 前端错误追踪、性能和 Analytics 的隐私边界。
5. Browser Session 与 Server/Client Component 的最终安全分工。

### 31.4 Testing and Quality

1. Unit/Integration/E2E 的目标执行时间和 Release Gate。
2. 关键模块 Coverage、Mutation 或场景覆盖的量化门槛。
3. 黄金命例集的 Owner、版本、访问和更新流程。
4. AI Evaluation 的固定集、人工抽检比例、成本预算和供应商调用频率。
5. Performance、Security、Privacy 和 DR Suite 的执行周期。
6. Flaky Test 最大修复期限与隔离权限。

### 31.5 Git and Review

1. Merge/Squash/Rebase 的主分支历史策略。
2. 是否需要 Release Branch，或完全通过 Tag/制品晋级发布。
3. PR Size、Review SLA、必需 Approval 数和 Code Owner 配置。
4. Commit Message 自动校验与 Issue/ADR 关联方式。
5. Security Fix 的私密协作和披露流程。

### 31.6 Security, Privacy and Legal

1. 开发、测试、支持和生产调试的数据访问级别。
2. 日志、Trace、Fixture、Snapshot 和失败制品的保留期限。
3. AI-Assisted Engineering 可使用的工具、数据分类和区域限制。
4. 第三方依赖许可证与传统知识材料在测试中的使用边界。
5. 用户数据删除后，测试/回归授权数据的撤回与清理流程。

### 31.7 Engineering Operations

1. Formatter、Linter、Type、SAST、Secret、Dependency、License 和 SBOM 工具选择。
2. Local Development 依赖使用真实服务、容器化替身还是受控 Sandbox 的组合。
3. 统一 Developer Setup、测试数据库和合成数据生成方式。
4. Engineering Metrics、Dashboard 和技术债务 Review 周期。
5. Production Hotfix、Break-Glass 和回退/前滚的批准人。

### 31.8 ADR Candidates

- ADR-CANDIDATE-IMPL-001：Monorepo/Polyrepo 与逻辑 Workspace 物理映射。
- ADR-CANDIDATE-IMPL-002：Python ORM、Migration、Repository 与 Unit of Work 实现组合。
- ADR-CANDIDATE-IMPL-003：Dependency Injection/Composition Root 工具与生命周期。
- ADR-CANDIDATE-IMPL-004：FastAPI Router、Worker、Scheduler 与 Background Task 工程边界。
- ADR-CANDIDATE-IMPL-005：Next.js Router、Server/Client、State 与 API Client 标准。
- ADR-CANDIDATE-IMPL-006：Testing、Static Analysis 和 Security Toolchain。
- ADR-CANDIDATE-IMPL-007：Git History、Release Branch、Commit 与 PR Governance。
- ADR-CANDIDATE-IMPL-008：Logging/Tracing SDK、Redaction 和 Audit Adapter 边界。
- ADR-CANDIDATE-IMPL-009：Outbox/Inbox、Domain Event Dispatch 和 Consumer Idempotency 实现。

---

## 32. Risks

| Risk | Manifestation | Impact | Mitigation / Gate |
|---|---|---|---|
| 目录替代架构 | 有文件夹但跨 Context 私有导入 | 模块化单体变泥球 | Architecture Tests、Code Owner、Review |
| Domain 贫血 | 规则全部进入 Service/Handler | 不变量失控、重复逻辑 | Domain Unit Test、Aggregate Review |
| FastAPI 侵入 | Dependency/Request/ORM 进入 Domain | 框架锁定、难测试 | Interface Adapter + Composition Root |
| Next.js 复制规则 | 浏览器计算正式命盘/权限 | 多真相源和安全风险 | API 为正式来源、前端只做 UX 验证 |
| Repository 失控 | 通用全库 Repository/跨 Context Join | 所有权和事务破坏 | Aggregate Port、Query Adapter、权限隔离 |
| ORM Lazy Load | 隐式查询、跨事务/Context 访问 | 性能和一致性不可控 | 显式加载、Mapper、Contract Test |
| 事务过大 | 外部调用或多个 Context 在同一事务 | 锁、失败和恢复困难 | 单 Aggregate UoW、Saga/Outbox |
| Event 丢失/重复 | 提交后未发或重复消费 | Projection/Saga 错误 | Outbox/Inbox、幂等、故障测试 |
| DI 复杂化 | Container 隐式解析和循环 | 调试困难、生命周期串扰 | Constructor Injection、Composition Root |
| 配置漂移 | 默认值、Flag、Business Version 混用 | 环境不一致、规则绕过 | Typed Config、分类、审计和启动校验 |
| 日志泄漏 | BirthInput、Prompt、Token 被记录 | 隐私和安全事件 | 禁记清单、Redaction、测试和扫描 |
| 错误吞掉 | 空列表/成功代替失败 | 用户误解、数据污染 | Stable Error、Catch Boundary、告警 |
| Mock 漂移 | 测试全绿但 Adapter 不兼容 | 生产失败 | Contract/Integration Test |
| E2E 过重 | 所有信心依赖 UI 测试 | 慢、Flaky、反馈延迟 | Test Pyramid、低层测试优先 |
| 黄金样例失管 | 无来源或版本的命例更新 | 排盘回归无可信基线 | Expert Approval、Version、Audit |
| AI 回归不稳定 | 供应商波动导致门禁失真 | 假失败或风险漏检 | 固定证据/版本、Validation、分层评估 |
| Git 长期分支 | 大批量合并、冲突和延迟反馈 | Release 风险 | 短分支、小 PR、Feature Flag |
| Review 形式化 | 只看格式不看边界/风险 | 缺陷进入主分支 | Required Owner、Checklist、证据 |
| 静态规则被关闭 | Suppression 无 Owner/期限 | 债务和安全盲区 | Exception Policy、到期阻断 |
| AI 辅助泄密 | 把代码/数据/Secret 发给未批准工具 | 知识产权与隐私风险 | Approved Tool、Data Policy、人工责任 |
| 未授权开工 | Guide 通过即创建代码 | 治理流程失效 | 明确 Authorization Gate、用户确认 |

---

## 33. 进入下一阶段《11-DEPLOYMENT-OPERATIONS.md》所需输入条件

- [ ] `10-IMPLEMENTATION-GUIDE.md` 已完成评审并成为 Approved 1.0 Engineering Baseline。
- [ ] 逻辑 Workspace、Backend Context/Layer 和 Frontend Feature 结构已确认。
- [ ] Monorepo/Polyrepo 若影响 Deployment Ownership，已通过 ADR 或保持为 11 的阻断输入。
- [ ] FastAPI Composition Root、Router、Worker、Scheduler 和 Background Task 边界已确认。
- [ ] Next.js Router、Server/Client、安全、i18n/RTL 和 API Client 原则已确认。
- [ ] DDD Entity、Value Object、Aggregate、Factory、Service、Event、Saga 的实现规则已确认。
- [ ] DI、Configuration、Secret、Feature Flag 和 Business Version 分工已确认。
- [ ] Logging、Error、Validation、Audit 和 Sensitive Data Redaction 规则已确认。
- [ ] Repository、ORM、Mapper、Unit of Work、Transaction、Outbox/Inbox 和 Concurrency 原则已确认。
- [ ] Testing Strategy、Golden Case、AI Regression、Security/Privacy、Performance 和 DR 门禁已确认。
- [ ] Code Style、Naming、Static Analysis、Git、Branch、Commit、PR 和 Review 标准已确认。
- [ ] Documentation、ADR、Exception、Debt、Dependency 和 AI-Assisted Engineering 治理已确认。
- [ ] 影响部署与运行的工具选择已有 Approved ADR，或 11 只描述不依赖具体产品的运行规范。
- [ ] 安全、隐私、法律和命理专家待确认项已有 Owner 与最迟决策点。
- [ ] Beta、RC、GA Scope Freeze 继续生效。
- [ ] 下一阶段仅生成 Deployment & Operations 设计，不生成业务代码、部署配置、Pipeline 文件或 Infrastructure as Code。
- [ ] 未收到用户明确的编码授权前，任何阶段都不得创建项目骨架或可运行实现。

只有本工程实现规范通过评审后，才可以生成 `11-DEPLOYMENT-OPERATIONS.md`。本次不得生成该文件，也不得进入代码实现阶段。

