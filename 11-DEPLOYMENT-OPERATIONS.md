# AI 八字命理分析平台：部署与运维规范

**文档编号：** 11  
**文档类型：** Deployment and Operations Architecture  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md`、`02-SRS.md`、`03-SYSTEM-ARCHITECTURE.md`、`04-DOMAIN-MODEL.md` 1.0、`05-DATA-MODEL.md` 1.0、`06-ROADMAP.md` 1.0、`07-APPLICATION-ARCHITECTURE.md` 1.0、`08-API-DESIGN.md` 1.0、`09-TECHNOLOGY-ARCHITECTURE.md` 1.0、`10-IMPLEMENTATION-GUIDE.md` 1.0（均已 Approved）  
**目标读者：** CTO、架构师、平台工程与 SRE、研发与测试负责人、安全与隐私负责人、数据负责人、值班人员、事件响应人员及发布治理人员

---

## Version 0.9 Change Log

- 首次定义环境、部署、发布、变更、回滚、迁移和运行治理规范。
- 定义日志、指标、追踪、健康检查、Synthetic、SLI、SLO、Error Budget 与告警运维模型。
- 定义 Incident、Severity、On-Call、Runbook、Problem Management 和人工处置规范。
- 定义 Backup、Restore、DR、Business Continuity、容量、性能、成本和供应商运维规范。
- 定义 PostgreSQL、Redis、Queue/Worker、Object Storage、安全、隐私、数据权利和 Audit 运维要求。
- 本文件不包含任何可执行部署配置、监控查询、告警规则、脚本或业务代码。

---

## 1. Document Purpose

### 1.1 目标

本文档定义 AI 八字命理分析平台如何安全、可重复地部署与发布，如何持续观察用户和领域质量，如何响应故障并恢复，以及如何管理生产访问、容量、成本、依赖、备份和数据权利。

运维目标不是“所有组件永不失败”，而是在失败发生时保护确定性事实、不可变历史、用户隐私、证据可信性与业务连续性，并提供可审计的恢复路径。

### 1.2 适用范围

本文覆盖：

- Local、Automated Test、Staging、Production 和 DR/Restore Sandbox；
- Immutable Artifact、Artifact Promotion、Rollout、Rollback/Forward-Fix 和数据库迁移；
- Logs、Metrics、Traces、Dashboards、Synthetic、SLI/SLO/Error Budget；
- Alert、Incident、On-Call、Escalation、Runbook 和 Problem Management；
- Backup、Restore、DR、Business Continuity；
- Capacity、Performance、Cost、Dependency/Vendor；
- Queue/Worker、PostgreSQL、Redis、Object Storage；
- Security、Privacy、Data Rights、Audit 和生产访问；
- Operational Readiness、Production Readiness 和治理。

### 1.3 不包含内容

本文不包含：

- Dockerfile、Compose、Kubernetes、Helm、Terraform、Ansible 或云配置；
- GitHub Actions、GitLab CI 或其他 Pipeline 配置；
- Shell、SQL、Python、TypeScript、FastAPI 或 Next.js 代码；
- Monitoring Query、Dashboard JSON 或 Alert Rule YAML；
- 数据库表、API、Repository 或业务逻辑实现；
- Aggregate、Entity、Value Object、Domain Event 或 Bounded Context 变更；
- Application、API、Data、Technology 或 Engineering Baseline 变更；
- 进入编码或部署执行阶段的授权。

### 1.4 Authority Boundary

运维工具可以观察、限制、路由、恢复和执行已批准操作，但不能创造或修改领域事实。监控、日志、Trace、Cache、Queue 和 Dashboard 都不是业务 Source of Truth。

### 1.5 Conflict Handling

若运维需求要求改变 Domain Model、Data Model、Application Architecture、API Contract、Technology Baseline 或 Engineering Baseline，只登记为 `ADR Candidate` 或 `Open Question`。未批准前选择保守降级、暂停受影响发布或维持现有基线。

---

## 2. Operations Principles

### OPS-P-001 User and Data First

运维决策优先保护用户数据、确定性事实、不可变历史和清晰状态，而不是优先维持表面“全绿”。

### OPS-P-002 Immutable Artifact

制品一次构建、签名/验证后在环境间晋级；不在生产重新构建或在线修改。

### OPS-P-003 Automated, Reviewed, Auditable

部署、迁移、配置、Secret、权限和恢复通过受控流程执行，保留 Actor、批准、制品、结果和关联标识。

### OPS-P-004 Default Deny

生产访问、Secret、数据库、对象、日志和 Audit 默认不可访问，仅按最小权限、Purpose 和时限授权。

### OPS-P-005 Progressive Delivery

按风险选择 Rolling、Canary 或 Blue-Green，并用 Release Gate、健康、业务、领域质量和安全信号逐步放量。

### OPS-P-006 Forward and Backward Compatibility

滚动窗口内应用、Worker、Schema、Message 和 API 保持兼容。Rollback 前先验证当前数据与 Schema 是否允许。

### OPS-P-007 Failure Is Explicit

Partial、Degraded、Blocked 和 Failed 必须可见，不把队列积压、投影延迟、删除遗漏或 AI 失败伪装为完成。

### OPS-P-008 Observability Without Data Leakage

可观察性提供足够调查证据，但不记录完整出生资料、会话正文、Prompt、AI 原始输出或报告全文。

### OPS-P-009 SLO over Component Uptime

以用户可观察结果、领域质量和数据权利完成为核心，组件运行不等于服务正确。

### OPS-P-010 Error Budget Is a Decision Tool

Error Budget 用于平衡可靠性和变更速度，但不能抵消安全、隐私、数据正确性、删除复活或审计丢失事故。

### OPS-P-011 Recoverability over Backup Existence

备份只有经过恢复、业务验证和删除墓碑重放才有价值。

### OPS-P-012 Idempotent Operations

部署、任务、重放、恢复和数据权利步骤设计为可安全重复；技术重试不能创造新的正式业务意图。

### OPS-P-013 Least Surprise

发布、降级、告警和维护对用户、支持和内部团队有明确状态与沟通，不进行隐蔽变更。

### OPS-P-014 Blameless and Accountable

Incident Review 不指责个人，同时明确系统缺陷、决定、Owner、期限和验证责任。

### OPS-P-015 Governed Evolution

环境、部署、SLO、DR、生产访问和值班模型的重大变化必须通过 ADR。

---

## 3. Environment Model

### 3.1 Environment Classes

| Environment | Purpose | Data | External Dependencies | Availability Expectation |
|---|---|---|---|---|
| Local | 单人开发、快速 Unit/Module 验证 | 合成数据 | Stub、Local 或批准 Sandbox | 无生产 SLO |
| Automated Test | CI、Contract、Integration、安全与兼容测试 | 每次可重建合成数据 | 隔离测试实例/Sandbox | 以 Pipeline 可靠性管理 |
| Staging | Release、Migration、Performance、Security 和 Runbook 验证 | 合成或严格批准去标识化数据 | 尽量使用生产同语义 Sandbox | 支撑 Release Gate，非用户 SLO |
| Production | 正式用户服务 | 正式数据 | 正式受控供应商 | 按批准 SLO 运行 |
| DR / Restore Sandbox | Backup Restore、PITR、Tombstone 和灾备演练 | 隔离恢复副本 | 受限或禁外联 | 按演练目标临时存在 |

### 3.2 Environment Isolation

- 各环境使用独立账户/项目、网络、数据库、Redis、Broker、Object Storage、Secret、Credential 和供应商项目。
- 环境间无默认网络或数据访问。
- Production 权限不因拥有 Local/Staging 权限自动获得。
- 日志、指标、Trace、Dashboard 和 Alert 按环境隔离。
- 环境 Identity 明确写入所有运行信号，防止误操作。

### 3.3 Production Data Prohibition

生产数据不得进入 Local、Automated Test 或普通 Staging。确需复现时优先构造合成 Fixture；只有完成用途、授权、去标识化、访问、期限和删除评审后，才可在专用隔离环境使用最小数据。

### 3.4 Secret and Credential Isolation

- 每个环境独立 Secret、Certificate、API Key 和 Workload Identity。
- 不允许 Staging Credential 调用 Production Data Plane，反之亦然。
- DR Restore 使用独立临时 Credential，不默认激活生产外部调用。
- Credential 轮换、撤销与访问全部审计。

### 3.5 Environment Configuration Differences

| Difference | Allowed | Required Control |
|---|---|---|
| Capacity / Instance Count | 是 | 明确记录，不改变功能语义 |
| Provider Sandbox | 是 | Contract 一致性与差异清单 |
| Domain/Algorithm/Rule Behavior | 否，除明确测试版本 | 版本显式、不能冒充 Production |
| Security Baseline | 仅可更严格或使用隔离替身 | 不得在 Staging 形成错误安全信心 |
| Retention | 可缩短 | 不影响删除与 Audit 测试语义 |
| Feature Flags | 可不同 | 差异登记、Release 时核对 |
| Locale/Timezone | 测试可扩展 | Production 默认与批准策略一致 |

### 3.6 Environment Parity

Staging 在运行模型、配置 Schema、网络边界、Migration、Health、Observability 和 Release Workflow 上尽量接近 Production。容量与供应商费用可以缩小，但所有差异必须可见且纳入风险评估。

### 3.7 DR Sandbox Safety

恢复副本默认无公网、无真实通知、无 AI/第三方回调、无用户登录。验证人员通过 JIT 权限访问，演练结束后按期限销毁并审计。

### 3.8 Environment Lifecycle

环境创建、用途变更、停用和销毁有 Owner、资产清单与数据处置。临时 Preview/Restore 环境自动到期；延长必须重新批准。

---

## 4. Deployment Model

### 4.1 Approved Runtime Shape

首阶段保持容器化模块化单体：Next.js Web、FastAPI API、Worker 和 Scheduler 可独立部署与扩缩容，但共享应用兼容版本；PostgreSQL、Redis、Broker、Object Storage 和 Observability 位于受控基础设施边界。

### 4.2 Deployment Units

| Unit | Deployment Responsibility | State Rule |
|---|---|---|
| Web | 第一方界面、静态资产、Server Rendering | 不保存正式业务状态 |
| API | 同步 Command/Query 与 Operation 接入 | 尽量无状态 |
| Worker Pools | Calculation、AI、Report、Index、Data Rights 等异步任务 | 任务状态持久化，不依赖本地内存 |
| Scheduler | 周期性触发批准的幂等应用意图 | 不直接修改数据库 |
| Database Migration | 向前兼容 Schema 变化 | 独立 Gate，不作为应用启动副作用 |
| Business Content Release | Algorithm/Rule/Knowledge/Prompt/Model Route | 与应用部署分离、版本化、审计 |

### 4.3 Immutable Artifact

- 每个制品关联源版本、依赖锁、测试、安全扫描、SBOM、构建身份和完整性证明。
- 不在 Staging 或 Production 重新构建。
- 不进入运行实例手工修改文件。
- 相同制品通过配置引用适配环境，但配置不能改变业务基线。
- 发现制品污染或来源不明立即停止晋级。

### 4.4 Artifact Promotion

制品按 Automated Test → Staging → Production 晋级。每次晋级验证签名/完整性、兼容矩阵、配置、Secret Reference、Migration 状态、Release Approval 和已知风险。

### 4.5 Compatibility Window

滚动期间允许 N/N-1 或批准的明确版本组合。Web、API、Worker、Message Contract、Schema 和 Cache Key 必须在窗口内兼容；最长混跑时间为 Open Question。

### 4.6 Deployment State

部署状态与领域状态分离。发布成功不等于 Calculation、AIAnalysis、Report 或 Data Rights Operation 完成；部署工具不得写业务终态。

### 4.7 Graceful Shutdown

- 实例先停止接收新流量或新 Message。
- API 完成或安全终止正在处理的短请求。
- Worker 仅在业务提交并确认后 Ack；未完成任务交由 Broker 重投。
- Scheduler 释放 Leader/Lease，不重复创建正式意图。
- 超过 Drain Budget 时记录未完成状态，不伪报成功。

---

## 5. Release Management

### 5.1 Release Types

| Type | Scope | Governance |
|---|---|---|
| Standard | 低风险、重复、已验证变化 | 预批准流程 + 自动 Gate |
| Normal | 常规功能、依赖或行为变化 | Change Review + Release Approval |
| High-Risk | Identity、Data、Security、Migration、AI Risk、Data Rights | 多 Owner、专项演练、渐进发布 |
| Emergency | 正在发生的重大 Incident 修复 | 缩短但不取消最小测试、双人和 Audit |
| Content Release | Rule/Knowledge/Prompt/Model/Algorithm | 独立 Governance，非普通应用发布 |

### 5.2 Release Package

每次 Release 至少包含：范围、关联 Requirement/ADR、Immutable Artifact、Change List、Compatibility、Migration、Config/Flag、Security/Privacy、Test Evidence、Rollout、Verification、Rollback/Forward-Fix、Communication 和 Owner。

### 5.3 Release Gate

- CI 和 Contract/Architecture/Security Gate 通过；
- Staging 部署与 Synthetic 通过；
- Migration 演练和锁/容量风险可接受；
- Error Budget 与 Incident 状态允许；
- Dashboard、Alert、Runbook、On-Call Ready；
- Secret/Config 已验证但未泄露；
- 变更符合 Beta/RC/GA Scope Freeze；
- 高风险内容与法律门禁完成。

### 5.4 Release Calendar

发布窗口考虑值班覆盖、供应商维护、业务高峰、法律截止、数据库窗口和团队支持。避免在无人值守、重大节假日或依赖不可支持时进行高风险变化，除非 Emergency。

### 5.5 Release Communication

内部沟通说明时间、影响、观察期、Owner、回退触发和用户支持信息。用户沟通保持克制，不暴露安全细节，也不把命理功能变化宣传为预测准确率提升。

### 5.6 Release Completion

只有 Deployment Verification、业务/领域指标、错误、安全与成本观察满足条件，并完成观察窗口，Release 才标记完成。Pipeline 结束不等于 Release 完成。

---

## 6. Change Management

### 6.1 Change Record

每个生产 Change 记录：目的、Scope、Owner、Risk、Affected Services/Data、Artifact/Config/Migration、Dependencies、Test、Schedule、Rollout、Verification、Rollback/Forward-Fix、Communication 和审批。

### 6.2 Risk Classification

| Factor | Higher Risk When |
|---|---|
| User Impact | 首次排盘、报告、登录或数据权利主路径 |
| Data | Schema、Identity、Version、Delete、Audit 或 Frozen History |
| Security/Privacy | Auth、Secret、Scope、Masking、AI Transmission |
| Compatibility | API/Message/Worker/Schema 跨版本 |
| Reversibility | 数据变化不可简单回滚 |
| Blast Radius | 全量用户、多环境、多供应商 |
| Novelty | 首次执行、无演练或新技术 |
| Capacity | 高峰、长 Migration、Connection/Queue 风险 |

### 6.3 Standard Change

Standard Change 必须重复、低风险、有成熟 Runbook、自动验证和清晰回退。定期复审；发生 Incident 后取消预批准资格，重新评估。

### 6.4 Emergency Change

Emergency Change 仅用于减少正在发生或迫近的重大用户/安全/数据影响。至少需要 Incident/Change Owner、第二人 Review、最小测试、范围限制、实时观察和事后 Review。

### 6.5 Change Freeze

Roadmap 的 Beta、RC、GA Scope Freeze 继续生效。Incident、合规或安全修复可以通过 Emergency/Approved Removal 流程处理，但不能借机增加功能。

### 6.6 Configuration Change

配置变化与代码部署同样记录、审批、验证和回滚。Business Version Config 不走普通配置通道。

### 6.7 Unauthorized Change

任何未通过流程的生产变化视为运维事件：先停止扩散、保存证据、评估影响、恢复已知状态并进行 Incident/Problem Review。

---

## 7. Deployment Workflow

### 7.1 Standard Workflow

1. 确认 Approved Change、Artifact 与 Owner。
2. 检查当前 Incident、Error Budget、Maintenance 和依赖状态。
3. 验证 Artifact、SBOM、Config Schema、Secret Reference 和 Compatibility。
4. 执行 Staging 部署、Migration 演练和 Synthetic。
5. 获取所需审批并发布内部通知。
6. 执行 Expand 类数据库变化（如有）。
7. 按风险选择 Rolling、Canary 或 Blue-Green 开始放量。
8. 验证 Health、API、业务、领域质量、安全、隐私、Queue 和成本指标。
9. 继续放量、暂停、Rollback 或 Forward-Fix。
10. 完成 Migrate/Contract 的批准后续阶段。
11. 观察稳定窗口并关闭 Change。
12. 更新 Release、Runbook、Known Issue 和 Debt。

### 7.2 Pre-Deployment Verification

- Artifact 与源/测试证据一致；
- Environment/Region/Account 明确；
- Config Diff 与 Secret Reference 已 Review；
- Database Backup/PITR 状态符合风险要求；
- Queue/Worker Drain 和版本兼容准备完成；
- On-Call、Incident Channel 和 Rollback Owner 可用；
- 用户支持和维护通知就绪。

### 7.3 Deployment Verification

验证分层：

| Layer | Verification |
|---|---|
| Infrastructure | Instance、Network、Secret、Dependency、Readiness |
| API | Auth、Error、Idempotency、常规 Query/Command |
| Domain | 已批准 Synthetic Calculation、版本和边界结果 |
| Async | Broker、Worker、Operation、Retry、DLQ |
| AI/Report | 去标识化、Validation、冻结与降级 |
| Data Rights | Export/Delete 状态，不执行真实用户测试 |
| Observability | Log、Metric、Trace、Alert 和 Correlation |
| Security | WAF/Rate Limit、权限拒绝、Secret 不泄漏 |

### 7.4 Post-Deployment Observation

观察窗口按风险设定，监控新旧版本对比、Error Code、Latency、Domain Quality、Queue Age、Provider Cost、Privacy/Audit 和用户旅程。无异常证据才能扩大流量或关闭 Change。

### 7.5 Failure During Deployment

立即暂停扩流，保护证据，确认数据/Schema/Message 兼容；由 Release Owner 决定 Rollback、Forward-Fix、Flag Off 或能力降级。不得边调查边继续全量发布。

---

## 8. Rollout Strategy

### 8.1 Selection Principle

不规定所有发布统一使用一种方式。按变更风险、可逆性、兼容窗口、状态、容量、成本和观察信号选择。

### 8.2 Strategy Matrix

| Strategy | Suitable For | Advantages | Risks / Preconditions |
|---|---|---|---|
| Rolling | 兼容、低至中风险、无状态 Web/API/Worker | 成本较低、持续可用 | 新旧版本必须兼容；观察粒度有限 |
| Canary | 高风险、可按流量/租户隔离、指标明确 | 限制 Blast Radius、可比较 | 需要可靠路由、样本和快速停止 |
| Blue-Green | 需要快速流量切换、环境可并行 | 回切清晰、环境验证充分 | 成本较高；共享数据库仍需兼容 |
| Feature Flag | 用户能力渐进开放、降级开关 | 与制品部署解耦 | Flag 不能修复 Schema 不兼容或绕过安全 |

### 8.3 Rolling Deployment

- 控制最大不可用/额外实例，确保容量。
- 新实例通过 Startup/Readiness 才接流量。
- 旧实例 Graceful Drain 后停止。
- Worker Consumer 版本混跑必须支持 Message Contract。
- Migration Contract 阶段在旧实例退出并验证后执行。

### 8.4 Canary Deployment

Canary 按内部用户、匿名试算、低风险 Tenant/流量或区域逐步开放，但不得使用敏感属性或命理结果选择样本。比较技术、业务、领域质量、安全和成本指标。

### 8.5 Blue-Green Deployment

Green 使用 Production-equivalent Config 和安全 Synthetic 验证。切换前确认 Database/Message/Object 共享状态兼容。Blue 保留期限有限，不能长期成为第二个漂移生产环境。

### 8.6 Feature Flags

- Flag 有 Owner、Scope、到期、回退和清理计划。
- Server 端执行安全和授权；前端隐藏不是关闭能力。
- Business Version、Consent、Risk 和 Immutable Rules 不可被 Flag 绕过。
- Flag 变化属于 Change，需记录和观察。

### 8.7 Rollout Stop Conditions

候选停止条件包括：Error/Latency 显著回归、Calculation/Evidence/Audit 质量异常、Queue Age 增长、权限/隐私事件、AI 成本异常、Crash/Resource Saturation 或 Synthetic 失败。具体阈值需在 Release Plan 中批准。

---

## 9. Rollback and Forward-Fix Strategy

### 9.1 Decision Criteria

| Prefer Rollback | Prefer Forward-Fix |
|---|---|
| Artifact 可安全回退、Schema 向后兼容 | 数据已按新语义写入且旧版本不兼容 |
| 问题明确由新代码引起 | 修复很小、可快速验证、回退风险更大 |
| 回退时间短于修复 | 安全漏洞要求保留新防护 |
| 没有不可逆外部副作用 | Migration 已越过不可回退阶段 |

### 9.2 Rollback Rules

- 回退前验证 Schema、Message、Cache、Config 和业务版本兼容。
- 使用已批准 Immutable Artifact，不临时重建旧制品。
- 不回滚 Domain Event、Frozen Report、Audit 或已发生用户决定。
- 回退应用不自动回滚数据库数据。
- Rollback 后重新执行 Synthetic、业务/领域质量和安全验证。

### 9.3 Forward-Fix Rules

Forward-Fix 保持最小范围、快速 Review、专项测试和渐进发布。不得在压力下扩大重构范围。修复后补齐正常测试、文档和 Problem Action。

### 9.4 Feature Disablement

可通过 Approved Flag 或 Route/Queue 停止受影响新流量，同时保留已完成历史。关闭 AI 不影响确定性排盘；关闭 Search 不允许虚构引用；关闭 Object 生成不公开临时制品。

### 9.5 Data Correction

禁止直接生产数据库编辑。数据修复通过受控、可审计、幂等的 Application Use Case 或批准的 Migration/Repair Process，先备份、Dry Run、限定范围并验证不可变历史影响。

### 9.6 Post-Rollback

Rollback 触发 Change/Incident Review，记录触发、决策、恢复时间、遗留数据、重新发布条件和纠正行动。不得立即以相同方案重发。

---

## 10. Database Migration Operations

### 10.1 Expand–Migrate–Contract

| Phase | Purpose | Operational Gate |
|---|---|---|
| Expand | 增加向后兼容结构/能力 | 旧应用仍可运行；锁风险可接受 |
| Migrate | 分批转换/回填并验证 | 可暂停、可重试、可观察、有限负载 |
| Contract | 删除旧结构或兼容路径 | 旧版本完全退出、使用量为零、备份与回退评估完成 |

### 10.2 Migration Change Record

记录 Schema/Data 影响、预计行/对象量、锁、I/O、持续时间、Batch、Throttle、Checkpoint、Validation、Backup、Rollback/Forward-Fix 和 Owner。

### 10.3 Pre-Migration

- 在生产规模近似数据上演练；
- 验证 Backup/PITR 和恢复路径；
- 检查长事务、复制延迟、磁盘与连接预算；
- 确认应用兼容窗口；
- 定义暂停/终止条件；
- 准备 Dashboard、Alert 和 On-Call。

### 10.4 Online Migration

长回填使用分批、限速、Checkpoint 和幂等，避免单大事务。不得让 Migration 脚本绕过 Domain 语义改变正式状态；业务语义修复走受控 Use Case。

### 10.5 Validation

验证记录数、唯一/引用/版本、不变量、Sample Hash、Query、性能、不可变历史、Audit 和对象引用。只验证“Migration 成功退出”不足以完成变更。

### 10.6 Contract Phase

Contract 前证明旧代码、旧 Message、旧 API 和旧 Query 不再使用结构，经过观察窗口和审批。破坏性删除不与首次代码发布同一时点执行。

### 10.7 Migration Failure

停止 Batch、保护 Checkpoint、评估数据状态和应用兼容。无法安全回退时保持 Expand 状态并 Forward-Fix；不得在未知状态继续 Contract。

---

## 11. Configuration and Secret Operations

### 11.1 Configuration Change

- 所有生产 Config 有版本、Owner、环境、验证、批准和回退。
- 配置 Diff 在不暴露 Secret 的前提下可审查。
- 启动/动态配置先验证完整性和范围，再生效。
- 部分传播失败保持最后已验证版本或关闭能力。
- Business Version Config 继续走独立 Governance。

### 11.2 Drift Detection

持续比较声明基线与运行状态。发现 Drift 先判定是否 Emergency Change；未经批准的手工修改必须收敛、审计和复盘。

### 11.3 Secret Lifecycle

| Stage | Required Operations |
|---|---|
| Create | 最小用途、环境、Owner、到期和审计 |
| Distribute | Workload Identity 获取，不人工复制 |
| Rotate | 受控重叠、健康验证、旧 Secret 撤销 |
| Revoke | 快速传播、依赖确认、Incident 关联 |
| Recover | KMS/Secret 平台批准流程，不导出明文 |
| Retire | 删除访问和引用，保留安全 Audit |

### 11.4 Secret Incident

疑似泄漏立即撤销/轮换、限制访问、保存证据、评估调用/数据影响并启动 Security Incident。删除 Git 历史中的值不能替代 Credential 撤销。

### 11.5 Feature Flag Operations

Flag 列表、Owner、状态、环境、目标范围、创建/到期、依赖和清理可查询。Emergency Flag Change 仍需双人/审计和事后 Review。

---

## 12. Production Access Control

### 12.1 Default Deny and Least Privilege

生产 Console、Database、Redis、Broker、Object、Logs、Traces、Secrets、CI/CD 和 Audit 默认不可访问。权限按 Role、Purpose、Environment、Resource 和时间最小授予。

### 12.2 Strong Authentication

- 高权限访问使用强认证与 MFA。
- 禁止共享账户和共享个人 Credential。
- Workload 使用独立机器身份，不冒充人员。
- 离职、角色变化和 Incident 后及时撤销。

### 12.3 Just-in-Time and Time-Limited Access

常规生产访问通过 JIT 请求，说明工单/Incident、Purpose、范围、期限和审批。到期自动撤销；延长需重新批准。

### 12.4 Break-Glass

- 仅用于重大 Incident 或常规 IAM 不可用。
- 强认证、最小范围、短时、实时告警。
- 访问会话记录或使用等价不可抵赖 Audit。
- 使用后立即轮换/封存 Credential 并事后复核。
- Break-Glass 不得成为永久 On-Call 权限。

### 12.5 Session Recording / Equivalent Audit

对高风险 Console、Database、Secret 和生产调试记录 Actor、时间、目标、命令/操作摘要和结果。Recording 本身须受敏感数据保护，不作为大规模收集业务正文的理由。

### 12.6 No Direct Database Modification

人员不得直接修改生产业务表。只读调查也使用受控账户、Purpose、字段遮蔽、时间限制和 Audit。紧急数据修复走 Approved Repair/Migration Process。

### 12.7 Emergency Access

Emergency Access 关联 Incident、双人确认、限定目标和实时 Operations Lead 监督。结束后撤销、对账、检查数据变化并更新 Timeline。

### 12.8 Access Review

定期审查人员、Service Account、CI/CD、Vendor 和 Break-Glass 权限，删除无 Owner、未使用或超范围授权。频率属于 Security Open Question。

---

## 13. Observability Operations

### 13.1 Signals

Observability 包含 Logs、Metrics、Traces、Dashboards、Synthetic、Business Metrics、Domain Quality、Security、Privacy 和 Cost。各信号通过 RequestId、CorrelationId、TraceId、OperationId 和安全 Resource Reference 关联。

### 13.2 Source of Truth Boundary

监控系统不是业务 Source of Truth：

- Dashboard 的 Completed 不改变 Aggregate 状态；
- 缺失 Metric 不证明业务未发生；
- Log 不替代 AuditEvent；
- Trace 不替代 Domain Event；
- Alert Acknowledged 不等于 Incident Resolved。

### 13.3 Data Prohibition

Observability 不记录完整出生资料、详细地点、会话正文、Prompt、AI 原始输入/输出、报告全文、Credential 或签名 URL。使用安全 Identity、分类、长度、Hash 或统计值。

### 13.4 Dashboard Portfolio

| Dashboard | Audience | Focus |
|---|---|---|
| Executive / Product Reliability | Product/CTO | 用户旅程、SLO、风险、成本 |
| API / Web | Engineering/On-Call | Availability、Latency、Error、Rate Limit |
| Calculation / Domain Quality | Domain/Engineering | 验证、差异、版本、黄金失败 |
| AI / Evidence / Report | AI/Content/On-Call | Queue、Validation、Citation、Risk、Cost |
| Data Platform | DBA/Platform | PostgreSQL、Redis、Broker、Object、Search |
| Security / Privacy | Security/Privacy | Auth、Access、Export/Delete、Audit |
| Deployment | Release Owner | Version、Rollout、Change、Regression |
| DR / Backup | Operations | Backup、PITR、Restore Drill、Tombstone |

### 13.5 Operational Use

每个 Dashboard 有 Owner、Purpose、数据源、Freshness、访问级别、Runbook 和 Review 日期。无 Owner Dashboard 不作为 Release/Incident 决策依据。

### 13.6 Data Quality of Observability

监控 Pipeline 自身有健康、延迟、丢失、采样和成本指标。信号缺失明确显示 `Unknown/No Data`，不能默认为 Healthy。

---

## 14. Logging Operations

### 14.1 Log Classes

Access、Application、Worker、Security、Audit 和 Dependency Log 分开治理。普通 Log 与 Audit 的保留、访问和防篡改不同。

### 14.2 Ingestion and Aggregation

- 结构化日志集中聚合并按 Environment/Module/Sensitivity 隔离。
- 采集失败有 Buffer/Drop Policy、Metric 和告警。
- 高风险 Audit 不依赖普通日志采集作为唯一保证。
- 日志时间源、Release 和 Correlation 字段一致。

### 14.3 Redaction Operations

Redaction 在产生端执行，聚合端进行二次检测。定期扫描禁记字段和异常高基数字段。发现敏感泄漏立即限制访问、停止继续采集、启动 Privacy/Security Incident 并按法律要求处置既有日志。

### 14.4 Retention and Access

不同 Log Class 采用可配置保留。具体期限是法律、安全、隐私和成本 Open Question。查询生产日志需最小权限；批量导出和长时间范围查询需要更强审批。

### 14.5 Log Levels

- Error：需要调查的系统/依赖失败；
- Warning：降级、接近阈值或可恢复异常；
- Info：关键生命周期与结果摘要；
- Debug：默认不在生产长期开启，且仍遵守禁记规则。

业务拒绝不自动作为 Error；Critical 安全/数据事件不依赖 Log Level 单独定义。

### 14.6 Operational Queries

本文不生成查询。正式查询模板应按 Incident/Runbook 管理，使用 Route Template、Error Code、Release、Correlation、Operation 和安全 Resource Reference，不搜索敏感正文。

---

## 15. Metrics Operations

### 15.1 Metric Families

| Family | Examples |
|---|---|
| Technical | CPU、Memory、Connection、Latency、Error、Saturation |
| Business | 首次排盘完成、三分钟完成、报告到达、对话使用 |
| Domain Quality | Calculation Validation、Golden Difference、Rule Conflict、Citation Validity |
| Security | Auth Failure、IDOR、WAF、Rate Limit、JIT/Break-Glass |
| Privacy | Consent Revocation、Export/Delete、Partial、Retention Backlog |
| Cost | AI Token/有效输出、Storage、Database、Egress、Trace |

### 15.2 Metric Naming and Labels

名称稳定、单位明确、Counter/Gauge/Histogram 语义一致。Label 禁止 UserId、Birth Data、Conversation、Prompt、Report Text、RequestId 等高基数/敏感值。Release、Environment、Module、Result、Error Family 和 Version 使用受控值。

### 15.3 Cardinality Management

Metric 新增必须评估 Label Cardinality 与成本。个体调查使用受限 Log/Trace/Audit，不把每个用户或 Resource 变成 Time Series。

### 15.4 Recording Rules and Aggregation

长期 Dashboard/SLO 使用可验证的聚合语义。任何聚合变更需验证窗口连续性；不能在 Incident 中修改计算方式使 SLO 看起来恢复。

### 15.5 Metric Retention

高分辨率短期、聚合长期的方向由成本和调查需求决定。SLO/Release 证据保留足以支持趋势和复盘，具体期限待确认。

---

## 16. Distributed Tracing Operations

### 16.1 Trace Scope

Trace 覆盖 Edge、Web、API、Application、Repository、Broker、Worker、External Adapter、Search 和 Object Storage。Async Producer/Consumer 通过 Context/Link 关联，不伪造同步调用。

### 16.2 Trace Identifiers

RequestId、CorrelationId、TraceId、CausationId、IdempotencyKey 和 Domain Identity 分离。外部 Trace Context 经验证，不承载授权。

### 16.3 Sampling

采样按 Environment、Error、Latency、Risk 和 Cost。Error/High-Latency 可提高采样，但仍先 Redact。Audit 与 Security Detection 不依赖普通 Trace Sample。

### 16.4 Sensitive Attributes

禁止 Span 记录完整 Request/Response、BirthInput、Conversation、Prompt、AI Raw Output、Report、Token 或 Object Signed URL。Provider Request ID 使用安全映射。

### 16.5 Trace Operations

On-Call 通过 Correlation/Operation 定位跨 API、Queue 和 Worker 流程。Trace 后端不可用不自动阻断低风险服务，但触发 Observability Degraded；高风险发布可因此暂停。

### 16.6 Retention and Access

Trace 默认短于 Audit；具体期限待评审。生产 Trace 访问使用 JIT/Purpose 并审计，禁止无工单批量浏览。

---

## 17. Health Checks and Synthetic Monitoring

### 17.1 Health Types

| Check | Purpose | Operational Action |
|---|---|---|
| Startup | Config、Secret、Schema、Client 初始化 | 失败不接流量 |
| Liveness | 进程能否继续 | 必要时重启实例 |
| Readiness | 实例能否安全服务 | 从流量/消费池移除 |
| Dependency | 外部能力状态 | 降级、Circuit、告警 |
| Synthetic | 用户/领域路径是否工作 | SLO/Release/Incident 信号 |

### 17.2 Dependency Semantics

PostgreSQL Primary 不可用影响正式写与多数 Readiness；Redis、AI、Search、Object 等按降级矩阵处理，不把可选依赖失败全部绑定 Liveness，避免重启风暴。

### 17.3 Synthetic Coverage

- 第一方页面与 API 基础可达；
- 认证成功/拒绝；
- 使用合成输入的确定性 Calculation 与锁定 Version；
- 已知 Frozen Report 读取；
- Broker/Worker 受理和完成；
- AI/Provider 使用批准 Sandbox 或不产生正式内容的健康路径；
- 权限越界拒绝；
- Object 下载授权；
- Audit 写入验证（不产生敏感正文）。

### 17.4 Synthetic Data

使用显式标记的合成 Subject/Resource，排除业务成功指标、研究和真实用户通知。定期清理且不触发真实 Webhook、邮件或成本不可控 AI 调用。

### 17.5 No-Data Handling

Health/Synthetic 缺少结果显示 Unknown，不显示 Green。连续 No Data 作为监控链故障告警。

---

## 18. SLI Definition

### 18.1 SLI Principles

- SLI 有明确用户、事件、Good/Valid/Total 定义、数据源、窗口和排除项。
- 排除项在事故前批准，不事后调整。
- 每个 SLI 有 Owner、Dashboard、Alert 与验证测试。
- 技术成功不自动等于领域有效，例如 AI HTTP 200 不等于 Valid Result。

### 18.2 Candidate SLI Catalog

| SLI | Good Event / Measurement | Valid Population | Primary Source |
|---|---|---|---|
| API Availability | 有效请求返回非平台 5xx/超时，并符合契约 | 允许的 First-Party/API 请求 | Edge + API Metrics |
| API Latency | 请求在阈值内完成 | 按 Route Class 的成功有效请求 | API Histogram |
| Deterministic Calculation Success Rate | 使用 Published Version 完成 Valid Snapshot 或明确业务拒绝不计失败 | 合法且获授权的 Calculation | Application/Domain Metrics |
| Calculation Latency | 从可靠受理到 Valid/明确终态的时间 | 成功有效 Calculation | Operation/Domain Time |
| AI Valid Result Rate | 通过结构、事实、引用、冲突和风险检查 | 进入正式生成且依赖可用的 Analysis | AI Validation Metrics |
| AI First Valid Response Time | 受理到首个通过验证的可展示内容 | 成功 AI Request | Operation + AI Metrics |
| Report Generation Success Rate | 生成、验证并 Frozen | 输入完整、获授权的 Report Intent | Report Domain/Application |
| Queue Oldest Message Age | 各 Queue 最老可处理消息年龄 | Ready/Retryable Message | Broker Metrics |
| Data Export Completion | 在批准期限内 Completed，且无遗漏来源 | 有效已核验 Export Request | Data Rights Process |
| User Deletion Completion | 各 Context 完成/合法 Hold 明确，用户状态正确 | 有效已核验 Deletion Request | Deletion Saga + Audit |
| Backup Success | 备份完成、完整性可验证 | 计划 Backup | Backup System |
| Restore Verification | Restore 后通过数据、版本、对象、Audit、Tombstone 验证 | 计划 Drill/Recovery | DR Checklist Evidence |
| Audit Write Success | 必需 Audit 与业务/管理动作可靠关联 | 所有需审计动作 | Audit Pipeline + Application |

### 18.3 Valid Request Exclusions

明确的客户端 Validation、Authentication/Authorization 拒绝、Consent 拒绝和 Rate Limit 是否计入特定 SLI，按 SLI 契约预先定义。不能用大量业务拒绝提高 Availability。

### 18.4 Domain Quality SLIs

除可用性外，持续观察黄金差异、Critical VerificationBlocked、Rule/Evidence 完整性、Citation Validity、AI Fact Failure 和 Frozen Report 可复现。它们可以作为 Release Gate，即使不全部折算为 Availability SLO。

### 18.5 Privacy and Audit SLIs

Export、Deletion、Consent Propagation 和 Audit Write 以权威 Saga/Audit 数据计算，不以客服关闭工单或 Dashboard 手工标记为完成。

---

## 19. SLO Definition

### 19.1 Status of SLO Values

上游已批准部分性能压测基线，但未批准完整正式 SLO。本文所有未被上游明确批准的比例、窗口、RPO/RTO 均标记为 `Candidate` 或 `Open Question`，不得作为市场承诺。

### 19.2 Candidate SLO Catalog

| SLI | Candidate Objective | Status / Note |
|---|---|---|
| API Availability | 数值与窗口待确认 | Candidate；区分 First-Party/Developer/Governance |
| Common API Latency | P95 ≤ 500 ms | Approved 性能测试基线，不等于正式 SLO |
| Deterministic Calculation Success Rate | 比例待确认 | Candidate；业务拒绝/歧义单独分类 |
| Calculation Latency | P95 ≤ 2 s | Approved 性能测试基线，不等于正式 SLO |
| AI Valid Result Rate | 比例待模型/评估基线确认 | Candidate；不能只看供应商成功 |
| AI First Valid Response Time | P95 目标 ≤ 15 s | Approved 性能目标基线，不等于正式 SLO |
| Complete AI Report Time | P95 目标 ≤ 60 s | Approved 性能目标基线，不等于正式 SLO |
| Report Generation Success Rate | 比例与窗口待确认 | Candidate |
| Queue Oldest Message Age | 按 Queue Class 分阈值 | Candidate；AI、Deletion 不同 |
| Data Export Completion | 法律/产品期限待确认 | Open Question |
| User Deletion Completion | 法律/Legal Hold 语义待确认 | Open Question |
| Backup Success | 比例与连续失败门禁待确认 | Candidate |
| Restore Verification | 演练频率和成功标准待确认 | Candidate |
| Audit Write Success | Candidate 100% 必需动作可靠记录 | 数值/窗口待批准；任何静默丢失为高风险 |

### 19.3 SLO Segmentation

按 Surface、User Journey、Region、Release、Operation Type 和 Dependency 分析，但不为小样本或高敏感属性创建不稳定 SLO。AI 不可用与确定性排盘不可用分开。

### 19.4 SLO Approval

正式 SLO 需 Product、Engineering、Operations、Security/Privacy 和 Cost Owner 批准，具备至少一个观测基线窗口、明确排除项、用户影响和支持能力。

### 19.5 SLO Review

每个 Milestone、容量变化、重大供应商变化和 Incident 后复审。调整 SLO 不用于掩盖长期不达标，需 ADR/治理记录。

---

## 20. Error Budget Policy

### 20.1 Calculation

对于可用性比例 SLO，在批准滚动窗口内：允许失败量 = 有效事件总量 × (1 − SLO 目标)。基于时间的 SLO 使用窗口分钟数计算。Latency SLO 的 Budget 是超过目标阈值的有效事件比例。

具体窗口（例如 28/30 天）尚未批准，属于 Open Question。

### 20.2 Consumption

平台错误、超时、超过 Latency 目标、未按承诺完成的有效 Operation 消耗相应 Budget。排除项与计划维护是否计入，必须在 SLO 定义时预先确认。

### 20.3 Burn Rate

使用短窗口和长窗口 Burn Rate 检测快速与持续消耗。具体倍率和告警阈值待 SLO Baseline 后确认，不在本文擅自设定。

### 20.4 Budget States

| State | Meaning | Default Action |
|---|---|---|
| Healthy | 消耗符合计划 | 正常 Change Governance |
| At Risk | 持续消耗或预测超预算 | 降低高风险发布、增加 Reliability Work |
| Exhausted | 已超批准 Budget | 暂停非必要高风险发布，优先恢复与修复 |
| Exceptional | Security/Privacy/Data Correctness/Audit 事故 | 不用普通 Budget 抵消，立即专项处置 |

### 20.5 Release Policy

Error Budget Exhausted 时暂停可能扩大影响的功能、依赖升级和高风险迁移；允许安全修复、可靠性修复、范围移除和经批准的 Emergency Change。

### 20.6 Non-Budgetable Events

以下不能以“仍有 Budget”为由接受：重大安全/隐私泄漏、确定性事实系统性错误、Frozen 历史被改写、用户删除数据复活、未授权访问、Critical Audit 静默丢失和法律违规。

### 20.7 Governance

Budget 计算、排除、手工调整和例外全部审计。Product 不能单方面借 Budget 放宽安全；Operations 也不能用 SLO 阻止必要合规修复。

---

## 21. Alerting Strategy

### 21.1 Alert Principles

- Alert 必须可行动、有 Owner、有 Runbook、有严重度和用户/数据影响。
- Page 针对需要立即人工行动的症状，不针对每个单次错误。
- Ticket 针对趋势、容量、债务和非紧急问题。
- Dashboard 用于探索，不替代 Alert。
- No Data 与 Healthy 分离。

### 21.2 Alert Sources

| Category | Candidate Alerts |
|---|---|
| SLO | 快速/持续 Burn、Availability/Latency 回归 |
| Domain Quality | Critical Calculation Difference、Evidence/Citation 异常 |
| Async | Queue Age、DLQ、Stuck Operation、Worker Saturation |
| Data | PostgreSQL Failover、Disk、Lock、Backup/Restore Failure |
| Security | Auth Abuse、IDOR、Secret Access、Break-Glass |
| Privacy | Export/Delete 逾期、Partial、Tombstone/Reindex Failure |
| Audit | 必需写入失败、Pipeline Lag、不可变保护异常 |
| Cost | AI/Storage/Egress 异常增长、Quota 接近 |
| Observability | Log/Metric/Trace Pipeline 丢失或 No Data |

### 21.3 Alert Quality

监控 Precision、Actionability、Duplicate、Time-to-Acknowledge 和 False Positive。频繁静音、无 Owner 或无行动的 Alert 必须修复或退役。

### 21.4 Routing

按 Service/Context、Severity、Environment、Business Hours 和 Security/Privacy 分类路由。跨域 Incident 由 Incident Commander 统一协调，避免多人重复操作。

### 21.5 Suppression

Maintenance/Incident 期间可受控 Suppress 重复 Alert，但保留原始信号和关键 Security/Privacy Alert。Suppress 有 Owner、范围和自动到期。

### 21.6 Alert Changes

Alert Rule 变化走 Change Review、Staging/Replay 验证和 Owner 批准。本文不生成任何规则配置。

---

## 22. Incident Management

### 22.1 Incident Lifecycle

Detect → Triage → Declare → Assign Roles → Contain/Mitigate → Recover → Validate → Communicate → Close → Post-Incident Review → Corrective Actions。

### 22.2 Core Roles

| Role | Responsibility | Must Not Do |
|---|---|---|
| Incident Commander | 设 Severity、目标、优先级、决策和角色协调 | 同时深陷所有技术操作 |
| Operations Lead | 执行诊断、缓解、恢复和变更协调 | 未经 IC 同时开展冲突操作 |
| Communications Lead | 内外状态、支持、时间线和 Stakeholder | 推测原因或泄露敏感信息 |
| Security / Privacy Lead | 评估泄漏、访问、法律/通知和证据保护 | 未评估就宣布无数据影响 |
| Domain/Data Lead | 验证事实、版本、删除、Audit 和数据完整性 | 用监控状态替代业务验证 |
| Scribe / Timeline Owner | 记录时间、行动、决定、证据和结果 | 事后凭记忆重建全部事实 |

### 22.3 Detection and Declaration

任何人员或自动系统可提出 Incident。达到 Severity 条件立即声明，不因原因未知或担心指标而延迟。安全/隐私疑似事件按较高等级保守处理。

### 22.4 Mitigation

优先限制 Blast Radius：停止发布、Flag Off、Circuit Open、限流、Queue Pause、撤销 Credential、隔离环境或切换已验证能力。缓解不得破坏证据或不可变历史。

### 22.5 Recovery Validation

恢复不仅看组件 Up，还验证用户旅程、Domain Quality、Queue、Audit、Data Rights、Security、Cost 和 Synthetic。Partial 未清理时不能宣布完全恢复。

### 22.6 Communications

按 Severity 和批准频率更新：已知影响、正在采取的行动、下一次更新时间和用户可用替代。未确认 Root Cause 不公开推测。命理内容事件不使用科学准确率表述。

### 22.7 Closure

满足影响停止、服务验证、数据/安全状态明确、短期监控就绪、遗留任务有 Owner 后关闭。关闭 Incident 不等于所有 Corrective Action 完成。

### 22.8 Post-Incident Review

重大 Incident 进行无责但有责任的 Review：影响、Timeline、Detection、Contributing Factors、决策、有效/无效响应、用户沟通、Corrective Actions 和验证。

---

## 23. Incident Severity Levels

### 23.1 Severity Model

| Severity | Definition | Examples | Response Expectation |
|---|---|---|---|
| SEV-1 | 广泛或关键业务中断；重大安全/隐私/数据正确性；恢复能力失效 | 大范围无法排盘/登录、系统性错误命盘、敏感数据泄漏、删除数据复活、Critical Audit 丢失 | 立即全天候响应、IC 与全角色、持续沟通 |
| SEV-2 | 重要能力严重降级或特定大群体受影响，有替代但影响显著 | AI/Report 大范围失败、Queue 严重积压、Data Export/Delete 大量逾期、单区域故障 | 快速响应、明确 IC、定期沟通 |
| SEV-3 | 有限用户/单功能影响，稳定绕过或无数据风险 | 单一 Provider 部分错误、特定 Report 类型失败、非关键 Dashboard 缺失 | 工作时段优先处理或按值班策略 |
| SEV-4 | 轻微缺陷、可观察问题或无即时用户影响 | 文档/低优先级告警、趋势性容量、非关键工具失败 | 进入正常 Backlog/Problem Management |

### 23.2 Severity Modifiers

安全/隐私、未成年人/高风险内容、不可逆数据、跨境、Frozen 历史、删除/Audit 和媒体/法律影响可提升等级。影响人数少不自动降低敏感数据事件等级。

### 23.3 Severity Changes

IC 可随证据升级/降级，记录时间与理由。降级不删除早期影响或停止必要法律评估。

### 23.4 Response Targets

具体 Acknowledge、Role Assignment、Communication 和 Mitigation 时间尚未批准，属于 Open Question；上线前必须量化并与 On-Call 能力匹配。

---

## 24. On-Call and Escalation

### 24.1 On-Call Coverage

On-Call 模型根据正式 SLO、用户时区、团队规模和供应商支持确定。未批准前不擅自承诺 24×7；GA 前必须明确哪些 Severity 需要全天候响应。

### 24.2 Rotation

- 主值班与备份值班；
- 公平轮换和最大负担；
- 交接当前 Incident、Change、Risk、Maintenance 和供应商问题；
- 值班人员具备 Runbook、权限申请和升级渠道；
- 值班不等于永久生产权限。

### 24.3 Escalation Paths

按 Service/Context、Database、Security/Privacy、Domain/Calculation、AI/Vendor、Data Rights 和 Executive/Legal 设升级路径。联系信息由受控系统维护，不写入公开文档。

### 24.4 Handoff

交接包含 Incident Timeline、当前假设、已做操作、下一动作、风险、Access/Change 和 Communication。口头交接需同步到 Incident Record。

### 24.5 On-Call Safety

避免单人高风险操作；疲劳时主动升级。SEV-1/2 使用明确 IC 与双人关键操作。事后评估值班负担、Alert Noise 和培训缺口。

### 24.6 Vendor Escalation

维护 AI、Database、Object、Network、Identity 等供应商支持等级、Case 路径和合同响应。供应商 Case 不替代平台 Incident 管理。

---

## 25. Runbook Standards

### 25.1 Required Content

每份 Runbook 包含：Purpose、Scope、Owner、Prerequisites、Safety、Detection、Diagnosis、Decision Tree、Mitigation、Recovery、Verification、Rollback、Escalation、Communication、Audit 和 Last Drill Date。

### 25.2 Runbook Principles

- 步骤可由非作者值班人员理解。
- 所有高风险操作标明审批与双人要求。
- 不包含明文 Secret、真实用户数据或永久访问路径。
- 不用“直接改数据库”作为标准修复。
- 指向权威 Dashboard/Tool，不复制易漂移内容。
- 有停止条件，避免无限排查或重试。

### 25.3 Minimum Runbook Set

- API/Web Availability；
- PostgreSQL Failover/Connection/Lock/Storage；
- Redis Down/Eviction；
- Queue Backlog/DLQ/Poison Message；
- Worker Saturation/Stuck Operation；
- AI/Location/Object/Vendor Outage；
- Calculation Critical Difference；
- Audit Write Failure；
- Data Export/Delete Partial；
- Secret Leak/Rotation；
- Backup/Restore/PITR；
- Deployment Rollback/Forward-Fix；
- Observability Pipeline Failure。

### 25.4 Validation and Drills

Runbook 在 Staging/DR Sandbox 定期演练，记录耗时、权限、缺失步骤和改进。未演练的 Runbook 标为 `Unverified`，不能作为唯一 GA 保障。

### 25.5 Ownership

Runbook 有主 Owner、备份 Owner 和 Review 日期。无 Owner、过期或链接失效的 Runbook 触发 Operational Readiness 缺陷。

---

## 26. Problem Management

### 26.1 Incident vs Problem

Incident 目标是恢复服务；Problem Management 目标是理解根因、消除重复和改善系统。无用户可见 Incident 的趋势也可创建 Problem。

### 26.2 Problem Sources

重复 Incident、SLO Burn、Alert Noise、Capacity Trend、Security Finding、Restore Failure、Manual Workaround、Vendor Instability、Flaky Operation 和 Architecture Drift。

### 26.3 Root Cause Analysis

分析系统与过程因素：设计、测试、发布、监控、权限、文档、培训、供应商和组织，不停留在“操作失误”。避免无证据单一根因。

### 26.4 Corrective Actions

每项 Action 有类型（Prevent/Detect/Mitigate/Recover）、Owner、优先级、期限、验证与关联 Incident/ADR。只写“加强监控/注意”不算完成。

### 26.5 Known Error

无法立即修复的问题记录影响、触发、Workaround、Risk、Owner、Sunset 和用户/支持说明。Workaround 不得违反安全或不可变规则。

### 26.6 Trend Review

定期审查重复模式、MTTD/MTTR、Change Failure、Alert Quality、Vendor、Capacity、Cost 和 Corrective Action Aging。

---

## 27. Backup Operations

### 27.1 Backup Scope

| Asset | Protection |
|---|---|
| PostgreSQL | 定期/连续 Backup、PITR、加密、独立权限 |
| Object Storage | Version/Lifecycle、Integrity Manifest、Legal Hold 协调 |
| Configuration | 版本化、环境映射、恢复验证 |
| Secret/KMS | 平台级恢复与 Key 可用性，不导出明文 |
| Audit | 独立保护、防篡改、保留与恢复验证 |
| Broker | 按产品能力保护；正式 Operation 状态仍在 Source of Truth |
| Search/Projection | 以可重建为主，保留 Source/Version |
| Redis | 不依赖备份恢复正式业务真相 |

### 27.2 PostgreSQL Backup

- Backup 计划与 PITR 覆盖满足待批准 RPO。
- 加密并与生产运行凭据隔离。
- 监控完成、大小、持续时间、连续性和可恢复性。
- 定期验证 Catalog、Checksum/Integrity 和实际 Restore。
- Backup Failure 按连续失败与恢复风险告警。

### 27.3 Object Storage Protection

保护 PDF、Export、附件和 Frozen Artifact 的 Version、Hash、Owner、Retention 与 Legal Hold。对象版本保护不能无限阻止合法删除；删除策略与备份到期协调。

### 27.4 Configuration Backup

保存声明配置、版本、环境映射和发布历史，不含明文 Secret。恢复后重新验证 Secret Reference 与当前环境。

### 27.5 Secret/KMS Recovery

验证 KMS/Secret 平台故障、Key Rotation、Credential Reissue 和 Break-Glass 流程。Key Backup/Recovery 权限与应用访问分离。

### 27.6 Audit Protection

Audit Backup 保持追加历史、访问限制和完整性证据。恢复不能让普通管理员获得修改能力。

### 27.7 Backup Retention

保留周期与数据类别、法律、Legal Hold、成本和删除权协调；具体期限待确认，不在代码中硬编码。

### 27.8 Backup Monitoring

成功状态、最后成功时间、覆盖范围、容量、加密、到期删除和 Restore Drill 统一可见。只有 Backup Job “Succeeded”不等于保护有效。

---

## 28. Restore Operations

### 28.1 Restore Triggers

灾难恢复、误删除/损坏调查、PITR、定期演练和法律/审计验证。Restore 不直接回写 Production，先进入 DR/Restore Sandbox。

### 28.2 Restore Workflow

1. 声明目的、时间点、范围、Owner 和权限。
2. 创建隔离 Sandbox，禁用外部通知/Callback。
3. 恢复 PostgreSQL、Object Metadata、Config 和必要 Audit。
4. 验证 Integrity、Identity、Version、Reference 和 Frozen History。
5. 重放删除墓碑、Consent Revocation、Retention 和 Legal Hold。
6. 重建 Search、Vector、Cache 和 Read Projection。
7. 执行 Domain、Security、Privacy、Data Rights 和 Synthetic 验证。
8. 记录实际 RPO/RTO、差异和决定。
9. 按批准方案恢复 Production 或结束演练。
10. 安全销毁 Sandbox。

### 28.3 Restore Validation

| Area | Validation |
|---|---|
| Domain | Calculation Snapshot、Version、Rule/Evidence 链 |
| Report | Frozen 内容、Manifest、Object Hash |
| Identity/Consent | 当前授权、撤回和资源归属 |
| Data Rights | Deleted/Partial/Hold 状态和墓碑 |
| Audit | 关键行为、顺序、完整性和只读权限 |
| Operations | Queue/Projection 重建、Config、Secret Reference |
| Security | 网络隔离、Credential、无外部副作用 |

### 28.4 Point-in-Time Recovery

PITR 选择时间点前评估跨系统一致性：数据库恢复时点与对象、Broker、外部 Event 的差异。恢复后依靠权威状态、幂等和重放策略收敛，不盲目重发全部消息。

### 28.5 Deleted Data Resurrection Prevention

Restore 必须重新应用删除墓碑和到期策略，清理数据库、对象、Search、Cache、Task 和分析副本。无法确认时保持隔离/受限并进入 Privacy Manual Review。

### 28.6 Restore Evidence

保存 Backup Identity、Restore Point、执行人、环境、步骤、验证、差异、RPO/RTO 和销毁证据。不保存不必要业务正文。

---

## 29. Disaster Recovery

### 29.1 DR Model

首阶段 DR 以可恢复的 PostgreSQL、对象保护、配置/Secret 恢复、可重建 Projection 和受控 Runtime 重建为基础。是否跨区域 Warm Standby 或更高级模式尚未批准。

### 29.2 RPO and RTO

RPO/RTO 必须按能力和数据分类定义：Identity/Consent、Calculation/Frozen History、Audit、Object、AI In-Flight、Search/Cache 可不同。所有具体数值均为 Open Question，未批准前不得承诺。

### 29.3 Disaster Scenarios

- 数据库 Primary/Cluster 丢失；
- 整个 Region/Account 不可用；
- Object Storage 大范围不可用/损坏；
- KMS/Secret/IAM 不可用；
- Broker 丢失或长期积压；
- 供应链或 Credential 全面受损；
- 错误 Migration/Deletion；
- Observability/Audit 平台故障；
- 关键供应商长期退出。

### 29.4 DR Activation

由 Incident Commander 与 DR/Business Owner 根据影响、预计恢复、数据风险和依赖状态决定。Security/Privacy 事件需相应 Lead 参与。激活、切换和回切全部审计。

### 29.5 Recovery Priorities

1. Identity、Authorization、Consent 和安全边界；
2. PostgreSQL Source of Truth 与 Audit；
3. 确定性排盘和已保存 Frozen 资产；
4. Broker/Worker 与 Data Rights；
5. Object/PDF/Export；
6. AI、Search/Vector 和非关键投影。

### 29.6 DR Drill

定期演练技术恢复、角色、沟通、JIT/Break-Glass、供应商和业务验证。演练不能只做桌面推演；至少按批准周期进行隔离恢复。频率为 Open Question。

### 29.7 Failback

回切前确认数据收敛、Message/Operation、DNS/Route、Secret、Cache、Search 和用户会话。使用渐进流量和验证；不得在未知数据差异下 Big Bang 回切。

---

## 30. Business Continuity

### 30.1 Continuity Priorities

在部分基础设施/供应商不可用时，优先维持：安全登录/告知、确定性排盘、已保存报告读取、数据权利状态与支持沟通。AI、PDF、知识增强和非关键通知可降级。

### 30.2 Degraded Modes

| Dependency Failure | Continuity Mode | Forbidden |
|---|---|---|
| AI | 排盘、规则摘要、已存报告；AI 排队/明确不可用 | 模板冒充 AI 完成 |
| Location | 已存命盘、受控本地数据、稍后重试 | 猜测时区/地点 |
| Search/Vector | 结构化材料或停止知识增强 | 虚构 Citation |
| Redis | DB Read、Cache Miss、保守限流 | 无限开放或丢正式状态 |
| Object Storage | 在线结果；延后 PDF/Export | 公开临时对象 |
| Broker | 安全只读；拒绝无法可靠受理的新异步任务 | 内存假 202 |
| Notification | 状态可在站内查询 | 把未通知当业务未完成 |

### 30.3 Manual Operations

关键业务连续性可以使用受控人工审核/沟通，但人工不得直接改 Aggregate/Database。所有 Manual Decision 有工单、Purpose、双人（如高风险）和 Audit。

### 30.4 Communication Continuity

维护状态页、客服模板和内部通知替代渠道。状态页不暴露用户/安全细节，明确哪些能力可用、受限或等待。

### 30.5 Supplier Continuity

对 AI、地点、通知和存储维护退出/替代计划、数据导出、Credential 撤销和 Contract Test。多供应商不是默认全部 Active；切换前仍需 Validation 与版本治理。

---

## 31. Capacity Management

### 31.1 Capacity Domains

API/Web、PostgreSQL Connection/CPU/Storage、Redis Memory、Broker Throughput/Backlog、Worker Pool、AI Provider Quota、Object Storage、Search/Vector、Observability 和 Network/Egress。

### 31.2 Approved Initial Baseline

继承上游压测基线：100 并发交互请求、20 并发 AI 任务、持续 10 requests/second；这些不是正式 SLO 或无限增长承诺。

### 31.3 Forecasting

基于用户增长、首次排盘、Report、AI 对话、保存对象、Retention、版本增长和 Event/Log Volume 建模。Forecast 明确假设、季节性和不确定性。

### 31.4 Headroom

各关键资源保留应急、部署和故障转移余量。具体 Headroom 百分比待 Capacity Test；不得靠长期超配掩盖泄漏或低效查询。

### 31.5 Capacity Thresholds

定义 Early Warning、Action 和 Critical 阈值及 Lead Time。扩容不能只看 CPU，也看 Queue Age、Connection、Lock、Provider Quota、Cost 和用户 SLI。

### 31.6 Capacity Review

每个 Milestone、重大营销/发布、Retention 变化、供应商配额变化和 Incident 后复审。GA 前完成峰值与降级演练。

### 31.7 Scaling Decisions

先优化浪费、查询、Cache 和 Worker 隔离，再水平扩展；分片、独立 Search、多区域和微服务必须满足技术架构触发条件并通过 ADR。

---

## 32. Performance Operations

### 32.1 Performance Baselines

持续验证 Common API P95 ≤ 500 ms、Calculation P95 ≤ 2 s、AI 首个有效响应 P95 目标 ≤ 15 s、完整 AI Report P95 目标 ≤ 60 s。它们是 Approved 测试基线，不自动成为外部 SLO。

### 32.2 Continuous Monitoring

按 Route/Operation、Release、Environment、Dependency 和 Cache State 观察 P50/P95/P99、Throughput、Error、Saturation。避免用平均值掩盖尾延迟。

### 32.3 Regression Detection

Release 前后、Canary/Control、同版本历史和 Synthetic 对比。回归同时检查 Domain Quality 与 Cost，避免“更快但跳过 Validation”。

### 32.4 Performance Testing Operations

Staging/专用环境执行 Load、Stress、Soak、Spike、Backlog、Failover、Cache Cold 和 Provider Slow。测试数据合成，不攻击 Production 或供应商配额。

### 32.5 Slow Query and Lock Operations

监控慢查询、锁等待、长事务、连接泄漏和计划变化。修复通过索引/查询/Use Case Review，不以随意提高超时作为首选。

### 32.6 Performance Incident

尾延迟、Queue Age 或 Saturation 影响 SLO 时按 Incident 处理：限流/降级、停止发布、隔离高成本任务、扩容或回退，并保留诊断证据。

---

## 33. Cost Management

### 33.1 Cost Dimensions

AI Model/Token、PostgreSQL、Redis、Broker、Object/Backup、Search/Vector、Observability、Network/Egress、CDN/WAF 和供应商支持。

### 33.2 Cost Allocation

按 Environment、Runtime、Feature/Operation、Model、Tenant/Plan（V2）和有效结果统计，不使用用户敏感属性作为 Cost Label。

### 33.3 AI Cost

每次调用记录任务类型、Model Reference、Input/Output Usage、Cache、Retry、Validation Result 和估算成本。以“通过验证的有效输出”衡量单位成本，不能只看供应商请求成功。

### 33.4 Budget and Alerts

设置月度/项目/供应商 Budget、Forecast、异常增长和 Quota 接近告警。具体金额待商业确认。成本告警有 Owner 和行动，不自动删除质量检查。

### 33.5 Optimization Order

减少无关上下文 → 复用确定性 Evidence 摘要 → 选择合适 Model → 限制 Retry → 按任务路由 → 优化输出长度。不得跳过事实、引用、风险、安全或隐私检查。

### 33.6 Cost vs Reliability

降低副本、保留、Backup、Observability 或 On-Call 前评估 SLO、DR、安全和法律影响。成本不能作为删除 Audit 或降低数据权利完成质量的理由。

### 33.7 Cost Review

每月及每个主要 Release 复审 Forecast、单位成本、浪费、闲置资源、Retention 和供应商折扣/锁定风险。

---

## 34. Dependency and Vendor Operations

### 34.1 Inventory

维护生产依赖清单：Owner、用途、数据分类、区域、Credential、Version、SLO/SLA、Quota、Cost、Support、Status Page、Escalation、替代与退出计划。

### 34.2 Health and Status

监控 Availability、Latency、Error、Quota、Contract Change 和 Security Advisory。供应商状态页是输入，不是唯一证据；平台使用自身 SLI 验证影响。

### 34.3 Contract and Change

供应商 API/SDK/模型变化先在 Adapter Contract Test 与 Staging 验证。自动模型升级不得替换 Production Model Reference。

### 34.4 Vendor Incident

平台声明自己的 Incident、执行 Circuit/降级/限流并向供应商升级。供应商恢复后逐步恢复流量，验证数据与结果，不立即全量回切。

### 34.5 Security and Privacy

定期复审数据用途、地区、留存、训练禁用、子处理者、删除、审计和通知义务。重大变化触发 Privacy/Security Review 和可能的 ADR。

### 34.6 Exit Plan

关键 Vendor 有数据导出、Credential 撤销、Adapter 替代、兼容测试、并行验证、用户影响和合同终止计划。退出不修改 Domain/API Contract。

### 34.7 Unowned Dependency

无 Owner、无支持、无替代或不可观察的依赖不得作为 Stable 生产关键路径。

---

## 35. Queue and Worker Operations

### 35.1 Queue Signals

| Signal | Operational Meaning |
|---|---|
| Queue Depth | 待处理数量；需结合 Arrival/Drain Rate |
| Oldest Message Age | 用户等待和积压严重度的核心信号 |
| Processing Time | Worker 执行分布与超时 |
| Retry Rate | 暂时依赖、缺陷或 Poison 风险 |
| DLQ Count/Age | 无法自动处理的工作 |
| Worker Saturation | CPU、Memory、Concurrency、Provider Quota |
| Stuck Operation | 状态长期无进展或 Lease 丢失 |

### 35.2 Retry Operations

按错误分类和总预算有限重试，保持原 IdempotencyKey、Identity 和版本。Validation、Authorization、Consent、Immutable Conflict 不自动重试。

### 35.3 Dead Letter Queue

DLQ 有 Owner、访问控制、Retention、Alert、Triage 和 Replay Runbook。Message Payload 按敏感级别保护，不允许无工单批量下载。

### 35.4 Poison Message

重复导致同一 Consumer 崩溃/失败的 Message 隔离为 Poison，停止无限重试，记录 Safe Error、Contract Version 和影响，进入缺陷/人工处理。

### 35.5 Worker Saturation

区分 CPU、I/O、Provider Quota、DB Connection 和 Memory。按 Queue Class 扩容/限流/降级，避免 AI 高成本任务挤占 Calculation/Data Rights。

### 35.6 Stuck Operation

使用状态更新时间、Lease/Heartbeat、Queue/Event 和依赖状态判断。不得仅因超时把 Operation 设为 Failed/Completed；先确认是否正在执行、已提交或等待人工。

### 35.7 Manual Replay

Replay 前必须：

1. 确认原因已修复；
2. 验证 Message Contract 与 Consumer 版本；
3. 重新校验 Idempotency 和现有结果；
4. 重新校验 Consent、Authorization、Purpose、Ownership 和 Legal Hold；
5. 确认 Algorithm/Rule/Prompt/Model Version 不被静默切换；
6. 限定范围、速率和观察；
7. 记录 Actor、批准、结果和失败。

### 35.8 Queue Pause and Drain

发布、Migration、Provider Incident 可按 Queue Class Pause。Drain 不删除 Message；恢复时控制速率，防止 Thundering Herd。

---

## 36. Database Operations

### 36.1 PostgreSQL Responsibilities

PostgreSQL 是事务 Source of Truth。运维保护 Availability、Integrity、Version、Backup、PITR、Connection、Lock、Storage 和权限，不改变 Domain/Data Model。

### 36.2 Access

- 应用、Migration、Read-Only、Audit 和 DBA Identity 分离。
- 人员访问 JIT、MFA、Purpose、时限和 Session Audit。
- 禁止 Shared Account 和 Direct Business Data Edit。
- 高敏感 Query 使用字段遮蔽和范围限制。

### 36.3 Routine Operations

监控 Connection Pool、CPU、Memory、I/O、Storage、Vacuum/Statistics、Lock、Long Transaction、Slow Query、Replica Lag、Backup 和 Failover Readiness。具体维护动作由批准 Runbook 执行。

### 36.4 Connection Management

API/Worker 各有连接预算。扩容时先检查数据库总连接与 Pool，避免实例横向扩展导致连接耗尽。连接泄漏和长 Idle Transaction 告警。

### 36.5 Read Replica

仅服务允许最终一致的 Query。Authorization、Consent、写前校验和需最新状态的读取不依赖延迟 Replica。Replica Lag 可见并影响路由。

### 36.6 Failover

Failover Runbook 验证连接、事务、Readiness、应用重试、Replication、数据点和业务 Synthetic。Failover 不自动重放未知结果 Command。

### 36.7 Storage and Bloat

按数据类别、Version 增长、Audit、Outbox/Inbox 和 Retention Forecast 管理。清理通过批准保留/Archive 流程，不用临时删除历史。

### 36.8 Database Incident

优先停止新正式写、保护一致性和备份，确认 Primary/Replica 状态。数据损坏或错误 Migration 升级为高 Severity，并由 Data Lead 参与。

---

## 37. Redis Operations

### 37.1 Allowed Roles

Redis 用于 Cache、Rate Limit、短期 Session/Revocation 辅助、任务协调、短锁和可丢进度。不得作为正式命盘、报告、Audit 或唯一额度真相源。

### 37.2 Signals

Availability、Latency、Memory、Eviction、Hit/Miss、Connection、Hot Key、Command Error、Replication/Failover、Rate Limit 和 Lock/Coordination 状态。

### 37.3 Failure Mode

Redis 不可用时 Cache 视为 Miss、进度降级、Rate Limit 保守化、正式状态从 PostgreSQL/可靠任务恢复。不得无限开放额度或丢失正式 Operation。

### 37.4 Eviction and Capacity

Key 分类有 TTL 与容量预算。Eviction 不能删除唯一业务事实；异常 Eviction/Memory Growth 触发 Capacity/Leak 调查。

### 37.5 Key Privacy

Key 不含姓名、出生资料、Conversation、Report Text 或 Secret。Tenant/User、Version、Locale 和授权视图使用安全不透明引用。

### 37.6 Flush / Manual Commands

禁止未经审批的全局 Flush 或生产交互式修改。维护使用限定 Scope、Dry Run、Backup/Recovery 评估和 Audit。

### 37.7 Failover and Recovery

Redis Failover 后验证 Cache、Rate Limit、Session Revocation 和 Worker Coordination；不将恢复 Redis 数据用于覆盖 PostgreSQL 权威状态。

---

## 38. Object Storage Operations

### 38.1 Scope

存放 PDF、Export、Knowledge Attachment、大型 Frozen Artifact 和批准上传。Database Metadata 保存 Owner、Hash、Version、Retention、State 和 Legal Hold。

### 38.2 Access

- Bucket/Container 默认私有；
- Server-side Authorization 后提供短期签名访问；
- 不可猜 URL 不是授权；
- Public Access Block/等价控制持续验证；
- Object Key 不含敏感业务语义。

### 38.3 Integrity

上传/生成后验证 Size、Hash、Media Type 和 Version。Frozen Artifact 不原地覆盖；重新生成创建新 Object/Report。

### 38.4 Lifecycle

按临时、正式、Frozen、Export、Attachment、Legal Hold 分类设置 Retention/Transition/Deletion。Lifecycle Change 先在 Staging/Inventory 评估，防止批量误删。

### 38.5 Security Monitoring

监控 Public Policy、异常下载、签名 URL 滥用、跨 Tenant、加密、失败上传、恶意文件检查和删除失败。高风险访问进入 Security/Audit。

### 38.6 Deletion

Data Rights Saga 删除活动对象、历史版本、临时/失败制品和相关 Index；Legal Hold/Backup Expiry 另行记录。Object 删除结果与 Metadata 对账。

### 38.7 Recovery

对象恢复需验证 Hash、Owner、Version、授权和墓碑。版本保护不能让已删数据重新向用户可见。

---

## 39. Security Operations

### 39.1 Security Monitoring

认证异常、Credential、IDOR、WAF/DDoS、Rate Limit、JIT/Break-Glass、Secret、供应链、Egress、Object Access 和管理员敏感访问。

### 39.2 Vulnerability Management

资产/依赖/制品持续扫描，按严重度、可利用性、暴露和数据影响设修复 SLA。例外有 Owner、期限、补偿和风险接受。

### 39.3 Credential Operations

创建、轮换、撤销、过期、使用和异常访问可见。发现泄漏先撤销/隔离，再调查；不得等待完整 Root Cause 才止损。

### 39.4 Security Incident

疑似数据/账户/供应链事件保守提升 Severity，Security Lead 参与证据、Containment、Forensics、Legal/Privacy 和通知。日志/Trace 访问本身受审计。

### 39.5 Patch Operations

Security Patch 通过 Immutable Artifact 和 Emergency/Normal Change 发布。不能在生产实例手工修补。高风险依赖升级验证 API/Data/Message 兼容。

### 39.6 Access Review

定期复审 Human/Workload/Vendor Role、Scope、JIT、Break-Glass、Database、Secret、CI/CD 和 Audit。无 Owner/未使用权限撤销。

### 39.7 Evidence Preservation

Incident 证据使用受控、完整性保护的存储，记录 Chain of Custody。不得为了恢复服务销毁关键证据，但也不无限复制用户敏感内容。

---

## 40. Privacy and Data Rights Operations

### 40.1 Data Export

- 强身份复核、Purpose、Scope 和 Request Identity；
- 各 Context 提供授权投影，按截止时间形成清单；
- Export Artifact 加密/短期授权、到期删除；
- Partial/Failed 明确，不能缺一部分仍标 Completed；
- 完成期限待法律/产品确认。

### 40.2 User Deletion

Deletion Saga 覆盖 Identity、Consent、Birth、Chart、AI/Conversation、Timeline、Report、Object、Search、Cache、Task/Projection 和适用研究副本。每个 Context 独立事务与结果。

### 40.3 Partial Completion

失败步骤保持 `PartiallyBlocked/Failed/Processing`，限制新使用，自动有限重试后进入 Manual Review。用户状态沟通说明已完成、待处理、Legal Hold 和下一更新时间。

### 40.4 Legal Hold

Legal Hold 有依据、范围、Owner、开始/复审/结束、访问限制和 Audit。Hold 阻止相应物理删除但不授权新用途；可删除或匿名化的非 Hold 数据继续处置。

### 40.5 Backup Expiry

无法从不可变 Backup 立即物理删除的数据按批准到期周期处理，墓碑防止恢复后重新激活。向用户的完成语义需法律确认。

### 40.6 Search Index Removal

先阻止新召回，再删除/重建相关 Keyword/Vector Index，验证 Article/User/Resource Identity 不再出现。Search Lag/Failure 进入 Partial 状态。

### 40.7 Cache Removal

清理 User/Tenant、Session、Report/Timeline Projection 和 Authorization Cache；即使清理失败，Source Authorization/Deletion 状态必须阻止访问。

### 40.8 Object Storage Deletion

删除活动/版本/临时对象并对账 Metadata。签名 URL 立即失效或通过授权层拒绝。Legal Hold 与 Backup 例外单独记录。

### 40.9 Consent Revocation

停止新可选用途，评估在途 AI、Research、Feedback 和衍生数据；各步骤最终一致并可审计。撤回不改写合法历史事实。

### 40.10 Manual Review

Reviewer 使用 JIT、Purpose、最小遮蔽视图和明确处置选项，不能直接数据库修改。每个决定、依据和结果审计。

### 40.11 User Status Communication

提供 Received、Processing、PartiallyCompleted、LegalHold/Review、Completed、Failed 等清晰状态和安全说明；不泄露内部架构或其他主体数据。

---

## 41. Audit Operations

### 41.1 Audit Scope

认证安全、权限/Scope、敏感访问、规则/知识/Prompt/Model 发布、Config/Secret、Deployment/Migration、Data Export/Delete、Consent、Break-Glass、Manual Replay 和重大 Incident 决策。

### 41.2 Reliability

必需 Audit 与业务/管理动作可靠关联。Audit 写入失败时，高风险发布、敏感访问或治理动作按基线阻断或明确告警；不得静默继续。

### 41.3 Immutability

Audit 追加、防篡改、普通管理员只读。Correction 追加新记录引用原事件，不覆盖或删除历史。

### 41.4 Access

Auditor/批准调查 Purpose、JIT、范围和 Session Audit。查询 Audit 本身也审计。禁止普通运营批量浏览敏感事件。

### 41.5 Retention and Legal Hold

具体保留、不可变程度和归档介质待法律/安全确认。Audit 最小化内容，不因长保留复制完整 Birth/Conversation/Report。

### 41.6 Audit Monitoring

监控 Write Success、Lag、Storage、Integrity Check、Query Access、Backup/Restore 和 Time Synchronization。No Data/采集停止为高风险。

### 41.7 Incident Use

Incident Timeline 可引用 Audit Identity，不编辑 Audit。取证导出有 Hash、访问与 Chain of Custody。

---

## 42. Maintenance Windows

### 42.1 Purpose

用于需要用户影响或高风险基础设施工作的批准窗口，例如 Major Database、KMS、Network、Provider 或 DR 演练。

### 42.2 Selection

考虑用户低峰、On-Call、供应商支持、Backup、业务活动、法律截止和跨时区。具体周期与时长待运营确认。

### 42.3 Communication

提前通知内部团队和受影响用户，说明能力、开始/预计结束、替代路径和状态更新。Emergency Maintenance 可缩短通知但必须记录。

### 42.4 SLO Treatment

计划维护是否排除于 SLO 必须在 SLO 定义中预先批准，不能事后为了达标排除。安全/隐私/数据事件即使发生在维护窗口也不自动免责。

### 42.5 Window Controls

Change Freeze、Owner、Runbook、Backup、Rollback、Verification、Status Communication 和自动到期。超时未完成则停止、回退或升级 Incident。

---

## 43. Operational Readiness Review

### 43.1 Review Timing

新 Service/Runtime/Dependency、重大 Feature、数据/安全变化、Beta、RC、GA 和区域/供应商变化前执行 ORR。

### 43.2 ORR Inputs

- Architecture/API/Engineering Baseline；
- Ownership、SLO/SLI、Capacity、Cost；
- Dashboard、Alert、Synthetic、Runbook；
- Deployment、Migration、Rollback/Forward-Fix；
- On-Call、Escalation、Vendor Support；
- Security、Privacy、Data Rights、Audit；
- Backup、Restore、DR 和 Business Continuity；
- Known Risks、Exceptions、Debt 和 ADR。

### 43.3 Decision

`Ready`、`Ready with Time-Bounded Conditions` 或 `Not Ready`。条件有 Owner、期限和限制；安全、数据完整性、不可恢复、无 On-Call/Runbook 等阻断项不能用一般风险接受绕过。

### 43.4 Evidence

ORR 保存测试、演练、Dashboard、Access、Backup/Restore、Release 和批准证据，不只依赖会议结论。

### 43.5 Re-Review

重大 Incident、架构/供应商变化、长期 SLO 失败或 DR 演练失败触发重新评审。

---

## 44. Production Readiness Checklist

### 44.1 Ownership and Support

- [ ] Service/Module、Dashboard、Alert、Runbook、Dependency 有主/备 Owner。
- [ ] On-Call、Escalation、Incident 角色和供应商支持可用。
- [ ] 用户/内部 Communication 和状态页准备完成。

### 44.2 Deployment and Change

- [ ] Immutable Artifact、Promotion、签名/SBOM 可验证。
- [ ] Rolling/Canary/Blue-Green 选择有风险依据。
- [ ] Graceful Shutdown、Compatibility Window 和 Stop Condition 已测。
- [ ] Feature Flag 有 Owner、到期和 Server-side Control。
- [ ] Rollback 与 Forward-Fix 都经过演练。
- [ ] Beta/RC/GA Scope Freeze 符合 Roadmap。

### 44.3 Data and Migration

- [ ] Expand–Migrate–Contract、锁、Batch、Checkpoint 和验证明确。
- [ ] PostgreSQL Backup/PITR 和实际 Restore 验证通过。
- [ ] Frozen History、Version、Audit 与 Object Hash 已验证。
- [ ] 删除墓碑在 Restore 后可重放。
- [ ] 无 Direct Production Database Edit 路径。

### 44.4 Observability and SLO

- [ ] Logs/Metrics/Traces 去敏且关联 ID 可用。
- [ ] Dashboard/Synthetic/Alert 有 Freshness、Owner 和 Runbook。
- [ ] SLI Good/Valid/Total、数据源和排除项明确。
- [ ] SLO 数值已批准或明确 Candidate，不对外误承诺。
- [ ] Error Budget、Burn、Release Policy 和例外已确认。
- [ ] Domain Quality、Security、Privacy、Cost Metrics 可见。

### 44.5 Reliability and Capacity

- [ ] Timeout、Retry、Circuit、Bulkhead、Rate Limit 和 Backpressure 已测。
- [ ] Queue Depth/Age、DLQ、Poison、Stuck、Replay Runbook 就绪。
- [ ] Database/Redis/Object/Vendor Failure 降级已演练。
- [ ] Capacity、Connection、Worker、Provider Quota 和 Cost Headroom 足够。
- [ ] Backup、Restore、DR、RPO/RTO 有批准目标或 GA 阻断项。

### 44.6 Security and Privacy

- [ ] Default Deny、MFA、JIT、Time-Limited、Break-Glass 和无 Shared Account。
- [ ] Secret/Credential 环境隔离、轮换、撤销和 Incident 流程就绪。
- [ ] Observability 不含完整 Birth/Conversation/Prompt/AI Raw/Report。
- [ ] Export、Deletion、Partial、Legal Hold、Backup Expiry 和用户状态已演练。
- [ ] Audit 必需写入、不可变、访问和恢复已验证。
- [ ] 法律、安全、隐私待确认项已关闭或明确阻断上线。

---

## 45. Operations Governance

### 45.1 Architecture Baseline

01–10 Approved 文档与本文件未来 Approved 版本构成 Operations Baseline。运维实践不得以工具便利改变业务、领域、数据、应用、API、技术或工程语义。

### 45.2 Ownership

每个生产 Runtime、Dependency、SLO、Alert、Dashboard、Runbook、Backup、Secret、Change Class 和 Incident Action 有 Owner 与备份。

### 45.3 Policy Hierarchy

Architecture Baseline → Approved ADR → Operations Standard → Runbook → Change/Incident Record。下层不能覆盖上层；紧急偏离走 Exception/Emergency Process。

### 45.4 Exception

例外记录 Scope、Reason、Risk、Compensating Control、Owner、Expiry 和 Exit。涉及 ADR Matrix 的变化仍需 ADR。无到期永久例外禁止。

### 45.5 Operational Debt

无 Runbook、Noisy Alert、未演练 Restore、手工步骤、Access 过大、配置 Drift、未 Owner 依赖和长期 Partial Operation 进入 Debt Register。安全、隐私、删除、Audit、不可恢复为最高优先级。

### 45.6 Governance Cadence

定期 Review：SLO/Error Budget、Incident/Problem、Alert Quality、Access、Backup/DR、Capacity/Cost、Vendor、Dependency、Change Failure、Debt 和 ADR。

### 45.7 Metrics for Improvement

使用 MTTD、MTTA、MTTR、Change Failure Rate、Rollback Rate、Alert Precision、Restore Success、Action Aging 和 Toil 改进系统，不用于个人绩效惩罚。

### 45.8 Automation Governance

自动化有 Owner、权限、Dry Run、Idempotency、Limit、Audit 和 Kill Switch。自动化不能直接绕过 Application 层修改业务数据。

---

## 46. ADR Reference Matrix

| Topic | ADR Required | Trigger Example |
|---|---|---|
| Environment Model | Yes | 合并环境、允许生产数据下沉或新增正式环境 |
| Deployment Model | Yes | 从模块化单体容器模型改为其他运行边界 |
| Artifact Promotion | Yes | 生产重新构建或改变制品晋级信任链 |
| Rollout Strategy | Yes | 改变默认风险模型或引入新流量切分机制 |
| Rollback Strategy | Yes | 改变兼容窗口、数据回退或 Forward-Fix 政策 |
| Database Migration Operations | Yes | 改变 Expand–Migrate–Contract 或在线迁移边界 |
| Production Access Model | Yes | 改变 JIT、MFA、Break-Glass 或 Direct DB 禁令 |
| Observability Platform | Yes | 替换主日志/指标/Trace 平台或信任边界 |
| Logging Retention | Yes | 改变敏感日志保留、访问或 Redaction 责任 |
| SLI / SLO Policy | Yes | 改变计算、排除、窗口或正式目标 |
| Error Budget Policy | Yes | 改变消耗、冻结发布或非预算事件规则 |
| Incident Severity Model | Yes | 改变 SEV 定义、角色或响应义务 |
| Backup Strategy | Yes | 改变 Backup Source、PITR、对象/Audit 保护 |
| RPO / RTO | Yes | 新设或调整正式恢复目标 |
| Disaster Recovery Model | Yes | 引入 Warm Standby、Active-Active 或新恢复权威 |
| Multi-Region Operations | Yes | 增加跨区域流量/数据/Failover |
| On-Call Model | Yes | 改变 24×7、Rotation、Escalation 或权限模式 |
| Secret Operations | Yes | 改变 Secret/KMS、Rotation、Recovery 或 Workload Identity |
| Change Management | Yes | 改变 Standard/Normal/Emergency Gate |
| Maintenance Window Policy | Yes | 改变 SLO 排除、通知或窗口审批 |
| Queue Replay Policy | Yes | 改变 DLQ、人工 Replay 或幂等重验 |
| Data Rights Operations | Yes | 改变 Completed、Legal Hold、Backup Expiry 语义 |
| Audit Operations | Yes | 改变必需写入、不可变、保留或访问模型 |

任何涉及以上主题的修改，都不得直接修改本文档。必须先通过 ADR，记录背景、选项、风险、数据与安全影响、迁移、回退、成本、Owner 和验证；批准后才能更新 Operations Baseline。

---

## 47. Operations Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐做法 |
|---|---|---|---|
| Manual Production Deployment | 人员直接在生产执行不可重复步骤 | Drift、漏审计、难回退 | Pipeline + Immutable Artifact + Approval |
| Mutable Artifact | 同一版本在环境间内容不同或在线修改 | 无法复现、供应链风险 | 一次构建、完整性验证、晋级 |
| Configuration Drift | 运行配置与声明/环境不一致 | 隐性故障、恢复失败 | 版本化 Config、Drift Detection、Change Record |
| Shared Production Account | 多人共用身份 | 无法追责、权限过大 | 个人/Workload Identity、MFA、JIT |
| Direct Production Database Editing | 绕过 Domain、Transaction 与 Audit | 不变量/版本链损坏 | Approved Repair Use Case/Migration |
| Alert on Every Error | 每个单次失败都 Page | 疲劳、关键事件被淹没 | SLO/Burn/用户影响告警 |
| Noisy Alerts | 低精度、重复、无行动告警 | On-Call 忽略、MTTR 上升 | Owner、去重、阈值验证、退役 |
| Missing Runbook | Page 无诊断/缓解说明 | 响应慢、危险试错 | 上线前 Runbook + Drill |
| Infinite Retry | 无总预算重复任务/依赖调用 | 故障风暴、AI 成本、重复副作用 | 有限退避、Circuit、DLQ、幂等 |
| Blind Message Replay | 未检查原因/状态就批量重放 | 重复 Report/Delete、越权 | 修复验证、范围限制、幂等/Consent 重验 |
| Monitoring as Source of Truth | 用 Dashboard 状态改业务终态 | 错误完成、数据污染 | 业务状态来自 Aggregate/Saga Source |
| Logging Sensitive Data | 记录 Birth、Conversation、Prompt、AI Raw、Report | 隐私与安全事件 | 禁记、Redaction、扫描、最小引用 |
| Backup Without Restore Test | 只有成功 Job 无恢复验证 | 灾难时不可用 | 定期隔离 Restore + 业务验证 |
| Treating Backup as Disaster Recovery | 认为有备份即具备连续性 | 无角色、RTO、切换和验证 | DR Plan、Runbook、Drill、Business Continuity |
| Ignoring Error Budget | 可靠性持续恶化仍高风险发布 | Incident 增多、用户信任下降 | Budget State 驱动 Release/Repair |
| Permanent Break-Glass Access | 紧急权限长期有效 | 未授权访问与审计缺陷 | 短时 JIT、实时告警、用后撤销 |
| Snowflake Server | 单实例手工配置不可重建 | Failover/扩容/审计失败 | 声明式、可替换 Runtime |
| Big Bang Deployment | 一次全量切换无渐进验证 | Blast Radius 最大 | Rolling/Canary/Blue-Green 按风险选择 |
| Rollback Without Compatibility Check | 直接回旧应用 | 新 Schema/Data/Message 不兼容 | 回退矩阵、Forward-Fix、演练 |
| Silent Partial Failure | Export/Delete/Projection 失败仍显示完成 | 权利、数据和信任风险 | 分步骤状态、Manual Review、用户沟通 |
| Unowned Alerts | 无团队负责 Page | 无响应、长期噪声 | 每个 Alert Owner/Runbook/Escalation |
| Unowned Dependencies | 关键 Vendor/组件无负责人 | 漏升级、Incident 无升级路径 | Dependency Inventory、Owner、Exit Plan |
| Hiding Incidents | 为指标或声誉延迟声明 | 影响扩大、证据和信任损失 | 保守声明、透明 Timeline、治理保护 |
| Blameless Without Accountability | 不责备被误解为无行动/无 Owner | 同类事故重复 | 系统性复盘 + 明确 Action/Owner/期限 |
| Maintenance as SLO Exclusion Trick | 事后把故障标维护 | SLO 失真、用户影响被隐藏 | 预批准窗口和排除规则 |
| Cache Flush as First Response | 遇到问题全局清 Cache/Redis | 惊群、会话/限流风险 | 定位 Scope、受控失效、容量保护 |
| Suppressing Security Alerts During Release | 发布时关闭关键告警 | 攻击/泄漏被掩盖 | 仅抑制预期噪声，保留安全/隐私信号 |
| Declaring Recovery on Green Infrastructure | 组件 Up 即关闭 Incident | 领域/Queue/Data Rights 仍错误 | 用户旅程与数据验证后恢复 |

---

## 48. Review Checklist

### 48.1 Baseline and Scope

- [ ] 文档是否为 Review 0.9。
- [ ] 是否严格继承 01–10 Approved 基线。
- [ ] 是否未修改 Domain、Data、Application、API、Technology 或 Engineering Baseline。
- [ ] 是否没有任何可执行配置、代码、SQL、脚本或监控规则。
- [ ] 是否未进入编码/部署执行阶段。

### 48.2 Environment and Deployment

- [ ] Local/Test/Staging/Production/DR 是否定义并隔离。
- [ ] 生产数据是否禁止进入低环境。
- [ ] Secret/Credential 是否按环境隔离。
- [ ] Artifact 是否不可变且环境间晋级。
- [ ] Rolling/Canary/Blue-Green 是否按风险选择而非一刀切。
- [ ] Feature Flag、Graceful Shutdown、Compatibility Window 是否明确。
- [ ] Database Expand–Migrate–Contract 是否可演练、可验证。

### 48.3 Observability and Reliability

- [ ] Logs/Metrics/Traces/Synthetic/Dashboard 是否有 Owner 与 Freshness。
- [ ] Observability 是否不作为业务 Source of Truth。
- [ ] 是否禁止记录完整 Birth/Conversation/Prompt/AI Raw/Report。
- [ ] SLI Good/Valid/Total 是否明确。
- [ ] 未批准 SLO 是否标 Candidate/Open Question。
- [ ] Error Budget 是否不能抵消安全/隐私/正确性/Audit 事故。
- [ ] Alert 是否可行动、有 Runbook、有 Owner。

### 48.4 Incident and Operations

- [ ] SEV-1 至 SEV-4、IC、Comms、Ops、Security/Privacy Lead 是否明确。
- [ ] Timeline、Mitigation、Recovery、PIR 和 Action 是否完整。
- [ ] On-Call、Escalation、Handoff 和 Vendor 支持是否定义。
- [ ] Runbook 是否有 Owner、停止条件和 Drill。
- [ ] Problem Management 是否追踪根因与重复趋势。

### 48.5 Backup, DR and Data Rights

- [ ] PostgreSQL Backup/PITR、Object、Config、Secret/KMS、Audit 是否覆盖。
- [ ] Restore 是否验证 Domain、Version、Object、Audit 和权限。
- [ ] 删除墓碑是否防止恢复后数据复活。
- [ ] RPO/RTO 未批准值是否保持 Open Question。
- [ ] DR Drill 与 Business Continuity 是否覆盖依赖失败。
- [ ] Export/Delete/Partial/Legal Hold/Backup Expiry/Search/Cache/Object 是否完整。
- [ ] Manual Review 和用户状态沟通是否明确。

### 48.6 Platform and Governance

- [ ] Queue Depth/Age、DLQ、Poison、Saturation、Stuck、Replay 是否覆盖。
- [ ] Replay 前是否重验幂等、Consent、Authorization 与版本。
- [ ] Database/Redis/Object 的 Source of Truth 和失败边界是否正确。
- [ ] Production Access 是否 Default Deny、MFA、JIT、限时、无共享账户。
- [ ] 是否禁止 Direct Database Modification。
- [ ] Cost、Capacity、Vendor、Security、Privacy 和 Audit 是否有 Owner。
- [ ] ADR Matrix 是否覆盖重大运维变化。
- [ ] Beta/RC/GA Scope Freeze 是否继续生效。

---

## 49. Open Questions

### 49.1 SLI / SLO / Error Budget

1. API、Calculation、AI、Report、Queue、Export、Deletion、Backup、Restore 和 Audit 的正式 SLO 数值与窗口。
2. 计划维护、客户端错误、Rate Limit 和供应商不可用的 SLI 计入/排除规则。
3. Error Budget 窗口、Burn Rate、At Risk/Exhausted 阈值和发布冻结条件。
4. First-Party、Developer API 与 Governance 是否采用不同 SLO。
5. Domain Quality 指标哪些成为正式 Release/SLO Gate。

### 49.2 Release and Change

1. 各风险等级默认 Rollout Strategy 与 Canary Step/观察窗口。
2. N/N-1 Compatibility 最大混跑时间。
3. Standard Change 目录、Approval 数和 Emergency Change 最小门禁。
4. Release/Maintenance 窗口、用户通知提前期和 Freeze Calendar。
5. Release Branch/Tag/Artifact Promotion 的最终运行工具与责任。

### 49.3 Incident and On-Call

1. SEV-1 至 SEV-4 的 Acknowledge、Role、Communication 和 Mitigation 目标。
2. GA 是否需要 24×7 On-Call，以及团队/供应商覆盖范围。
3. Incident Communication 的内部、状态页、用户和法律触发条件。
4. PIR 完成期限、Action Aging 和升级机制。
5. Session Recording/等价 Audit 的技术与法律边界。

### 49.4 Backup / Restore / DR

1. 各数据类别 RPO、RTO、Backup Frequency 和 Retention。
2. PostgreSQL HA/PITR、对象版本、Audit 归档的具体能力。
3. DR 是 Same-Region Restore、Cross-Region Cold/Warm 还是其他模型。
4. Restore/Failover/Full DR Drill 频率。
5. Backup Expiry 后 User Deletion 的正式完成表述。
6. KMS/Secret 平台不可用时的恢复与 Break-Glass。

### 49.5 Capacity and Cost

1. Production API 实例、Worker Pool、DB Connection 和 Redis/Broker Headroom。
2. AI、Calculation、Report、Index、Data Rights Queue 的 Priority 与配额。
3. Cost Budget、异常阈值、Unit Economics 和 Owner。
4. Observability、Backup、Object 和 Log Retention 的成本上限。
5. 何种证据触发独立 Search、微服务或 Multi-Region。

### 49.6 Security / Privacy / Audit

1. Production JIT 最大时限、MFA、Break-Glass 和 Access Review 周期。
2. Logs、Metrics、Traces、Audit、Incident Evidence 的保留与访问。
3. Audit 使用同库权限域、独立数据库还是不可变外部归档。
4. Data Export/Delete 法律期限、Legal Hold 与用户通知。
5. AI 供应商地区、留存、训练禁用与 Incident 通知。
6. Security Patch、漏洞例外和供应商披露 SLA。

### 49.7 Technology and Tooling

1. 容器平台、Artifact Registry、CD、Config/Secret、Observability、Alert/On-Call 工具选型。
2. Message Broker、DLQ、Replay、Scheduler 和 Queue Dashboard 工具。
3. Database/Redis/Object 托管层与供应商支持等级。
4. Status Page、Incident Timeline、Runbook 和 Change System 工具。
5. Drift Detection、Session Audit 和 Synthetic 平台。

### 49.8 ADR Candidates

- ADR-CANDIDATE-OPS-001：正式 Environment/Account/Region 模型。
- ADR-CANDIDATE-OPS-002：Artifact Promotion、Rollout 和 Rollback/Forward-Fix 标准。
- ADR-CANDIDATE-OPS-003：SLI/SLO/Error Budget 与 Release Freeze Policy。
- ADR-CANDIDATE-OPS-004：Incident Severity、On-Call、Escalation 和 Communication。
- ADR-CANDIDATE-OPS-005：PostgreSQL Backup/PITR、RPO/RTO 与 DR 模型。
- ADR-CANDIDATE-OPS-006：Production JIT/MFA/Break-Glass/Session Audit。
- ADR-CANDIDATE-OPS-007：Observability、Retention、Redaction 和 Audit 物理边界。
- ADR-CANDIDATE-OPS-008：Queue/DLQ/Replay 与 Worker Isolation Operations。
- ADR-CANDIDATE-OPS-009：Data Rights、Backup Expiry 和 Restore Tombstone 语义。
- ADR-CANDIDATE-OPS-010：Multi-Region、Vendor Continuity 和 Failover。

---

## 50. Risks

| Risk | Manifestation | Impact | Mitigation / Gate |
|---|---|---|---|
| Environment Leakage | Prod Data/Secret 进入低环境 | 隐私和供应链事件 | 账户/网络/Credential 隔离、扫描、Review |
| Artifact Drift | 环境重新构建或手改 | 无法复现/回退 | Immutable Promotion、Integrity Check |
| Compatibility Failure | Web/API/Worker/Schema 混跑失败 | 中间态中断、数据错误 | N/N-1 Matrix、Canary、Expand/Contract |
| Unsafe Rollback | 旧应用读新数据失败 | 二次 Incident | Compatibility Check、Forward-Fix Option |
| Migration Lock | 长锁/大事务 | 全站时延或不可用 | 演练、Batch、Throttle、Stop Condition |
| Config/Secret Drift | 环境值不一致或泄漏 | 安全/行为不可预测 | Version、Drift Detection、Rotation |
| Excess Production Access | 永久/共享/直连数据库 | 未授权修改与追责失败 | MFA、JIT、No Shared、No Direct Edit |
| Observability Leakage | 敏感正文进入 Log/Trace | 隐私和保留扩大 | 禁记、Redaction、扫描、Incident |
| Monitoring Blindness | 信号丢失却显示 Green | 延迟发现、错误发布 | No Data、Pipeline Health、Synthetic |
| Invalid SLO | 未量化/错误排除 | 错误决策和外部承诺 | Baseline Window、Approval、Audit |
| Error Budget Misuse | 用 Budget 接受安全/正确性事故 | 数据和信任损失 | Non-Budgetable Policy |
| Alert Fatigue | Noise、重复、无 Owner | Critical 告警被忽略 | Alert Quality、Runbook、Retire |
| Incident Underreporting | 延迟声明/隐藏影响 | Blast Radius、法律风险 | 保守 Declare、Timeline、Governance |
| On-Call Gap | 无覆盖/权限/训练 | MTTR 增加 | ORR、Rotation、Drill、Escalation |
| Backup Illusion | Job 成功但不可恢复 | 灾难数据丢失 | Restore Drill、业务验证 |
| Data Resurrection | Restore 未重放墓碑 | 违反删除权 | Tombstone、Isolation、Privacy Review |
| Queue Retry Storm | 无限 Retry/Poison | 成本、积压、重复 | Budget、Circuit、DLQ、Idempotency |
| Blind Replay | Consent/状态已变仍重放 | 越权、重复正式结果 | Manual Gate、Revalidation、Rate Limit |
| Database Saturation | 连接/锁/存储耗尽 | 核心 Source 不可用 | Capacity、Pool Budget、Slow Query Ops |
| Redis Failure Misdesign | 限流失效或业务状态丢失 | 滥用/重复/中断 | 保守降级、DB Source of Truth |
| Object Exposure | Public Policy/长签名 URL | Report/Export 泄漏 | Private Default、短期授权、Audit |
| Vendor Concentration | AI/Cloud/Identity 长期故障 | 能力中断、迁移困难 | Adapter、Exit Plan、Continuity |
| Cost Runaway | AI Retry、Log/Trace/Cardinality | 预算超支和服务限制 | Cost Metrics、Quota、Owner、Optimization |
| Capacity Surprise | 峰值/版本增长未预测 | Queue/SLO 失败 | Forecast、Headroom、Load Test |
| Runbook Decay | 步骤/链接/权限过期 | Incident 中危险操作 | Owner、Review Date、Drill |
| Corrective Action Aging | PIR 有结论无修复 | 重复事故 | Owner、Due Date、Governance Review |
| Scope Creep | 运维文档引入新产品/微服务 | Roadmap 延期与架构冲突 | Baseline/ADR/Scope Freeze |

---

## 51. 进入下一阶段《12-SECURITY-PRIVACY.md》所需输入条件

- [ ] `11-DEPLOYMENT-OPERATIONS.md` 已完成评审并成为 Approved 1.0 Operations Baseline。
- [ ] Local、Automated Test、Staging、Production、DR/Restore Sandbox 与隔离规则已确认。
- [ ] Immutable Artifact、Promotion、Release Gate、Rolling/Canary/Blue-Green 选择标准已确认。
- [ ] Graceful Shutdown、Compatibility Window、Rollback/Forward-Fix 和 Expand–Migrate–Contract 已确认。
- [ ] Config、Secret、Feature Flag、Drift 和 Production Access Operations 已完成安全评审。
- [ ] Logs、Metrics、Traces、Dashboard、Synthetic 和敏感数据禁记边界已确认。
- [ ] SLI Good/Valid/Total、候选 SLO、Error Budget 和非预算事件已确认。
- [ ] Alert、SEV-1 至 SEV-4、Incident Roles、On-Call、Escalation、Runbook 和 PIR 已确认。
- [ ] PostgreSQL Backup/PITR、Object、Config、Secret/KMS、Audit、Restore Validation 和 Tombstone 已确认。
- [ ] RPO/RTO、DR Model、Drill 和 Business Continuity 已批准，或明确为 12/GA 阻断事项。
- [ ] Capacity、Performance、Cost、Dependency/Vendor Operations 有 Owner 和目标。
- [ ] Queue/Worker、Database、Redis、Object Storage 的运行、失败和人工处置已确认。
- [ ] Data Export、User Deletion、Partial、Legal Hold、Backup Expiry、Search/Cache/Object Removal 和用户沟通已完成法律/隐私评审。
- [ ] Audit Write、Immutability、Access、Retention、Backup/Restore 和 Incident Use 已确认。
- [ ] Operational Readiness 和 Production Readiness Gate 已批准。
- [ ] ADR Reference Matrix 中影响 Security/Privacy 的决策已批准或保持阻断，不擅自选择。
- [ ] Beta、RC、GA Scope Freeze 继续生效。
- [ ] 下一阶段只生成 Security & Privacy Architecture，不生成代码、配置、策略文件、扫描规则或部署资产。

只有本部署与运维规范通过评审后，才可以生成 `12-SECURITY-PRIVACY.md`。本次不得生成该文件，也不得进入编码或部署执行阶段。

