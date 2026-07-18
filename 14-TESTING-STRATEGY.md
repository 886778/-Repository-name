# AI 八字命理分析平台：测试策略

**文档编号：** 14  
**文档类型：** Testing Strategy  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md` 至 `13-AI-ARCHITECTURE.md`（均已 Approved 1.0）  
**目标读者：** CTO、测试架构师、研发与质量负责人、产品负责人、命理领域专家、AI/知识负责人、安全与隐私负责人、平台与运维人员、发布经理

---

## Version 0.9 Change Log

- 首次定义平台整体测试体系、质量目标、测试金字塔和分层职责。
- 定义 Unit、Domain、Aggregate、Value Object、Application、Integration、Contract、API 与 E2E 测试策略。
- 定义 AI、Prompt Regression、RAG、Output Validation、事实与引用一致性测试策略。
- 定义安全、隐私、性能、负载、压力、可靠性、恢复和可规划 Chaos Testing。
- 定义 Test Data、Mock、Isolation、Environment、Automation、Coverage、Defect 和 Release Quality Gate。
- 定义 Testing Governance、ADR Reference Matrix、Anti-Patterns、评审清单、待确认事项和风险。
- 本文件不包含任何测试代码、测试脚本、配置、流水线或可执行实现。

---

## 1. Document Purpose

### 1.1 目标

本文档定义 AI 八字命理分析平台如何通过可重复、可追溯、风险驱动的测试，证明已批准需求与架构约束在发布时得到满足。测试的核心对象包括确定性命盘事实、领域不变量、跨 Context 契约、证据链、AI 输出、权限隐私、不可变历史、故障恢复和用户主旅程。

本文档把“质量”落实为可观察的证据和明确的发布门禁，但不替代产品验收、命理专家判断、法律结论或生产运行监控。

### 1.2 适用范围

本文覆盖：

- Value Object、Entity、Aggregate、Domain Service 和领域事件；
- Application Command、Query、Policy、Process Manager / Saga 和事务边界；
- Repository、数据库、缓存、消息、搜索、对象存储和外部 Provider Adapter；
- API 的认证、授权、幂等、错误、分页、兼容和异步操作契约；
- Chart Calculation、RuleRun、EvidenceBundle、Timeline、AIAnalysis、Conversation 和 Report；
- Prompt、Model、RAG、Retrieval、Citation、Validation、Risk 和 Degradation；
- 身份、Consent、PII、导出、删除、Legal Hold、Audit 和安全控制；
- 性能、容量、可靠性、恢复、可用性、国际化与可访问性；
- 测试数据、环境、自动化、覆盖、缺陷、门禁与治理。

### 1.3 不包含内容

本文不包含：

- 任何业务代码、测试代码、测试脚本或可执行示例；
- 任何测试框架、压测工具或浏览器自动化工具的具体实现；
- CI/CD、容器、基础设施或环境配置；
- SQL、数据迁移、API Payload 或 Schema；
- Prompt 内容、模型参数、Provider SDK 或 AI Evaluation 实现；
- 新增或修改 Aggregate、Entity、Value Object、Domain Event、API、Data 或 Context Boundary；
- 对尚未确定的命理规则、法律结论和产品阈值作出假设；
- 对命理有效性或未来预测准确性的科学证明。

### 1.4 基线优先级

测试不得为了便于自动化而改变已批准 Domain、Application、Data、API、Technology、Security 或 AI Baseline。若可测试性需要改变边界、契约、身份、版本、不可变规则或安全模型，只登记为 `ADR Candidate` 或 `Open Question`。

### 1.5 质量声明边界

测试可以证明实现与已批准规则、样例和契约一致，但不能证明命理具备科学预测能力。黄金命例通过、用户主观认同、模型一致性或专家意见均不得被转化为“预测准确率”宣传。

---

## 2. Testing Principles

### TST-P-001 Risk Based

测试深度由错误影响、发生概率、可检测性、数据敏感度和恢复难度共同决定。确定性排盘、权限、Consent、不可变历史、引用、安全与删除属于高风险区域。

### TST-P-002 Shift Left and Continuous

领域不变量、契约、安全规则和可测试性在设计阶段确认；测试不是发布前一次性活动。每类变更在最早能够提供可靠反馈的层级验证。

### TST-P-003 Deterministic Core

纯领域与确定性计算测试必须控制时钟、时区、身份生成、随机源、算法版本、规则版本和输入数据，不依赖当前日期、执行顺序或真实网络。

### TST-P-004 Evidence over Assertion Count

质量以风险场景、正确断言、失败诊断和可追溯结果衡量，不以测试数量或单一覆盖率代替判断。

### TST-P-005 Independent and Repeatable

测试互不依赖执行顺序，共享资源有明确隔离，失败可以在同一版本与环境条件下重现。

### TST-P-006 Test the Contract, Not the Implementation

测试关注外部可观察行为、不变量和稳定契约，避免绑定内部方法、ORM 结构、日志措辞或 Provider 私有 Payload。

### TST-P-007 Real Boundaries Need Real Verification

Mock 不能证明数据库、消息、对象存储、Provider 或 API 兼容。边界必须配套真实语义的 Integration 或 Contract Test。

### TST-P-008 Security and Privacy by Test

认证、授权、最小权限、数据最小化、去标识化、Consent、删除、保留、Audit 和敏感日志均有负向场景；仅验证成功路径不构成通过。

### TST-P-009 AI Is Untrusted Until Validated

模型原始输出不是正式结果。测试必须区分模型生成、平台 Validation、正式 AIAnalysis 结果和用户可见内容。

### TST-P-010 Version Reproducibility

正式回归结果锁定 CalculationSnapshot、Algorithm、Rule、Knowledge、Evidence、Prompt、Model、Validation 和 Risk Policy 版本。版本不完整的结果不能作为发布证据。

### TST-P-011 Failure Is a First-Class Path

Timeout、Retry、Circuit、Queue、重复消息、部分失败、撤回、删除、恢复和降级与成功路径同等重要。

### TST-P-012 Quality Gates over Calendar

关键门禁不因日期压力静默跳过。若无法满足，应缩小范围、延后发布或通过正式例外治理；不得降低结论标准。

### TST-P-013 Production Is Not a Test Environment

生产监控、Canary 和受控验证不替代发布前测试。禁止以真实用户和未授权数据进行探索性试验。

### TST-P-014 Traceability

每个 Must 需求、关键不变量、威胁和发布条件至少映射到一个测试或人工验证证据，并记录 Owner、版本、环境、结果与例外。

---

## 3. Testing Pyramid

### 3.1 分层模型

| 层级 | 相对数量 | 主要目标 | 典型执行时机 |
|---|---:|---|---|
| Pure Unit / Domain | 最大 | Value Object、Aggregate、不变量、算法边界 | 每次变更 |
| Application / Policy | 较大 | Use Case、权限、幂等、Saga 决策 | 每次变更 |
| Adapter / Contract | 中等 | Repository、Event、Provider、存储契约 | 合并前与定期 |
| Component | 较少 | 单 Context 的纵向能力 | 合并前与候选发布 |
| API / E2E | 最少但关键 | 公共契约和核心用户旅程 | 合并前、Beta、RC |
| Security / Performance / Reliability | 风险驱动 | 非功能与故障门禁 | 按变更、里程碑、RC |

### 3.2 金字塔解释

金字塔不规定僵化比例。高价值确定性逻辑应由快速、隔离测试大量覆盖；跨系统场景由较少但稳定的 Component、Contract 和 E2E 测试证明。AI Evaluation、性能、安全和恢复属于独立风险维度，不应被简单画作金字塔顶端后忽略。

### 3.3 测试职责不重叠原则

- Unit Test 定位本地逻辑错误，不承担基础设施兼容证明。
- Integration Test 验证 Adapter 与真实依赖语义，不重复所有领域组合。
- Contract Test 验证双方兼容，不替代业务流程验收。
- E2E Test 验证关键旅程，不穷举所有边界。
- 人工评审验证文化语境、理解度和复杂风险表达，不替代自动事实校验。

### 3.4 推荐执行套件

| Suite | 触发 | 阻断范围 |
|---|---|---|
| Fast Feedback | 每次变更 | Unit、Domain、Application、Architecture Boundary |
| Integration | 合并前 | Repository、Storage、Message、Provider、Contract |
| Domain Regression | 合并前与定期 | 黄金命例、历法边界、规则、证据 |
| AI Evaluation | Prompt/Model/RAG/Validation 相关变化 | 事实、引用、范围、风险、成本 |
| Security & Privacy | 风险变更与定期 | 权限、会话、注入、删除、日志、供应链 |
| Performance & Capacity | 里程碑与 RC | NFR-025 至 NFR-030 |
| Reliability & Recovery | 定期与 RC | 故障、备份、恢复、重放、降级 |
| Release Acceptance | Beta、RC、GA | 用户旅程、门禁、例外与证据包 |

---

## 4. Quality Objectives

### 4.1 质量属性

| 质量属性 | 需要证明的结果 | 主要证据 |
|---|---|---|
| Functional Correctness | 功能满足可验收需求 | Requirement Trace、Functional Test |
| Domain Integrity | 不变量、状态与所有权不被绕过 | Domain/Aggregate Test |
| Deterministic Accuracy | 同版本同输入产生一致事实 | Golden/Boundary/Metamorphic Test |
| Traceability | 结果可定位至完整版本与证据 | Manifest、Audit、Reproduction Test |
| Security | 未认证、越权与攻击被阻断 | Security/Permission Test |
| Privacy | 数据最小化、Consent 与权利流程有效 | Privacy Lifecycle Test |
| AI Grounding | AI 不补造事实且引用支持结论 | AI/RAG/Validation Evaluation |
| Reliability | 失败可控、可恢复且不破坏历史 | Failure/Recovery Test |
| Performance | 时延、容量、长度和限流符合基线 | Performance/Load/Stress Test |
| Usability | 普通用户理解并完成主旅程 | Usability/Accessibility Test |
| Compatibility | API、Event、Version 可兼容演进 | Contract/Backward Compatibility Test |
| Operability | 故障可发现、定位、回滚和审计 | Observability/Runbook Exercise |

### 4.2 MVP 已批准性能测试基线

| 指标 | 基线 | 测试解释 |
|---|---|---|
| 确定性排盘 | P95 ≤ 2 秒，P99 ≤ 5 秒 | 基准负载、缓存未命中、地点解析已完成；不少于 1,000 次黄金命例混合执行 |
| 常规已认证 API | P95 ≤ 500 毫秒，P99 ≤ 1.5 秒 | 排除 AI、PDF、地点外部查询和异步报告；按资源分别统计 |
| AI 首次有效响应 | P95 目标 ≤ 15 秒 | 包含生成、结构、事实和引用检查；1 秒内返回已受理或进度 |
| 完整 AI 报告 | P95 初始目标 ≤ 60 秒 | 分别统计成功、降级、失败；模型选型后复核 |
| 峰值容量 | 100 并发交互、20 并发 AI、持续 10 请求/秒 | 至少 30 分钟；错误率不超过 1%，超过容量时限流或排队 |
| 用户活动命盘 | 默认最多 100 个 | 并发配额一致性与管理员调整审计 |
| 在线报告长度 | 最多 30,000 Unicode 字符 | 不截断证据标识和风险提示 |
| AI 单条回答 | 最多 8,000 Unicode 字符 | 安全压缩、拆分或拒绝 |

以上数字是 Approved 测试基线，不是外部 SLO 或市场承诺。任何调整必须通过需求或架构治理，不得由测试或实现人员静默放宽。

### 4.3 尚待确认的质量阈值

以下保持 `Open Question`：首次排盘完成率、三分钟完成率、用户理解度、引用有效率、事实一致性、风险漏检率、AI 单位成本、正式可用性与恢复阈值。未批准前应先建立基线分布，不擅自设定通过数字。

### 4.4 Exit Evidence

每个发布候选保存：构建与基线版本、测试集版本、执行环境、数据来源、执行结果、失败与豁免、Owner、审批人、时间、已知风险和可重现路径。

---

## 5. Unit Testing

### 5.1 范围

Unit Test 验证最小可独立行为，包括纯函数、Policy、Validator、Mapper、状态判断和无外部依赖的服务。其目标是快速定位逻辑回归，而非模拟整个系统。

### 5.2 必测类别

- 正常、边界、无效和缺失输入；
- 状态转换允许与拒绝路径；
- 时间、时区、精度、排序、范围和单位；
- 权限条件、Scope、Purpose 与资源归属；
- 幂等判断和重复输入；
- 错误分类、是否可重试和安全消息映射；
- 版本兼容、不可变对象和历史引用；
- 脱敏、最小化和敏感字段过滤。

### 5.3 隔离要求

Unit Test 不访问数据库、网络、文件存储、系统当前时钟或共享队列。Clock、Identity、Random 和外部 Port 使用受控替身，但不替换被测领域行为本身。

### 5.4 断言质量

断言应验证业务结果、拒绝原因、事件意图和不变量。禁止只断言“没有抛错”、内部调用次数或实现私有结构而不验证业务语义。

### 5.5 完成标准

新增或修改逻辑必须有正向、负向和关键边界场景；失败信息能够定位被破坏的不变量；测试不依赖执行顺序且重复运行结果一致。

---

## 6. Domain Testing

### 6.1 目标

Domain Test 证明领域模型的统一语言、生命周期、聚合边界和不变量得到实现，而不依赖 Application 或 Infrastructure。

### 6.2 Value Object Test

必须验证：

- 合法值创建与非法值拒绝；
- 基于值的相等性、比较和不可变性；
- 规范化不丢失业务含义；
- HeavenlyStem、EarthlyBranch、FourPillars、TimePrecision、TimeZoneInfo、VersionInfo、EvidenceStatus 和 RiskLevel 等已批准语义；
- 不同时间精度、歧义时间和边界条件不被假装为精确值。

### 6.3 Entity Test

验证 Identity 稳定、生命周期转换、所有权、删除语义和版本引用。Identity 不包含业务含义，也不与 Sequence、Ordinal 或 Version 混用。

### 6.4 Aggregate Test

至少覆盖：

- User、SubjectConsent、Chart、RuleRun、EvidenceBundle、Knowledge、AIAnalysis 和 Report 的一致性边界；
- 内部 Entity 只能由 Aggregate Root 管理；
- 外部 Context 只引用 Aggregate Root Identity 或批准 Snapshot；
- Chart 只管理确定性计算与 CalculationSnapshot，不管理 RuleRun、Evidence、AIAnalysis 或 Report 生命周期；
- RuleRun Completed 后不得新增 RuleFinding；
- EvidenceBundle Frozen 后不得新增 Evidence；
- AIAnalysis Completed 不得回到 Generating；
- Frozen Report 不得回到 Draft 或 Generating；
- CalculationSnapshot Valid 后事实不可修改；
- Consent 同一主体、目的和范围同一时刻只有一个有效决定。

### 6.5 Domain Service Test

ChartCalculationService、RuleExecutionService、EvidenceBuilder、AIAnalysisService、ReportGenerator 和 TimelineBuilder 按已批准输入输出测试。测试不得把 Domain Service 变成跨 Context 事务协调者。

### 6.6 Domain Event Test

验证事件触发条件、最小 Payload、版本、顺序意图和不重复发布。`BirthProfileCreated` 只表示容器创建；正式时间标准化与排盘以 `BirthInputConfirmed` 为触发。事件测试不假设跨 Context 同步事务。

### 6.7 Golden Case Strategy

黄金命例必须具有来源、适用范围、预期事实、专家批准、版本和变更历史。预期值只能由获授权命理专家确认；争议规则保留多观点，不以测试强行形成唯一答案。

### 6.8 Boundary and Metamorphic Tests

覆盖节气边界、子时换日、闰月、时区、夏令时、真太阳时开关、不存在/重复本地时间、时间不确定和支持日期边界。对于可定义不变量的输入变换，验证版本、格式或无关身份变化不改变确定性事实。

---

## 7. Integration Testing

### 7.1 目标

Integration Test 验证应用 Port 与真实基础设施或兼容实现之间的语义，重点关注事务、序列化、并发、错误、恢复和版本，而非重复领域组合。

### 7.2 Repository Integration

验证：

- Aggregate 按 Root 加载和保存；
- 内部 Entity 不被跨 Context 直接访问；
- 乐观并发与唯一约束阻止双写；
-不可变 Snapshot、Frozen Bundle 和 Report 不被原地覆盖；
- Archive、Logical Delete、Anonymization、Legal Hold 与历史引用一致；
- 事务失败回滚，不产生半完成正式状态。

### 7.3 Messaging Integration

覆盖 Outbox/Inbox 语义、重复投递、乱序、延迟、消费者重启、不可处理消息、幂等和重放。事件最终一致不允许破坏所属 Aggregate 的本地一致性。

### 7.4 Cache Integration

验证 Key 隔离、Tenant/User/Chart 边界、TTL、版本失效、撤回与删除后的清除。Cache Miss 或 Cache 不可用时回源正确；Cache 绝不成为 Source of Truth。

### 7.5 Search and Vector Integration

验证 Published/Rights Filter、Index Version、重建、延迟、删除、Knowledge 撤回和 Tenant 隔离。相似度结果不得直接作为 Evidence 或事实。

### 7.6 Object Storage Integration

验证授权、加密、不可预测 Identity、短期访问、保留、删除、Legal Hold 和损坏检测。对象存储失败不得冻结不完整 Report。

### 7.7 External Provider Integration

地点、模型、通知等 Provider 通过 Adapter Contract 测试 Timeout、Rate Limit、Error Mapping、Region/Retention Policy 和降级。生产凭据与真实用户数据不得进入普通测试环境。

### 7.8 Transaction Integration

覆盖 Commit、Rollback、并发冲突、进程崩溃点、外部调用超时、Audit 失败、Outbox 写入和重试。跨 Context 不使用共享事务保证一致性。

---

## 8. API Testing

### 8.1 契约范围

API Test 验证 Resource、Command、Query、HTTP 语义、认证授权、幂等、错误、分页、过滤、版本、异步操作和兼容规则，不泄漏内部 Aggregate 或数据库结构。

### 8.2 HTTP Semantics

验证方法安全性与幂等性、成功与错误状态、条件请求、缓存边界和重试提示。错误响应遵循批准的 Problem Details、稳定错误码和本地化安全消息。

### 8.3 Authentication and Authorization

每个资源至少覆盖：未认证、Token/Session 失效、错误 Role、错误 Scope、错误 Purpose、跨用户/租户、已撤回 Consent、已归档/删除资源和合法访问。

### 8.4 Idempotency

对要求幂等的 Command 验证：首次处理、同 Key 同意图重放、同 Key 不同意图拒绝、并发重复、处理中重试、完成后重试和保留窗口。最终只产生一个正式业务结果。

### 8.5 Error Model

验证 `AUTH`、`CONSENT`、`INPUT`、`TIME`、`CALC`、`RULE`、`EVIDENCE`、`KNOWLEDGE`、`AI`、`REPORT`、`PRIVACY`、`RATE` 和 `SYSTEM` 分类的稳定语义。响应不暴露堆栈、SQL、模型原始输出、Secret 或内部拓扑。

### 8.6 Pagination, Filtering and Sorting

验证默认/最大页大小、稳定游标、重复/遗漏、非法过滤、排序稳定性、权限过滤先于分页，以及数据变化时的契约语义。

### 8.7 Async Operations

验证受理、Operation Identity、Polling、完成、失败、取消（如批准）、过期、Retry-After 和重复请求。异步完成不得绕过最终 Validation、权限或 Audit。

### 8.8 Compatibility and Versioning

验证同一 API 主版本内新增可选能力不破坏旧 Client；删除、重命名、语义改变、错误契约或分页策略变化按 Breaking Change 处理。基于已保存消费者契约执行兼容回归。

### 8.9 Correlation

RequestId、CorrelationId 和 TraceId 在合法边界内可关联请求、异步任务与日志；客户端提供的不可信值经校验，且不被用于授权或泄漏其他租户信息。

---

## 9. Application Testing

### 9.1 Command Testing

验证前置条件、授权、Aggregate 加载、领域调用、事务提交、事件意图、幂等、错误映射和 Audit。Command Handler 不实现领域规则或直接修改多个 Context Aggregate。

### 9.2 Query Testing

验证过滤、排序、Projection 新鲜度标识、权限和脱敏。Query 不触发 Command；Read Model 不作为 Domain Source of Truth。

### 9.3 Policy Testing

权限、风险、保留、路由、配额和降级 Policy 使用组合场景验证；策略版本改变必须能追溯测试集和批准记录。

### 9.4 Process Manager / Saga Testing

验证成功、重复事件、乱序、超时、补偿、部分失败、恢复和终止。Saga 只协调，不成为跨 Context Domain Aggregate，也不直接修改其他 Aggregate。

### 9.5 AnalysisProgress Testing

只读投影视图聚合 Chart、RuleRun、EvidenceBundle、AIAnalysis、Timeline 和 Report 状态时，验证延迟、缺失、失败和重建。投影视图不得反向修改任何源 Aggregate。

### 9.6 Authorization Boundary

Use Case 在加载敏感数据和执行副作用前完成必要授权。测试同时覆盖 Endpoint、Application 和资源所有权层，避免只在 UI 隐藏能力。

---

## 10. AI Testing

### 10.1 测试目标

AI Test 证明正式结果受版本、证据、范围、风险和 Validation 控制。它衡量 Grounding、结构、安全、帮助度和成本，不衡量或宣称命理预测准确率。

### 10.2 测试分层

| 层级 | 固定输入 | 主要验证 |
|---|---|---|
| Pipeline Unit | 锁定 Fixture | Context 顺序、预算、Redaction、Validator |
| Gateway Contract | 受控 Provider 响应 | Provider Abstraction、错误、计量、版本 |
| Offline Evaluation | 版本化评估集 | 事实、引用、范围、冲突、风险、质量 |
| Adversarial Evaluation | 攻击与异常样本 | Injection、Leakage、Jailbreak、越权 |
| Human Review | 去标识候选结果 | 文化语境、可理解性、克制表达 |
| Canary / Online Guard | 受控生产流量 | Drift、延迟、成本、拒绝和事故信号 |

### 10.3 AIAnalysis Lifecycle

覆盖 Planned、Generating、Validating、Completed、Rejected 和 Failed。Completed 不得回到 Generating；模型原始输出不能直接成为正式结果；失败或 Fallback 不静默覆盖原 AIAnalysis。

### 10.4 Input Authority

测试模型只接收已授权、去标识化且在 AnalysisPlan 范围内的 CalculationSnapshot、RuleRun、Frozen EvidenceBundle、Knowledge Citation 和必要对话上下文。模型不得计算命盘事实、创建 Evidence 或扩大分析范围。

### 10.5 Multi-Provider and Routing

验证 Model Gateway 是唯一正式调用入口；路由遵守 Task、语言、风险、区域、能力、成本和健康状态。技术重试保持相同 Analysis、Prompt、Model 和 Bundle；切换 Provider/Model 的 Fallback 按已批准语义创建新的 AIAnalysis 并保留失败历史。

### 10.6 Output Validation Test

至少验证：

- 结构与必填片段；
- Scope、主体、Chart 和未来三年边界；
- CalculationSnapshot 事实一致；
- RuleFinding 和 Evidence 引用存在且有权访问；
- Claim 与 Citation 支持关系；
- 冲突观点和证据等级表达；
- 高风险主题、绝对化语言和专业建议边界；
- Prompt/Secret/PII 泄漏；
- 长度、字符与展示安全；
- Rejected、Repair、Fallback 和 Degradation 路径。

### 10.7 Hallucination Evaluation

构造缺少证据、冲突证据、无检索结果、用户诱导、错误前提和超范围问题。期望系统澄清、不足说明、拒绝或降级，而不是补造事实。

### 10.8 Human Review

人工评审使用标准 Rubric，至少区分事实、引用、冲突、风险、通俗度、文化语境和帮助度。Reviewer 经过校准，抽样与分歧处理可审计。人工认同不得被标记为预测准确。

### 10.9 Drift Testing

持续比较 Model、Provider、Prompt、Retrieval、Validation 和 Risk Policy 版本的分布变化。Drift 信号触发调查、Block、回滚或新版本，不允许同名模型静默变化绕过评估。

### 10.10 AI Cost Test

按 Task、Model、Prompt、Context、Retry、Fallback 和 Validated Result 记录 Token 与成本。验证 Budget、Quota、预警、拒绝和降级；成本优化不得跳过安全或质量 Gate。

---

## 11. Prompt Regression Testing

### 11.1 边界

本文只定义 Prompt Regression 方法，不包含任何 Prompt 内容。Prompt Registry、PromptVersion、Review、Published、Compatibility 和 Rollback 继承 AI Baseline。

### 11.2 触发条件

以下变化必须触发相应回归：PromptVersion、ModelReference、Provider、Output Contract、Context Assembly、Knowledge/Retrieval、Validation、Risk Policy、Locale 和术语版本。

### 11.3 回归集合

至少包含：标准解释、证据不足、规则冲突、时间不确定、未来三年边界、高风险主题、注入攻击、引用失配、长上下文、不同中文表达和拒答样例。

### 11.4 比较策略

不要求逐字相同。比较结构合规、事实一致、引用支持、范围、风险、关键语义、长度、延迟和成本。对非确定性输出使用属性与 Rubric，而不是脆弱字符串快照。

### 11.5 发布与回滚门禁

Prompt 新版本只有在兼容矩阵、离线评估、安全样本和必要人工复核通过后可发布。回滚使用已发布不可变版本，并验证与当前 Model、Output 和 Validation 兼容。

### 11.6 Regression Record

记录 PromptVersion、ModelReference、DatasetVersion、参数策略引用、结果分布、失败样本、Reviewer、成本、批准和回滚点；不得记录不必要的完整敏感上下文。

---

## 12. RAG Testing

### 12.1 目标

RAG Test 验证合法知识被正确切分、索引、检索、排序、引用和撤回；相似度高不等于事实正确或 Evidence 有效。

### 12.2 Knowledge Ingestion

验证只有 Published、授权有效、语言/流派/适用范围清晰的 Knowledge 进入正式索引。Deprecated、Retired、撤权或 Legal Hold 内容按批准政策处理。

### 12.3 Chunk Strategy

验证 Chunk 保留来源、标题、版本、段落稳定身份、语言、流派、权利和适用范围。切分不得把限定条件、否定、争议观点与正文分离。

### 12.4 Embedding Strategy

验证 EmbeddingModel、ChunkVersion 和 IndexVersion 可追溯、可重建、隔离且不默认包含个人命例。模型变化必须全量或明确增量重建，不混用不可比较向量。

### 12.5 Retrieval Evaluation

评估 Precision、Recall、Ranking、Zero Result、错误来源抑制和权限过滤。具体阈值待批准；发布前至少报告按主题、语言、流派和风险分类的分布。

### 12.6 Hybrid Retrieval and Ranking

验证 Structured Filter、Lexical、Vector 和 Reranking 的顺序与版本；权限、发布状态、Rights 和 Scope Filter 必须先于最终 Context 使用。

### 12.7 Citation Test

验证 Citation 指向稳定 KnowledgeVersion/片段，用户有权查看必要来源元数据，Claim 得到实际支持，撤回后按历史策略展示。禁止只验证“引用存在”而不验证支持关系。

### 12.8 Adversarial Knowledge

覆盖隐藏指令、Prompt Injection、伪造来源、冲突元数据、重复内容、语言混淆和超长片段。Knowledge 内容始终作为数据，不获得指令优先级。

### 12.9 Index Freshness and Deletion

验证发布、更新、撤权、删除和重建事件最终反映到索引；延迟期间有状态与告警，不允许已撤权内容继续进入新 AIAnalysis。

---

## 13. Validation Testing

### 13.1 Validation Layers

| Layer | 验证内容 | 失败处置 |
|---|---|---|
| Input | 格式、范围、精度、Consent | 拒绝或澄清 |
| Domain | 不变量与状态 | 阻断事务 |
| Reference | Identity、Version、Ownership | 拒绝正式处理 |
| Evidence | Frozen、完整、支持关系 | 不得生成确定结论 |
| AI Structure | 正式输出结构 | Repair、Rejected 或 Failed |
| AI Fact | 与 Snapshot/Rule 一致 | Rejected |
| Citation | 存在、权限、支持、权利 | Rejected 或降级 |
| Risk | 主题、绝对化、专业边界 | 拒绝、改写或人工复核 |
| Presentation | 长度、i18n、可访问性 | 修复或阻断发布 |

### 13.2 Negative Validation

每条 Validator 必须有至少一个拒绝场景，且验证失败不会产生 Frozen、Published 或 Completed 正式对象。

### 13.3 Validator Versioning

正式结果记录 Validator/Policy 版本。新版本不得回写旧结果；历史重验产生新验证记录或新正式对象，遵守已批准生命周期。

### 13.4 Repair Boundary

Repair 只能修复允许的结构或表达，不得改变上游事实、Evidence 或 Analysis Scope。Repair 次数有限并纳入成本与 Audit。

### 13.5 Validation Observability

统计失败类型、版本、模型、主题、语言和修复结果，避免记录完整敏感正文。异常突增触发发布阻断或 Incident 调查。

---

## 14. Security Testing

### 14.1 范围

安全测试覆盖身份、Session/Token、MFA、RBAC、ABAC、最小权限、API、Web、AI、供应链、Secret、Audit 和运行环境。测试计划由 Threat Model、数据分类和变更风险驱动。

### 14.2 Authentication Testing

覆盖登录、失败限制、MFA、Session 固定/劫持、Token 过期/撤销/轮换、并发会话、登出、密码或凭证恢复和异常设备。长期 Token 与共享管理员账号视为阻断缺陷。

### 14.3 Permission Testing

构建 Role × Action × Resource × Ownership × Purpose × Context 矩阵，验证允许和拒绝。重点覆盖跨用户 Chart/Report/Conversation、管理员敏感访问、专家发布职责分离和服务账号最小权限。

### 14.4 Application Security

覆盖客户端输入不可信、注入、跨站请求、跨站脚本、服务端请求伪造、对象级越权、开放重定向、上传、分页枚举、错误泄漏和 Rate Limit 绕过。安全测试只定义验证目标，不在本文提供攻击脚本。

### 14.5 AI Security

覆盖 Prompt Injection、Indirect Injection、Prompt Leakage、Jailbreak、Scope 扩大、数据外带、模型滥用、超长上下文和输出注入。当前默认无 Tool；未来若改变必须经 ADR 和独立安全测试。

### 14.6 Secret and Key Testing

验证 Secret 不出现在源码、日志、Trace、Prompt、Fixture、错误和制品中；轮换、撤销、最小权限和环境隔离有效。测试凭据不得与生产共享。

### 14.7 Audit Security

验证关键事件完整、顺序可解释、访问受控、篡改可检测和保留有效。Audit 不记录不必要敏感正文，且失败按基线阻断关键操作或进入明确恢复流程。

### 14.8 Security Test Cadence

高风险变更执行专项测试；依赖与静态风险持续检查；Beta/RC 前执行完整评估；GA 前完成正式安全评审与必要人工验证。具体工具和频率由后续实施治理确定。

---

## 15. Performance Testing

### 15.1 目标

证明系统在批准基准负载下满足时延、吞吐、容量、长度和资源约束，并在超载时限流、排队或降级而非无界耗尽。

### 15.2 Workload Model

工作负载按真实业务比例构成：匿名/注册输入、确定性排盘、规则与证据、查询、AI 对话、报告、Timeline、后台操作和隐私任务。快速健康检查不得稀释业务请求时延。

### 15.3 Measurement Rules

报告 Environment、Build、Dataset、Cache State、并发、吞吐、持续时间、P50/P95/P99、错误、超时、队列、资源和依赖状态。成功、失败、降级和限流分开统计。

### 15.4 Deterministic Calculation

按 NFR-025 使用正式黄金命例混合数据不少于 1,000 次，地点解析预先完成，缓存未命中，AI 时延不计入。结果同时验证正确性，不能用错误快速响应满足时延。

### 15.5 API Performance

按资源类型统计常规已认证 API；排除已批准的 AI、PDF、外部地点和异步报告。权限和审计不能在性能测试中关闭。

### 15.6 AI Performance

“首次有效响应”必须通过展示条件和 Validation，不以原始首 Token 代替。分别测量 Gateway、Queue、Provider、Retrieval、Validation、Repair 和完整 Operation。

### 15.7 Data Growth

测试用户命盘、Snapshot、RuleRun、Evidence、Conversation、Report、Audit、知识版本和索引增长后的查询、归档、删除和恢复行为。

### 15.8 Regression Policy

相同基准环境对比历史趋势。显著回归即使仍低于绝对阈值也需解释；环境差异不可被当作产品改善或回归结论。

---

## 16. Load Testing

### 16.1 基准负载

MVP 初始负载为 100 个并发交互请求、20 个并发 AI 任务和持续 10 请求/秒的核心混合负载，至少持续 30 分钟。

### 16.2 验收条件

- 错误率不超过已批准 1% 基线；
- Must 时延违反单独报告；
- 幂等、权限、版本和 Audit 不因负载失效；
- Queue、连接、线程/执行单元和 Provider Quota 保持有界；
- 超过容量时返回明确限流、排队或降级状态；
- 无跨用户 Cache、Context 或结果污染。

### 16.3 场景组合

覆盖 Cache Warm/Cold、读写混合、突发 AI、报告集中生成、后台发布、Privacy Export/Delete 与普通用户流量共存。

### 16.4 Soak

在批准窗口持续运行以发现内存、连接、Queue、日志、Token、Cache 和成本累积。正式时长和通过阈值待容量计划批准。

---

## 17. Stress Testing

### 17.1 目标

确定容量拐点、失效模式和恢复特性，而非证明无限扩展。Stress Test 不在生产直接进行。

### 17.2 场景

- 并发、吞吐和 AI Queue 超过设计容量；
- Provider Rate Limit 或高延迟；
- 数据库连接、缓存、消息积压和对象存储受限；
- 超长但合法报告、回答和知识片段；
- 热点用户、热点 Chart 和重复 Idempotency Key；
- Audit、日志和 Trace 量激增。

### 17.3 安全失效要求

系统优先保护数据完整、权限、不可变历史和 Audit。可降级 AI、排队非关键任务或拒绝新请求，但不得绕过 Validation、扩大权限或丢失正式状态。

### 17.4 恢复验证

压力解除后验证 Circuit、Queue、连接、Worker、Cache 和 Projection 收敛；不产生重复正式对象、孤儿对象或未审计副作用。

---

## 18. Reliability Testing

### 18.1 目标

验证系统面对依赖失败、网络分区、超时、进程重启、重复消息和部分成功时保持一致、可恢复和可观察。

### 18.2 Failure Matrix

| Failure | 期望行为 | 验证重点 |
|---|---|---|
| AI Provider 不可用 | 保留确定性能力并受控降级 | 不伪造 AI Completed |
| Retrieval 不可用 | 无证据时拒绝或降级 | 不绕过 Citation Gate |
| Cache 不可用 | 正确回源或限流 | Cache 非真相源 |
| Message 重复/乱序 | 幂等处理、最终收敛 | 无重复正式对象 |
| Object Storage 失败 | Report 不冻结 | 可重试、Audit 完整 |
| Database 短暂失败 | 有限重试或安全失败 | 事务与并发一致 |
| Audit 写入失败 | 按关键性阻断或恢复 | 无静默缺口 |
| Projection 落后 | 标注延迟、可重建 | 不反向修改 Source |
| 删除部分失败 | 状态可见并继续收敛 | 不宣称已完全删除 |

### 18.3 Retry and Idempotency

验证单一 Retry Owner、退避、总预算、不可重试分类和重复副作用防护。无限重试、层层重试和 Fallback 隐藏失败均不允许。

### 18.4 Circuit Breaker and Bulkhead

验证 Circuit Open/Half-Open/Close、隔离维度、最小样本和恢复。一个 Provider、模型或重任务故障不得耗尽全部核心资源。

### 18.5 Backup and Restore

恢复测试验证数据、版本、引用、不变量、不可变历史、Audit、索引重建和删除 Tombstone。只验证备份任务成功不等于恢复通过。

### 18.6 Disaster Recovery

按已批准运维基线执行恢复演练。尚未批准的 RPO/RTO 不由本文自行设定；演练先建立事实基线并登记差距。

---

## 19. Chaos Testing（可规划）

### 19.1 定位

Chaos Testing 是受控可靠性验证能力，可在系统具备基础可观察性、故障隔离、回滚和运行手册后规划，不是 MVP 发布的默认前置实现要求。

### 19.2 前置条件

- 明确假设、影响范围、停止条件和 Owner；
- 使用隔离的非生产环境或经批准的最小生产实验；
- 有实时监控、回滚、数据保护和安全审批；
- 不使用真实敏感数据或未经授权用户流量；
- 不与数据迁移、重大发布或 Incident 同时进行。

### 19.3 候选实验

Provider 延迟/失败、缓存不可用、消息重复/延迟、Worker 重启、对象存储短暂失败、Projection 落后和网络抖动。数据库破坏性实验、跨区域故障和生产注入需独立风险评审。

### 19.4 成功标准

实验验证预期降级、告警、隔离、恢复和无数据破坏；任何意外权限、隐私或不可变历史影响立即停止并按 Incident 处理。

---

## 20. E2E Testing

### 20.1 原则

E2E 数量保持有限、稳定和高价值，验证真实用户可观察结果与跨 Context 协作，不用于穷举领域组合或依赖内部实现。

### 20.2 MVP 核心旅程

至少覆盖：

1. 匿名用户阅读定位与边界，输入必要出生信息并确认 BirthInput；
2. 时间不确定、地点歧义、真太阳时开关和子时规则说明；
3. 确定性排盘、规则发现、证据与通俗依据展示；
4. 当前大运与未来三年时间轴；
5. 受限 AI 解读与当前命盘对话；
6. AI 不可用时仍展示确定性结果；
7. 在线报告、打印和 Frozen 历史；
8. 注册、登录、保存、归档与活动命盘配额；
9. Consent 撤回、数据导出、删除和部分失败状态；
10. 管理员/专家发布职责分离与敏感访问拒绝；
11. 简体中文正式体验及 i18n/RTL 架构骨架。

### 20.3 首次用户完整旅程验收

从入口理解、匿名选择、输入、参数确认、计算、结果首屏、依据展开、时间轴、AI 问答到报告打印均记录成功/失败和耗时。三分钟完成率目标保持待产品可用性测试确认，不由自动 E2E 自行声明。

### 20.4 Cross-Context Assertions

E2E 只验证最终可观察状态和 Correlation，不要求跨 Context 同步完成。允许 AnalysisProgress 显示延迟，但不允许其作为真相源或反向修改 Aggregate。

### 20.5 Accessibility and Locale

覆盖键盘路径、语义、焦点、错误关联、颜色之外提示、移动端、数字/日期/时区展示和 RTL 布局骨架。英文与阿拉伯语未人工复核前不得宣称上线质量。

---

## 21. Test Data Strategy

### 21.1 数据分类

| 类型 | 用途 | 规则 |
|---|---|---|
| Synthetic | 默认开发与自动化 | 不映射真实个人 |
| Golden Case | 排盘与规则验收 | 来源、专家批准、版本、权限 |
| Boundary Case | 历法、状态、安全边界 | 可生成、可重复 |
| Adversarial | 注入、越权、AI 风险 | 受控、无真实攻击凭据 |
| Production-like | 容量与兼容 | 合成规模与分布 |
| Authorized Real Case | 仅必要研究/评估 | 单独 Consent、去标识、可撤回、隔离 |

### 21.2 Data Minimization

Fixture 不含真实姓名、联系方式、详细地址、Credential、完整 Prompt、生产日志或 Provider Secret。出生信息即使去名仍可能敏感，应按高保护等级处理。

### 21.3 Golden Dataset Governance

黄金命例由命理专家 Owner 管理，记录适用算法/规则、争议、来源和批准时间。算法或专家口径改变创建新版本，不原地改写旧预期。

### 21.4 Referential Integrity

跨 Context Fixture 只使用 Aggregate Root Identity、Snapshot 或 Event Contract；不直接构造对其他 Context 内部 Entity 的非法引用。

### 21.5 Data Lifecycle

测试数据有创建、授权、保留、刷新、撤回、删除和 Legal Hold 规则。测试运行结束清理临时数据；长期回归集按版本归档并定期复审。

### 21.6 Masking and Anonymization

生产数据默认不进入测试。极少数批准场景先最小化、去标识、抽样和风险评估；可重新识别风险不能被简单字段替换掩盖。

### 21.7 Test Clock and Identity

时间、时区、Identity 和随机性可控。测试 Identity 仍遵循无业务含义、全局唯一和不可复用原则，不把时间或版本编码进 Identity。

---

## 22. Test Environment

### 22.1 环境类型

| 环境 | 目的 | 数据与依赖 |
|---|---|---|
| Local / Isolated | 快速 Unit 与 Component | 合成数据、替身依赖 |
| Integration | Adapter 与 Contract | 隔离真实语义依赖 |
| Test | 跨模块与自动回归 | 生产相似配置、合成数据 |
| Staging / Pre-Production | Release、性能、安全、恢复 | 最大程度生产同构、非生产凭据 |
| Production | 监控、Canary、受控验证 | 真实权限，不作为常规测试场 |

### 22.2 Environment Isolation

账号、网络、Secret、数据库、Cache、Queue、Storage、Provider Project、日志和成本预算按环境隔离。禁止测试环境访问生产数据平面或复用生产 Credential。

### 22.3 Parity

关键 Runtime、数据库语义、时区数据、依赖版本、安全控制和 Feature 状态与生产一致或明确记录差异。环境差异必须进入测试报告和风险判断。

### 22.4 Ephemeral Isolation

可采用按变更或测试运行创建的临时逻辑隔离，但不在本文指定技术实现。销毁前保存必要的去敏证据；销毁失败有告警和清理 Owner。

### 22.5 Environment Readiness

运行前验证版本、迁移状态、Seed、Clock、Provider Stub/真实模式、Quota、Observability 和数据清洁度。环境不健康时结果标记无效，不通过重跑制造假绿。

### 22.6 Provider Test Modes

Provider 测试区分模拟错误、契约 Sandbox 和受控真实调用。真实调用有预算、去标识化、区域与保留审查，且不成为所有快速测试的唯一依赖。

---

## 23. Test Automation Strategy

### 23.1 自动化选择

优先自动化高频、确定、关键、可重复和回归价值高的场景。文化语境、复杂风险表达、可用性和探索性安全仍需要人工评审。

### 23.2 Mock Strategy

| 替身类型 | 合适用途 | 不得证明的内容 |
|---|---|---|
| Stub | 固定外部返回与错误 | 真实兼容性 |
| Fake | 内存 Port、状态场景 | 数据库并发/事务语义 |
| Spy | 观察副作用意图 | 最终外部完成 |
| Mock | 严格交互边界的少量场景 | 整体业务正确性 |
| Simulator | Provider 故障与延迟模型 | 供应商真实行为全部细节 |

禁止 Mock 一切。关键 Adapter 必须有真实 Contract/Integration Test；领域对象本身不得被 Mock。

### 23.3 Test Isolation

测试按 User/Tenant、Database Namespace、Queue、Object Prefix、Cache Key、Provider Project 和 Clock 隔离。并行执行不得产生跨测试数据依赖。

### 23.4 Flaky Test Policy

Flaky Test 是缺陷。重跑只用于收集诊断，不得把首次失败改写为通过。临时隔离必须记录 Owner、原因、影响、到期和修复任务；关键安全、领域和发布门禁不可被隔离后放行。

### 23.5 Execution Tiers

快速套件在每次变更提供反馈；高成本 AI、性能、安全和恢复按风险与里程碑运行。任何分层都必须保证相关变更在发布前执行完整门禁。

### 23.6 Test Artifact

保存结构化结果、版本清单、环境、数据集、指标分布、失败证据和审批；默认不保存敏感正文、完整 Prompt、Secret 或生产 PII。

### 23.7 Maintenance

每个 Suite 有 Owner、目的、触发、最大预期时长、失败处置和退役条件。失去需求映射、重复或长期无信号的测试应评审，不得盲目累积。

---

## 24. Coverage Strategy

### 24.1 多维覆盖

Coverage 至少包含：

- Requirement Coverage：Must/Should 与 Acceptance Criteria；
- Domain Coverage：Aggregate、不变量、状态和 Domain Event；
- Risk Coverage：威胁、失败、隐私和高影响场景；
- Code Coverage：实现路径的辅助信号；
- Contract Coverage：API、Event、Repository 和 Provider；
- Data Coverage：标准、边界、冲突、无效和规模；
- Platform Coverage：浏览器、设备、Locale、时区和辅助技术；
- AI Coverage：Task、Model、Prompt、主题、风险、语言和输出处置。

### 24.2 Critical Coverage

以下要求场景级完整覆盖并作为阻断：关键 Aggregate 不变量、认证授权、Consent、不可变历史、版本引用、幂等、删除/导出、事实/引用 Validation、风险拒绝和关键 Audit。

### 24.3 Code Coverage Policy

不在本文件设定统一百分比。各模块结合风险建立基线和最低门槛，禁止通过无意义断言提高数字。低覆盖必须有风险分析、补偿测试和 Owner。

### 24.4 Mutation and Fault Sensitivity

可在后续实施中评估变异或故障注入以验证断言敏感性；是否采用及范围属于工程决策，不在本文指定工具。

### 24.5 Traceability Matrix

每个关键需求映射 Requirement → Risk/Invariant → Test Level → Test Case/Dataset → Result → Defect/Exception → Release。矩阵按版本冻结并可审计。

### 24.6 Coverage Exceptions

无法自动化的场景记录人工步骤、证据、Reviewer 和频率。无法测试不等于可忽略；涉及基线可测试性变化时登记 ADR Candidate。

---

## 25. Defect Lifecycle

### 25.1 状态

建议逻辑生命周期：`New → Triaged → Accepted → InProgress → Resolved → Verified → Closed`。也允许 `Duplicate`、`NotReproducible`、`Deferred` 或 `Rejected`，但必须有理由与审批。该流程不定义具体工具配置。

### 25.2 Severity

| Severity | 定义 | 示例 |
|---|---|---|
| Critical | 数据/安全/隐私严重损害或核心不可恢复 | 越权、敏感泄漏、历史被覆盖 |
| High | 核心 Must 失败或正式结果错误 | 排盘事实错误、无效引用通过 |
| Medium | 重要功能受损且有有限替代 | 部分流程失败、明显性能回归 |
| Low | 低影响表现或非关键问题 | 次要文案、非阻塞展示 |

Severity 表示影响，Priority 表示修复顺序，两者不得混用。

### 25.3 Triage

Triage 确认版本、环境、数据、复现、影响、Context Owner、是否安全/隐私 Incident、回归范围和发布影响。命理结论争议由专家判断，不由普通缺陷流程自行裁定规则真伪。

### 25.4 Resolution Evidence

修复需有根因、变更范围、自动/人工回归、相邻风险和版本证据。仅“无法复现”不能在缺少环境与数据分析时关闭高风险缺陷。

### 25.5 Escape and Learning

生产逃逸缺陷追踪为何未被预防/检测、应在哪一层增加信号、是否涉及基线或治理。复盘聚焦系统改进，不以缺陷数量做个人绩效排名。

### 25.6 Defect Exception

未修复缺陷进入发布必须有影响、用户暴露、补偿控制、Owner、期限、批准和撤回条件。Critical 安全/隐私、数据完整性、核心权限或不可变历史问题不得例外放行。

---

## 26. Release Quality Gates

### 26.1 Gate 原则

Gate 由证据决定 Go/No-Go。缺失、过期、环境不可信或版本不匹配的结果等同未通过。任何豁免都不能静默存在。

### 26.2 Change Gate

每次合并至少通过相关 Unit、Domain、Application、Architecture Boundary、Contract 和静态质量检查。涉及特定风险的变更追加 AI、安全、隐私、性能或迁移验证。

### 26.3 Alpha Gate

- 核心确定性排盘和黄金/边界命例可重复；
- 关键 Aggregate 不变量与事件契约通过；
- 匿名首次旅程可完成；
- 已知 Critical/High 风险有明确阻断或处置；
- 测试环境、数据和基础可观察性可用。

### 26.4 Beta Gate

- MVP Feature Scope 已冻结，Beta 后不得新增 MVP Feature；
- 核心 E2E、AI/RAG、权限、Consent、报告和降级通过；
- 用户理解度与三分钟旅程完成至少一轮研究并形成基线；
- 安全、隐私、AI 风险和数据生命周期无阻断问题；
- 失败与回滚路径完成验证。

### 26.5 RC Gate

- RC 后仅允许阻塞问题修复或批准的范围移除；
- 全量回归、性能容量、安全隐私、恢复和运营演练通过；
- 发布制品与测试对象一致；
- 无未处置 Critical，High 缺陷按批准政策收敛；
- 正式法律和命理专家门禁完成或明确阻断；
- 所有例外有 Owner、期限和 Go/No-Go 批准。

### 26.6 GA Gate

- GA 前不得新增任何需求；
- RC 缺陷修复完成针对性与回归验证；
- 产品、架构、质量、安全、隐私、法律、运维和领域专家签署各自结论；
- 数据保留期限、高风险内容边界和正式发布区域完成法律确认；
- 监控、告警、Incident、回滚和用户支持准备完成；
- 发布证据包冻结并可审计。

### 26.7 Non-Negotiable Gates

以下不能因进度默认跳过：Domain Regression、Authentication/Authorization、Consent、Sensitive Data、Immutable History、Critical Audit、Calculation Correctness、Evidence/Citation Validation、AI Risk、Delete/Export、Security Incident 阻断和发布制品一致性。

### 26.8 Gate Exception

例外写明范围、理由、风险、补偿、Owner、到期、退出和批准。涉及基线变化仍需 ADR；例外不得改变测试结果本身，只能记录带风险的发布决策。

---

## 27. Test Metrics

### 27.1 指标分类

| 类别 | 候选指标 | 使用目的 |
|---|---|---|
| Execution | Pass/Fail/Blocked、Duration | 套件健康与反馈速度 |
| Stability | Flaky Rate、Retry、Environment Failure | 信号可信度 |
| Coverage | Requirement、Risk、Invariant、Contract | 识别盲区 |
| Defect | Escape、Reopen、Severity、Age | 发现系统性问题 |
| Domain | Golden/Boundary/Conflict Results | 确定性与规则回归 |
| AI | Grounding、Citation、Scope、Risk、Reject | AI 质量与安全 |
| RAG | Retrieval、Ranking、Zero Result、Rights | 检索质量 |
| Performance | P50/P95/P99、Throughput、Error、Queue | 容量与回归 |
| Cost | Cost per Validated Result、Retry/Fallback | AI 单位经济性 |
| Release | Gate Status、Exception、Open Risk | Go/No-Go |

### 27.2 指标解释边界

- Pass Rate 不代表风险全部覆盖；
- Coverage 高不代表断言有效；
- 用户认同不代表命理准确；
- 模型一致不代表事实正确；
- 引用存在不代表支持结论；
- 平均时延不得替代尾延迟；
- 低拒答率不得成为绕过风险 Gate 的目标。

### 27.3 Metric Integrity

指标定义、分母、窗口、过滤、版本和环境保持稳定。阈值改变需治理记录；不得排除失败或降级样本制造改善。

### 27.4 Dashboard and Audit

Dashboard 使用聚合去敏数据；Release Evidence 保存原始结果身份与 Hash/Version 引用。访问遵循最小权限和保留策略。

---

## 28. Testing Governance

### 28.1 Ownership

| 资产 | 主要 Owner | 必要协作者 |
|---|---|---|
| Testing Strategy | 测试/质量架构负责人 | CTO、架构委员会 |
| Domain/Golden Tests | Context Owner | 命理专家、测试 |
| AI Evaluation | AI 质量负责人 | 知识、安全、产品、专家 |
| Security/Privacy Tests | 安全与隐私负责人 | 研发、运维、法律 |
| Performance/Recovery | 平台与运维负责人 | 测试、应用 Owner |
| E2E/User Journey | 产品质量负责人 | 设计、前后端、可访问性 |
| Release Gate | 发布经理 | 各 Gate Owner |
| Test Data | 数据治理 Owner | 安全、隐私、专家 |

### 28.2 Architecture Baseline

01–13 Approved 文档属于 Architecture Baseline。测试策略不得修改基线；测试发现冲突时创建缺陷、Open Question 或 ADR Candidate。

### 28.3 Test Asset Versioning

Test Case、Dataset、Rubric、Contract、Environment Profile 和 Gate Definition 均版本化。已用于正式发布的证据不可原地修改。

### 28.4 Review Cadence

每个 Milestone 检查需求追踪、黄金集、AI Drift、Flaky、环境差异、安全风险、性能趋势、缺陷逃逸和门禁例外。重大 Provider、Model、Prompt、Rule、Algorithm 或 Security 变化执行专项评审。

### 28.5 Independence and Segregation

测试设计由团队共同负责，关键发布结论由相应 Owner 审核。Rule/Knowledge/Prompt 的作者不能单独批准自己的正式回归结果；高风险例外需要独立批准。

### 28.6 Legal and Expert Gates

命理预期、争议规则和术语由授权专家确认；数据保留、跨境、Provider、Content Labeling、高风险主题和用户权利由法律/隐私负责人确认。测试团队只验证批准规则的执行。

### 28.7 Scope Freeze

Beta 后不得新增 MVP Feature；RC 后仅允许阻塞问题修复或批准范围移除；GA 前不得新增需求。测试发现问题不自动扩大产品范围，应按缺陷、风险或后续版本处理。

### 28.8 Auditability

正式门禁变更、运行、失败、豁免、重跑和批准均可审计。不得删除失败记录或用后续通过结果覆盖原结果。

---

## 29. Testing ADR Reference Matrix

任何涉及下列主题的重大变化，不得直接修改本文档或实现，必须先批准 ADR，再更新相应基线。

| Topic | ADR Required | 典型触发 |
|---|---|---|
| Testing Strategy | Yes | 总体分层、职责或风险模型变化 |
| Test Pyramid | Yes | 层级职责或主要反馈结构变化 |
| AI Evaluation | Yes | 评估框架、正式判定机制变化 |
| Prompt Regression | Yes | 版本比较、兼容或发布机制变化 |
| RAG Testing | Yes | Retrieval/Rights/Citation 验证架构变化 |
| Coverage Policy | Yes | 关键覆盖门槛或例外机制变化 |
| Release Quality Gate | Yes | Go/No-Go、不可豁免门禁变化 |
| Performance Strategy | Yes | 基准模型、统计口径或容量方法变化 |
| Security Testing | Yes | 威胁验证、渗透或安全门禁变化 |
| E2E Strategy | Yes | 核心旅程范围或跨 Context 验证方式变化 |
| Test Environment | Yes | 隔离模型、生产验证边界变化 |
| Test Data Policy | Yes | 真实数据、黄金数据、保留或匿名化变化 |
| Contract Testing | Yes | API/Event/Provider 兼容治理变化 |
| Defect Exception | Yes | Critical/High 放行政策变化 |
| Reliability / Chaos | Yes | 生产故障注入或恢复模型变化 |

以下发现尤其不得由测试设计直接修正：Aggregate Boundary、Cross Context Relationship、Identity、Version、Immutable Object Rules、API Contract、Security/Privacy Model、AIAnalysis/Fallback 语义。它们必须回到对应 Approved Baseline 与 ADR 流程。

---

## 30. Testing Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐做法 |
|---|---|---|---|
| No Unit Test | 最小逻辑无快速反馈 | 回归晚发现、定位困难 | 为领域、策略和 Validator 建立隔离测试 |
| Testing Only UI | 只从最慢最脆弱层验证 | 组合爆炸、失败难定位 | 遵循分层金字塔，UI 只覆盖关键旅程 |
| Manual Testing Only | 依赖不可重复人工步骤 | 发布不稳定、历史不可追溯 | 自动化确定性回归，人工聚焦语境与探索 |
| Shared Test Data | 测试共享可变数据 | 顺序依赖、并发污染、隐私风险 | 每次运行隔离数据和 Identity |
| Flaky Tests | 相同条件结果不稳定 | 团队忽略失败、门禁失信 | 作为缺陷治理，有限隔离并限期修复 |
| Mock Everything | 所有依赖都由自定义返回替代 | 契约漂移、生产行为未验证 | Mock 最小化，真实边界做 Contract/Integration |
| No Regression Testing | 只验证新增功能 | 旧规则、版本和旅程被破坏 | 建立风险驱动的版本化回归集 |
| No AI Evaluation | 模型结果凭主观抽看发布 | 幻觉、越界、成本和 Drift 不可控 | 离线评估、对抗样本、人工校准与 Gate |
| No Performance Testing | 用开发体验推测容量 | 上线时延迟、耗尽与成本失控 | 按批准负载与尾延迟执行基线测试 |
| No Security Testing | 假设框架默认安全 | 越权、泄漏、注入和合规事故 | Threat-driven 自动与人工安全验证 |
| Low Coverage Without Risk Analysis | 关键区域未测且无解释 | 隐性盲区进入发布 | 场景/风险覆盖分析、补偿和 Owner |
| Ignoring Failed Tests | 将失败视为噪音或直接重跑 | 真实缺陷被掩盖 | 保留首次失败、分类根因、阻断相关发布 |
| Testing Production Directly | 把真实用户当测试样本 | 数据、可用性与法律风险 | 隔离环境；生产只做批准的受控验证 |
| Test Coupled to Implementation | 断言私有方法和内部结构 | 重构成本高、行为缺陷漏检 | 针对契约、结果和不变量断言 |
| No Release Gate | 结果不影响发布决策 | 已知高风险仍上线 | 建立可审计 Go/No-Go 与不可豁免门禁 |
| Golden Case Without Expert Approval | 测试人员自行决定命理预期 | 错误规则被固化 | 专家批准、版本化并保留争议 |
| Snapshot Everything | 用整页/整段快照替代语义断言 | 无意义变更频繁、错误难识别 | 对关键结构与语义属性断言 |
| Happy Path Only | 不测失败、撤回和降级 | 事故时数据损坏或误导 | 建立 Failure Matrix 与负向场景 |
| Coverage as Target | 为数字编写低价值测试 | 假安全感、维护成本 | Coverage 作信号，结合风险与变异敏感性 |
| Retry Until Green | 自动重跑直至通过 | Flaky 和真实故障被覆盖 | 记录首次失败，重跑仅用于诊断 |
| Real PII in Fixtures | 复制用户数据方便测试 | 隐私泄漏和用途越界 | 合成数据；例外需 Consent、去标识和隔离 |
| AI Exact String Assertion | 要求非确定输出逐字一致 | 测试脆弱或诱导固定话术 | 验证结构、事实、引用、范围和 Rubric |
| Citation Existence Only | 只查引用 ID 存在 | 来源不支持结论仍通过 | 执行 Claim-to-Citation 支持验证 |
| Average-only Performance | 只看平均时延 | 尾延迟和少数用户问题被掩盖 | 报告 P50/P95/P99 与分组分布 |
| Disabled Controls in Test | 性能/E2E 时关闭权限或审计 | 结果不代表生产 | 保持生产等价安全控制并记录差异 |
| Cross-Context Fixture Coupling | 直接构造他 Context 内部 Entity | 固化非法依赖 | 通过 Root Identity、Snapshot 或 Event Contract |

---

## 31. Review Checklist

### 31.1 Baseline and Scope

- [ ] 文档状态是否为 Review、版本是否为 0.9。
- [ ] 是否严格继承 01–13 Approved 1.0。
- [ ] 是否未修改 Domain、API、Data、Technology、Engineering、Security 或 AI Baseline。
- [ ] 是否没有代码、脚本、配置、流水线或 Prompt 内容。
- [ ] 是否未进入编码阶段或下一文档。
- [ ] 冲突是否只记录为 ADR Candidate 或 Open Question。

### 31.2 Pyramid and Functional Tests

- [ ] Unit、Domain、Application、Integration、Contract、API、Component 和 E2E 职责是否清晰。
- [ ] Value Object、Entity、Aggregate、Domain Service 和 Event 是否有场景。
- [ ] Chart 与 RuleRun/Evidence/AI/Report 边界是否保持自治。
- [ ] Immutable Object Rules 是否全部成为阻断测试。
- [ ] Mock 是否最小化且真实边界有 Contract Test。
- [ ] Flaky Test 是否按缺陷治理。

### 31.3 Domain and Expert

- [ ] 黄金命例是否来源明确、版本化并由授权专家批准。
- [ ] 节气、换日、闰月、时区、夏令时、真太阳时和不确定时间是否覆盖。
- [ ] 争议规则是否保留不同观点而非由测试强行统一。
- [ ] AI/用户认同是否未被解释为命理科学准确。
- [ ] 待专家确认的规则是否仍保持待确认。

### 31.4 AI, Prompt and RAG

- [ ] AI 是否不计算事实、不创建 Evidence、不扩大 Scope。
- [ ] Raw Output 是否必须经过结构、事实、引用、冲突、风险和泄漏检查。
- [ ] Prompt Regression 是否版本化且不要求逐字相同。
- [ ] Fallback 是否保留原失败并遵守新 AIAnalysis 语义。
- [ ] RAG 是否验证 Rights、Chunk、Index、Ranking、Zero Result 和 Citation 支持。
- [ ] Drift、Human Review、成本和 Degradation 是否进入门禁。

### 31.5 Security and Privacy

- [ ] Authentication、MFA、Session/Token、RBAC/ABAC 和最小权限是否覆盖。
- [ ] IDOR、注入、跨站、服务端请求伪造、Rate Limit 和 AI 攻击是否覆盖。
- [ ] Consent、导出、删除、保留、Legal Hold 和备份复活是否覆盖。
- [ ] Test Data 是否默认合成且环境无生产 Credential。
- [ ] 日志、Trace、Artifact 是否完成敏感信息检查。
- [ ] 关键 Audit 的完整性与不可篡改性是否验证。

### 31.6 Performance and Reliability

- [ ] NFR-025 至 NFR-030 是否按批准口径测试。
- [ ] P50/P95/P99、错误、降级、限流和环境是否分别报告。
- [ ] 负载是否至少覆盖批准的并发、AI 任务、吞吐和持续时间。
- [ ] Timeout、Retry、Circuit、Queue、重复/乱序和部分失败是否覆盖。
- [ ] Backup/Restore 是否验证数据、不变量、版本、Audit 和 Tombstone。
- [ ] Chaos 是否仅在满足前置条件后规划。

### 31.7 Governance and Release

- [ ] Requirement/Risk/Test/Result/Exception 是否可追溯。
- [ ] Test Dataset、Rubric、Contract、Environment 和 Gate 是否版本化。
- [ ] Alpha、Beta、RC、GA Gate 是否与 Roadmap Scope Freeze 一致。
- [ ] 不可豁免 Gate 是否明确。
- [ ] Release Evidence 是否完整、去敏、冻结且可审计。
- [ ] ADR Matrix 中变化是否先获得批准。

---

## 32. Open Questions

### 32.1 Product and Quality

1. 首次排盘完成率、三分钟完成率和用户理解度的正式样本、阈值与观察窗口。
2. 哪些用户旅程是 Alpha、Beta、RC 和 GA 的强制阻断场景。
3. 普通用户对“依据充分/一般/有限/冲突”的理解验收方法。
4. 打印最大报告在主流设备与浏览器的正式支持矩阵。
5. MVP 已知缺陷的 Release Exception 权限与 High 缺陷放行政策。

### 32.2 命理专家

1. 黄金命例、边界命例、争议命例的首批清单、来源、版权和批准流程。
2. 具体旺衰、格局、调候、用神、喜神、忌神测试预期。
3. 起运顺逆与起运时间、子时换日、真太阳时最终口径。
4. 首批神煞及适用、不适用、冲突和信息不足样例。
5. 多流派冲突优先级及是否允许无优先结论。
6. 规则、证据和术语变更所需专家 Reviewer 数量和一致性处理。

### 32.3 AI and RAG

1. Grounding、引用有效、事实一致、风险漏检、拒答和帮助度的正式门槛。
2. Prompt Regression Dataset、Rubric、Reviewer 和版本比较政策。
3. RAG Precision/Recall/Ranking/Zero Result 的正式阈值和主题分层。
4. Model-as-Judge 是否允许、校准方式及其不能单独决定的门禁。
5. Human Review 比例、抽样方法、分歧仲裁和 SLA。
6. AI Drift 窗口、阈值、Block、回滚和 Incident 等级。
7. Provider 真实测试调用的预算、区域、Retention 和数据边界。

### 32.4 Performance and Reliability

1. Soak 时长、资源饱和和长期泄漏阈值。
2. 正式生产 SLO、Error Budget、RPO 和 RTO；当前测试基线不自动等于这些指标。
3. 数据增长规模、热点比例、Queue Backlog 和 Provider Slow 的正式模型。
4. 何时允许在生产进行最小 Chaos/Canary 验证及审批人。
5. 性能回归相对阈值和不同环境的归一化方法。

### 32.5 Security, Privacy and Legal

1. 正式渗透、安全评审和第三方评估范围与频率。
2. 测试数据、结果、AI 原始输出和安全证据的保留期限。
3. 真实命例用于评估的 Consent、去标识化、撤回和删除流程。
4. Legal Hold 与测试清理、删除验证及备份恢复之间的优先规则。
5. 目标地区对 AI Content Labeling、高风险主题和用户权利测试的要求。
6. 英文与阿拉伯语人工术语、安全和法律复核方法。

### 32.6 Engineering and Environment

1. 具体自动化框架、测试管理与报告平台；选择不得改变本策略。
2. Monorepo/Polyrepo 下 Suite Ownership 和触发策略。
3. 临时环境、Provider Sandbox 和生产同构程度。
4. 各模块 Code Coverage 基线与风险豁免流程。
5. 契约制品的发布、兼容窗口和消费者责任。
6. Flaky 隔离最长时限和门禁恢复责任。

### 32.7 ADR Candidates

- ADR-CANDIDATE-TEST-001：测试金字塔、Suite 分层与执行门禁。
- ADR-CANDIDATE-TEST-002：黄金命例、测试数据、真实命例授权和版本治理。
- ADR-CANDIDATE-TEST-003：AI Evaluation、Prompt Regression、Human Review 和 Drift Gate。
- ADR-CANDIDATE-TEST-004：RAG、Retrieval、Citation 与 Rights 测试方法。
- ADR-CANDIDATE-TEST-005：Coverage、Traceability、Flaky 与 Defect Exception Policy。
- ADR-CANDIDATE-TEST-006：性能工作负载、统计口径、Soak 与容量门禁。
- ADR-CANDIDATE-TEST-007：Security/Privacy Testing、数据保留和第三方评估。
- ADR-CANDIDATE-TEST-008：Test Environment、Provider Test Mode 和生产验证边界。
- ADR-CANDIDATE-TEST-009：Reliability、Recovery、Chaos 和正式演练范围。
- ADR-CANDIDATE-TEST-010：Alpha/Beta/RC/GA Release Quality Gate。

---

## 33. Risks

| Risk | Manifestation | Impact | Mitigation / Gate |
|---|---|---|---|
| Baseline Drift | 测试为方便而改变领域/API | 架构失真 | ADR Gate、Boundary Review |
| False Confidence | 通过率高但关键风险未覆盖 | 缺陷上线 | 多维覆盖、Risk Traceability |
| Golden Case Error | 未经专家确认的预期固化 | 错误规则成为基线 | Expert Owner、Version、Review |
| Scientific Overclaim | 将命例/AI 通过称为预测准确 | 误导与法律风险 | 指标语义审查、产品 Gate |
| Flaky Normalization | 团队习惯忽略红灯 | 门禁失效 | Flaky Defect Policy、期限 |
| Mock Drift | 替身与真实依赖不一致 | 集成/生产失败 | Contract + Integration Test |
| Shared Data Contamination | 并行测试互相修改 | 不稳定、隐私泄漏 | Isolation、Synthetic Data |
| Production Data Leakage | 真实命例进入普通测试 | 隐私与用途越界 | Default Deny、Consent、DLP Review |
| Environment Drift | 测试与生产语义不同 | 假通过 | Parity Manifest、差异风险 |
| AI Non-determinism | 输出波动导致脆弱测试 | 假失败或放过错误 | 属性/Rubric、分布、人工校准 |
| Model Silent Change | 同名模型行为漂移 | 回归未被触发 | ModelReference、Drift Gate |
| Citation False Positive | 引用存在但不支持 Claim | 虚假可信 | Support Validation |
| RAG Rights Leak | 撤权内容仍被检索 | 版权/合规风险 | Rights Filter、Index Deletion Test |
| Risk Under-testing | 高风险主题样本不足 | 有害内容漏出 | Adversarial Set、Human Review |
| Cost Blindness | AI 测试无限调用 | 预算失控 | Test Budget、Cost per Valid Result |
| Performance Misreporting | 平均值/健康检查稀释 | 尾延迟被隐藏 | 分资源 P95/P99、口径审计 |
| Load Data Corruption | 压测绕过权限/幂等 | 错误容量结论 | 功能断言与负向检查并行 |
| Retry Storm | 测试/系统层层重试 | 依赖放大、成本增长 | Single Retry Owner、Budget |
| Recovery Not Proven | 只看备份成功 | 灾难时无法恢复 | Restore Drill、Invariant Verification |
| Delete Resurrection | 恢复/索引重建复活数据 | 隐私事故 | Tombstone、Backup/Index Test |
| Security Scope Gap | 只做自动扫描 | 业务越权未发现 | Threat Model、Permission Matrix、人工测试 |
| E2E Explosion | 所有组合放进端到端 | 慢、脆弱、反馈迟 | Pyramid、关键旅程限定 |
| Test Artifact Leakage | 报告含 Prompt/PII/Secret | 二次泄漏 | Redaction、Retention、Access Control |
| Gate Exception Abuse | 例外长期存在 | 风险累积 | Owner、Expiry、Independent Approval |
| Schedule Compression | 测试被排到最后 | RC 堵塞或带病上线 | Shift Left、Scope Reduction |
| Ownership Gap | 失败无负责人 | 长期 Block/Flaky | Asset Owner、Escalation |
| Scope Creep | 测试发现被转为新增 MVP | 延误与冻结破坏 | Defect/Risk 分类、Scope Freeze |

---

## 34. 进入下一阶段《15-ARCHITECTURE-DECISION-RECORDS.md》所需输入条件

- [ ] `14-TESTING-STRATEGY.md` 已完成评审并成为 Approved 1.0 Testing Baseline。
- [ ] 测试原则、金字塔、层级职责和 Suite 触发已确认。
- [ ] Quality Objectives 与 Approved 性能基线解释已确认。
- [ ] Unit、Domain、Value Object、Aggregate、Event 和 Golden Case 策略已确认。
- [ ] Integration、Repository、Messaging、Cache、Search、Storage 和 Provider Contract 策略已确认。
- [ ] API、Application、Saga、幂等、授权和 Projection 测试已确认。
- [ ] AI、Prompt Regression、RAG、Output Validation、Hallucination、Citation、Drift 和 Human Review 已确认。
- [ ] Security、Permission、Privacy、Consent、Export、Delete、Legal Hold 和 Audit 测试已确认。
- [ ] Performance、Load、Stress、Reliability、Recovery 和可规划 Chaos 策略已确认。
- [ ] E2E 首次用户旅程、i18n/RTL、可访问性与降级场景已确认。
- [ ] Test Data、Mock、Isolation、Environment、Artifact 与 Retention 策略已确认。
- [ ] Coverage、Traceability、Defect、Flaky 和 Release Exception Policy 已确认。
- [ ] Alpha、Beta、RC、GA Quality Gate 与 Scope Freeze 已确认。
- [ ] 测试指标定义和“不得声称命理科学准确”边界已确认。
- [ ] 命理专家、产品、法律、安全和 AI 待确认项已有 Owner 与阻断规则。
- [ ] ADR Reference Matrix 的 Candidate 已分类，未批准 ADR 未改变任何基线。
- [ ] 下一阶段仅建立 ADR 文档治理，不生成业务代码、测试代码、脚本、配置或流水线。

只有本测试策略通过评审后，才可以生成 `15-ARCHITECTURE-DECISION-RECORDS.md`。本次不得生成该文件，也不得进入编码阶段。
