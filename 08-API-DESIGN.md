# AI 八字命理分析平台：API 设计规范

**文档编号：** 08  
**文档类型：** API Design Specification  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md`、`02-SRS.md`、`03-SYSTEM-ARCHITECTURE.md`、`04-DOMAIN-MODEL.md` 1.0、`05-DATA-MODEL.md` 1.0、`06-ROADMAP.md` 1.0、`07-APPLICATION-ARCHITECTURE.md` 1.0（均已 Approved）  
**目标读者：** 产品负责人、API 与应用架构师、安全与隐私负责人、领域与数据负责人、研发、测试、运维及开发者平台负责人

---

## Version 0.9 Change Log

- 首次建立 REST Resource、Command API、Query API、认证授权、错误、幂等、分页、版本与兼容性规范。
- 建立长任务、轮询、Callback 和 Event API 的边界。
- 建立 API Lifecycle、Deprecation、Governance、ADR Reference Matrix 和 Anti-Patterns。
- 本版本仅定义设计规范与概念契约，不是 OpenAPI 文件，不授权进入实现阶段。

---

## 1. Document Purpose

### 1.1 目标

本文档把已批准的产品、领域、数据和应用架构约束映射为稳定、可治理、可测试的 API 设计规范。它定义客户端如何表达业务意图、读取资源、识别异步进度、处理错误和重试，以及平台如何保护身份、权限、隐私、版本和审计边界。

API 是 Interface Layer 的契约，不是 Domain Model 的远程镜像。API 只能调用《07-APPLICATION-ARCHITECTURE.md》批准的 Command、Query 和 Process Manager，不得创造新的领域行为。

### 1.2 适用边界

本文档覆盖三类逻辑 API 边界：

| API Surface | 使用者 | 目的 | 开放阶段 |
|---|---|---|---|
| First-Party API | 平台 Web、未来受控官方客户端 | 支撑普通用户与后台已批准用例 | 随对应产品版本开放 |
| Developer API | 经认证的 DeveloperClient | 使用批准的 Charts、Calculations、Analyses、Reports 等资源 | V2；不属于 MVP/V1 默认范围 |
| Governance API | 经授权的内部编辑、专家、审核、审计与支持角色 | 执行审核、发布、调查和数据权利流程 | 随治理能力受控开放，不作为公共 API |

三类 Surface 可以有不同授权和可见范围，但必须共享本文件定义的资源语义、错误原则、安全基线和治理门禁。

### 1.3 不包含内容

本文档不包含：

- OpenAPI、Swagger、GraphQL Schema 或 gRPC Proto；
- Controller、DTO、Repository、Service 实现或业务逻辑；
- Request Body、Response Body 或字段级传输 Schema；
- Java、Go、Python、TypeScript、SQL 或 SDK；
- 数据库、网络拓扑、网关产品或部署配置；
- 具体认证产品、密钥格式或加密算法选型；
- Aggregate、Entity、Value Object、Domain Event 或 Bounded Context 的重新定义；
- 具体命理算法、规则、Prompt 或知识内容。

### 1.4 基线冲突处理

如果 API 便利性要求改变 Aggregate Boundary、Context Relationship、Identity、Version、Immutable Object Rules 或应用用例语义，本文只登记 `ADR Candidate` 或 `Open Question`。ADR 未批准且对应基线未更新前，API 不得采用该变化。

---

## 2. API Design Principles

### API-P-001 Resource Oriented

URI 表达稳定业务资源或用例产生的操作资源，不使用 Controller、表名或任意动词作为模型。

### API-P-002 Use Case Aligned

写接口只暴露已批准 Command 的外部意图；读接口只暴露已批准 Query。一个 Endpoint 不得发明新的业务路径。

### API-P-003 Contract Before Implementation

接口语义、授权、幂等、错误、兼容性和审计必须先评审，再进入实现设计。实现细节不能反向改变外部契约。

### API-P-004 Default Deny

认证成功不等于有权访问资源。每次调用均在服务端验证 Role、Scope、Ownership、Tenant、Purpose、Consent 和资源状态。

### API-P-005 Data Minimization

只暴露完成当前用途所需的信息。出生资料、命盘、对话、报告、审计和第三方 AI 相关数据按敏感级别最小化、遮蔽和隔离。

### API-P-006 Explicit Version

客户端必须明确所调用的 API Major Version；业务结果同时保留自身 Algorithm、Rule、Knowledge、Prompt、Model、Snapshot 和 Report Version，二者不得混淆。

### API-P-007 Idempotent Intent

可能重复提交、重试或产生正式对象的 Command 必须具有业务幂等语义。技术重试不得变成新的正式业务意图。

### API-P-008 Observable and Auditable

每次调用具有 RequestId；跨请求流程具有 CorrelationId；分布式追踪使用 TraceId。关键调用必须形成最小充分审计。

### API-P-009 Async by Explicit Contract

耗时或跨 Context 流程返回独立 Operation 身份和可查询状态，不让同步连接无限等待，也不把已受理伪装为已完成。

### API-P-010 Safe Errors

错误对客户端可诊断、可本地化并明确是否可重试，同时不得暴露堆栈、SQL、供应商原始输出、密钥或资源存在性敏感信息。

### API-P-011 Backward Compatible by Default

同一 Major Version 内只允许兼容性扩展或已治理弃用。客户端不得依赖未承诺的字段顺序、默认排序或内部枚举。

### API-P-012 Immutable History

API 不提供原地修改 Valid Snapshot、Completed RuleRun、Frozen EvidenceBundle、Completed AIAnalysis、Published 定义或 Frozen Report 的能力。

### API-P-013 Context Ownership

一个 API Resource 可组合展示已授权信息，但写操作只能由目标 Aggregate 所属 Context 执行。API 不建立跨 Context 事务。

### API-P-014 Human-Centered

面向普通用户的 API 支持清晰进度、明确不确定性和安全错误；不得通过接口语义暗示命理具有科学预测能力或必然准确。

---

## 3. REST Resource Model

### 3.1 Resource 分类

| Resource Type | 含义 | 示例 |
|---|---|---|
| Primary Resource | 具有稳定身份、可独立授权和查询的业务资源 | Chart、Report、Conversation |
| Immutable Snapshot Resource | 内容冻结后只读的版本事实 | CalculationSnapshot、Frozen Report 表示 |
| Child Resource | 生命周期由父资源约束，但仍通过稳定身份引用 | Conversation Message、Consent Record |
| Operation Resource | 表示异步或多步骤请求的处理状态 | Calculation Operation、Analysis Operation、Deletion Operation |
| Collection Resource | 同一授权边界下的资源集合 | 当前用户的 Charts、Reports |
| Governance Resource | 仅供内部受控角色审核与发布 | AlgorithmVersion、RuleSetVersion、KnowledgeArticleVersion |
| Projection Resource | 可重建、最终一致的只读视图 | AnalysisProgress、Usage Summary |

Resource Type 不改变 Domain Model。Operation 和 Projection 尤其不得被解释为新的 Domain Aggregate。

### 3.2 Resource Catalog

| Resource | API 语义 | 允许的主要能力 | 可见范围 | 禁止语义 |
|---|---|---|---|---|
| Current User | 当前认证主体的账户视图 | 读取偏好、管理允许的账户动作 | First-Party | 枚举其他用户 |
| Consents | SubjectConsent 的用途决定视图 | 查询当前决定、授予、拒绝、撤回 | First-Party / Governance 最小范围 | 改写历史 ConsentRecord |
| Birth Profiles | 出生资料容器与输入确认入口 | 创建、读取、确认输入、归档 | First-Party | API 自动补全不确定出生事实 |
| Charts | 确定性命盘业务对象 | 创建、读取、归档、读取当前 Snapshot 引用 | First-Party / Developer V2 | 管理 RuleRun、AI、Evidence 或 Report 生命周期 |
| Calculation Snapshots | 已验证计算事实的不可变视图 | 按明确 SnapshotId 读取 | First-Party 专业视图 / Developer V2 | 修改事实或静默切换到最新版本 |
| Calculations | 发起和观察确定性计算的 Operation Resource | 提交、查询状态、读取结果引用 | First-Party / Developer V2 | 选择未发布算法或覆盖历史 Snapshot |
| Analyses | 受范围约束的分析与正式 AIAnalysis 结果视图 | 发起、查询状态、读取已验证结果 | First-Party / Developer V2 | 绕过 Evidence 和风险检查 |
| Conversations | 受 Chart 与主题范围约束的会话 | 创建、查询、关闭 | First-Party / Developer V2 | 跨 Chart 泄漏上下文 |
| Messages | Conversation 内的消息意图和完成状态 | 提交用户消息、读取安全结果 | First-Party / Developer V2 | 直接提交模型供应商原始结果为正式答案 |
| Evidence | 对有权主体开放的证据及来源元数据 | 查询 Bundle 摘要和 Evidence | First-Party / Developer V2 | 暴露受限知识全文或其他主体证据 |
| Timelines | Basic 或 Analytical Timeline 视图 | 发起允许范围构建、查询版本和节点 | First-Party / Developer V2 | 无界生成或绝对吉凶裁决 |
| Reports | 报告生成意图、状态和 Frozen 结果 | 创建、查询、归档、明确再生成 | First-Party / Developer V2 | 原地修改 Frozen Report |
| Usage | 当前主体或租户的额度与调用摘要 | 查询用量、限流和成本摘要 | Developer V2 / First-Party | 暴露供应商密钥或其他租户用量 |
| Webhook Subscriptions | 客户端对批准事件的订阅意图 | 创建、暂停、轮换凭据、删除 | Developer V2 | 订阅敏感正文或内部 Domain Event 全量流 |
| Operations | 长任务与 Saga 的外部状态投影 | 查询进度、结果引用、失败和可选取消能力 | 依原资源授权 | 作为领域事实来源或直接改 Aggregate |
| Analysis Progress | 跨流程只读查询投影 | 展示步骤状态、延迟和终态 | First-Party / 受控 Developer | 反向驱动或修改源对象 |
| Audit Views | 经批准调查的最小审计投影 | 检索、调查、导出受控摘要 | Governance only | 普通管理员修改或删除审计事实 |

### 3.3 Public Developer API Scope

V2 Developer API 的正式资源边界继承 SRS：Charts、Calculations、Analyses、Reports、Timeline、Conversations、Evidence、Usage 和 Webhooks。Birth Profiles、Consents、治理资源、Audit Views 和数据权利接口是否向第三方开放，属于独立产品、安全、隐私与法律决策；未批准前默认不开放。

### 3.4 Resource Representation Rules

本文不定义具体 Response Body，但所有正式表示必须遵循以下语义：

1. 使用稳定 Identity，不把版本、时间、地区或顺序编码进 ID。
2. 显式区分 Resource Identity、Business Version、API Version 和 Projection Version。
3. 对不可变资源显示其冻结或有效状态以及上游版本引用。
4. 资源链接只能指向调用方有权发现的对象。
5. 缺失敏感字段不得被解释为字段不存在；可能是授权遮蔽。
6. 时间表达必须带明确时区或声明为 UTC；出生本地时间仍遵循领域中的 TimeZoneInfo 和精度语义。
7. 枚举值和状态值由契约注册表治理，不暴露内部类名。
8. AI 与命理文本必须保留证据状态、风险提示和非科学预测定位。

### 3.5 Aggregate Boundary Protection

- API 可以为阅读体验组合多个 Read Model，但组合结果不成为新的写入 Aggregate。
- 跨 Context 只传递 Aggregate Root Identity、不可变 Snapshot 引用或批准的 Integration Event。
- API 不允许客户端直接创建 RuleFinding、Evidence、CalculationSnapshot 或 AuditEvent 等内部对象。
- 子资源路径不表示客户端可以绕过 Aggregate Root 修改内部 Entity。
- 任何资源模型变化若影响 Domain/Data 基线，必须先通过 ADR。

---

## 4. URI Design Rules

### 4.1 基本格式

| 规则 | 规范 |
|---|---|
| API Major Version | URI 顶层显式包含 Major Version，例如 `/v1`；示例仅表达规范，不承诺已开放版本 |
| Resource Name | 使用英文、小写、复数、连字符分词的名词 |
| Identity Segment | 使用不透明稳定 ID，不含业务含义 |
| Collection | 资源复数名词表示集合 |
| Single Resource | 集合后跟该 Resource Identity |
| Child Resource | 仅在所有权和生命周期确有父子关系时嵌套 |
| Operation | 使用名词化 Operation Resource，不使用任意 RPC 动词 |
| Query Parameters | 仅用于筛选、排序、分页、字段视图和明确的只读展开 |

### 4.2 Resource Naming

- 使用平台统一英文术语：`charts`、`calculations`、`analyses`、`reports`、`timelines`、`conversations`、`evidence`、`operations`。
- 不使用数据库表名、内部模块名、代码类名或供应商名。
- 不在 URI 中使用 `get`、`create`、`update`、`delete`、`execute` 等通用方法动词。
- 对明确业务动作，优先创建命名清晰的意图或 Operation Resource，例如 report regeneration request，而不是通用 `/action`。
- 缩写只有进入统一术语表后才可使用；ID、AI 等已批准术语除外。

### 4.3 Nesting Rules

1. 嵌套只表达真实所有权或访问上下文，不表达任意导航便利。
2. 嵌套深度原则上不超过两级资源关系；更深关系使用稳定 Identity 和链接表达。
3. Conversation Messages 可以作为 Conversation 子资源；CalculationSnapshot 不因展示便利成为任意 Report 子资源。
4. 同一资源只有一个规范 URI；其他导航路径只能作为链接或重定向策略的候选，不制造多身份。

### 4.4 URI Privacy

URI 不包含姓名、出生日期时间、地点、命理结论、邮箱、手机号、会话问题、Consent 决定、模型名或其他敏感业务内容。URI 可能进入日志、浏览器历史和中间设施，因此只使用不透明 Identity 与非敏感控制参数。

### 4.5 URI Stability

已发布 URI 的资源含义在同一 Major Version 内不可改变。重命名、移动根路径或改变 Identity 解释均属于 Breaking Change，必须执行 ADR、迁移和弃用流程。

---

## 5. HTTP Method Semantics

| Method | 允许语义 | 幂等期望 | 成功状态原则 | 禁止行为 |
|---|---|---|---|---|
| GET | 读取单资源、集合或 Projection | 安全且幂等 | 200；条件读取可为 304 | 触发计算、修复、重试、冻结或删除 |
| POST | 创建资源、提交 Command 或创建 Operation | 默认非幂等；受 Idempotency-Key 保护 | 同步创建 201；异步受理 202；已完成命令可为 200 | 把所有动作塞入单一 Endpoint |
| PUT | 仅在客户端完整替换一个允许替换且 URI 已知的可变资源时使用 | 幂等 | 200 或 204 | 替换 Immutable/Frozen/Published 对象 |
| PATCH | 对允许修改的资源表达受限部分变化 | 业务上需并发控制；不当然幂等 | 200 或 204 | 绕过领域行为进行任意字段更新 |
| DELETE | 请求删除允许删除的资源或 Subscription | 幂等结果语义 | 204、202 或合规拒绝 | 物理删除受 Legal Hold/历史引用保护对象 |
| HEAD | 获取与 GET 一致的元数据而无表示内容 | 安全且幂等 | 200/304/404 策略一致 | 绕过授权探测存在性 |
| OPTIONS | 表达协议能力或受控跨域协商 | 安全且幂等 | 204 或标准结果 | 暴露未授权内部能力 |

### 5.1 Status Code Rules

| HTTP Status | 统一语义 |
|---|---|
| 200 OK | 同步读取成功，或已存在业务意图返回正式结果 |
| 201 Created | 新资源已同步创建，并提供其规范位置 |
| 202 Accepted | 请求已被可靠受理但尚未完成；必须提供 Operation 位置 |
| 204 No Content | 已成功完成且无需返回表示的幂等动作 |
| 304 Not Modified | 合法条件读取命中，且授权仍有效 |
| 400 Bad Request | 协议、语法或通用输入格式无法处理 |
| 401 Unauthorized | 缺少、无效或过期的认证凭据；不得表示资源授权结果 |
| 403 Forbidden | 已认证但明确无权执行；外部可按防枚举策略改用 404 |
| 404 Not Found | 资源不存在，或依据防枚举策略不可向调用方确认存在 |
| 409 Conflict | 当前生命周期、幂等键、唯一性或业务状态冲突 |
| 412 Precondition Failed | If-Match 等并发前置条件不成立 |
| 422 Unprocessable Content | 结构可理解但业务验证、领域前置条件或范围不满足 |
| 429 Too Many Requests | 触发速率、额度或并发限制，并提供 Retry-After（允许重试时） |
| 500 Internal Server Error | 未分类内部失败；不泄漏内部细节 |
| 502 Bad Gateway | 受控依赖返回无效结果 |
| 503 Service Unavailable | 暂时不可用、容量保护或维护；可提供 Retry-After |
| 504 Gateway Timeout | 上游等待超时；不得因此断言业务操作未发生 |

### 5.2 Conditional Requests

- 对允许修改的资源，使用 ETag/If-Match 或等价版本前置条件防止丢失更新。
- 对不可变 Snapshot 和 Frozen Report，ETag 可用于缓存验证，但不得成为修改许可。
- 缺失必要前置条件时可以拒绝修改；具体强制范围由资源契约评审确认。
- 条件失败不自动重试写操作，客户端必须重新读取并重新表达意图。

---

## 6. Command API Principles

### 6.1 Command Exposure Rules

1. 外部 Command 必须映射到《07-APPLICATION-ARCHITECTURE.md》已批准的 Use Case/Command。
2. 并非所有内部 Command 都对外开放；Process Manager 步骤、审计追加和系统完成命令默认内部可见。
3. Command Endpoint 只接受业务意图，不接受客户端指定内部状态转换结果。
4. 客户端不能直接把资源设为 Valid、Completed、Frozen、Published 或 Deleted。
5. Command 在目标 Context 重做授权、状态和不变量校验，不信任上游界面判断。
6. 跨 Context Command 返回 Operation，而不是持有跨 Context 事务。

### 6.2 External Command Catalog

下表定义概念映射，不定义 Request Body、Response Body 或最终 URI 清单。

| External Intent | Resource Approach | Application Command / Use Case | Execution | Required Controls |
|---|---|---|---|---|
| 创建 BirthProfile | 创建 Birth Profile Resource | CreateBirthProfile / UC-A01 | 同步优先 | Consent、年龄、Ownership、幂等、审计 |
| 确认 BirthInput | 创建 Input Confirmation 意图 | ConfirmBirthInput / UC-A02 | 同步验证 | 精度、不确定性、幂等、不可变输入 |
| 创建 Chart | 创建 Chart Resource | CreateChart / UC-A03 | 同步创建 | Confirmed Input、Ownership、幂等 |
| 执行 Calculation | 创建 Calculation Operation | ExecuteCalculation / UC-A04 | 同步或 202，依性能门禁 | Algorithm Version、幂等、验证、审计 |
| 选择 Current Snapshot | 提交 Snapshot Selection 意图 | SetCurrentSnapshot / UC-A05 | 同步 | If-Match、Ownership、Snapshot Valid |
| 创建 RuleRun | 默认由内部流程创建；专业/开发者开放待批准 | RequestRuleRun / UC-A09 | 异步或内部 | Published RuleSet、Scope、幂等 |
| 构建 EvidenceBundle | 默认内部流程，不直接开放 Evidence 创建 | Build/FreezeEvidenceBundle / UC-A10 | 异步内部 | 上游版本、冻结不变量、审计 |
| 发起 AIAnalysis | 创建 Analysis Resource/Operation | PlanAIAnalysis / UC-A12 | 202 | Frozen Bundle、Scope、Consent、Quota、风险策略 |
| 创建 Conversation | 创建 Conversation Resource | CreateConversation / UC-A13 | 同步 | Chart Ownership、Purpose、Quota |
| 提交 Message | 创建 Conversation Message Resource | SubmitAIMessage / UC-A14 | 通常 202 | 三年与主题范围、幂等、速率限制 |
| 构建 Timeline | 创建 Timeline Operation | BuildBasic/AnalyticalTimeline / UC-A15/16 | 同步或 202 | Horizon、版本、Evidence 条件 |
| 生成 Report | 创建 Report Resource/Operation | GenerateReport / UC-A17 | 202 | VersionManifest、上游可用、幂等 |
| 再生成 Report | 创建新的 Regeneration Intent 与新 Report | RegenerateReport / UC-A18 | 202 | 原 Frozen Report 引用、新意图、审计 |
| 归档/恢复资源 | 创建受限状态变更意图 | 对应 Archive/Restore Use Case | 同步优先 | Ownership、If-Match、Legal Hold 语义 |
| 授予/撤回 Consent | 对 SubjectConsent 提交新决定 | Grant/Decline/RevokeConsent / UC-A20 | 同步 | PolicyReference、身份复核、审计 |
| 数据导出 | 创建 Data Export Operation | UC-A21 | 202 | 强身份复核、范围、期限、审计 |
| 用户删除 | 创建 User Deletion Operation | UC-A22 | 202 | 强身份复核、Legal Hold、逐 Context 状态 |

### 6.3 Command Result Semantics

Command 对外结果必须明确区分：

| Result | 含义 |
|---|---|
| Completed | 本次业务意图已完成，并给出目标资源引用 |
| Accepted | 意图已可靠受理，给出 Operation 引用，但业务结果尚未完成 |
| Duplicate | 相同幂等意图已有结果，返回同一资源或 Operation 语义 |
| Rejected | 授权、Consent、风险、不可变规则或领域前置条件禁止 |
| Conflict | 当前状态或版本与意图冲突，需要重新读取后决定 |
| Failed | 操作已到不可恢复终态；不能伪装为 Accepted 或 Completed |

### 6.4 Governance Command Boundary

AlgorithmVersion、RuleSetVersion、KnowledgeArticleVersion 和高风险配置的提交、审核、批准、发布、停用必须使用分离的 Governance API 权限。创建者不得通过同一身份完成要求职责分离的全部步骤。Published 定义不能通过通用 PATCH 修改。

---

## 7. Query API Principles

### 7.1 Query Rules

1. Query 不触发 Command、重算、修复、冻结、发布、删除或业务重试。
2. Query 可以读取 Aggregate 公开投影、Immutable Snapshot 或 Read Model。
3. 所有 Query 执行服务端 Ownership、Role、Scope、Purpose、Consent 和字段级遮蔽。
4. Read Model 必须暴露其一致性或更新时间语义，不能伪装为实时事务事实。
5. 查询历史对象时使用明确 Identity/Version，不自动替换为最新对象。
6. 对资源枚举风险使用一致的 403/404 隐藏策略。

### 7.2 Query Catalog

| Query Resource | Source Semantics | Consistency | Authorization Focus | Prohibited Side Effect |
|---|---|---|---|---|
| Chart Detail | Chart Read Model + 当前 Snapshot 引用 | 当前状态，标明投影时间 | Ownership、专业字段权限 | 不触发 Calculation |
| Calculation Snapshot | Immutable Snapshot Projection | 强版本一致 | Chart Ownership/授权 | 不切换 Current Snapshot |
| Analysis Detail | AIAnalysis/Evidence 的授权投影 | Completed 结果不可变；处理中最终一致 | Scope、Purpose、Consent | 不发起新分析 |
| Conversation History | Conversation Read Model | 单会话顺序 + 状态 | Conversation Ownership | 不跨会话拼接敏感上下文 |
| Evidence Detail | Frozen Bundle 投影 | 冻结版本一致 | Chart Ownership、知识权利遮蔽 | 不返回受限知识全文 |
| Timeline | Basic/Analytical 明确版本 | 明确 Kind、Version、投影时间 | Chart Ownership、Horizon | 不自动构建缺失 Timeline |
| Report | Frozen Report Projection | Frozen 内容强一致 | Ownership/合法分享权限 | 不按当前规则重写旧报告 |
| Analysis Progress | 可重建跨 Context Projection | 最终一致 | 对源 Chart 的访问权 | 不推进 Saga 或修复源状态 |
| Usage Summary | 计量投影 | 标明结算/统计截止时间 | 当前主体/租户 | 不改变额度 |
| Audit Search | Audit Read Model | 追加历史、索引可延迟 | Auditor、调查 Purpose | 不修改源事实 |
| Export Status | Data Rights Process Projection | 分步骤最终一致 | 强身份复核 | 不绕过 Legal Hold |

### 7.3 Sparse and Expanded Views

- 默认表示只包含完成主要用户任务所需的最小信息。
- 专业依据、证据、版本清单和关系展开必须由授权与用途控制。
- `include`、`expand` 或字段选择能力若开放，必须使用白名单、深度上限和成本预算。
- 展开关系不得绕过被展开资源本身的授权。
- API 不承诺任意字段投影；具体字段集合在后续契约阶段定义。

### 7.4 Caching

- 私有敏感资源默认禁止共享缓存。
- 可缓存资源必须把身份、租户、语言、授权视图和 API Version 纳入缓存隔离。
- Consent 撤回、权限变化和删除状态必须触发允许范围内的缓存失效或短期安全策略。
- Frozen/Immutable 资源可使用长期验证式缓存，但访问权仍需检查。
- 缓存命中不得绕过审计要求较高的敏感访问。

---

## 8. Authentication

### 8.1 Authentication Surfaces

| Caller | 认证原则 | 基线要求 |
|---|---|---|
| 匿名试算用户 | 使用受限匿名会话和短生命周期能力 | 不长期保存默认数据；不能访问注册用户资源 |
| 注册用户 | 使用安全、可轮换、可撤销的用户会话 | 退出失效、恢复安全、会话固定防护 |
| 高权限内部用户 | 强认证并满足独立 MFA 策略 | 上线安全评审前确认；敏感操作再认证 |
| DeveloperClient | V2 使用受控 API Credential | 凭据材料安全保存、可轮换、可撤销、Scope 化 |
| System Actor | 使用独立工作负载身份 | 不冒充用户；携带最小 Subject/Purpose 上下文 |

### 8.2 Credential Rules

- 凭据不得出现在 URI、业务 Resource Identity、日志、报告或错误详情中。
- API Credential 只保存不可逆摘要或受控密钥材料，继承系统安全基线。
- 每个凭据绑定明确 Subject/Client、环境、Scope、状态和有效期策略。
- 凭据轮换允许短期受控重叠，撤销必须在安全评审规定的时间内生效。
- 认证失败不得泄露账户或 Client 是否存在。
- 匿名会话升级为注册会话时，不得静默扩大原数据用途或 Consent。

### 8.3 Authentication Failure

认证缺失、过期、签名无效、凭据撤销和会话风险阻断使用 `401` 及 `AUTH-xxx`。是否允许重新认证、刷新或人工恢复由具体认证 Surface 决定，API 不返回敏感判断细节。

### 8.4 Authentication Open Boundary

具体采用何种用户身份协议、Developer Credential 协议、MFA 机制和 Token 生命周期属于 Security Architecture 决策。本文只规定能力与安全结果；选型必须在实施前通过安全评审，重大策略变化需 ADR。

---

## 9. Authorization

### 9.1 Authorization Context

每次调用至少评估适用的：

- Actor Identity；
- Subject Identity；
- Client/Tenant Identity；
- Role 与 API Scope；
- Resource Ownership 或明确授权关系；
- Purpose of Use；
- Consent 当前决定；
- Resource 生命周期与敏感级别；
- 管理操作的工单、理由、期限或双人审批；
- Legal Hold、删除处理中和风险限制。

### 9.2 Authorization Boundary

1. Interface/API 层完成初步鉴权，但目标 Application Service 必须再次执行业务授权。
2. API Gateway 或前端隐藏不构成最终授权。
3. 跨 Context 调用只传递最小可信安全上下文；目标 Context 独立验证。
4. 一个资源的访问权不自动授予其关联资源访问权。
5. Share Credential、Webhook Credential、API Credential 和用户会话互不替代。
6. 管理员不是全局数据所有者；敏感访问需要 Purpose、理由和审计。

### 9.3 Least Privilege

- Scope 按资源与动作拆分，不使用默认全能 Scope。
- Read、Create、Manage、Govern、Audit 和 Data Rights 权限分离。
- 开发者客户端只能访问其 Subject/Tenant 明确授权的数据。
- 内部支持人员默认看到遮蔽视图，临时提权需有时限。
- 发布、权利审核和高风险配置遵循职责分离。

### 9.4 Ownership and Enumeration Protection

对直接对象引用进行资源归属校验。对于无权发现的对象，API 可以统一返回 `404` 与安全 `AUTH-xxx`/通用错误语义；内部审计仍记录真实拒绝原因。列表查询也必须在数据源端施加授权过滤，不能先全量读取再由客户端隐藏。

### 9.5 Authorization Changes

权限撤销、Consent 撤回、Share 撤销和 Client 停用必须阻止新请求。正在运行的流程如何停止、降级或完成，遵循其 Saga 与法律保留规则，不由 API 任意决定。

---

## 10. Security Headers

### 10.1 Request and Trace Headers

| Header / Field | 语义 | 规则 |
|---|---|---|
| Authorization | 提交允许的认证凭据 | 不记录原值；不得出现在 URI |
| Idempotency-Key | 标识一个可重试业务意图 | 适用于规定的 Command；不承载业务敏感信息 |
| X-Request-Id | 单次 HTTP 请求身份 | 客户端可建议；平台验证后接受或重新生成 |
| X-Correlation-Id | 跨请求业务流程关联身份 | 若缺失由平台生成；不得作为授权凭据 |
| traceparent | 标准分布式追踪上下文 | 验证格式与采样策略；不信任外部附带权限 |
| If-Match | 可变资源并发前置条件 | 必要写操作缺失时可拒绝 |
| Accept-Language | 首选本地化语言 | 不改变领域事实；MVP 简体中文为正式质量语言 |

TraceId 来源于受控 Trace Context。RequestId、CorrelationId、TraceId、Resource Identity 和 Idempotency-Key 是不同概念，不得复用。

### 10.2 Response Security and Control Headers

| Header / Policy | 用途 | 规则 |
|---|---|---|
| Strict-Transport-Security | 强制安全传输 | 仅在完整 HTTPS 域治理确认后启用合适策略 |
| Content-Security-Policy | 保护浏览器承载内容 | 适用于浏览器页面/报告展示；不替代输出转义 |
| X-Content-Type-Options | 阻止内容类型嗅探 | 对下载与网页响应统一治理 |
| Referrer-Policy | 限制敏感路径外泄 | 采用隐私保护策略 |
| Cache-Control | 控制私有、不可缓存或验证式缓存 | 敏感资源不得进入公共缓存 |
| Content-Disposition | 控制报告/导出下载 | 文件名不得包含不必要敏感信息 |
| X-Request-Id | 返回平台接受的请求身份 | 所有 API 结果均可关联 |
| X-Correlation-Id | 返回流程关联身份 | 异步受理和错误均保留 |
| Retry-After | 指示允许的最早重试时间 | 用于 429、503 或明确可重试状态 |
| Deprecation / Sunset | 表达弃用与停止支持信息 | 仅按已批准生命周期计划发布 |

### 10.3 CORS and Browser Boundary

CORS 默认拒绝未知 Origin，只允许明确登记的第一方或批准开发者 Origin、Method 和 Header。不得使用宽泛凭据跨域策略。具体 Origin 清单和预检缓存属于部署配置，不在本文定义。

### 10.4 Sensitive Data Masking

- 日志和错误中遮蔽 Token、API Key、Cookie、出生原始输入、详细地点、会话正文及模型原始输出。
- 支持与审计 API 按 Purpose 返回最小字段；遮蔽规则不能由客户端关闭。
- 列表与搜索结果使用比单资源详情更严格的默认视图。
- 导出属于数据权利用例，不通过通用字段展开规避遮蔽。

---

## 11. Idempotency Strategy

### 11.1 Required Commands

以下类型必须支持 `Idempotency-Key`：

- 创建 Chart、Calculation、RuleRun（若开放）、AIAnalysis、Report、Conversation Message；
- Report 再生成；
- 额度或用量会受影响的操作；
- Consent 决定提交；
- 数据导出、对象删除和用户删除；
- Webhook Subscription 创建或凭据轮换；
- 任何客户端可能因超时安全重试的 Command。

### 11.2 Key Semantics

1. Key 在调用主体、API Surface、目标用例和规定有效窗口内唯一。
2. Key 是不透明随机值，不含出生资料、用户 ID、命理主题或其他业务含义。
3. 同一 Key 与同一规范化意图重复提交，返回原 Resource/Operation 及其当前结果语义。
4. 同一 Key 携带不同意图指纹，返回 `409` 和稳定幂等冲突错误。
5. 幂等记录过期不代表可以绕过领域唯一性或创建重复正式结果。
6. 平台故障后无法确定原操作是否完成时，先查询原 Operation，不建议盲目更换 Key。

### 11.3 Concurrent Duplicates

并发相同意图只能有一个 Owner 执行；其他调用返回相同 Operation、处理中结果或明确冲突。外部响应超时不证明后台操作失败。

### 11.4 Event and Callback Idempotency

Webhook/Event Delivery 具有稳定 DeliveryId/EventId。消费者必须按 EventId 幂等；平台重投不改变事件事实。Callback 接收方的重复确认不得重复推进 Saga。

### 11.5 Retention

Idempotency 记录保留期必须覆盖客户端最大重试窗口和最长相关异步流程。具体期限受隐私、成本和运行策略约束，列为 Open Question；期限变化不得破坏历史正式对象的唯一性。

---

## 12. Error Model

### 12.1 Problem Details

错误响应采用 Problem Details 语义，遵循统一媒体类型和可扩展契约。本文不定义具体 Response Body Schema，但正式错误表示至少具备以下概念：

| Concept | 语义 |
|---|---|
| type | 稳定、可文档化的问题类型标识 |
| title | 可本地化的简短安全标题 |
| status | 对应 HTTP Status |
| detail | 面向当前调用方的安全说明，不泄露内部信息 |
| instance | 本次问题实例的安全引用 |
| code | 平台稳定错误码 |
| requestId | 单次请求关联标识 |
| correlationId | 跨流程关联标识 |
| retryable | 是否允许在条件满足后重试 |
| retryAfter | 允许重试时的时间提示 |
| fieldIssues | 允许公开的输入问题集合；不得回显敏感原值 |

`detail` 不得成为客户端业务分支依据；客户端以 HTTP Status、稳定 `code` 和契约化扩展判断。

### 12.2 Error Code Registry

错误码遵循 SRS 已批准前缀。以下为 API 层首批稳定语义目录；具体码值在契约评审中只能按治理规则新增或弃用。

| Prefix | Owner / Scope | API 语义示例 |
|---|---|---|
| AUTH-xxx | Identity / Authorization | 未认证、凭据过期、Scope 不足、Ownership 拒绝 |
| CONSENT-xxx | Consent | 必要同意缺失、Purpose 不允许、授权已撤回 |
| INPUT-xxx | Birth / 通用输入 | 格式无效、地点歧义、时间精度不足 |
| TIME-xxx | Calendar & Time | 本地时间不存在、偏移重复、边界需确认 |
| CALC-xxx | Chart Calculation | 算法版本不可用、验证失败、交叉验证阻断 |
| RULE-xxx | Rule Evaluation | 无适用规则、执行失败、版本已停用、存在冲突 |
| EVIDENCE-xxx | Evidence | Bundle 未冻结、引用不可用、证据权限不足 |
| KNOWLEDGE-xxx | Knowledge | 来源停用、权利限制、版本不可用 |
| AI-xxx | AI | 超时、结构验证失败、事实不一致、风险拒绝 |
| REPORT-xxx | Report | 生成失败、未冻结、VersionManifest 不完整 |
| PRIVACY-xxx | Data Rights / Privacy | 身份核验失败、Legal Hold、部分删除失败 |
| RATE-xxx | Quota / Capacity | 速率、额度、并发或成本限制 |
| SYSTEM-xxx | Platform / Dependency | 临时不可用、依赖失败、未知内部错误 |

### 12.3 Error Code Stability

- 同一 API Major Version 内不得改变已有码的含义、Owner 或 retryable 语义。
- 可以新增错误码；客户端必须安全处理未知同前缀错误。
- 弃用错误码需保留文档和替代码，不得立即复用其编号。
- 同一业务错误在不同 Endpoint 应保持相同稳定码和 HTTP Status 原则。
- 内部供应商错误映射为平台错误，不透传供应商堆栈或原始响应。

### 12.4 Validation Errors

输入问题只返回客户端可修复且有权查看的路径、原因和安全提示。不回显完整出生资料、自由文本或 Credential。多个独立输入问题可以聚合返回；一旦涉及授权或资源发现风险，优先返回安全的统一错误。

### 12.5 Retry Classification

| Category | Retry Rule |
|---|---|
| Validation / Authorization / Consent | 不自动重试；先修正输入或权限 |
| Conflict / Precondition | 重新读取资源后由调用方形成新决定 |
| Rate Limit | 遵守 Retry-After，并使用原 Idempotency-Key |
| Timeout / Dependency | 先查询 Operation；确认可重试后有限退避 |
| Non-Retryable Domain Failure | 不自动重试；新业务意图需要新 Key |
| Partial Saga Failure | 查询分步骤状态并等待或进入人工处理 |

---

## 13. Pagination Strategy

### 13.1 Default Strategy

集合 API 默认采用不透明 Cursor Pagination。Cursor 只表达服务端分页位置和排序上下文，不承载可解读业务信息，也不作为长期 Resource Identity。

### 13.2 Pagination Contract

| Element | Rule |
|---|---|
| pageSize | 有安全默认值和按资源定义的最大值；超出则拒绝或按明确规则限制 |
| cursor | 不透明、有完整性保护、绑定过滤/排序/授权上下文 |
| next | 仅在有下一页且调用方仍有权访问时提供 |
| previous | 非所有资源保证；若支持必须保持同一快照语义 |
| totalCount | 默认不保证，避免高成本和隐私推断；需要时单独治理 |
| stableOrder | 每个集合必须有确定排序及唯一 Tie-Breaker |
| snapshotTime | 对需要一致翻页的集合标明读取截止时间或一致性 Token |

### 13.3 Pagination Consistency

- 翻页期间新增或删除数据不得造成无限循环或同一资源无解释重复。
- 权限或 Consent 变化后，旧 Cursor 可以失效；安全优先于继续翻页。
- Cursor 过期返回稳定错误，不自动从第一页面静默重启。
- Audit、Usage 和 Timeline 等大集合必须设置时间或范围上限。

### 13.4 Offset Pagination

Offset 只可用于规模小、稳定且无隐私枚举风险的内部集合。对用户资源、审计、消息和事件等可增长集合，不作为默认策略。任何公共 API 改用 Offset 必须通过 API Review；若改变全局策略则需 ADR。

---

## 14. Filtering & Sorting

### 14.1 Filtering

- 过滤字段采用每个 Resource 的显式白名单。
- 不允许客户端传递任意表达式、数据库字段名或执行脚本。
- 时间区间必须有最大跨度；Timeline、Audit、Usage 和 Messages 必须限制范围。
- 过滤不能扩大授权结果；服务端先应用安全边界，再应用业务筛选。
- 敏感字段默认不可作为模糊搜索条件，避免枚举和侧信道。
- 过滤值的语言、时区和规范化规则必须明确。

### 14.2 Sorting

- 每个集合定义默认稳定排序。
- 允许排序字段使用白名单，并声明升序/降序语义。
- 所有排序增加稳定唯一 Tie-Breaker，但不把 ID 的生成顺序解释为业务时间。
- 不允许按高敏感或推断性字段排序。
- 更改默认排序可能改变分页结果，属于兼容性评审项。

### 14.3 Search

搜索是 Query，不触发索引修复或知识发布。搜索结果需标明 Projection 延迟语义。Knowledge 和 Evidence 搜索遵守来源权利、语言、Purpose 和字段遮蔽；不得通过搜索接口获取受限正文。

---

## 15. Versioning Strategy

### 15.1 Version Dimensions

| Version Type | 用途 | 不得混淆为 |
|---|---|---|
| API Major Version | 外部协议与资源契约兼容边界 | Product Version 或 Domain Version |
| API Contract Revision | 同 Major 内的兼容性文档演进 | Resource Identity |
| Product Version | MVP、V1、V2 发布范围 | API Major Version |
| Resource Version | 可变资源并发与内容演进 | Resource Identity |
| Snapshot Sequence | Chart 内 Snapshot 顺序 | SnapshotId |
| Algorithm/Rule/Knowledge/Prompt/Model Version | 正式结果的上游可复现条件 | API Version |
| Report Version / Ordinal | 报告演进和替代关系 | ReportId |
| Event Contract Version | Integration Event 契约 | Domain Event 事实身份 |

### 15.2 Major Version Location

API Major Version 使用 URI 顶层路径表达。客户端必须选择明确 Major；平台不依据“最新版本”隐式路由正式请求。具体初始 Major 编号在发布审批时确认，文中 `/v1` 仅为命名规则示意。

### 15.3 Compatible Changes

同一 Major 内通常允许：

- 增加可选、可忽略的表示信息；
- 增加新的 Resource 或 Endpoint，且不改变既有语义；
- 增加新的错误码或枚举值，但客户端契约已声明开放集合；
- 增加新的过滤或排序能力；
- 放宽非安全性输入限制且不破坏结果解释；
- 修正文档但不改变运行语义。

所有兼容变更仍需 Contract Review、测试和 Change Log。

### 15.4 Breaking Changes

以下通常属于 Breaking Change：

- 删除或重命名 Resource、URI、Header 或已承诺概念；
- 改变 Identity、Version、状态、错误码或授权含义；
- 把同步成功改为调用方无法处理的异步契约，或反之；
- 新增必需输入、缩小既有允许范围或改变默认排序；
- 改变分页 Cursor、幂等、重试或一致性保证；
- 从遮蔽改为暴露敏感信息，或改变 Purpose/Consent 边界；
- 改变 Event Contract 中已承诺事实语义；
- 将 Read Model 当作新的 Source of Truth。

Breaking Change 必须通过 ADR，通常需要新 API Major Version 和迁移期。

### 15.5 Version Selection for Business Results

客户端可以在获准范围内请求已发布且兼容的业务版本；不能指定 Draft、Rejected、Retired 或无权使用的版本。服务端不得在任务运行中静默切换 Algorithm、Rule、Knowledge、Prompt 或 Model Version。

---

## 16. Long Running Operations

### 16.1 Applicable Operations

下列用例默认按长任务评估：AIAnalysis、较长 AI Message、复杂 RuleRun、多流派分析、Analytical Timeline、Report/PDF、数据导出、数据删除、影响分析、索引构建及通知。确定性 Calculation 可在性能门禁内同步，否则使用 Operation。

### 16.2 Operation Resource Semantics

Operation 是应用流程状态投影，不是 Domain Aggregate。它至少表达以下概念，但本文不定义传输 Schema：

- OperationId；
- Operation Type；
- Target Resource Reference；
- Status；
- Progress Stage（非伪精确百分比）；
- Submitted/Started/Updated/Completed Time；
- CorrelationId；
- Result Reference；
- Safe Error；
- Retry/Cancel Capability；
- Projection Freshness。

### 16.3 Operation States

| State | 语义 |
|---|---|
| Accepted | 已可靠接收，尚未开始正式处理 |
| Running | 正在执行一个或多个受治理步骤 |
| Waiting | 等待依赖、人工决定或重试窗口 |
| Completed | 目标结果已正式完成并可引用 |
| Rejected | 安全、Consent、风险或领域规则拒绝 |
| Failed | 已达到失败终态 |
| CancelRequested | 已接受取消意图，但尚未保证停止 |
| Cancelled | 在允许边界内停止，未宣称撤销已发生事实 |
| PartiallyCompleted | 仅用于数据权利等批准流程，并明确未完成步骤 |

Operation 状态不得替代 Chart、RuleRun、EvidenceBundle、AIAnalysis、Timeline 或 Report 的领域生命周期。

### 16.4 Polling

- `202 Accepted` 提供 Operation 的规范查询位置。
- 客户端遵守 Retry-After 或服务端建议的轮询间隔，使用退避与抖动。
- Polling GET 安全且幂等，不触发重试或推进流程。
- Operation 完成后提供目标资源引用；不把完整敏感结果强制内嵌在状态表示中。
- Operation 保留期和完成后访问期限待运行、隐私与产品确认。

### 16.5 Cancellation

取消是显式 Command，只在应用用例声明支持时开放。取消不能删除已发布事件、已产生审计或回滚 Immutable/Frozen 对象。无法取消时返回明确 Conflict，而不是伪报成功。

---

## 17. Async APIs

### 17.1 Async Acceptance

异步受理必须在返回 `202` 前可靠记录业务意图、Idempotency-Key、Actor/Subject、Purpose、输入版本引用和 CorrelationId。仅将任务放入易失内存不构成可靠受理。

### 17.2 Completion Channels

| Channel | 适用场景 | 安全要求 |
|---|---|---|
| Polling | 所有异步 Operation 的基础能力 | 每次查询重新授权；遵守限流 |
| Callback | 第一方或特别批准集成 | 目标白名单、认证、签名/完整性、重放保护、最小内容 |
| Webhook | V2 DeveloperClient 订阅批准事件 | Subscription Scope、凭据轮换、EventId、重试与死信治理 |
| First-Party Notification | 用户可见完成提醒 | 不在通知正文暴露敏感结果 |

### 17.3 Callback Concept

Callback 仅作为概念能力，不在本文定义协议或内容结构。客户端不能在单次任意请求中提交不受控回调地址；回调目标须预登记、验证、限制网络目标，并防止 SSRF、重放和敏感数据外泄。Callback 失败不改变源业务结果。

### 17.4 Delivery Semantics

- 采用至少一次投递与消费者幂等，不承诺恰好一次。
- 重试使用有限指数退避和上限；永久失败进入可观察的 Dead Letter/Manual Review 流程。
- 乱序事件按 Resource Identity、Event Version 和前置状态处理。
- 接收确认只表示传递成功，不表示接收方业务处理成功，除非独立契约明确。

---

## 18. Event Driven API Boundary

### 18.1 Boundary Principle

外部 Event API 只发布批准的 Integration Event，不直接暴露内部 Domain Event、Aggregate 内部 Entity、数据库变化日志或第三方模型原始输出。

### 18.2 Event Eligibility

一个事件可进入外部契约前必须满足：

1. 具有明确业务订阅价值；
2. 不泄露受限敏感正文；
3. 具有稳定 Event Type、EventId、Occurrence Time、Subject/Resource Reference 和 Contract Version；
4. 定义授权 Scope、租户边界和 Purpose；
5. 定义重复、乱序、重试、撤回和弃用语义；
6. 通过安全、隐私、法律和 API Contract Review。

### 18.3 Candidate Event Families

| Family | 允许的外部语义 | 禁止内容 |
|---|---|---|
| Calculation Status | 已受理、完成、失败和结果资源引用 | 原始出生资料、内部校验细节 |
| Analysis Status | 处理中、完成、拒绝、失败 | 模型原始输出、Prompt、跨主体 Evidence |
| Report Status | 生成、冻结、归档状态和 Report 引用 | 报告敏感正文默认推送 |
| Data Rights Status | 导出/删除步骤的安全状态 | 其他 Context 的内部对象清单 |
| Subscription Status | 凭据轮换、暂停、投递失败 | Secret 原值 |

该表只定义候选事件家族，不新增或重定义正式 Domain Event。具体 Integration Event Contract 必须单独评审。

### 18.4 Event Contract Versioning

Event Contract Version 与 API Version 分离。兼容性扩展不得改变既有字段语义；Breaking Change 需要新 Contract Version、订阅者迁移和 Sunset 计划。事件生产者不得在同一版本中静默改变时间、Identity、状态或重试含义。

### 18.5 Webhook Security

- Subscription 与事件类型、资源范围和 Tenant/Client 绑定。
- 目标地址预验证，只允许安全传输，并限制重定向与私有网络访问。
- Delivery 使用可轮换凭据或签名完整性机制，具体方案待技术与安全设计。
- EventId、DeliveryId、Timestamp 和重放窗口相互区分。
- Webhook 日志不记录 Secret 或敏感 Payload 全文。

---

## 19. Rate Limiting

### 19.1 Limit Dimensions

限流可以按 IP 风险、匿名会话、User、Client、Tenant、Credential、Endpoint、Resource、并发 Operation、AI Token/成本和时间窗口组合执行。任何策略都不能因共享出口误伤而成为唯一身份判断。

### 19.2 Rate Limit Classes

| Class | 示例 | 原则 |
|---|---|---|
| Authentication | 登录、恢复、凭据验证 | 严格防暴力尝试，不泄露账户存在性 |
| Low-Cost Query | 普通 Chart/Report 查询 | 允许合理交互，防枚举和批量抓取 |
| Deterministic Compute | Calculation、Timeline Basic | 受并发和资源预算控制 |
| AI/High-Cost | AIAnalysis、Messages、复杂 Report | 同时受额度、成本、并发和风险控制 |
| Governance | 发布、敏感访问、导出、删除 | 低频、强审计，不以提高配额绕过审批 |
| Webhook Delivery | 对单订阅目标投递 | 防目标故障拖垮平台，有限重试 |

### 19.3 Rate Limit Contract

- 超限使用 `429` 和 `RATE-xxx`。
- 可重试时返回 `Retry-After`；不可仅靠错误文本说明。
- 可以提供 RateLimit-Limit、RateLimit-Remaining 和 RateLimit-Reset 等标准化语义，但不得泄露安全检测阈值。
- 额度耗尽与短时速率超限使用不同稳定错误语义。
- Client 提升配额需独立授权、成本与风险评审。

### 19.4 Abuse Protection

平台可以对异常枚举、Credential Sharing、自动化抓取、Prompt 攻击和高风险主题滥用采取更严格限制。安全限制不得被客户端参数关闭；相关拒绝和管理员调整必须审计。

---

## 20. API Lifecycle

### 20.1 Lifecycle States

| State | 可见性 | 契约保证 | 使用限制 |
|---|---|---|---|
| Proposed | 架构/产品内部 | 无外部保证 | 仅评审，不实现承诺 |
| Experimental | 受邀测试 | 可变化，必须显著标识 | 不承载不可替代生产流程 |
| Beta | 批准客户 | 兼容性目标明确；范围冻结 | 监控、配额和支持受控 |
| Stable | 正式支持 | 遵守版本与弃用政策 | 适用正式 SLO 与支持政策 |
| Deprecated | 仍可用但不建议新接入 | 维持已声明兼容期 | 返回弃用信息和迁移路径 |
| Sunset | 停止新使用或已关闭 | 仅保留必要文档/迁移支持 | 按批准日期结束服务 |
| Retired | 不再提供 | 不可调用 | 历史审计和契约记录保留 |

### 20.2 Promotion Gates

进入 Stable 前至少完成：契约评审、安全与隐私评审、授权矩阵测试、幂等与重试测试、兼容性测试、错误码登记、容量评估、审计验证、文档与支持准备，以及适用地区法律确认。

### 20.3 Product Release Alignment

API Lifecycle 不自动等同 Alpha/Beta/RC/GA。Roadmap 的 Beta Scope Freeze、RC Scope Freeze 和 GA 前禁止新增需求继续适用。Developer API 仍是 V2 范围，不能因本文完成而提前进入 MVP/V1。

---

## 21. Deprecation Policy

### 21.1 Deprecation Requirements

弃用必须包含：

- 受影响的 Resource、Endpoint、Method、Header、错误码或事件契约；
- 弃用原因和兼容替代方案；
- 公告时间、迁移窗口和 Sunset 日期；
- 调用方影响与可观察使用数据；
- 安全、隐私和历史可复现影响；
- 回滚与延长条件；
- 责任人和支持渠道。

### 21.2 Communication

已批准弃用通过文档、Change Log、开发者通知和适用的 Deprecation/Sunset Header 表达。敏感安全问题可缩短期限，但必须经过紧急治理、记录理由并提供安全迁移路径。

### 21.3 Historical Access

API 停止新请求不等于删除历史数据或改写旧报告。历史 Frozen Report、Snapshot 和 Audit 的保留与访问继续遵守 Data Model、Legal Hold、Retention 和授权规则。

### 21.4 Error Code Deprecation

弃用错误码不得复用编号或改变旧语义。替代码进入注册表，客户端迁移期内平台按已发布契约保持兼容。

---

## 22. Compatibility Rules

### 22.1 Consumer Rules

客户端必须：

- 忽略契约允许的未知可选信息；
- 不依赖对象成员顺序、集合默认隐含顺序或 ID 可排序性；
- 按稳定 Error Code 而不是本地化消息分支；
- 对开放枚举安全处理未知值；
- 使用 Operation 和 Resource Link，不自行拼接未承诺 URI；
- 遵守 Retry-After、Idempotency-Key 和 Cursor 语义；
- 不把 Projection 延迟视为领域失败。

### 22.2 Provider Rules

平台必须：

- 不在同一 Major 中删除或改变已承诺语义；
- 不把可选信息改为必需输入；
- 不静默改变授权、遮蔽、排序、分页、时区或版本选择；
- 不改变 Frozen/Immutable 资源表示的事实含义；
- 不把内部供应商变化暴露为外部 Breaking Change；
- 对兼容性修复保留 Contract Test 和变更记录。

### 22.3 Compatibility Test Matrix

| Test Area | 必须验证 |
|---|---|
| Old Client / New Provider | 旧客户端面对新增可选信息和枚举值安全运行 |
| Error Contract | 已有码语义、HTTP Status 和 retryable 不漂移 |
| Pagination | Cursor、排序和过滤组合保持稳定 |
| Idempotency | 重试跨版本部署不创建重复正式对象 |
| Authorization | 新 Scope/Role 不扩大旧 Client 权限 |
| Async | Operation 状态和 Result Link 向后兼容 |
| Events | 旧订阅者可处理兼容事件扩展 |
| Localization | 消息变化不影响机器判断 |
| Immutable History | 新 API 版本仍不改写旧 Snapshot/Report |

---

## 23. API Governance

### 23.1 Architecture Baseline

01–07 Approved 文档与本文件未来 Approved 版本共同构成 Architecture Baseline。API 设计不得修改 Domain、Data、Context 或 Application 边界。

### 23.2 Contract Ownership

| Governance Role | 责任 |
|---|---|
| API Product Owner | 确认调用者、价值、版本范围和生命周期 |
| API Architect | 维护资源、URI、方法、兼容性和 ADR 一致性 |
| Context Owner | 确认 Command/Query 只使用其批准能力 |
| Security Owner | 评审认证、授权、凭据、限流和攻击面 |
| Privacy/Legal Owner | 评审目的、最小化、跨境、保留、导出和删除 |
| Data/Domain Owner | 防止 Identity、Version、Immutable 和 Aggregate 泄漏 |
| Operations Owner | 评审 SLO、限流、异步、重试和可观察性 |
| QA/Contract Owner | 维护兼容性、安全与契约测试基线 |

### 23.3 API Review Gate

任何新 Endpoint 或重大修改至少检查：Use Case 来源、Resource Owner、授权矩阵、数据分类、幂等、事务/一致性、错误、版本、分页/限流、审计、异步、兼容性、弃用和测试。缺少 Owner 或基线来源不得进入 Stable。

### 23.4 Contract Registry

治理注册表至少维护：

- API Surface、Resource 与 Owner；
- Major Version 与 Contract Revision；
- Endpoint Lifecycle；
- Scope、Role、Purpose 和数据分类；
- Error Code Registry；
- Event Contract Registry；
- Idempotency 要求；
- Rate Limit Class；
- Deprecation/Sunset 计划；
- ADR 和评审记录。

### 23.5 Change Process

1. 提出用例和调用者问题；
2. 确认上游基线允许；
3. 分类为兼容变更、Breaking Change 或 ADR Candidate；
4. 完成领域、应用、安全、隐私、运行与测试评审；
5. 更新契约注册表和 Change Log；
6. 通过发布门禁后开放；
7. 监控使用、错误、成本和滥用；
8. 按生命周期治理弃用。

### 23.6 Audit Requirements

以下 API 行为必须审计：认证安全事件、权限/Scope 变化、敏感资源访问、数据导出与删除、Consent 变化、治理发布与停用、Credential 创建/轮换/撤销、Webhook Subscription 变化、配额调整、管理员遮蔽解除、重大错误人工处置。

审计记录包含主体、Client、Purpose、动作、目标资源引用、结果、时间、RequestId、CorrelationId 和批准理由；不复制不必要敏感正文。

### 23.7 ADR Gate

ADR 未批准时，API 只能保持现有基线、缩小开放范围或登记 Open Question，不得以兼容层、临时 Endpoint 或实验 Header 绕过架构决策。

---

## 24. ADR Reference Matrix

| Topic | ADR Required | Trigger Example |
|---|---|---|
| Resource Model | Yes | 将内部 Entity 提升为独立公共 Resource |
| URI Strategy | Yes | 从路径版本切换为 Header 版本或更改根路径 |
| API Versioning | Yes | 改变 Major Version 规则或版本选择方式 |
| Authentication | Yes | 改变用户、Client 或工作负载认证信任模型 |
| Authorization | Yes | 改变 Scope、Ownership、Purpose、Consent 或 Tenant 边界 |
| Error Contract | Yes | 更换 Problem Details 语义或改变错误码稳定规则 |
| Command Model | Yes | 新增未在 Application Architecture 批准的外部意图 |
| Query Model | Yes | Query 获得写入、副作用或新的 Source of Truth |
| Event Contract | Yes | 对外开放新事件事实类型或改变已发布事实含义 |
| Compatibility Policy | Yes | 改变 Breaking Change 判定或迁移义务 |
| Pagination Strategy | Yes | 公共集合从 Cursor 改为 Offset 或改变一致性保证 |
| Idempotency Strategy | Yes | 改变 Key 范围、重复结果或保留语义 |
| Transaction Boundary | Yes | 一个 API 请求计划跨 Context 原子修改 |
| Async Operation Model | Yes | 改变 Operation 身份、终态或轮询基本契约 |
| Security Model | Yes | 改变信任边界、Credential 处理或敏感 Header 策略 |
| Privacy Model | Yes | 扩大数据用途、默认暴露或第三方传输范围 |
| Audit Model | Yes | 减少关键审计范围或改变防篡改责任 |
| Rate Limit Model | Yes | 改变全局维度并影响商业或安全边界 |

任何涉及以上内容的修改，都不得直接修改本文档。必须先提交 ADR，完成替代方案、影响、兼容性、安全、隐私和迁移评估；ADR 批准后，才可更新对应 Architecture Baseline。未批准 ADR 不构成 API 变更授权。

---

## 25. API Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐方式 |
|---|---|---|---|
| RPC Style REST | URI 以大量动作动词模拟远程方法，资源和 HTTP 语义失去一致性 | Endpoint 爆炸、重试和缓存语义混乱、难以治理 | 用名词资源、Operation Resource 和标准 Method 表达已批准用例 |
| Resource Leakage | 直接暴露 Aggregate 内部 Entity、数据库字段或供应商对象 | Context 边界破坏、敏感数据泄漏、内部重构成为 Breaking Change | 建立稳定 API Resource/Projection，只暴露用途所需信息 |
| Overloaded Endpoint | 一个 Endpoint 根据参数执行多个无关 Command 或 Query | 授权、幂等、错误和审计无法清晰定义 | 每个 Endpoint 对齐一个明确资源意图和 Owner |
| Breaking Compatibility | 在同一 Major 中删除字段、改变状态或错误语义 | 客户端静默故障、历史调用不可复现 | 兼容扩展优先；Breaking Change 走 ADR、新 Major 和迁移期 |
| Missing Idempotency | 创建任务、报告或删除请求没有业务重复保护 | 重复对象、重复成本、重复删除或流程污染 | 必需 Command 使用 Idempotency-Key、意图指纹和结果复用 |
| Business Logic in Controller | Interface 层直接判断命理、状态转换或领域不变量 | 规则重复、绕过 Aggregate、测试和版本失控 | Controller 只完成协议适配，调用批准的 Application Command/Query |
| Leaking Internal Aggregate | 把 Aggregate 结构一比一作为公共契约 | 外部客户端绑定内部边界，后续领域演进受阻 | 以用例稳定性设计 Resource，保护 Aggregate Root 和内部 Entity |
| Direct Database API | 允许客户端按表、列或任意查询表达式访问数据 | 越权、注入、数据所有权和版本规则失效 | 所有访问通过授权 Resource、Command 与 Query Contract |
| Chatty API | 完成一个普通用例需要大量顺序往返和内部关系遍历 | 高时延、部分失败、客户端承担编排 | 提供用例对齐的聚合读视图或 Async Operation，不扩大写事务 |
| God Endpoint | 单个万能 Endpoint 处理所有资源和动作 | 责任、限流、监控、兼容和权限边界崩溃 | 按 Resource、Context 和用例拆分稳定契约 |
| Query With Side Effects | GET 或列表读取隐式触发计算、修复或状态推进 | 缓存/重试产生重复写入，用户无法预期 | Query 严格只读；变化使用显式 Command |
| Read Model as Source of Truth | 用最终一致 Projection 决定领域写入或宣称正式完成 | 过期状态破坏不变量和终态 | 写入由所属 Aggregate 校验；Read Model 仅展示并标注新鲜度 |
| Client-Controlled State Transition | 客户端直接设置 Completed、Frozen、Published 等状态 | 绕过验证、审核和不可变规则 | 客户端表达意图，领域与应用流程决定合法结果状态 |
| Cross-Context Atomic Endpoint | 一个请求承诺同时修改多个 Context 或全部回滚 | Context 自治失效、故障和锁范围扩大 | 每 Context 独立事务，使用 Operation/Saga 与最终一致性 |
| Sensitive Data in URI | 把出生时间、地点、问题或 Credential 放入路径/查询 | 日志、历史、缓存和中间设施泄漏 | URI 只含不透明 ID 和非敏感控制信息，敏感内容最小化传输 |
| Error Detail Leakage | 错误返回堆栈、SQL、模型原文、密钥或真实拒绝细节 | 攻击面扩大、隐私和供应商信息泄漏 | 使用安全 Problem Details、稳定码和内部关联 ID |
| Unbounded Collection | 无分页、范围或最大结果限制 | 容量失控、批量枚举、成本和隐私风险 | Cursor Pagination、范围上限、白名单过滤和 Rate Limit |
| Version in Identity | 把版本号、时间或顺序编码为 Resource Identity 语义 | Identity 与 Version 混淆、迁移困难 | 使用不透明稳定 Identity，版本使用独立属性和契约 |
| Callback to Arbitrary URL | 每次请求接受任意回调目标 | SSRF、数据外泄、重放和供应链风险 | 预登记验证目标，使用最小事件、完整性和重放保护 |
| Hidden Retry | 平台或客户端无限重试且不展示 Operation | 成本叠加、重复副作用、故障风暴 | 有限退避、Idempotency-Key、Retry-After、终态和人工处理 |

---

## 26. Review Checklist

### 26.1 Resource and Semantics

- [ ] 每个 Endpoint 是否来源于批准的 Use Case、Command 或 Query。
- [ ] Resource 是否使用稳定业务语义，而非表、类或供应商模型。
- [ ] 是否避免暴露 Aggregate 内部 Entity。
- [ ] URI 是否使用小写复数名词、不透明 Identity 和明确 Major Version。
- [ ] HTTP Method 与 Status Code 是否符合统一语义。
- [ ] Query 是否无业务副作用。
- [ ] Frozen、Valid、Completed、Published 对象是否保持不可变。

### 26.2 Security and Privacy

- [ ] 是否在服务端验证 Actor、Subject、Tenant、Role、Scope、Ownership、Purpose 和 Consent。
- [ ] 是否遵循默认拒绝与最小权限。
- [ ] 凭据和敏感信息是否不会进入 URI、日志或错误。
- [ ] 是否实施资源枚举保护和字段遮蔽。
- [ ] 管理员敏感访问是否有工单、理由、期限和审计。
- [ ] Callback/Webhook 是否防 SSRF、重放和敏感数据泄漏。
- [ ] 是否完成目标地区法律、隐私和安全评审。

### 26.3 Reliability and Operations

- [ ] 必需 Command 是否定义 Idempotency-Key 和意图冲突语义。
- [ ] 长任务是否返回 202 和独立 Operation。
- [ ] Polling 是否只读并遵守 Retry-After。
- [ ] Timeout 是否不会被错误解释为业务未执行。
- [ ] Event/Webhook 是否采用至少一次投递与消费者幂等。
- [ ] Rate Limit 是否区分短时限流、额度和并发。
- [ ] RequestId、CorrelationId 与 TraceId 是否分离并可追踪。
- [ ] 审计是否最小充分且不复制敏感正文。

### 26.4 Compatibility and Governance

- [ ] API Version 是否与 Product/Domain/Resource/Event Version 分离。
- [ ] 变更是否分类为兼容、Breaking 或 ADR Candidate。
- [ ] 错误码是否登记且语义稳定。
- [ ] 分页、过滤、排序是否有白名单和稳定顺序。
- [ ] 是否完成旧客户端兼容性测试。
- [ ] 是否定义 Lifecycle、Deprecation、Sunset 和迁移责任。
- [ ] ADR Reference Matrix 涉及项是否已先获批准。
- [ ] Beta/RC/GA Scope Freeze 是否继续生效。
- [ ] Developer API 是否仍保持 V2 范围，未提前进入 MVP/V1。

### 26.5 Document Boundary

- [ ] 本文件是否没有 OpenAPI、Swagger、Schema、DTO、Controller 或 SDK。
- [ ] 是否没有代码、SQL、ORM、Repository 实现或部署配置。
- [ ] 是否没有重定义 Aggregate、Entity、Value Object 或 Domain Event。
- [ ] 是否没有修改任何上游 Approved 文档。
- [ ] 是否没有授权进入实现阶段。

---

## 27. Open Questions

### 27.1 Product

1. V2 Developer API 的首批正式 Resource 是否全部按 SRS 开放，或分批开放 Charts、Calculations、Reports 后再开放 AI 相关资源。
2. ProfessionalUser 与 DeveloperClient 的证据、参数和版本可见深度。
3. API 套餐、额度、并发和成本展示规则；MVP 不接真实支付的基线保持不变。
4. AI 不可用时是否允许 Developer API 请求规则型无 AI 报告。
5. Operation 对普通用户和开发者展示到何种阶段粒度。

### 27.2 API Contract

1. 初始 API Major 编号、主域名和 Surface 隔离方式。
2. 每个集合的默认/最大 pageSize、Cursor 有效期和 totalCount 支持范围。
3. 哪些可变资源强制 If-Match，哪些只使用业务幂等与状态校验。
4. Calculation 在何种性能门槛下同步返回，何时统一转为 202。
5. Operation、Idempotency 结果和 Webhook Delivery 的保留期限。
6. 对外 Error Code 的具体编号、文档地址和本地化策略。
7. 外部 Event Family 的首批正式事件、Contract Version 与 Payload 最小范围。

### 27.3 Security

1. 用户会话、DeveloperClient、工作负载身份的具体认证协议。
2. 高权限账户 MFA、敏感操作再认证和临时提权时限。
3. API Credential 轮换重叠期、撤销传播 SLO 和 Scope 粒度。
4. Webhook 完整性、重放窗口、目标验证和 Secret 轮换方案。
5. 全局与高成本 Endpoint 的 Rate Limit 阈值及安全阈值保密策略。

### 27.4 Privacy and Legal

1. Birth Profiles、Consents、数据导出/删除 API 是否允许第三方 DeveloperClient 调用。
2. 中国大陆目标地区对自动生成内容标识、个人信息出境、日志和审计保留的最终要求。
3. 分享链接、Webhook 和 Callback 可传递的最小信息边界。
4. 数据导出格式、完成时限、身份复核和 Legal Hold 告知方式。
5. 健康、婚姻、投资等高风险主题的最终 API 内容与拒绝边界。

### 27.5 Domain and Application

1. `DataRightsRequest` 当前继续只作为应用流程身份；若要成为正式 Aggregate Root，必须先通过 ADR 并更新 Domain/Data 基线。
2. 多候选出生时间是否需要新的外部分析流程；不得借 API 改变 Chart Aggregate Boundary。
3. RuleRun 和 EvidenceBundle 是否对 DeveloperClient 独立开放，或仅通过 Analyses/Evidence 投影访问。
4. Consent 撤回后在途 AIAnalysis、Report 和 Webhook Delivery 的精确停止/降级语义。
5. Report 再生成对外暴露为独立意图资源还是只创建新 Report 的最终 URI 形式。

### 27.6 Operations

1. API、Calculation、AI、Report 和 Webhook 的 SLO、P95/P99 与并发目标。
2. Retry-After 的最小/最大窗口和客户端退避建议。
3. Operation Projection 延迟阈值、告警和人工处理 SLA。
4. Deprecated API 的最短迁移期和紧急安全 Sunset 例外流程。

### 27.7 ADR Candidates

- ADR-CANDIDATE-API-001：用户、DeveloperClient 与工作负载身份的认证协议及信任边界。
- ADR-CANDIDATE-API-002：初始 URI Major Version、Surface 隔离与长期版本策略。
- ADR-CANDIDATE-API-003：外部 Integration Event/Webhook Contract 与兼容性模型。
- ADR-CANDIDATE-API-004：公共集合的 Cursor、快照一致性和 totalCount 策略。
- ADR-CANDIDATE-API-005：`DataRightsRequest` 是否升级为领域 Aggregate；批准前仅表达 Operation/应用流程身份。

---

## 28. Risks

| Risk | 表现 | 影响 | 缓解与门禁 |
|---|---|---|---|
| Domain Leakage | API 一比一暴露 Aggregate/Internal Entity | Context 无法演进、越权和兼容风险 | Resource Review、Context Owner 审核、ADR Gate |
| Developer API 提前扩围 | V2 能力进入 MVP/V1 | 普通用户体验和合规准备被挤压 | Roadmap Scope Freeze、产品门禁 |
| 认证选型过早固化 | 未完成安全评审即承诺协议 | 迁移和安全债务 | 保持能力规范；选型走 ADR/安全评审 |
| 授权只在网关 | 下游服务信任前端或 Gateway | IDOR、跨租户访问 | 目标 Application Service 重验 Ownership/Scope/Purpose |
| 敏感数据泄漏 | URI、日志、Error、Webhook 含出生或会话正文 | 隐私事件和法律风险 | 最小化、遮蔽、扫描、Subscription Scope |
| 幂等失效 | 超时重试创建多个 Analysis/Report | 成本、版本链和用户体验受损 | Idempotency-Key、意图指纹、原 Operation 查询 |
| 异步伪完成 | 202 被解释为业务完成 | 客户端展示错误状态 | Operation 状态与领域终态分离 |
| Event Contract 漂移 | 事件字段/语义静默改变 | 下游处理错误和数据污染 | Contract Version、兼容测试、Event Registry |
| Cursor 不稳定 | 翻页重复、遗漏或越权 | 数据质量与隐私风险 | 稳定排序、授权绑定、快照语义 |
| Error Contract 泄漏 | 透传堆栈、模型原始错误 | 攻击与供应商信息泄漏 | Problem Details、平台码映射、安全测试 |
| Rate Limit 误伤 | 仅按 IP 或统一阈值 | 共享网络用户无法使用 | 多维限流、可观察性、人工申诉 |
| Callback SSRF | 任意 URL 或重定向 | 内网探测与数据外传 | 预登记、目标验证、网络限制、最小事件 |
| Breaking Change | 同 Major 改状态、默认排序或授权 | Client 静默故障 | ADR、新 Major、Deprecation/Sunset |
| Read Model 误用 | Progress 被当作正式事实 | 状态倒退或错误决策 | Freshness、源资源链接、禁止写回 |
| 审计不足 | 无法解释敏感访问或删除 | 调查和合规失败 | 关键 API Audit Gate、Correlation 链 |
| 审计过度 | 复制敏感 Request/Response | 二次数据暴露 | 最小元数据、字段禁记清单 |
| 命理表述失控 | API 文本暗示科学准确或确定预测 | 产品信任和合规风险 | 证据状态、风险提示、内容边界测试 |
| 成本失控 | AI、报告和轮询无预算 | 商业不可持续、服务拥塞 | Quota、Rate Limit、Operation 退避、Usage 投影 |

---

## 29. 进入下一阶段《09-TECHNOLOGY-ARCHITECTURE.md》所需输入条件

- [ ] `08-API-DESIGN.md` 已完成评审并成为 Approved 1.0 Architecture Baseline。
- [ ] First-Party、Developer 和 Governance API Surface 边界已确认。
- [ ] V2 首批公共 Resource、开放顺序和明确不开放范围已确认。
- [ ] URI、HTTP Method、Status Code、Problem Details 和 Error Registry 规则已确认。
- [ ] Authentication 协议候选、Authorization Context、Scope、Ownership、Purpose、Consent 和 Tenant 责任已完成安全评审。
- [ ] Idempotency-Key 范围、记录保留和冲突语义已确认。
- [ ] Cursor Pagination、过滤、排序和集合上限已确认。
- [ ] API Major Version、Breaking Change、Compatibility、Deprecation 和 Sunset 政策已确认。
- [ ] Operation、Polling、Callback、Webhook 和 Event Contract 的边界已确认。
- [ ] Rate Limit、Quota、并发、Retry-After 和容量目标已确认或有明确责任人与决策点。
- [ ] Sensitive Data Masking、日志禁记清单、Audit Requirement 和数据权利边界已完成隐私/法律评审。
- [ ] ADR Reference Matrix 中涉及的未决事项已批准，或在技术架构中继续保持候选且不改变基线。
- [ ] Remaining Open Questions 中会影响技术选型、信任边界或部署拓扑的问题已有 Owner 和最迟决策点。
- [ ] Beta、RC、GA Scope Freeze 继续生效。
- [ ] 下一阶段只定义 Technology Architecture，不生成代码、OpenAPI、数据库实现、部署配置或业务逻辑。

只有本 API 设计通过评审后，才可以生成 `09-TECHNOLOGY-ARCHITECTURE.md`。本次不得生成该文件，也不得进入代码实现阶段。

