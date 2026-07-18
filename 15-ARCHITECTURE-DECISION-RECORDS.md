# AI 八字命理分析平台：架构决策记录治理与登记册

**文档编号：** 15  
**文档类型：** Architecture Decision Records Governance & Register  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md` 至 `14-TESTING-STRATEGY.md`（均已 Approved 1.0）  
**目标读者：** CTO、架构委员会、产品与工程负责人、领域/数据/应用/API/技术架构师、安全与隐私负责人、AI 与测试负责人、运维与发布负责人、命理领域专家、法律评审人员

---

## Version 0.9 Change Log

- 首次建立统一 ADR 原则、范围、生命周期、状态、编号、模板与审批流程。
- 定义影响、备选、风险、安全隐私、AI、测试、迁移、回滚、替代与例外治理。
- 定义 ADR 与 01～14 Approved Architecture Baseline 的关系、索引、审计和追踪要求。
- 将 01～14 已批准文档中的 31 项关键架构结论登记为 `ADR-BL-*` 基线继承决策。
- 建立 18 项未决 `ADR-CANDIDATE-*` 候选登记；候选登记不代表批准或偏好。
- 本文件不生成独立 ADR 文件、代码、配置、脚本、目录或实现资产。

---

## 1. Document Purpose

### 1.1 目标

本文档定义平台如何提出、评审、批准、实施、复审、替代和审计重大架构决策，并为 01～14 已批准基线中的关键结论建立统一索引。

ADR 的目的不是增加文档数量，而是让重要决策具备可回答的问题：为什么需要决定、有哪些可行选项、为何选择当前方案、承担哪些后果、如何迁移和回滚、何时必须复审。

### 1.2 两类登记

本文区分：

1. **Baseline-Inherited Decision：** 已经由 01～14 Approved 1.0 明确形成的结论。本文件仅归纳和建立索引，不重新决策、不伪造历史日期。
2. **ADR Candidate：** 已被基线识别为需要未来决策的事项。登记只表示需要治理，不表示任何选项已获批准。

### 1.3 不包含内容

本文不包含：

- 对 01～14 任何基线的直接修改；
- 独立 `ADR-0001`、`ADR-0002` 等记录文件；
- 对候选方案作出选择；
- 代码、配置、脚本、项目目录或部署资产；
- 技术产品、云厂商、模型或协议的实现选型；
- 未经专家确认的命理规则或未经法律确认的合规结论；
- 编码阶段授权。

### 1.4 冲突处理

发现现有基线之间不一致时，只能登记为：

- `ADR Candidate`：需要未来架构决定；
- `Open Question`：缺少事实、Owner 或批准输入；
- `Baseline Conflict`：两个或多个 Approved 基线对同一事项给出不可同时满足的规范。

本文件不得通过措辞重新解释来静默解决 Baseline Conflict。

---

## 2. ADR Principles

### ADR-P-001 Context Before Decision

没有业务背景、问题边界和决策驱动因素，不作架构决定。

### ADR-P-002 Significant and Durable

ADR 用于跨团队、高成本、长期、难逆、安全隐私、数据语义或基线级决定，不记录每个小型实现选择。

### ADR-P-003 Alternatives Are Mandatory

至少分析维持现状和一个可行替代；若只有一个合法选项，说明约束来源和为何其他选项不成立。

### ADR-P-004 Consequences Are Part of the Decision

正面与负面后果、成本、债务和限制必须在批准前明确，不能只记录收益。

### ADR-P-005 Baselines Are Immutable by Conversation

会议、聊天、工单或代码合并不能直接改变 Approved Baseline。重大变化先批准 ADR，再按影响更新基线。

### ADR-P-006 Approved Records Are Append-Only

Accepted、Rejected、Superseded 或 Deprecated ADR 不原地改写历史结论。更正元数据需留下审计；实质变化创建新 ADR。

### ADR-P-007 One Decision, Clear Owner

每个 ADR 有一个 Accountable Owner。多方参与评审不等于无人最终负责。

### ADR-P-008 Evidence Proportional to Risk

高风险决定需要更强的 PoC、Threat Model、数据、测试、成本、恢复和法律证据；低风险决定保持轻量。

### ADR-P-009 Reversibility Explicit

明确决定是可逆、困难可逆还是实质不可逆，并给出 Migration、Rollback 或退出条件。

### ADR-P-010 Security, Privacy and AI Are Cross-Cutting

涉及身份、敏感出生信息、Provider、模型、知识、Prompt、审计或用户权利的 ADR 必须经过相应专项评审。

### ADR-P-011 No Retroactive Approval Fiction

可以用 ADR 记录当前需要正式化的既有事实，但不得假装该记录在历史上曾被评审。本文的 `ADR-BL-*` 明确标记为基线继承摘要。

### ADR-P-012 Review Triggers over Expiry Alone

ADR 由规模、风险、法规、供应商、事故、性能或基线变化触发复审；定期检查用于发现触发条件，不意味着自动失效。

### ADR-P-013 Decision and Implementation Are Separate

ADR 说明“选择什么、为什么和约束”，实施计划说明“如何交付”。ADR 不承载代码或详细配置。

### ADR-P-014 Traceability

ADR 必须链接需求、基线、风险、测试、迁移、发布和后续 ADR，使结论可验证、可复现、可审计。

---

## 3. ADR Scope

### 3.1 必须进入 ADR 的范围

下列变化原则上必须经过 ADR：

- Product/SRS 的核心定位、系统边界或高风险内容边界；
- Bounded Context、Aggregate、Identity、Version 或 Immutable Object Rules；
- Application Service、Saga、Event、Transaction 或 Consistency Strategy；
- API Resource、Version、Authentication、Authorization、Error 或 Compatibility Contract；
- Primary Data Store、Cache、Broker、Search、Storage、Deployment 或 Observability 架构；
- Security、Privacy、Consent、Encryption、Audit 或 Threat Model；
- Model Gateway、Provider、Model Routing、Prompt、RAG、Embedding、Citation、AI Evaluation 或 Tool；
- Test Pyramid、Release Quality Gate、正式 SLO/RPO/RTO 或跨区域运行；
- 已批准基线的任何重大修改。

### 3.2 通常不需要 ADR

- 不改变公共契约的局部重构；
- 已批准框架内的可逆实现细节；
- 缺陷修复且恢复原基线语义；
- 小型依赖补丁且不改变运行、安全或数据边界；
- 文案、拼写、格式和非实质元数据更正；
- 已有 ADR 明确授权范围内的实施选择。

### 3.3 边界不清时

Owner 先提交轻量 Architecture Triage。若变化影响两个以上 Context、正式数据、外部契约、安全隐私、AI 供应商、不可变历史或回滚成本高，则默认需要 ADR。

### 3.4 不得用 ADR 扩权

ADR 不能替代法律授权、用户 Consent、命理专家确认、预算批准或生产变更审批。它只能记录架构结论及前置条件。

---

## 4. ADR Governance Model

### 4.1 治理层级

| 层级 | 职责 | 产出 |
|---|---|---|
| Proposer | 提出问题、选项和证据 | Draft ADR |
| Accountable Owner | 对范围、质量和后果负责 | Review-ready ADR |
| Domain Reviewers | 验证 Context、Aggregate、规则与语言 | Domain Opinion |
| Cross-Cutting Reviewers | 安全、隐私、AI、数据、运维、测试 | Impact Opinions |
| Architecture Council | 审核跨基线一致性与技术方向 | Accept/Reject/Return |
| Business/Legal/Expert Gate | 对产品、法律或命理前提作决定 | Required Approval/Block |
| Baseline Custodian | 批准后更新相关基线与索引 | Baseline Revision |
| Implementation Owner | 按 ADR 迁移、测试与回滚 | Delivery Evidence |

### 4.2 决策权限

局部且可逆决定由相应架构 Owner 批准；跨 Context、基线、安全隐私、重大 AI、数据迁移、正式 SLO/RPO/RTO 或跨区域决定由 Architecture Council 与对应 Gate Owner 联合批准。

### 4.3 职责分离

提案人可以是 Owner，但高风险 ADR 不能由一人独立提出、评审和批准。安全隐私、数据删除、AI 高风险、命理规则或法律结论需要独立 Reviewer。

### 4.4 决策会议

会议用于解决分歧，最终决定仍以 ADR 中记录的版本为准。口头结论只有写入并完成审批后才生效。

### 4.5 Governance Gate

未批准 ADR 不得改变 Domain、Data、Context、API、Security、AI 或 Testing Baseline。代码、配置或部署已经存在也不能使未批准决策自动合法化。

---

## 5. ADR Lifecycle

### 5.1 生命周期

`Candidate → Draft → In Review → Accepted / Rejected / Withdrawn → Implementing → Verified → Active → Superseded / Deprecated`

状态并非所有 ADR 都必须逐一经历；例如 Rejected 不进入实施，Accepted 的纯治理决定可以在基线更新后直接 Verified。

### 5.2 Candidate

问题已识别但证据、Owner、选项或时机不足。Candidate 不允许改变现状。

### 5.3 Draft

Owner 已确认，Context、Problem、Drivers、Options 和初步影响齐备，可供协作完善。

### 5.4 In Review

内容冻结到一个评审版本，必需 Reviewer 已邀请，PoC/测试/法律等证据可访问。评审期间的实质修改产生新评审版本。

### 5.5 Accepted

所有必需批准完成，决定可进入基线更新与实施。Accepted 不代表实施已经完成。

### 5.6 Implementing and Verified

Implementing 表示迁移进行中；Verified 表示实施、测试、可观察性、迁移和回滚证据满足 ADR。基线更新与实际行为必须一致。

### 5.7 Active

决定已成为当前有效架构约束。若 ADR 仅批准未来能力但尚未启用，应保持 Accepted/Implementing 而非误标 Active。

### 5.8 Superseded and Deprecated

Superseded 表示新 ADR 替代其决策语义；Deprecated 表示仍在兼容期但不用于新设计。历史记录保留且指向替代 ADR。

---

## 6. ADR Status Model

| Status | 含义 | 是否允许指导新实施 | 是否可原地改决策 |
|---|---|---:|---:|
| Candidate | 待评估事项 | No | Yes，尚非 ADR 正式结论 |
| Draft | 提案编写中 | No | Yes，保留版本历史 |
| In Review | 正式评审中 | No | 仅新评审版本 |
| Accepted | 已批准，待/可实施 | Yes | No |
| Rejected | 选项未获批准 | No | No |
| Withdrawn | 提案人撤回 | No | No |
| Implementing | 批准方案迁移中 | 仅按迁移范围 | No |
| Verified | 已验证，待正式激活/基线闭环 | Yes | No |
| Active | 当前有效决定 | Yes | No |
| Deprecated | 不用于新设计，兼容期保留 | Restricted | No |
| Superseded | 已被新 ADR 替代 | No | No |

### 6.1 Baseline-Inherited Status

本文件的 `ADR-BL-*` 使用 `Accepted — Baseline-Inherited`。它表示来源基线已 Approved，不表示曾存在独立 ADR 审批记录。未来若被替代，必须创建正式 ADR。

### 6.2 状态变更规则

每次状态变化记录 Actor、时间、理由、审批和关联证据。Rejected、Withdrawn、Deprecated 和 Superseded 记录不得删除。

---

## 7. ADR Numbering Convention

### 7.1 正式新 ADR

未来正式 ADR 使用：`ADR-NNNN`，四位连续序号，例如 `ADR-0001`。编号全局唯一、永久存在、不得重用，不编码 Context、日期、状态或版本。

### 7.2 基线继承决策

本文件当前登记使用：`ADR-BL-NNN`。`BL` 明确表示 Baseline-Inherited 摘要，不占用未来正式 ADR 序号。

### 7.3 候选登记

候选使用：`ADR-CANDIDATE-{AREA}-NNN`，其中 AREA 仅用于索引分类，不是永久正式 Identity。候选进入 Draft 时分配新的 `ADR-NNNN`，并保留 Candidate 关联。

### 7.4 编号规则

- 编号只表示稳定身份，不表示优先级、时间、版本或依赖顺序；
- 被拒绝或撤回的正式编号不回收；
- 一个 ADR 只做一个可清晰命名的决定；
- 多个强耦合决定可以建立 Related ADR，但不得用一个“超级 ADR”掩盖独立审批。

---

## 8. ADR Template

未来独立 ADR 至少包含以下逻辑字段；本文不创建独立文件或模板资产。

| Field | Required Content |
|---|---|
| ADR ID | 全局唯一、不可重用的正式编号 |
| Title | 使用决定性、可搜索的标题 |
| Status | 当前生命周期状态 |
| Date | 创建、决定和最近状态变化日期 |
| Owner | 单一 Accountable Owner |
| Reviewers | 必需与实际 Reviewer、职责 |
| Context | 业务、领域、技术和历史背景 |
| Problem | 要解决的具体问题与不做事项 |
| Decision Drivers | 需求、约束、质量、成本、合规和时机 |
| Options | 至少包含维持现状及可行替代 |
| Decision | 被批准的选择和边界 |
| Rationale | 选择原因及证据 |
| Positive Consequences | 获益与能力 |
| Negative Consequences | 成本、限制、债务与复杂度 |
| Risks | 发生条件、影响、缓解和 Owner |
| Security Impact | 身份、权限、攻击面、Secret、供应链 |
| Privacy Impact | 数据分类、Purpose、Consent、Retention、Region、权利 |
| AI Impact | Provider、Model、Prompt、RAG、Validation、Cost、Risk |
| Data Impact | Identity、Version、Migration、Delete、Audit、Consistency |
| API Impact | Resource、Contract、Compatibility、Error、Version |
| Operations Impact | Deployment、Capacity、SLO、DR、Observability、Runbook |
| Testing Impact | Suite、Dataset、Contract、Performance、安全与 Gate |
| Migration Plan | 分阶段、兼容、数据、Owner、停止条件 |
| Rollback Plan | 回退点、数据兼容、时限、验证和不可逆部分 |
| Observability | 成功/失败指标、日志、追踪、告警、审计 |
| Approval | 决策人、意见、条件和日期 |
| Review Trigger | 规模、事故、法规、供应商、时间或指标触发 |
| Related ADR | Depends On、Supersedes、Conflicts With、Related To |
| Related Documents | 需求、基线、测试、Threat Model、Runbook 等 |

### 8.1 Template Quality Rule

不适用字段写明 `Not Applicable` 及理由，不留空。未批准候选不得填写成决定语气。

---

## 9. ADR Creation Criteria

### 9.1 Mandatory Criteria

满足任一条件应创建 ADR：

- 修改 Approved Baseline；
- 改变 Bounded Context、Aggregate、跨 Context 依赖或事务；
- 改变 Identity、Version、Immutable 或历史重现规则；
- 引入/替换关键数据库、Broker、Cache、Search、Storage、Provider、模型或部署模型；
- 改变 Authentication、Authorization、Encryption、Consent、Audit 或数据区域；
- 改变 API/Event Compatibility 或公共 Error Contract；
- 需要不可逆数据迁移、长兼容期或多团队协调；
- 改变正式 SLO、RPO/RTO、Release Gate 或安全边界；
- 事故揭示当前架构原则必须改变。

### 9.2 Decision Test

创建前回答：影响是否超过一个模块、是否难以回滚、是否影响用户/数据/合规、是否形成长期先例、未来团队是否会问“为什么”。多数答案为“是”时，应使用 ADR。

### 9.3 Duplicate Control

先检索 Current Register、Candidate、Rejected 与 Superseded ADR。若问题已覆盖，更新关联证据或创建 Superseding ADR，不复制平行决定。

### 9.4 Emergency Trigger

Incident 中可先采取最小安全缓解，但永久架构变化必须进入 Emergency ADR/Exception 流程，不能用紧急状态绕过治理。

---

## 10. ADR Approval Process

### 10.1 标准流程

1. 提交 Candidate/Triage；
2. 指定 Owner 与决策截止条件；
3. 编写 Context、Problem、Drivers 和 Options；
4. 完成影响、风险、迁移、回滚和证据；
5. 识别必需 Reviewer 与 Gate；
6. 进入 In Review，收集书面意见；
7. 解决分歧或记录少数意见；
8. Architecture Council 作 Accept/Reject/Return；
9. 完成必要业务、法律、专家和预算批准；
10. 更新状态与索引；
11. Accepted 后更新受影响 Baseline；
12. 实施、测试、迁移并 Verified；
13. 进入 Active 或按条件复审。

### 10.2 Approval Conditions

批准可以附带前置条件、范围、有效期、试验阶段或停止条件。条件未满足时不得把 ADR 标为 Active。

### 10.3 Disagreement

分歧以 Drivers、证据和后果讨论。无法达成一致时由 Accountable Decision Authority 裁决，并保留不同意见；不得通过模糊措辞假装一致。

### 10.4 Baseline Update Gate

ADR Accepted 之后、相关基线更新之前，旧基线仍是当前规范；若迁移需要双轨，ADR 必须明确兼容窗口和 Source of Truth。

---

## 11. ADR Review Roles

| Role | 必须评审的主题 | 可阻断条件 |
|---|---|---|
| CTO / Architecture Council | 跨基线、长期方向、重大成本 | 基线冲突、证据不足 |
| Product Owner | 用户价值、范围、版本、体验 | 违背 Product/SRS |
| Domain Architect | Context、Aggregate、语言、不变量 | 破坏领域边界 |
| Data Architect | Identity、Version、Migration、Delete | 数据不可恢复/不可追溯 |
| Application/API Architect | Use Case、Saga、Contract、Compatibility | 跨事务或 Breaking 未治理 |
| Technology/Operations | Runtime、依赖、容量、SLO、DR | 不可运营/不可恢复 |
| Security Owner | Threat、Auth、Secret、供应链 | 不可接受安全风险 |
| Privacy/Legal Owner | Purpose、Consent、Region、Retention、权利 | 缺少合法依据或评审 |
| AI Owner | Provider、Model、Prompt、RAG、Validation | 无评估、无版本或越界 |
| Test/Quality Owner | 可测试性、Gate、回归、证据 | 关键风险不可验证 |
| 命理专家 | 算法、规则、术语与争议 | 擅自确定待确认规则 |
| Finance/Cost Owner | 供应商、容量、单位成本 | 无预算或退出策略 |

### 11.1 Reviewer Selection

Reviewer 由影响矩阵决定，不要求所有角色评审每个 ADR。涉及 Restricted Sensitive 数据、AI 高风险主题或历史不可变对象时，对应 Reviewer 必选。

---

## 12. ADR Impact Analysis

### 12.1 影响维度

每个 ADR 至少判断：Product、SRS、Context、Domain、Data、Application、API/Event、Technology、Operations、Security、Privacy、AI、Testing、Cost、People/Process 和 Timeline。

### 12.2 Impact Matrix

| Dimension | Questions |
|---|---|
| Domain | 是否改变 Aggregate、生命周期、不变量、语言或所有权 |
| Data | 是否改变 Identity、Version、Immutability、Delete、Audit、Migration |
| Integration | 是否改变 Event、Idempotency、Ordering、Consistency、Provider |
| API | 是否 Breaking、需要新 Version、Sunset 或 Client Migration |
| Security | 是否增加攻击面、权限、Secret 或供应链风险 |
| Privacy | 是否新增 Purpose、Recipient、Region、Retention 或识别风险 |
| AI | 是否改变 Model/Prompt/RAG/Citation/Validation/Cost |
| Operations | 是否影响容量、部署、SLO、DR、On-call、Vendor |
| Testing | 是否需要新 Dataset、Contract、性能、安全或 Gate |
| Organization | 是否需要新 Owner、技能、支持或职责分离 |

### 12.3 Change Surface

列出直接受影响基线、模块、数据对象、消费者、环境、供应商和发布阶段。禁止只写“无影响”而不给出验证依据。

### 12.4 Compatibility Window

涉及双写、双读、版本共存或消费者迁移时，明确起止条件、权威来源、差异检测和退役门禁。

---

## 13. ADR Alternatives Analysis

### 13.1 最低要求

至少比较：

- Option 0：维持现状/不做；
- Option 1：主要候选；
- Option 2：一个现实可行替代（若存在）。

### 13.2 比较维度

按业务适配、领域一致性、安全隐私、可靠性、性能、成本、可逆性、团队能力、供应商锁定、迁移和时间比较。权重与不妥协约束在评审前声明。

### 13.3 Evidence

可以使用基准测试、PoC、Threat Model、容量数据、成本模型、用户研究、事故记录、法律意见或专家评审。营销材料和单一主观偏好不能单独支撑重大决定。

### 13.4 Rejected Alternatives

保留被拒选项、拒绝原因和适用前提。未来条件变化时可复审，但不能删除旧分析以强化当前结论。

---

## 14. ADR Risk Analysis

### 14.1 风险结构

每项风险记录 Trigger、Likelihood、Impact、Detectability、Mitigation、Residual Risk、Owner 和 Review Trigger。评分模型可以后续确定，但定义必须稳定。

### 14.2 必测风险

- 数据丢失、污染、重复和不可恢复；
- 权限绕过、隐私泄漏和 Purpose 扩张；
- 跨 Context 耦合和 Source of Truth 混乱；
- Provider/模型/供应商锁定；
- 迁移失败、回滚无效和兼容期失控；
- 性能、容量、成本和运营复杂度；
- AI 幻觉、引用失配、Prompt Injection 和 Drift；
- 测试无法证明关键后果。

### 14.3 Residual Risk Acceptance

残余风险由有权限的 Owner 接受，不能由提案作者代替业务、安全、法律或运营承担。Critical 风险无有效缓解时不得批准。

---

## 15. ADR Security and Privacy Review

### 15.1 Security Review Trigger

Authentication、Authorization、Session/Token、Encryption、Key/Secret、Network、WAF、Provider、Tool、Audit、生产访问或供应链变化必须安全评审。

### 15.2 Privacy Review Trigger

新增数据类别、Purpose、Recipient、跨境/区域、Retention、训练/优化用途、用户导出删除、Legal Hold、去标识或可重新识别风险必须隐私与法律评审。

### 15.3 Required Evidence

更新 Data Flow、Threat Model、权限矩阵、数据分类、Retention、Deletion、Provider 条款、安全测试和 Incident/Exit 计划。若缺少目标地区法律结论，ADR 保持 In Review 或附阻断条件。

### 15.4 No Security Exception by Architecture

ADR 不能通过“内部系统”或“低流量”理由取消 TLS、最小权限、MFA、Audit、Consent 或敏感数据保护。

---

## 16. ADR AI Review

### 16.1 AI Review Trigger

Provider、Model、Routing、Prompt、RAG、Embedding、Reranker、Context、Cache、Validation、Model-as-Judge、Fallback、Tool、Cost 或 Evaluation 变化必须 AI Review；涉及数据还需安全隐私评审。

### 16.2 Required AI Evidence

- Task/Scope 与不做事项；
- Model/Prompt/Knowledge/Validation 版本策略；
- Grounding、Citation、Risk 和 Hallucination 评估；
- Provider Region、Retention、Training、Subprocessor 与 Exit；
- Token/Context/Cost、Timeout、Retry、Circuit 和 Degradation；
- Golden/Adversarial/Human Evaluation 与 Drift；
- Fallback 是否保持新 AIAnalysis 和历史可追溯。

### 16.3 AI Non-Negotiables

AI 不计算命盘事实、不创建 Evidence、不扩大 Scope；Raw Output 不可信；正式结果必须验证；不得跨用户复用私人上下文 Cache；不得静默更换模型或 Prompt。

### 16.4 Scientific Claim Boundary

AI ADR 不得把用户认同、模型一致或专家规则转化为科学预测准确率。

---

## 17. ADR Testing Requirements

### 17.1 Test Impact

每个 Accepted ADR 明确新增、修改和退役哪些 Unit、Domain、Contract、Integration、API、AI/RAG、安全、性能、可靠性和 E2E 测试。

### 17.2 Decision Validation

ADR 在 Accepted 前可以要求 PoC；在 Active 前必须满足正式 Test Evidence。PoC 结论不自动等于生产质量通过。

### 17.3 Baseline Comparison

迁移前建立旧方案基线；迁移中比较正确性、性能、成本、风险和可恢复性；不能只证明新方案“能运行”。

### 17.4 Release Gate

ADR 不能降低 14 中不可豁免的 Domain、权限、Consent、不可变历史、事实引用、安全隐私和发布门禁。若需改变 Gate，本身需要独立 ADR。

### 17.5 Test Traceability

ADR ID 进入测试计划、Dataset、结果和 Release Evidence；失败与例外反向关联 ADR 风险和 Rollback 条件。

---

## 18. ADR Migration Requirements

### 18.1 Migration Plan Minimum

迁移计划至少定义：范围、阶段、Owner、依赖、兼容、数据、流量、验证、停止条件、回滚点、用户影响、支持和退役。

### 18.2 Data Migration

涉及数据时说明 Source/Target、Identity/Version 映射、不可变历史、双写/双读、校验、删除墓碑、Audit、备份和恢复。禁止覆盖 Frozen/Published/Completed 历史对象。

### 18.3 API/Event Migration

说明 Version、消费者清单、兼容窗口、Sunset、重放、Idempotency 和错误语义。不得在同一 Contract Version 中静默改变含义。

### 18.4 Operational Migration

定义容量、观察窗口、Canary、告警、Runbook、On-call、供应商支持、成本和退出。迁移期间保留安全与隐私控制。

### 18.5 Completion

只有数据与消费者收敛、旧路径停止、证据保存和基线更新完成，迁移才可关闭。

---

## 19. ADR Rollback Requirements

### 19.1 Rollback Minimum

明确触发指标、决策人、可回退窗口、操作范围、数据兼容、用户影响、验证和沟通。只写“回滚发布”不充分。

### 19.2 Data Rollback

优先采用前向修复和可兼容迁移。若数据变化不可逆，必须在批准前明确并提供备份、恢复、双轨或补偿策略。

### 19.3 AI/Provider Rollback

回滚到已发布且兼容的 Prompt/Model/Route；不得在原 AIAnalysis 中静默换模型。历史结果保留原 Version Manifest。

### 19.4 Security Rollback

回滚不能恢复已撤销 Credential、扩大权限、重新暴露删除数据或关闭必要安全控制。

### 19.5 Rollback Test

高风险 ADR 在 Active 前演练回滚或说明无法演练的风险与补偿。回滚成功需验证业务、数据、Audit 和可观察性。

---

## 20. ADR Supersede and Deprecation

### 20.1 Supersede

新 ADR 明确 `Supersedes ADR-XXXX`，旧 ADR 标为 Superseded 并链接新记录。旧内容不删除、不改写。

### 20.2 Partial Supersede

若只替代部分决定，列出保留与替代段落；避免产生两个都声称 Active 的冲突结论。

### 20.3 Deprecation

兼容期内旧决定标为 Deprecated，说明新实施禁令、现有消费者、Sunset、迁移 Owner 和风险。

### 20.4 Rejection Revisit

条件变化可用新 ADR 重新评估已拒选项，并引用原记录；不把旧 Rejected 状态改为 Accepted。

### 20.5 Baseline Closure

替代完成后更新所有受影响 Baseline、Register、测试、Runbook 和文档引用，避免 ADR 已变但基线仍旧。

---

## 21. ADR Relationship with Baselines

### 21.1 Authority Order

在无冲突时，Approved Product/SRS 定义目的与需求，Architecture Baseline 定义当前设计约束，Accepted ADR 授权未来变更，更新后的 Approved Baseline 成为实施长期依据。

### 21.2 ADR Does Not Silently Override

Accepted ADR 在基线更新完成前不能被解释为已静默改写全部文档。迁移窗口的优先规则必须在 ADR 中明确。

### 21.3 Baseline Change Procedure

1. ADR Accepted；
2. 标记受影响文档与章节；
3. 形成显式基线修订；
4. 完成跨文档一致性评审；
5. 新版本 Approved；
6. 更新 ADR Index 和 Traceability；
7. 实施按新基线验证。

### 21.4 Baseline Conflict

若两个 Approved 文档冲突，登记 `BASELINE-CONFLICT-NNN`，说明来源、不可同时满足点、当前安全行为、Owner 和解决 ADR。不得由较新的普通段落自动覆盖较早 Approved 规则，除非版本治理明确。

### 21.5 Roadmap Boundary

Roadmap 只决定实施顺序，不修改 Domain、Data 或 Context。排期不能替代 ADR。

---

## 22. ADR Repository and Index

### 22.1 当前阶段

本文件是当前统一治理与索引文档。本阶段不创建独立 ADR 文件、新目录或项目结构。

### 22.2 未来逻辑 Repository

未来获准创建独立 ADR 后，应在受版本控制、可评审、可搜索、不可静默覆盖的架构文档区域保存；具体物理路径与工具在工程实施阶段决定。

### 22.3 Index Fields

索引至少记录 ADR ID、Title、Status、Owner、Decision Date、Area、Related Baselines、Supersedes/Depends On、Review Trigger 和最近复审日期。

### 22.4 Search and Discovery

按 ID、标题、Context、状态、Owner、基线、风险和技术主题检索。Rejected、Withdrawn、Deprecated 和 Superseded 仍出现在索引中。

### 22.5 Access

默认团队可读；编辑和状态变更受职责与审计控制。含安全敏感细节的附件可限制访问，但主 ADR 保留可理解的决定与后果。

---

## 23. ADR Audit and Traceability

### 23.1 Audit Events

记录创建、提交评审、内容版本、评论解决、批准、拒绝、撤回、状态变化、例外、复审、替代和基线更新。

### 23.2 Trace Graph

最小追踪关系：`Requirement → ADR → Baseline Revision → Implementation Change → Test Evidence → Release → Metric/Incident → Review`。

### 23.3 Integrity

Approved ADR 和审批证据不原地删除。更正拼写或链接时留下 Change Note；实质变化创建新 ADR。

### 23.4 Sensitive Information

ADR 不包含 Secret、完整攻击细节、真实 PII、用户命例正文、Prompt 内容或 Provider Credential。受限证据通过安全引用关联。

### 23.5 Review Evidence

每次复审记录触发原因、当前事实、结论、Owner 和下一触发点。无变化也记录“继续有效”的依据，而非机械更新时间。

---

## 24. ADR Exception Process

### 24.1 适用范围

Exception 只用于临时、有限、可撤销且有明确风险的偏离，不能永久绕过 ADR 或改变基线。

### 24.2 Required Fields

Exception 记录 Scope、Reason、Risk、Compensating Control、Owner、Approver、Start、Expiry、Exit、Monitoring 和 Related ADR/Baseline。

### 24.3 Prohibited Exceptions

不得用例外取消用户 Consent、跨用户隔离、最小权限、关键 Audit、不可变历史、事实/引用 Validation、法律阻断或 Critical 安全修复。

### 24.4 Emergency Exception

Incident 中可批准最小临时偏离，必须限时、持续监控并在恢复后复盘。若偏离需要长期保留，立即创建正式 ADR。

### 24.5 Expiry

到期自动失效，不自动续期。续期需要重新评估事实、风险和退出计划；连续续期触发 Architecture Council 审查。

---

## 25. Current Approved Decision Register

### 25.1 登记语义

以下 31 项均直接继承 01～14 Approved 1.0。状态统一为 `Accepted — Baseline-Inherited`。它们不是本文件新作出的选择，也不代表存在历史独立 ADR。Owner 为当前治理责任角色，不虚构个人姓名。

### ADR-BL-001 — Modular Monolith First

- **Decision ID：** ADR-BL-001
- **Decision Title：** Modular Monolith First
- **Context：** MVP 领域仍演进，团队需要低运维复杂度、清晰模块边界和快速交付。
- **Decision：** 第一阶段采用模块化单体；Web、API、Worker、Scheduler 可独立运行与扩缩，但属于同一应用版本和架构边界，不提前拆微服务。
- **Rationale：** 降低分布式复杂度，同时保留 Context、契约与未来拆分能力。
- **Alternatives Considered：** 初始微服务；无模块分层单体；维持模块化单体。
- **Consequences：** 部署与事务更简单；必须用依赖、数据所有权和治理防止演变为大泥球。
- **Risks：** 跨模块私有访问、共享数据库滥用、团队误把运行单元当微服务。
- **Related Documents：** 03、06、09、10。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** CTO / System & Technology Architecture Owner。
- **Review Trigger：** 量化的规模、团队、合规、故障隔离或 SLO 证据表明需拆分。

### ADR-BL-002 — Domain-Driven Design

- **Decision ID：** ADR-BL-002
- **Decision Title：** Domain-Driven Design
- **Context：** 命理规则、计算、证据、AI、报告与隐私具有不同语言、生命周期和所有权。
- **Decision：** 使用 DDD 统一语言、Bounded Context、Entity、Value Object、Aggregate、Domain Service、Repository 与 Domain Event 组织核心业务。
- **Rationale：** 保护复杂业务语义，避免基础设施或 AI 取代领域规则。
- **Alternatives Considered：** 数据表驱动 CRUD；框架驱动分层；DDD。
- **Consequences：** 边界和可测试性增强；团队需持续维护语言、模型与映射。
- **Risks：** 形式化过度、贫血模型、领域逻辑泄漏到应用/基础设施。
- **Related Documents：** 03、04、07、10、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Domain Architecture Owner。
- **Review Trigger：** 领域语言、核心模型或团队组织发生重大变化。

### ADR-BL-003 — Bounded Context Isolation

- **Decision ID：** ADR-BL-003
- **Decision Title：** Bounded Context Isolation
- **Context：** Identity、Consent、Birth、Calculation、Rule、Evidence、Knowledge、AI、Report 等职责不同。
- **Decision：** 每个 Context 拥有自己的模型、数据与一致性；其他 Context 不直接修改其内部状态。
- **Rationale：** 保持自治、所有权、可演进和安全边界。
- **Alternatives Considered：** 全局共享领域模型；按技术层共享对象；Context Isolation。
- **Consequences：** 依赖通过公开契约、Snapshot 或 Event；需要处理最终一致和 Projection 延迟。
- **Risks：** 模块名存在但数据/Repository 仍共享，形成伪隔离。
- **Related Documents：** 03、04、05、07、09。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Domain / Application Architecture Owner。
- **Review Trigger：** Context 职责、关系、所有权或部署拆分变化。

### ADR-BL-004 — Aggregate Root Only Cross-Context Reference

- **Decision ID：** ADR-BL-004
- **Decision Title：** Aggregate Root Only Cross-Context Reference
- **Context：** 跨 Context 长期引用内部 Entity 会破坏聚合一致性与自治。
- **Decision：** Context 间只引用 Aggregate Root Identity；必要历史事实通过不可变 Snapshot、Domain Event 或 Root 发布的只读引用交换。
- **Rationale：** 防止跨 Context 直接装载、修改或共同拥有内部 Entity。
- **Alternatives Considered：** 外键直连所有 Entity；共享 ORM 关系；Root Identity/Snapshot/Event。
- **Consequences：** 关系更稳定；查询可能需要 Projection 和显式组装。
- **Risks：** 将 Snapshot Exchange 误实现为内部 Entity 共享；跨库 Join 绕过边界。
- **Related Documents：** 04、05、07、10、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Domain & Data Architecture Owner。
- **Review Trigger：** 新跨 Context 关系、查询或数据迁移要求。

### ADR-BL-005 — Deterministic Calculation Before AI

- **Decision ID：** ADR-BL-005
- **Decision Title：** Deterministic Calculation Before AI
- **Context：** 命盘事实必须可复现，模型不适合作为历法和四柱事实来源。
- **Decision：** 时间标准化和确定性 Chart Calculation 先完成并锁定 CalculationSnapshot，AI 只解释已存在事实。
- **Rationale：** 保证相同输入、参数和版本可重现，AI 不补造事实。
- **Alternatives Considered：** 模型直接排盘；模型与算法混合生成；确定性先行。
- **Consequences：** AI 可替换和降级；计算算法与版本需独立治理。
- **Risks：** AI Prompt 重复计算；错误 Snapshot 被后续放大。
- **Related Documents：** 02、03、04、07、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Chart Calculation / AI Architecture Owner。
- **Review Trigger：** Calculation Boundary、Algorithm 或 AI 输入权威变化。

### ADR-BL-006 — Rule Evaluation Before Evidence

- **Decision ID：** ADR-BL-006
- **Decision Title：** Rule Evaluation Before Evidence
- **Context：** Evidence 必须说明哪些规则判断基于哪些确定性事实，而不能由模型倒推。
- **Decision：** RuleSetVersion 对 CalculationSnapshot 完成 RuleRun，形成 RuleFinding 与冲突后，EvidenceBuilder 才构建 EvidenceBundle。
- **Rationale：** 建立事实→规则→证据的单向可追溯链。
- **Alternatives Considered：** AI 先解释再补证据；规则与证据混合对象；分阶段构建。
- **Consequences：** 证据来源清晰；规则完整性失败会阻断下游正式分析。
- **Risks：** RuleFinding 与 Evidence 职责混淆；循环依赖 Timeline/Evidence。
- **Related Documents：** 03、04、05、07、13。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Rule Evaluation / Evidence Context Owner。
- **Review Trigger：** RuleRun、EvidenceBuilder 或分析依赖方向变化。

### ADR-BL-007 — Frozen Evidence Before AI

- **Decision ID：** ADR-BL-007
- **Decision Title：** Frozen Evidence Before AI
- **Context：** AI 正式分析需要稳定、完整、版本化且不可在生成中变化的证据输入。
- **Decision：** AIAnalysis 只能引用 Frozen EvidenceBundle；冻结后不得新增 Evidence，变化需创建新 Bundle/Analysis。
- **Rationale：** 保证输出可复现、引用稳定和证据不被模型生成结果反向污染。
- **Alternatives Considered：** AI 读取实时可编辑证据；AI 创建证据；先冻结再分析。
- **Consequences：** 历史可靠；证据变更需要新版本与新任务。
- **Risks：** 冻结前遗漏；通过旁路读取未冻结 Evidence。
- **Related Documents：** 04、05、07、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Evidence / AI Context Owner。
- **Review Trigger：** Evidence Lifecycle、AI Input 或 Reanalysis 语义变化。

### ADR-BL-008 — AI Raw Output Is Untrusted

- **Decision ID：** ADR-BL-008
- **Decision Title：** AI Raw Output Is Untrusted
- **Context：** 模型输出可能结构错误、幻觉、越界、引用失配或泄漏敏感内容。
- **Decision：** Provider 原始输出不是正式领域结果，必须通过结构、事实、Evidence、Citation、冲突、风险、泄漏和长度 Validation。
- **Rationale：** AI 概率输出不能直接进入用户报告或正式历史。
- **Alternatives Considered：** 原样展示；仅模型自检；平台多层 Validation。
- **Consequences：** 安全与可信度提高；增加延迟、成本和拒绝/降级路径。
- **Risks：** Validator 漏检、Repair 扩大范围、团队把生成成功等同完成。
- **Related Documents：** 07、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI / Security / Quality Owner。
- **Review Trigger：** Output Contract、Validation、Risk 或展示边界变化。

### ADR-BL-009 — Model Gateway as Only Provider Entry

- **Decision ID：** ADR-BL-009
- **Decision Title：** Model Gateway as Only Provider Entry
- **Context：** 直接调用 Provider 会分散安全、隐私、成本、版本和可靠性控制。
- **Decision：** 所有正式模型调用必须经过平台 Model Gateway。
- **Rationale：** 集中执行去标识、路由、计量、Timeout、Retry、Circuit、Audit 和策略。
- **Alternatives Considered：** 各模块直连；共享 SDK；统一 Gateway。
- **Consequences：** 控制一致、供应商可替换；Gateway 成为关键容量和可靠性组件。
- **Risks：** 单点、God Gateway、旁路调用。
- **Related Documents：** 03、09、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI Platform / Security Owner。
- **Review Trigger：** 新 Provider、Tool、边缘推理或调用拓扑变化。

### ADR-BL-010 — Provider Abstraction

- **Decision ID：** ADR-BL-010
- **Decision Title：** Provider Abstraction
- **Context：** Provider SDK、错误、能力、区域和计费存在差异并可能变化。
- **Decision：** 核心应用依赖稳定平台能力与 Provider Adapter，不依赖供应商私有 Payload/SDK。
- **Rationale：** 降低锁定并支持合规、成本和故障切换评估。
- **Alternatives Considered：** 单供应商深度耦合；最低公分母抽象；能力导向 Adapter。
- **Consequences：** 可替换性提高；需要维护能力差异、兼容与契约测试。
- **Risks：** 抽象泄漏、过度通用、隐藏供应商独特风险。
- **Related Documents：** 09、10、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI / Technology Architecture Owner。
- **Review Trigger：** Provider 能力、合同、区域、SDK 或 Exit 条件变化。

### ADR-BL-011 — Version Everything Affecting Meaning

- **Decision ID：** ADR-BL-011
- **Decision Title：** Version Everything Affecting Meaning
- **Context：** 算法、规则、知识、Prompt、模型和风险策略变化会改变正式结果含义。
- **Decision：** 正式结果记录所有影响语义的 Identity 与 Version Manifest，历史不被新版本静默覆盖。
- **Rationale：** 支持复现、审计、比较、回滚与责任定位。
- **Alternatives Considered：** 只保存当前版本；只保存输出文本；完整版本清单。
- **Consequences：** 数据和治理成本增加；历史可解释、可重现。
- **Risks：** Identity/Version 混用、供应商无稳定版本、清单缺失。
- **Related Documents：** 04、05、07、08、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Domain / Data / AI Architecture Owner。
- **Review Trigger：** 任何影响语义的新依赖、版本模型或历史策略变化。

### ADR-BL-012 — Prompt Registry and Immutable Prompt Version

- **Decision ID：** ADR-BL-012
- **Decision Title：** Prompt Registry and Immutable Prompt Version
- **Context：** Prompt 影响 AI 含义、风险和可复现性，不能散落或静默修改。
- **Decision：** Prompt 进入受控 Registry，版本化、评审、发布、兼容、回滚；Published PromptVersion 不原地修改。
- **Rationale：** 建立审查、回归、追踪和安全控制。
- **Alternatives Considered：** Prompt 写在代码；运行时自由编辑；受控不可变 Registry。
- **Consequences：** 发布流程更严谨；物理存储仍待候选决策。
- **Risks：** 配置旁路、Prompt 泄漏、版本兼容失配。
- **Related Documents：** 07、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI Prompt Governance Owner。
- **Review Trigger：** Prompt Lifecycle、Storage、Compatibility 或审批变化。

### ADR-BL-013 — RAG Is Not Source of Truth

- **Decision ID：** ADR-BL-013
- **Decision Title：** RAG Is Not Source of Truth
- **Context：** 向量相似和检索排序只能发现候选知识，不能定义命盘事实或正式证据真相。
- **Decision：** RAG/Index 是可重建 Retrieval Projection，不是 Chart、Rule、Evidence 或 Knowledge Publication 的 Source of Truth。
- **Rationale：** 防止相似度被误当事实，保持权威对象和版本边界。
- **Alternatives Considered：** Vector Store 作为知识真相源；模型记忆；受控 Knowledge + 可重建 Index。
- **Consequences：** 可重建和撤权更安全；需要来源映射、Rights Filter 与索引一致性。
- **Risks：** 索引延迟、撤权残留、相似内容误用。
- **Related Documents：** 03、05、09、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Knowledge / AI / Data Owner。
- **Review Trigger：** Search、Embedding、Index Authority 或 Knowledge Lifecycle 变化。

### ADR-BL-014 — Claim-to-Citation Validation

- **Decision ID：** ADR-BL-014
- **Decision Title：** Claim-to-Citation Validation
- **Context：** 引用存在不代表来源支持相应结论。
- **Decision：** 正式 AI/报告的重要 Claim 必须验证 Citation 存在、权限、版本、权利和支持关系。
- **Rationale：** 防止虚假可信感与无依据断言。
- **Alternatives Considered：** 仅附来源列表；仅检查 ID；Claim-to-Citation 支持验证。
- **Consequences：** 引用质量提高；需要结构化 Claim、验证策略和拒绝/降级。
- **Risks：** 支持判定误差、过度拒绝、Rights 变化影响展示。
- **Related Documents：** 02、04、08、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Evidence / AI Quality Owner。
- **Review Trigger：** Citation Contract、Knowledge Rights 或 Validator 变化。

### ADR-BL-015 — PostgreSQL as Primary Data Store

- **Decision ID：** ADR-BL-015
- **Decision Title：** PostgreSQL as Primary Data Store
- **Context：** MVP 需要事务、关系、版本、审计索引和初期向量能力，避免过多数据系统。
- **Decision：** PostgreSQL 是第一阶段主要事务数据存储与业务真相源，并优先承载结构化、全文和已批准向量扩展能力。
- **Rationale：** 成熟一致性、查询、备份恢复和团队可运营性适合首期规模。
- **Alternatives Considered：** 多数据库拼装；文档数据库；PostgreSQL 主存储。
- **Consequences：** 技术面简化；必须保持 Context 逻辑隔离，不能共享表绕过所有权。
- **Risks：** 单库耦合、连接/容量瓶颈、误把实例共享当模型共享。
- **Related Documents：** 03、05、09、11。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Data / Technology / Operations Owner。
- **Review Trigger：** 量化容量、合规、搜索或隔离需求超出当前能力。

### ADR-BL-016 — Redis Is Not Source of Truth

- **Decision ID：** ADR-BL-016
- **Decision Title：** Redis Is Not Source of Truth
- **Context：** Cache 可能驱逐、过期或不可用，不适合唯一承载正式状态。
- **Decision：** Redis 只用于可丢、可重建的 Cache、协调或受控短期能力；正式业务状态以批准持久化来源为准。
- **Rationale：** 防止重启或驱逐导致额度、任务、报告或权限状态丢失。
- **Alternatives Considered：** Redis 唯一状态；双重真相；持久化真相 + Cache。
- **Consequences：** 故障可回源/降级；需要失效、隔离和一致性策略。
- **Risks：** 隐式依赖 Cache、跨用户 Key 冲突、Cache Stampede。
- **Related Documents：** 03、09、11、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Technology / Data Architecture Owner。
- **Review Trigger：** Cache 职责、产品或一致性策略变化。

### ADR-BL-017 — Asynchronous AI and Report Operations

- **Decision ID：** ADR-BL-017
- **Decision Title：** Asynchronous AI and Report Operations
- **Context：** AI、报告及相关验证是长耗时、可失败、需进度和恢复的操作。
- **Decision：** AIAnalysis 和 Report 生成采用持久化异步操作语义，支持受理、进度、Polling、失败、重试和降级。
- **Rationale：** 避免长连接和请求事务承载长流程，提升可靠性与用户可见性。
- **Alternatives Considered：** 全同步请求；客户端长连接即真相；持久化异步 Operation。
- **Consequences：** 需要 Queue、Worker、Operation State、幂等和可观察性。
- **Risks：** 重复任务、队列积压、进度投影被当真相源。
- **Related Documents：** 03、07、08、09、11、13。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Application / Operations Owner。
- **Review Trigger：** Operation Contract、Runtime、SLO 或交互模式变化。

### ADR-BL-018 — Outbox/Inbox and Idempotency

- **Decision ID：** ADR-BL-018
- **Decision Title：** Outbox/Inbox and Idempotency
- **Context：** 跨 Context Event、重试和至少一次投递会产生重复、乱序和部分失败。
- **Decision：** 本地事务配合 Outbox，消费者用 Inbox/幂等去重；不宣称 Exactly Once。
- **Rationale：** 在不使用跨 Context 分布式事务时保证可靠衔接与可恢复。
- **Alternatives Considered：** 2PC；假设只投递一次；Outbox/Inbox + Idempotency。
- **Consequences：** 最终一致和重复处理成为显式设计；需保留、清理和监控记录。
- **Risks：** 层层重试、Key 作用域错误、消息语义不兼容。
- **Related Documents：** 07、08、09、10、11、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Application / Technology Architecture Owner。
- **Review Trigger：** Broker、Event Contract、Transaction 或 Retry Strategy 变化。

### ADR-BL-019 — API Versioning and Problem Details

- **Decision ID：** ADR-BL-019
- **Decision Title：** API Versioning and Problem Details
- **Context：** API 需要兼容演进和稳定、安全、可本地化的错误语义。
- **Decision：** API Version 与 Domain/Resource/Event Version 分离；错误采用 Problem Details 语义和稳定平台错误码。
- **Rationale：** 保护 Client 兼容，防止内部错误与敏感信息泄漏。
- **Alternatives Considered：** 无版本；每端自定义错误；统一 Version/Problem Contract。
- **Consequences：** Breaking Change 需要新版本、迁移和 Sunset；错误注册表需治理。
- **Risks：** 版本混用、同版本语义漂移、错误细节泄漏。
- **Related Documents：** 02、07、08、10、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** API Architecture Owner。
- **Review Trigger：** URI、Version、Error、Compatibility 或 Developer API 变化。

### ADR-BL-020 — Zero Trust and Least Privilege

- **Decision ID：** ADR-BL-020
- **Decision Title：** Zero Trust and Least Privilege
- **Context：** 平台处理敏感出生资料、AI 内容和后台权限，内部网络或管理员身份不能自动可信。
- **Decision：** 每次访问基于 Actor、Subject、Resource、Purpose、Scope、环境和风险验证，并授予最小必要权限。
- **Rationale：** 减少横向移动、越权和内部滥用。
- **Alternatives Considered：** 网络边界信任；粗粒度 Role；Zero Trust + RBAC/ABAC。
- **Consequences：** 授权与审计更严格；策略、性能和运维复杂度增加。
- **Risks：** Policy 漂移、服务账号过权、只在 UI 限制。
- **Related Documents：** 07、08、09、11、12、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Security Architecture Owner。
- **Review Trigger：** Identity、Auth、Role/Attribute、生产访问或信任边界变化。

### ADR-BL-021 — Privacy by Design

- **Decision ID：** ADR-BL-021
- **Decision Title：** Privacy by Design
- **Context：** 出生时间地点与派生分析具有敏感性，匿名用户和第三方 AI 增加生命周期风险。
- **Decision：** 从收集、处理、传输、保存、导出、删除到审计默认实施最小化、目的限制、去标识和保护。
- **Rationale：** 隐私不是上线后补丁，必须成为架构约束。
- **Alternatives Considered：** 先收集后治理；仅依赖隐私政策；Privacy by Design/Default。
- **Consequences：** 数据用途和可观察性受控；需要字段级 Data Flow、Retention 和权利流程。
- **Risks：** 二次用途扩张、日志泄漏、匿名数据可重识别。
- **Related Documents：** 01、02、05、07、09、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Privacy / Security / Product Owner。
- **Review Trigger：** 数据类别、Purpose、Recipient、Region 或 Retention 变化。

### ADR-BL-022 — Consent by Purpose and Scope

- **Decision ID：** ADR-BL-022
- **Decision Title：** Consent by Purpose and Scope
- **Context：** 基础服务、优化、研究、第三方处理等用途不能用一次授权概括。
- **Decision：** SubjectConsent 按 Subject、Purpose、Scope 和 PolicyReference 管理；ConsentRecord 追加，撤回可证明且不影响无关合法服务。
- **Rationale：** 使授权具体、可撤回、可审计并符合数据最小化。
- **Alternatives Considered：** 全局布尔同意；按账户同意；按 Purpose/Scope 聚合。
- **Consequences：** 用例必须携带并重验 Purpose；策略与 UI 更复杂。
- **Risks：** 同意捆绑、Policy 静默变化、撤回传播延迟。
- **Related Documents：** 02、04、05、07、12、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Consent Context / Privacy Owner。
- **Review Trigger：** Purpose、Scope、Policy、主体关系或法律要求变化。

### ADR-BL-023 — Append-Only Audit

- **Decision ID：** ADR-BL-023
- **Decision Title：** Append-Only Audit
- **Context：** 发布、撤回、冻结、敏感访问、权限和删除等行为需要不可抵赖追踪。
- **Decision：** AuditEvent 是追加式、不可原地修改的审计事实，采用最小正文、独立权限和防篡改控制。
- **Rationale：** 支持调查、合规、责任和历史还原。
- **Alternatives Considered：** 可编辑操作日志；业务表时间戳；追加式 Audit。
- **Consequences：** 存储与保留成本增加；敏感正文必须最小化。
- **Risks：** Audit 缺口、日志与 Audit 混用、恢复时丢失历史。
- **Related Documents：** 04、05、07、09、11、12、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Governance / Security / Data Owner。
- **Review Trigger：** Audit Source、Retention、不可变归档或法律要求变化。

### ADR-BL-024 — User Deletion Saga

- **Decision ID：** ADR-BL-024
- **Decision Title：** User Deletion Saga
- **Context：** 用户数据分布于多个 Context、缓存、索引、对象、任务和第三方，无法单事务完成。
- **Decision：** 用户删除使用可恢复、幂等、逐 Context 的 Saga；处理 Legal Hold、部分失败、验证和最终 UserDeleted，不伪报完成。
- **Rationale：** 保持 Context 自治并提供数据权利可见进度和审计。
- **Alternatives Considered：** 单库级联删除；人工工单；Deletion Saga。
- **Consequences：** 删除最终一致且有中间状态；需 Tombstone、重试和 Provider 协调。
- **Risks：** 数据复活、遗漏副本、Hold 处理错误、提前标完成。
- **Related Documents：** 05、07、08、09、11、12、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Privacy / Application / Context Owners。
- **Review Trigger：** 新数据存储、Provider、Retention 或法律删除语义变化。

### ADR-BL-025 — Infrastructure as Replaceable Adapter

- **Decision ID：** ADR-BL-025
- **Decision Title：** Infrastructure as Replaceable Adapter
- **Context：** Domain/Application 不应被数据库、框架、Provider 或云产品语义控制。
- **Decision：** 基础设施通过 Port/Adapter 与核心隔离，Repository、Provider、Storage 和 Messaging 实现可替换且不泄漏入 Domain。
- **Rationale：** 保持领域稳定、测试可隔离和供应商可退出。
- **Alternatives Considered：** Framework-driven Domain；直接 SDK/ORM；Ports and Adapters。
- **Consequences：** 映射和契约成本增加；核心更可维护。
- **Risks：** Adapter 过薄导致泄漏、God Repository、抽象与实际能力不匹配。
- **Related Documents：** 03、07、09、10、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Application / Technology Architecture Owner。
- **Review Trigger：** Framework、Repository、Provider 或部署边界变化。

### ADR-BL-026 — Test Pyramid and Risk-Based Testing

- **Decision ID：** ADR-BL-026
- **Decision Title：** Test Pyramid and Risk-Based Testing
- **Context：** 平台同时包含确定性领域、外部依赖、AI 非确定性和高敏感数据。
- **Decision：** 采用以 Domain/Unit 为基础、Contract/Integration 为中层、少量关键 E2E 为顶层，并叠加风险驱动 AI、安全、性能和恢复测试。
- **Rationale：** 平衡反馈速度、真实边界验证与发布风险。
- **Alternatives Considered：** UI-only；Manual-only；均匀测试；风险驱动金字塔。
- **Consequences：** Suite 职责清晰；需要 Test Data、Flaky 和 Coverage 治理。
- **Risks：** Mock 过度、E2E 膨胀、覆盖率数字化游戏。
- **Related Documents：** 02、10、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Test / Quality Architecture Owner。
- **Review Trigger：** 系统拓扑、风险分布、发布节奏或测试反馈失效。

### ADR-BL-027 — Release Quality Gates

- **Decision ID：** ADR-BL-027
- **Decision Title：** Release Quality Gates
- **Context：** 日期压力不能替代领域、AI、安全、隐私、性能与恢复证据。
- **Decision：** Alpha、Beta、RC、GA 设可审计 Go/No-Go Gate；关键 Domain、权限、Consent、历史、引用、安全与删除门禁不可默认豁免。
- **Rationale：** 让质量结果实际约束发布，并保持 Scope Freeze。
- **Alternatives Considered：** 日期驱动发布；团队自报；正式 Quality Gates。
- **Consequences：** 发布证据更完整；可能缩小范围或延后日期。
- **Risks：** 例外滥用、假绿、Gate 过期或与制品不一致。
- **Related Documents：** 06、10、11、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** Release / Quality / Product Owner。
- **Review Trigger：** Release Model、风险容忍度、事故或 Gate Effectiveness 变化。

### ADR-BL-028 — No Direct Provider Calls

- **Decision ID：** ADR-BL-028
- **Decision Title：** No Direct Provider Calls
- **Context：** 单独模块直连 AI Provider 会绕过 Gateway 的隐私、版本、成本和可靠性策略。
- **Decision：** 禁止业务模块、Prompt Pipeline、RAG 或 Validator 绕过 Model Gateway 直接调用模型/Embedding/Reranker Provider。
- **Rationale：** 使入口控制可强制、可审计并避免隐藏调用。
- **Alternatives Considered：** 团队自律直连；共享凭据；Gateway-only。
- **Consequences：** 新能力需先纳入 Gateway/Registry；少量延迟与平台依赖。
- **Risks：** 隐藏 SDK、实验代码进入生产、Tool 成为旁路。
- **Related Documents：** 09、10、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI Platform / Security Owner。
- **Review Trigger：** 新 AI 能力、Provider、Tool 或边缘执行需求。

### ADR-BL-029 — No Cross-User AI Cache

- **Decision ID：** ADR-BL-029
- **Decision Title：** No Cross-User AI Cache
- **Context：** AI Context 可能含出生资料、命盘、Conversation 和私人分析，复用可能造成严重泄漏。
- **Decision：** 私人 AI Context、Query Embedding、Raw/Validated Output 不跨用户或 Chart 复用 Cache；Key 必须包含授权与版本边界。
- **Rationale：** 防止跨用户数据污染和隐私泄漏。
- **Alternatives Considered：** 全局语义 Cache；匿名化全局 Cache；严格私有隔离。
- **Consequences：** Cache 命中率受限；隐私边界清晰。
- **Risks：** Key 缺失 Tenant/Chart、删除后残留、相似输入误复用。
- **Related Documents：** 09、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI / Privacy / Technology Owner。
- **Review Trigger：** AI Cache Eligibility、匿名化证明或用户共享产品变化。

### ADR-BL-030 — No Silent Model Fallback

- **Decision ID：** ADR-BL-030
- **Decision Title：** No Silent Model Fallback
- **Context：** 在同一 AIAnalysis 中偷换模型会使 ModelReference、质量、成本和历史失真。
- **Decision：** 技术 Retry 保持同一 Model/Prompt/Bundle；切换 Provider/Model 的 Fallback 创建新 AIAnalysis，关联原失败并完整验证。
- **Rationale：** 保持正式结果版本真实性与失败可追溯。
- **Alternatives Considered：** 同任务透明切换；覆盖 ModelReference；新 Analysis Fallback。
- **Consequences：** 流程与用户进度更复杂；审计与质量更可靠。
- **Risks：** 重复扣费、多个结果竞争、产品错误显示完成。
- **Related Documents：** 04、05、07、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** AI Architecture / Application Owner。
- **Review Trigger：** Model Routing、Retry、Fallback、Billing 或 AIAnalysis Lifecycle 变化。

### ADR-BL-031 — No Silent Baseline Changes

- **Decision ID：** ADR-BL-031
- **Decision Title：** No Silent Baseline Changes
- **Context：** 01～14 已成为正式输入，局部文档或实现修改可能破坏跨文档一致性。
- **Decision：** 重大架构变化必须先批准 ADR，再显式修订受影响基线；聊天、代码或 Roadmap 不直接改变基线。
- **Rationale：** 保持治理、追踪、评审与团队共同事实。
- **Alternatives Considered：** Latest Document Wins；实现即事实；ADR + Baseline Revision。
- **Consequences：** 变更更可控；需要持续维护 ADR 与文档一致性。
- **Risks：** 流程被视为负担、紧急变更形成事实漂移、ADR 与基线不同步。
- **Related Documents：** 06～15 全部治理章节，尤其 06、07、08、09、12、13、14。
- **Status：** Accepted — Baseline-Inherited。
- **Owner：** CTO / Architecture Council / Baseline Custodians。
- **Review Trigger：** Governance Model、基线集合或紧急例外流程变化。

---

## 26. ADR Candidate Register

### 26.1 登记规则

以下均为 `Candidate`，不是 Approved Decision。表中的“需要决定”描述决策问题，不表达推荐答案。进入正式评审时分配 `ADR-NNNN`。

| Candidate ID | Topic | Context / 需要决定 | 主要选项（非结论） | Owner | Required Review | Trigger / 前置证据 | Status |
|---|---|---|---|---|---|---|---|
| ADR-CANDIDATE-SEC-001 | Authentication Protocol | 大陆首发的用户认证、联合身份、恢复与标准兼容协议 | 自建账户协议、标准联合协议、组合 | Security / Identity | Product、Security、Privacy、API | 用户体系、威胁、合规和恢复需求明确 | Candidate |
| ADR-CANDIDATE-SEC-002 | JWT vs Opaque Token | Access/Refresh、撤销、实时授权和网关验证语义 | JWT、Opaque、Hybrid | Security Architecture | Identity、API、Operations、Testing | Session 风险、撤销 SLO 和规模基线 | Candidate |
| ADR-CANDIDATE-SEC-003 | Field-Level Encryption | Restricted Sensitive 字段是否需应用/字段级保护 | 平台静态加密、字段级、Tokenization/组合 | Security / Data | Privacy、Operations、Performance | Threat Model、查询、轮换、恢复评估 | Candidate |
| ADR-CANDIDATE-AI-001 | AI Provider Selection | 正式生成 Provider 的区域、保留、训练、能力、SLA 与退出 | 候选供应商集合 | AI / Procurement | Security、Privacy、Legal、Cost、Ops | 合同、评估、区域和 Exit 证据 | Candidate |
| ADR-CANDIDATE-AI-002 | Primary Model Selection | 各正式 Task 的主模型与兼容矩阵 | 候选模型/任务路由 | AI Quality Owner | Prompt、Security、Cost、Testing | 固定评估集、延迟、成本和安全结果 | Candidate |
| ADR-CANDIDATE-AI-003 | Embedding Model Selection | Knowledge/Query Embedding 的模型、区域与版本 | 候选 Embedding 模型 | Knowledge / AI | Privacy、Search、Cost、Testing | Retrieval 评估、重建、Rights 和区域 | Candidate |
| ADR-CANDIDATE-AI-004 | Reranker Selection | 是否需要独立 Reranker 及实现类别 | 无 Reranker、规则、模型 Reranker | AI / Knowledge | Privacy、Cost、Testing | Ranking 基线证明必要性与收益 | Candidate |
| ADR-CANDIDATE-AI-005 | Prompt Registry Physical Storage | 已批准逻辑 Registry 的物理存储、权限与发布方式 | 版本控制文档、数据库、专用系统/组合 | AI Governance | Security、Engineering、Operations | 访问、审计、回滚和发布需求 | Candidate |
| ADR-CANDIDATE-TECH-001 | Search Engine Introduction | PostgreSQL 全文/向量何时不足，是否引入独立 Search | 维持 PostgreSQL、独立 Search、分阶段 | Technology / Knowledge | Data、Ops、Privacy、Cost | 规模、查询、重建隔离和 SLO 证据 | Candidate |
| ADR-CANDIDATE-AI-006 | Multi-Provider Active Routing | 是否从主+备用演进为生产 Active Routing | 单主、主备、主动多路由 | AI Architecture | Security、Privacy、Ops、Cost、Testing | Provider 评估、复杂度和故障收益 | Candidate |
| ADR-CANDIDATE-AI-007 | Model-as-Judge Usage | 是否及如何用于 AI Evaluation/Validation | 不使用、辅助使用、受限自动 Gate | AI Quality | Testing、Security、Product、Expert | 人工一致性、偏差、成本和校准 | Candidate |
| ADR-CANDIDATE-AI-008 | Tool Calling | 是否允许模型调用任何工具及允许范围 | 默认无 Tool、受限只读、审批动作 | AI / Security | Privacy、Domain、Operations、Legal | 明确用例、Sandbox、Allowlist、Threat Model | Candidate |
| ADR-CANDIDATE-TECH-002 | Production Orchestration Platform | 正式 Runtime 调度与容器编排平台 | 托管平台、容器编排、其他成熟运行平台 | Technology / Operations | Security、Cost、DR、Engineering | 云/区域、团队、容量和运维能力 | Candidate |
| ADR-CANDIDATE-OPS-001 | Formal SLO/RPO/RTO | 各能力正式服务与恢复目标 | 按能力分级的候选目标 | Product / Operations | Security、Privacy、Cost、Legal | 至少一个观测窗口和业务影响分析 | Candidate |
| ADR-CANDIDATE-TEST-001 | Test Framework Selection | 各层自动化与报告工具组合 | 候选框架/平台组合 | Test / Engineering | Security、Technology、Developer Experience | Repository 拓扑、语言栈和 Suite 需求 | Candidate |
| ADR-CANDIDATE-OPS-002 | Observability Vendor | 日志、指标、追踪与告警后端 | 托管、开源自管、组合 | Operations / Security | Privacy、Cost、Technology | 数据区域、Retention、规模和退出 | Candidate |
| ADR-CANDIDATE-TECH-003 | Object Storage Vendor | 报告制品与对象的正式存储供应商 | 候选云/兼容对象存储 | Technology / Operations | Security、Privacy、DR、Cost | 区域、加密、生命周期、恢复和 Exit | Candidate |
| ADR-CANDIDATE-OPS-003 | Cross-Region Deployment | 是否、何时及采用何种跨区域运行/灾备 | 单区域恢复、Cold/Warm、Active/Active 等 | Operations / Data | Legal、Security、Product、Cost | 用户区域、数据驻留、RPO/RTO 和规模 | Candidate |

### 26.2 Candidate Non-Decision Rule

候选表中选项顺序不代表推荐。没有 Accepted ADR 和相应 Baseline Revision，当前系统必须继续遵守 01～14 的既有约束与默认禁令。

---

## 27. Open Questions

### 27.1 ADR Governance

1. Architecture Council 的具体成员、代理、法定人数和决策时限。
2. 哪些局部 ADR 可由单一 Context Owner 批准，哪些必须 Council 批准。
3. 正式 ADR 的未来物理存储路径、评审工具和访问模型。
4. ADR 审批签名、时间与防篡改证据的具体保存方式。
5. 定期复审频率与未响应 Owner 的升级路径。
6. Emergency ADR 的最长有效期和事后评审时限。

### 27.2 Baseline and Migration

1. Accepted ADR 到 Baseline Revision 的最长允许窗口。
2. 迁移期 ADR 与旧/新基线的权威优先规则如何展示给开发者。
3. Baseline Conflict 的编号、严重度与阻断政策。
4. 部分 Supersede 的索引和自动一致性检查方式。
5. 哪些历史决策需要未来补充为独立正式 ADR，哪些保留 `ADR-BL-*` 即可。

### 27.3 Product, Expert and Legal

1. 高风险健康、婚姻、投资主题的最终内容边界与批准责任。
2. 旺衰、格局、调候、用神、起运、子时、真太阳时、神煞和多流派冲突的专家决策流程。
3. 数据保留、Legal Hold、跨境、AI Provider、内容标识和用户权利的目标地区法律结论。
4. 产品范围变化何时属于 Product Decision、需求变更或 Architecture ADR。

### 27.4 Candidate Prioritization

1. 哪些 Candidate 是 Phase 0/MVP 开发前阻断项。
2. Provider/Model/Embedding/Prompt Registry 决策的评估顺序与共同证据集。
3. Authentication、Token 和 Field-Level Encryption 是否合并评审或保持独立 ADR。
4. 正式 SLO/RPO/RTO 与跨区域部署的先后依赖。
5. Tool Calling 是否维持未来版本 Won't，何种产品需求才允许启动 ADR。

### 27.5 Current Baseline Review

本轮归纳未发现必须在本文件内裁决的 Baseline Conflict。若评审发现 `ADR-BL-*` 与来源文档语义不一致，应修订本登记摘要，而不是修改来源基线或把摘要视为新决定。

---

## 28. ADR Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐做法 |
|---|---|---|---|
| Decision Without Context | 只记录选了什么，不说明问题 | 后人无法判断适用边界 | 先写 Context、Problem、Drivers |
| Decision Without Alternatives | 未证明为何当前选择更合适 | 偏好冒充架构证据 | 至少比较现状和可行替代 |
| Architecture by Chat | 聊天/会议结论直接生效 | 不可追踪、参与者理解不一 | 将结论写入 ADR 并正式审批 |
| Silent Decision | 代码或配置暗中形成新架构 | 基线与现实漂移 | 变更前 Triage，重大项走 ADR |
| Retroactive ADR | 事后假装历史上已评审 | 审计失真、遗漏真实后果 | 明确“记录既有事实”与当前日期 |
| ADR as Documentation Dump | 把所有调研、实现细节堆入 ADR | 决定不清、难复审 | 主文聚焦 Context/Options/Decision/Consequences，证据外链 |
| ADR Without Owner | 多人参与但无人负责 | 阻塞、风险无人处理 | 指定单一 Accountable Owner |
| ADR Without Consequences | 只写好处 | 成本和债务上线后暴露 | 明确正负后果和残余风险 |
| ADR Never Reviewed | 条件变化后仍机械沿用 | 过时方案成为约束 | 定义 Review Trigger 并保留复审记录 |
| Editing Approved ADR in Place | 原地改变 Accepted 结论 | 历史和审批证据丢失 | 新 ADR Supersede，旧记录保留 |
| Deleting Rejected Alternatives | 删除未选方案和原因 | 重复讨论、选择偏差 | 保留 Options 和拒绝依据 |
| Implementation Detail as ADR | 每个参数/类名都建 ADR | 治理噪音、团队绕过流程 | 只记录重大、持久、跨边界决定 |
| Every Small Change as ADR | 所有变更都进入委员会 | 决策吞吐崩溃 | 使用 Creation Criteria 与局部授权 |
| No Migration Plan | 只批准终态 | 双轨、数据和消费者无法收敛 | 分阶段、兼容、验证与退役计划 |
| No Rollback Plan | 默认发布工具能回滚 | 数据/契约变化后无法恢复 | 明确回退点、窗口、数据和演练 |
| Baseline Change Without ADR | 直接编辑 Approved 文档 | 跨文档冲突与隐性破坏 | 先 ADR，再显式 Baseline Revision |
| ADR as Permission Slip | 用 Accepted 状态掩盖法律/预算缺失 | 未授权实施 | 保留 Legal/Product/Budget Gate |
| Vendor-Name-Only Decision | 只写购买哪个产品 | 无能力、退出和风险边界 | 先写需求、能力、数据、成本和 Exit |
| Giant ADR | 一个 ADR 同时决定十个独立主题 | 无法单独批准/替代/回滚 | 按决策边界拆分并建立关系 |
| Permanent Exception | 用临时例外长期绕过架构 | 风险累积、基线失效 | 设置到期、补偿和正式 ADR |
| Approval Without Evidence | 仅凭资历或偏好决定 | 性能、安全、成本未知 | 风险比例的 PoC/Test/Review |
| ADR Replaces Baseline | 认为 ADR 一经批准即无需更新文档 | 开发者面对两套规范 | 完成 Baseline Revision 与 Traceability |
| Date-Driven Decision | 为赶里程碑降低驱动和评审 | 长期代价大于延期 | 缩小范围或维持现状，不伪造批准 |
| Unowned Review Trigger | 写了触发条件但无人监测 | ADR 永不复审 | Trigger 绑定 Metric/Event 和 Owner |

---

## 29. Review Checklist

### 29.1 Document Boundary

- [ ] 文档是否为 Review 0.9。
- [ ] 是否严格继承 01～14 Approved 1.0。
- [ ] 是否未修改任何 Existing Baseline。
- [ ] 是否没有代码、配置、脚本、目录或独立 ADR 文件。
- [ ] 是否未进入编码或第 16 文档。
- [ ] 冲突是否仅登记为 Candidate、Open Question 或 Baseline Conflict。

### 29.2 Governance

- [ ] ADR Principles、Scope、Lifecycle、Status 和 Numbering 是否明确。
- [ ] `ADR-NNNN`、`ADR-BL-*` 与 Candidate 身份是否不混用。
- [ ] Accepted ADR 是否禁止原地修改。
- [ ] Approval、Role、职责分离和 Gate 是否清晰。
- [ ] Exception 是否限时、补偿、可审计且不绕过禁区。
- [ ] Roadmap/Chat/Code 是否不能直接改变基线。

### 29.3 Template and Analysis

- [ ] Template 是否包含用户要求的全部字段。
- [ ] Context、Problem、Drivers、Options、Decision 和 Rationale 是否分离。
- [ ] Positive/Negative Consequences 与 Risks 是否完整。
- [ ] Security、Privacy、AI、Data、API、Operations、Testing Impact 是否覆盖。
- [ ] Migration、Rollback、Observability 和 Review Trigger 是否可验证。
- [ ] Rejected Alternatives 是否保留。

### 29.4 Baseline Relationship

- [ ] Accepted ADR 到 Baseline Revision 的流程是否明确。
- [ ] ADR 是否不静默覆盖当前基线。
- [ ] Baseline Conflict 是否有显式登记与解决入口。
- [ ] Superseded/Deprecated 是否保留历史和双向链接。
- [ ] Requirement→ADR→Baseline→Test→Release 是否可追踪。

### 29.5 Approved Decision Register

- [ ] 是否完整登记 31 项用户指定的已批准决策。
- [ ] 每项是否包含 ID、Title、Context、Decision、Rationale、Alternatives、Consequences、Risks、Related Documents、Status、Owner、Review Trigger。
- [ ] 每项是否能从 01～14 找到明确依据。
- [ ] 是否明确 `ADR-BL-*` 不是倒填的独立 ADR。
- [ ] 是否没有把未决供应商、协议、模型或阈值登记为 Approved。

### 29.6 Candidate Register

- [ ] 是否完整登记至少 18 项用户指定候选。
- [ ] Candidate 是否只描述问题和选项，不作结论或暗示推荐。
- [ ] Authentication、Token、Encryption、Provider/Model、RAG、Tool、Platform、SLO、Vendor 和 Region 是否保持待定。
- [ ] Candidate 是否有 Owner、Review 和触发证据。

### 29.7 Cross-Cutting Review

- [ ] Security/Privacy/AI Review Trigger 是否明确。
- [ ] 命理专家与法律权限是否未被架构委员会替代。
- [ ] Testing 与 Release Gate 是否绑定 ADR 实施。
- [ ] Migration/回滚是否保护 Identity、Version、Frozen History、Consent、Audit 和 Tombstone。
- [ ] AI 决策是否保持 Deterministic、Frozen Evidence、Validation、No Silent Fallback。

---

## 30. Risks

| Risk | Manifestation | Impact | Mitigation / Gate |
|---|---|---|---|
| Governance Theater | 有 ADR 但代码照旧 | 基线与现实分裂 | Verified/Active Gate、Architecture Test |
| Retroactive Fiction | BL 登记被当作历史 ADR | 审计失真 | Baseline-Inherited 明示、无虚构日期 |
| Candidate Leakage | 候选被实现为默认选型 | 未评审风险进入系统 | Candidate Non-Decision Rule |
| ADR Overload | 小改动都进委员会 | 流程停滞、团队绕过 | Creation Criteria、局部授权 |
| Under-documentation | 重大决定不建 ADR | 隐性依赖和重复争论 | Triage、Baseline Change Gate |
| Stale ADR | 条件变化未复审 | 过时决策持续生效 | Trigger Owner、定期 Review |
| Baseline Drift | ADR Accepted 但文档未更新 | 两套真相 | Baseline Custodian、Closure Gate |
| Implementation Drift | 实现偏离 ADR | 安全/数据后果未知 | Traceability、Test、Release Evidence |
| Missing Alternatives | 首选方案无比较 | 锁定与偏见 | Option 0 + 可行替代强制 |
| Hidden Negative Consequence | 只写收益 | 成本/复杂度后置 | Negative Consequence 与 Residual Risk Gate |
| No Rollback | 迁移失败无法恢复 | 停机、数据损害 | Rollback Plan/Test、Stop Condition |
| Data Irreversibility | 覆盖历史或 Identity | 无法追溯/恢复 | Migration Review、Immutable Gate |
| Security Review Bypass | 技术 ADR 未邀安全 | 攻击面和 Secret 风险 | Impact-driven Required Reviewer |
| Privacy Review Bypass | 新用途/区域未评审 | 法律与信任风险 | Data Flow、Purpose、Legal Gate |
| AI Quality Gap | Provider/Model 决策无评估 | 幻觉、引用、成本失控 | AI Review Evidence、Quality Gate |
| Expert Authority Gap | 架构师决定命理规则 | 错误规则固化 | Expert Gate、Open Question |
| Vendor Lock-In | 选型无 Exit | 成本、合规、故障受制 | Abstraction、Migration/Exit Plan |
| Exception Creep | 临时偏离不断续期 | 基线逐步失效 | Expiry、Independent Approval、Escalation |
| Giant ADR | 决策耦合不可拆 | 无法回滚/替代 | One Decision、Related ADR |
| Approval Bottleneck | Reviewer 无 SLA/代理 | 里程碑延误 | Governance Open Question、Delegation |
| Evidence Leakage | ADR 附件含 PII/Secret/Prompt | 安全隐私事故 | Restricted Reference、Data Minimization |
| Supersede Ambiguity | 新旧 ADR 同时 Active | 团队执行不一致 | 双向链接、部分替代范围 |
| Metric Manipulation | 为批准选择性展示数据 | 错误决策 | 可复现 Evidence、Reviewer 校验 |
| Emergency Normalization | 每次都以紧急绕过 | 技术债与风险累积 | 限时 Exception、Post-Incident ADR |
| Ownership Turnover | Owner 离职后无人维护 | Trigger/风险失管 | 角色 Owner、定期 Custodian Review |
| Document Scale | 单一登记册过长难维护 | 查找和复审困难 | Index；获准后分离独立 ADR，不删历史 |

---

## 31. 进入下一阶段《16-GLOSSARY-AND-APPENDIX.md》所需输入条件

- [ ] `15-ARCHITECTURE-DECISION-RECORDS.md` 已完成评审并成为 Approved 1.0 ADR Governance Baseline。
- [ ] ADR Principles、Scope、Governance、Lifecycle、Status 和 Numbering 已确认。
- [ ] 正式 `ADR-NNNN`、Baseline-Inherited `ADR-BL-*` 和 Candidate 身份规则已确认。
- [ ] ADR Template 的全部必需字段已确认。
- [ ] Creation Criteria、Approval Process、Review Roles 和职责分离已确认。
- [ ] Impact、Alternatives、Risk、Security/Privacy、AI 和 Testing Review 已确认。
- [ ] Migration、Rollback、Supersede、Deprecation 和 Exception 已确认。
- [ ] ADR 与 Approved Baseline 的权威顺序、Revision 和 Conflict 流程已确认。
- [ ] Logical Repository、Index、Audit、Traceability 和 Sensitive Evidence 边界已确认。
- [ ] 31 项 `ADR-BL-*` 决策与来源基线逐项复核，无误述或遗漏。
- [ ] 18 项 Candidate 保持未决，未被误登记为 Approved 或默认实现。
- [ ] Product、命理专家、法律、安全、隐私、AI、运维和测试 Open Question 已有 Owner 或阻断规则。
- [ ] 未发现 Baseline Conflict；若发现，已登记且未在本文擅自解决。
- [ ] 下一阶段只汇总统一语言、缩写、引用和附录，不修改任何 Architecture Baseline。
- [ ] 下一阶段不生成代码、配置、脚本、目录或实现资产。

只有本 ADR 治理与登记文档通过评审后，才可以生成 `16-GLOSSARY-AND-APPENDIX.md`。本次不得生成该文件，也不得进入编码阶段。
