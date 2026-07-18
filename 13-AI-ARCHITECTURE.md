# AI 八字命理分析平台：AI 架构

**文档编号：** 13  
**文档类型：** AI Architecture  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md` 至 `12-SECURITY-PRIVACY.md`（均已 Approved 1.0）  
**目标读者：** CTO、AI/应用/数据架构师、命理领域专家、知识与内容负责人、安全与隐私负责人、研发、测试、平台工程、成本与运营治理人员

---

## Version 0.9 Change Log

- 首次定义 AI 子系统、Model Gateway、Provider Abstraction、Model Registry 与 Routing 架构。
- 定义 Prompt Pipeline、Prompt Registry、Version、Review、Rollback 和 Governance。
- 定义 RAG、Knowledge Retrieval、Embedding、Chunk、Ranking、Citation 和 Context Assembly。
- 定义 AIConversation、AIAnalysis、Output Validation、Hallucination Mitigation 与 Human Review 边界。
- 定义 AI Cache、Cost、Reliability、Retry、Circuit Breaker、Fallback、Observability、Evaluation、Drift 和治理。
- 本文件不包含任何 Prompt 内容、代码、SDK、模型配置或可执行实现。

---

## 1. Document Purpose

### 1.1 目标

本文档定义平台如何把确定性命盘事实、规则发现、冻结证据、受控知识和用户问题组织成可验证的 AI 分析，并通过多供应商模型完成通俗、克制、可追溯的解释。

AI Architecture 的核心不是“让模型自由判断命理”，而是确保模型只能在已批准输入、范围、证据、风险和版本边界内生成候选解释，随后由平台完成结构、事实、引用、冲突和安全验证。

### 1.2 适用范围

本文覆盖：

- AIAnalysis、AIConversation 和 AIMessage 的 AI 技术协作；
- Model Gateway、Provider Adapter、Registry、Routing 和 Fallback；
- Prompt Registry、Pipeline、Version、Review、发布和回滚；
- RAG、Knowledge、Embedding、Chunk、Retrieval、Ranking 与 Citation；
- Context Window、Context Budget、Token Budget 和 Context Assembly；
- Output Validation、Hallucination、Risk、Human Review；
- Cache、Timeout、Retry、Circuit Breaker、Reliability 和 Degradation；
- Metrics、Evaluation、Drift、Cost、Security、Privacy 和 Governance。

### 1.3 不包含内容

本文不包含：

- 任何 System、Developer、User Prompt 内容或模板文本；
- Python、TypeScript、SQL、FastAPI、Next.js 或可运行代码；
- OpenAI、Anthropic 或其他 Provider SDK；
- LangChain、LlamaIndex、MCP Server 或 Tool Calling 实现；
- Model、Embedding、Vector Index 或 Prompt 的具体配置值；
- Docker、Kubernetes、Terraform、CI/CD 或部署脚本；
- 命理算法、旺衰、格局、调候、用神、起运等待专家确认规则；
- Domain、Aggregate、Entity、Value Object、Domain Event、Data、API、Technology、Engineering 或 Security Baseline 变更；
- 进入编码阶段的授权。

### 1.4 Baseline Priority

AI 便利性不能改变 Chart、RuleRun、EvidenceBundle、AIAnalysis、Conversation、Timeline 或 Report 的 Approved 生命周期与所有权。若需要新领域对象、跨 Context 事务、API 变化或安全例外，只登记为 `ADR Candidate` 或 `Open Question`。

### 1.5 Product Positioning

AI 输出属于传统文化分析与自我反思内容，不宣称科学预测准确、必然发生或替代医疗、法律、投资等专业意见。Evidence 和模型一致性也不等于命理观点经过现代科学验证。

---

## 2. AI Principles

### AI-P-001 Deterministic Facts Before Generation

Chart Calculation 产生事实，Rule Evaluation 产生 RuleFinding，Evidence Context 冻结证据；AI 不计算、补造或修改这些上游结果。

### AI-P-002 Evidence-Grounded

重要解释必须能定位到 Frozen Evidence、RuleFinding、CalculationSnapshot 或有权引用的 Knowledge Citation。无证据时明确“不足”而非自由补全。

### AI-P-003 Scope Bound

MVP 仅处理当前 Chart、未来三年和已批准主题。模型不能扩大时间、主体、Chart 或高风险主题范围。

### AI-P-004 Provider Independent Core

核心应用依赖平台 Model Gateway 和稳定能力，不直接依赖单一 Provider SDK、错误或 Payload。

### AI-P-005 Version Everything That Affects Meaning

正式结果记录 CalculationSnapshot、RuleRun、EvidenceBundle、Knowledge、Prompt、Model、Route、Risk Policy 和 Validation Version。

### AI-P-006 Raw Output Is Untrusted

Provider 原始输出不是正式领域结果，必须经过平台解析和多阶段 Validation。

### AI-P-007 Privacy by Design

第三方模型只接收去标识化、最小必要事实和证据。姓名、联系方式、UserId、详细地址、工单和无关 Conversation 不进入模型上下文。

### AI-P-008 Conflict and Uncertainty Are First-Class

使用“证据充分、一般、有限、存在冲突”等等级，不生成伪精确概率。规则分歧和输入不确定性必须保留。

### AI-P-009 Bounded Cost

每个 Analysis 有 Context、Token、Retry、Latency 和 Cost Budget。成本优化不能跳过事实、Citation 或 Risk Validation。

### AI-P-010 Controlled Multi-Provider

多 Provider 用于可替换、可靠性和成本治理，不意味着在一次正式 Analysis 中静默切换模型。

### AI-P-011 Safe Degradation

AI 不可用时确定性排盘、规则和已保存报告继续可用；平台明确降级，不用模板冒充已完成 AI 解读。

### AI-P-012 Observable but Minimal

观察 Model、Latency、Token、Validation、Retry、Cost 和结果状态，不记录完整 Prompt、Birth、Conversation、Raw Output 或 Report。

### AI-P-013 Human Governed

Prompt、Model、Knowledge、Risk 和 Evaluation 的生产发布经人工与自动门禁；用户反馈不自动修改规则或 Prompt。

### AI-P-014 No Hidden Tools

模型不拥有未声明的 Database、Internet、Code、File、Secret 或跨用户 Tool。未来 Tool 能力需独立 ADR、安全和授权设计。

### AI-P-015 Reproducible Inputs, Honest Outputs

平台保存重现正式输入和版本所需信息；无法保证 Provider 字节级确定时，明确区分“输入可复现”与“模型输出完全确定”。

---

## 3. AI System Overview

### 3.1 Subsystem Responsibilities

| Capability | Responsibility | Explicit Exclusion |
|---|---|---|
| AI Planning | 锁定 Scope、版本、预算、风险和输出类型 | 不生成命盘事实 |
| Context Assembly | 组合有权事实、Evidence、Knowledge 与问题 | 不改变上游内容 |
| Model Gateway | Provider/Model 调用、Timeout、Quota、Telemetry | 不决定领域真相 |
| RAG | 从 Published Knowledge 召回解释材料 | 不生成 RuleFinding/Evidence |
| Generation | 产生结构化候选解释 | 候选不是正式结果 |
| Validation | 验证结构、事实、引用、冲突、风险与范围 | 不用模型自评替代平台检查 |
| Governance | Prompt/Model/Route/Evaluation 发布与回滚 | 不自动从用户反馈上线 |
| Observability | 质量、时延、成本、漂移和安全信号 | 不记录敏感全文 |

### 3.2 Formal Input Chain

正式 AIAnalysis 的上游链为：

1. Confirmed BirthInput；
2. Valid CalculationSnapshot；
3. Completed RuleRun；
4. Frozen EvidenceBundle；
5. 允许范围的 Basic/Analytical Timeline（如需要）；
6. Published Knowledge Version 与有效 Rights；
7. Approved Prompt Version；
8. Approved Model/Route/Risk/Validation Version；
9. Actor、Purpose、Consent、Scope 与预算。

缺失必需上游时不开始正式生成，或明确选择已批准的无 AI/缩小范围能力。

### 3.3 Formal Output Chain

Provider Raw Output → Parsed Candidate → Fact/Citation/Risk/Scope Validation → ValidationResult → Completed/Rejected/Failed AIAnalysis → Conversation Answer 或 Report 输入。

### 3.4 AIAnalysis vs AIConversation

`AIAnalysis` 是一次独立结构化分析任务及正式结果；`AIConversation` 管理会话和 `AIMessage`。Conversation 回答可以引用独立 AIAnalysis，但 Conversation 本身不替代正式 Analysis、Evidence 或 Chart。

### 3.5 Read Model Boundary

AI Status、Conversation View、Usage、Evaluation Dashboard 和 AnalysisProgress 是可重建投影，不成为 AIAnalysis Source of Truth，也不推进 Saga。

---

## 4. AI Architecture

### 4.1 Logical Components

| Component | Input | Output | Owner Boundary |
|---|---|---|---|
| AI Application Service | Approved Use Case、ActorContext | AIAnalysis/Conversation Command Result | Application Layer |
| Analysis Planner | Scope、Bundle、Timeline、Policy、Budget | Immutable AnalysisPlan | AI Context |
| Context Assembler | Snapshot、Findings、Evidence、Knowledge、Question | Bounded Context Package | AI Context |
| Retrieval Orchestrator | Query Intent、Filters、Index Version | Ranked Knowledge Candidates | Knowledge/AI 协作 |
| Prompt Registry | Approved Prompt Definitions/Versions | PromptVersion Reference | Governance |
| Model Registry | Approved Provider/Model Capabilities | ModelReference/Route Eligibility | AI Governance |
| Model Gateway | Generation Request + ModelReference | Raw Provider Result/Failure | Infrastructure Adapter |
| Output Parser | Raw Result + Expected Contract Version | Structured Candidate | AI Context |
| Validation Pipeline | Candidate + Frozen Sources + Policy | ValidationResult/RiskDisposition | AI Context |
| AI Cache | Version-complete key + authorized scope | Reusable validated artifact | Infrastructure/AI Policy |
| AI Observability | Safe metadata/events | Metrics、Trace、Cost、Alerts | Operations |

### 4.2 Synchronous and Asynchronous Boundary

- Analysis Planning、权限、Consent、Quota 和 Input Manifest 校验可同步完成。
- AI Generation、复杂 Retrieval、长回答和 Report 解释通常异步，通过 Operation/Worker。
- 同步请求超时不证明 AIAnalysis 未执行；客户端查询 Operation。
- 外部模型调用不持有数据库事务。

### 4.3 Transaction Boundary

AIAnalysis 状态变化在单 Aggregate 本地事务提交。Model 调用、Retrieval 和 Object/Provider 网络等待在事务外。跨 Evidence、Knowledge、Timeline、Conversation 和 Report 通过稳定 Identity/Snapshot/Event 协调。

### 4.4 Process Boundary

Bundle → AIAnalysis、Message → AIAnalysis、AIAnalysis → Report/Message 均继承 Approved Process Manager。AI Worker 不直接修改 Report、Evidence 或 Conversation 内部状态。

### 4.5 Infrastructure Boundary

Provider SDK、HTTP、Embedding Client、Vector Query、Cache 和 Tokenizer 属于 Infrastructure Adapter。Domain/Application 不暴露供应商类型。

### 4.6 Technology Independence

本文不规定具体 Orchestration Framework。若引入 LangChain、LlamaIndex 或其他框架，只能作为 Adapter/Infrastructure 选择，不能改变核心边界，并需依赖与安全评审。

---

## 5. AI Context Boundaries

### 5.1 Owned by AI Context

- AIAnalysis、AnalysisPlan、PromptVersion Reference、ModelReference、ValidationResult、RiskDisposition 和正式结构化结果；
- AIConversation 与 AIMessage 的 AI 交互协调（按 Approved Domain Model）；
- Context Assembly、Model Routing、Generation、Validation、Degradation 和安全拒绝的领域/应用能力；
- AI Usage/Cost 的安全业务引用与投影。

### 5.2 Referenced but Not Owned

| Reference | Owning Context | AI Rule |
|---|---|---|
| Chart/CalculationSnapshot | Chart Calculation | 只读稳定事实，不修改 |
| RuleRun/RuleFinding | Rule Evaluation | 只读 Completed 结果，不补造 |
| EvidenceBundle/Evidence | Evidence | 只读 Frozen Bundle，不创建 |
| KnowledgeArticle/Citation | Knowledge | 只读 Published/权利有效版本 |
| Timeline | Timeline | 只读允许 Kind/Version/Node |
| Consent | Consent | 每次处理验证当前 Purpose 决定 |
| Report | Report | AI 只提供已验证输入，不控制 Report 生命周期 |
| Audit | Audit | 触发最小审计，不修改 AuditEvent |

### 5.3 Forbidden AI Actions

- 计算四柱、节气、起运或流年事实；
- 选择未 Published Algorithm/Rule/Knowledge；
- 创建或修改 RuleFinding、Evidence、Citation Source；
- 将不确定 BirthInput 补成精确值；
- 修改 Frozen/Completed/Published 对象；
- 跨 Chart、User 或 Tenant 读取上下文；
- 直接执行 Database、Delete、Payment、Notification 或治理发布；
- 将用户反馈自动变成规则或 Prompt。

### 5.4 Security Context

AI 调用携带最小 Actor/Subject/Purpose/Consent/Scope/Correlation 安全上下文。Provider 仅接收一次性 Analysis Reference，不接收平台 UserId 或授权内部细节。

### 5.5 Scope Manifest

每次 Analysis 锁定 Chart/Snapshot、主题、时间范围、EvidenceBundle、Knowledge Filters、Language、Output Type、Risk Level 和 Version Manifest。后续步骤不能静默扩大。

---

## 6. Model Gateway

### 6.1 Responsibilities

Model Gateway 是所有模型调用的唯一受控入口，负责：

- 验证 ModelReference 与 Registry 状态；
- Provider Credential、Region 和 Endpoint；
- 请求去标识化与最小化；
- Timeout、Concurrency、Rate、Quota 与 Circuit；
- Token/Context 估算与预算；
- Provider Error 归类与平台错误映射；
- Safe Telemetry、Usage 和 Cost；
- Raw Output 大小/格式安全；
- 实际 Provider/Model/Deployment Reference 记录。

### 6.2 Non-Responsibilities

Gateway 不决定 Chart Fact、Rule、Evidence、业务授权、Prompt 内容、Analysis Scope 或最终 ValidationResult。它不把 HTTP 成功映射为 AIAnalysis Completed。

### 6.3 Request Contract

Gateway 接收平台稳定生成意图、Approved ModelReference、Context Package、Output Contract Version、Timeout/Token Budget 和 Trace Reference。本文不定义任何 Request Body 或 Prompt。

### 6.4 Response Contract

Gateway 返回 Provider Result Reference、Raw Candidate、Usage、Finish Reason、Latency、Provider Error 和 Safety Metadata。Raw Candidate 只进入受控 Validation Pipeline。

### 6.5 Credential Isolation

Provider Credential 按 Environment、Provider、用途和项目分离，通过 Secret Management/Workload Identity 获取，不进入 Prompt、Log 或 AIAnalysis 正文。

### 6.6 Gateway Availability

Gateway 故障不影响确定性排盘和已保存资产。调用无法可靠受理时不返回虚假 Accepted；已受理任务依据持久 Operation/Queue 恢复。

### 6.7 Direct Call Prohibition

Interface、Application Handler、Report、Conversation 或测试外的生产代码不得绕过 Gateway 直接调用 Provider。例外必须 ADR、安全和观测等价控制。

---

## 7. Provider Abstraction

### 7.1 Stable Capability Contract

Provider Adapter 把平台能力映射到供应商：结构化生成、上下文限制、Usage、Timeout、Safety/Finish Reason、Region 和 Model Version。供应商专有字段不进入 Domain/API。

### 7.2 Multi-Provider

平台支持多个 Provider 的架构能力，用于合规地区、能力、可靠性、成本和退出治理。MVP 是否实际启用多个生产 Provider 由产品/运维评审，不因“多 Provider”增加无必要复杂度。

### 7.3 Adapter Responsibilities

- Provider 请求/响应映射；
- Credential/Endpoint/TLS；
- Provider-specific Token/Limit 归一；
- Error/Retry/Rate Limit 映射；
- Usage/Cost Metadata；
- Safe Provider Request ID；
- Contract Test 和 Compatibility。

### 7.4 Provider Selection Restrictions

只有完成 Security、Privacy、Data Region、Retention/Training、Subprocessor、Capability、Evaluation、Cost、SLA 和 Exit Review 的 Provider 才可进入 Approved Registry。

### 7.5 No Lowest-Common-Denominator Leakage

核心 Contract 保持稳定最小能力。需要 Provider 特性时通过显式 Capability/Policy，不能在业务代码中散落 Provider 条件。

### 7.6 Provider Exit

每个关键 Provider 有替换、数据删除、Credential Revoke、Contract Test、Evaluation 和用户影响计划。退出不改变 AIAnalysis 历史 ModelReference。

### 7.7 Provider Incident

Provider Outage 触发 Circuit、Queue/Degradation 和 Incident；供应商恢复后渐进恢复，并验证行为/质量漂移，不立即全量切回。

---

## 8. Model Registry

### 8.1 Registry Purpose

Model Registry 保存可用于生产路由的受治理技术/业务引用。它是 AI Governance Registry，不新增 Domain Aggregate；AIAnalysis 只保存 Approved `ModelReference`。

### 8.2 Registry Metadata

| Metadata | Purpose |
|---|---|
| ModelReference | 稳定、不可歧义的模型/部署引用 |
| Provider | Provider Adapter Owner |
| Capability | Language、Structured Output、Context、Latency Class |
| Region / Data Policy | 可用地区、Retention、Training/Privacy 条件 |
| Context/Output Limits | 最大上下文/输出和安全边界 |
| Status | Proposed、Evaluating、Approved、Deprecated、Blocked、Retired |
| Evaluation Version | 通过的评估集/门槛 |
| Cost Snapshot | 价格/计量版本与有效期 |
| Safety Profile | 已知限制、风险策略和适用主题 |
| Release/Drift Evidence | 上线、Canary、漂移和 Incident 历史 |

### 8.3 Model Identity

Provider 市场名称不足以作为正式 ModelReference。应绑定具体版本、部署或可验证行为引用。若 Provider 会静默更新，平台将其视为 Drift 风险并缩小正式使用或要求额外持续评估。

### 8.4 Registry States

| State | Meaning |
|---|---|
| Proposed | 候选，不可用于正式结果 |
| Evaluating | 仅隔离评估/Shadow |
| Approved | 可按 Route Policy 用于新 Analysis |
| Deprecated | 不建议新使用，兼容期受控 |
| Blocked | 因 Incident/Drift/Compliance 暂停 |
| Retired | 不用于新任务；历史 Reference 保留 |

### 8.5 Registry Change

新增/升级/状态变化需要 Evaluation、安全/隐私、成本、运行与 Owner 审批。Blocked 可紧急生效，但恢复 Approved 需重新验证。

### 8.6 Historical Resolution

历史 Report/AIAnalysis 必须能够解析其 ModelReference、Provider、Evaluation 和 Route Version，即使模型已 Retired；不要求继续调用已退役模型。

---

## 9. Model Routing

### 9.1 Routing Inputs

| Dimension | Examples |
|---|---|
| Task | Report Section、Conversation Answer、Summary、Validation Aid |
| Language | zh-CN；未来 en/ar 经人工复核 |
| Context Size | Fact/Evidence/Knowledge Token Estimate |
| Risk | Topic、User Input、Output Sensitivity |
| Capability | Structured Output、Context、Latency |
| Governance | Approved Status、Evaluation、Route Version |
| Privacy | Region、Retention、Provider Policy |
| Reliability | Health、Circuit、Quota、Incident |
| Cost | Task Budget、Plan/Tenant、Price Version |

### 9.2 Route Policy

Route Policy 版本化、可审计、可回滚，输出明确 ModelReference。Policy 不根据用户敏感属性或命理结论进行不透明差别待遇。

### 9.3 Planning Time Selection

ModelReference 在 AIAnalysis Planned 前确定并写入 AnalysisPlan。进入 Planned 后，技术重试保持相同 ModelReference、PromptVersion、Bundle 和 Plan。

### 9.4 Provider Routing

Provider Route 只在 Approved Capability/Region/Privacy/Cost 范围内选择。相同模型名但不同 Provider/Deployment 视为不同 ModelReference，必须记录实际选择。

### 9.5 Fallback Boundary

若原 ModelReference 失败，切换另一 Model/Provider 不能在同一 AIAnalysis 中静默完成。Fallback 必须：

1. 由批准的 Fallback Policy 触发；
2. 创建新的 AIAnalysis 正式身份或等价的已批准新分析意图；
3. 保留原 Analysis Failed/Degraded 历史；
4. 重新锁定 ModelReference、Prompt Compatibility、Budget 与 Validation；
5. 在用户 Operation/Conversation 中安全关联结果。

如未来希望同一 AIAnalysis 容纳 Route Candidate List，必须先修改 Domain Baseline 并走 ADR；当前不得采用。

### 9.6 Routing Observability

记录 Task、Route Version、ModelReference、Decision Reason Code、Fallback、新旧结果状态、Latency、Cost 和 Quality；不记录完整 Context。

### 9.7 Route Testing

覆盖健康/故障、Quota、Region、Risk、Context Size、Language、Cost、Deprecated/Blocked、Prompt Compatibility 和无可用 Model。

---

## 10. Prompt Pipeline

### 10.1 Pipeline Stages

| Stage | Responsibility | Output |
|---|---|---|
| Intent Classification | 识别用例、主题、风险和范围 | Approved/Rejected Intent |
| Plan Binding | 锁定 PromptVersion、Output Contract、ModelReference | AnalysisPlan |
| Source Preparation | 获取 Snapshot、RuleRun、Frozen Bundle、Timeline | Verified Source Manifest |
| Retrieval | 召回 Published Knowledge Candidates | Ranked Citations |
| Context Assembly | 按预算组织最小上下文 | Context Package |
| Prompt Materialization | 将 Approved Prompt Definition 与 Context 组合 | Provider-ready Generation Input |
| Generation | 经 Gateway 调用锁定模型 | Raw Candidate |
| Parsing | 转为 Expected Output Contract | Structured Candidate |
| Validation | Fact/Citation/Conflict/Risk/Scope/Length | ValidationResult |
| Finalization | 保存正式结果/拒绝/失败 | AIAnalysis Terminal State |

### 10.2 No Prompt Content

本文只定义 Pipeline 和治理，不包含任何 Prompt 文字、示例、片段、变量内容或指令实现。

### 10.3 Prompt Definition Boundary

Prompt Definition 描述角色、任务、输入槽、输出契约、风险和适用模型的版本化资产。它不是代码，不允许任意脚本执行或访问 Secret。

### 10.4 Context-Data Separation

用户问题、Knowledge Chunk、Evidence 和 Provider Tool Result 明确作为数据，不能覆盖平台安全/任务约束。Context Envelope 保留来源和类型标签。

### 10.5 Pipeline Failure

任一阶段失败返回明确分类：Input/Scope、Retrieval、Prompt Compatibility、Provider、Parse、Fact、Citation、Risk、Timeout 或 Budget。失败不由后续阶段静默忽略。

### 10.6 Pipeline Idempotency

同 AIAnalysis 技术重试保持 Plan/Prompt/Model/Bundle 不变；改变 Prompt、Model、Scope、Knowledge Version 或风险策略属于新正式 Analysis。

---

## 11. Prompt Versioning

### 11.1 Prompt Registry

Prompt Registry 保存 PromptDefinitionId、PromptVersion、Purpose/Task、Language、Input Contract、Output Contract、Compatible Models、Risk Policy、Status、Review、Change Summary 和 Evaluation Reference。它属于治理资产，不新增 Domain Aggregate。

### 11.2 Version Identity

PromptDefinition Identity 与 PromptVersion 分离。AIAnalysis 保存实际 PromptVersion，不用“latest”作为历史引用。

### 11.3 Version States

Draft → InReview → Approved → Published → Deprecated → Retired；Rejected 返回新 Draft 修订。只有 Published 可用于新正式 Analysis。

### 11.4 Breaking Prompt Change

改变任务、输入语义、输出契约、风险边界、Citation 要求、Language 或 Compatible Models 通常视为新版本并重新评估。不能原地编辑 Published。

### 11.5 Prompt Rollback

Rollback 是 Route/Registry 将新 Analysis 恢复选择一个已批准旧 PromptVersion，不修改已完成 AIAnalysis。Rollback 前验证旧 Prompt 与当前 Model、Output Contract、Risk 和 Knowledge 兼容。

### 11.6 Historical Reproduction

保存 PromptVersion Reference、Hash/Integrity、输入槽版本、Output Contract 和 ModelReference，以复核历史。受安全限制时，普通用户不查看完整 Prompt 内容。

### 11.7 Version Compatibility

PromptVersion 与 ModelReference、Context Assembler、Output Parser、Validation Policy 和 Language 维护兼容矩阵。任何一项不兼容阻断路由。

---

## 12. Prompt Governance

### 12.1 Roles

| Role | Responsibility |
|---|---|
| Prompt Author | 创建 Draft、说明目的和变化 |
| Domain Expert | 评审命理术语、Evidence 和克制表述 |
| Safety/Privacy Reviewer | Injection、Leakage、高风险和数据最小化 |
| Evaluation Owner | 运行质量/安全/成本评估 |
| Publisher | 在职责分离下发布 |
| Auditor | 查看 Version、Review、Release，不修改内容 |

### 12.2 Review Requirements

Prompt Review 至少检查：Use Case/Scope、上游事实、Citation、冲突/不确定性、风险主题、Prompt Injection、Prompt Leakage、输出结构、语言、Model Compatibility、Token/Cost 和降级。

### 12.3 Evaluation Gate

Published 前通过固定 Evaluation Set、Golden/Adversarial Cases、Human Review、Model Matrix 和 Regression。用户“有帮助”反馈不能替代事实/安全评估。

### 12.4 Separation of Duties

Author 不能单人完成高风险 Prompt 的 Author→Approve→Publish。Emergency Block 可由受权角色执行，恢复发布需完整 Review。

### 12.5 Change Impact

分析受影响 Task、Model、Language、Report Section、Conversation、Risk、Token/Cost 和 Historical Reproducibility。重大变化按 Canary/Shadow 验证。

### 12.6 Prompt Access

完整 Prompt 属于 Confidential Governance Asset，按 Role/Purpose 访问并审计。它不包含 Secret；保密也不作为唯一安全防线。

### 12.7 Feedback

用户反馈进入独立数据流，去标识化并有 Consent。反馈形成 Review 候选，不自动修改 Prompt、Rule、Knowledge 或 Model Route。

---

## 13. RAG Architecture

### 13.1 Purpose

RAG 为 AI 提供已审核、可引用的解释材料和术语背景，提升 Grounding 与 Citation；它不决定命理事实、规则结论或 Evidence 状态。

### 13.2 Source Hierarchy

1. CalculationSnapshot：确定性事实；
2. RuleRun/RuleFinding：规则输出；
3. Frozen EvidenceBundle：正式分析证据；
4. Timeline：允许的时间结构/节点；
5. Published KnowledgeArticle/Chunk：解释和背景材料；
6. 用户当前问题：表达需求，不成为事实来源。

### 13.3 RAG Components

| Component | Responsibility |
|---|---|
| Knowledge Ingestion | 解析、Rights、Language、Structure、Review |
| Chunk Builder | 生成稳定 Chunk 与 Source Metadata |
| Embedding Pipeline | 为 Published Chunk 生成 Versioned Vector |
| Lexical/Structured Index | 关键词、主题、术语、过滤 |
| Retrieval Planner | 根据 Task/Scope 选择 Query 与 Filter |
| Candidate Retrieval | 结构化、Lexical、Vector 候选 |
| Ranking/Reranking | 相关、权利、版本、来源、多样性排序 |
| Citation Builder | 生成可验证 Source/Version/Chunk 引用 |
| Context Selector | 在预算内选择内容，不覆盖正式 Evidence |

### 13.4 Data Ownership

Knowledge Context 拥有 Article、Version、Rights 和发布状态；AI 只通过公开 Retrieval/Query 能力读取。向量索引是可重建 Projection，不是 Knowledge Source of Truth。

### 13.5 Rights and Publication Gate

只有 Published、Rights 有效、适用语言/范围明确的内容进入正式 RAG。Draft/Rejected/Withdrawn/Retired 不用于新 Analysis。

### 13.6 RAG Security

Retrieved Chunk 视为不可信数据，防间接 Prompt Injection。Chunk 不含可执行 Tool 指令；外部链接/附件不自动访问。

### 13.7 RAG Failure

检索不可用时：使用 Frozen Evidence 与已验证结构化解释，或停止 Knowledge Enhancement；不得生成不存在 Citation。

---

## 14. Knowledge Retrieval

### 14.1 Retrieval Input

Task/Topic、Language、School/RuleSet、Evidence Terms、Time Scope、Knowledge Version、Rights/Publication、Risk 和 Context Budget。User Identity 不作为语义 Query 输入。

### 14.2 Pipeline

1. 验证 Actor/Purpose/Scope；
2. 锁定 Knowledge/Index Version；
3. 从 Evidence/Rule/Question 构造最小 Query Intent；
4. 应用硬 Filter；
5. Structured/Lexical/Vector 候选召回；
6. 去重、Ranking/Reranking；
7. Rights/Source/Citation 再验证；
8. 多样性与预算选择；
9. 返回 Ranked Citation Candidates 与质量信号。

### 14.3 Hard Filters Before Ranking

Published State、Rights、Language、Topic、School/Rule Compatibility、Region/Policy 和 Knowledge Version 必须在最终使用前满足。向量高相似度不能绕过。

### 14.4 Retrieval Result

结果包含 KnowledgeArticleId、Version、ChunkId/Stable Locator、Source、Rights、Score Components、Reason 和 Index Version。Score 不被解释为命理结论概率。

### 14.5 No Result

零结果/低可信候选是合法状态。AI 缩小解释、只用 Evidence 或明确知识不足，不降低阈值到无关内容。

### 14.6 Withdrawal

Rights Withdrawal 先停止新召回，再清理/重建 Index。历史 Frozen Report 如何展示 Citation 由法律/Knowledge Governance 决定，不由 Retrieval 静默改写。

### 14.7 Retrieval Observability

记录 Query Class、Filters、Candidate Count、Latency、Zero Result、Selected Count、Index/Knowledge Version 和 Rights Failure，不记录完整问题/Chunk 文本。

---

## 15. Embedding Strategy

### 15.1 Scope

MVP 使用 PostgreSQL 向量扩展保存已批准 Knowledge Chunk 的 Embedding。Embedding 用于候选召回，不用于决定 Evidence 或命理结论。

### 15.2 Embedding Registry

记录 EmbeddingModelReference、Provider/Runtime、Dimension、Language Capability、Normalization、Index Compatibility、Status、Evaluation、Cost 和 Security/Region。

### 15.3 Versioning

Embedding 与 KnowledgeArticleVersion、ChunkVersion、EmbeddingModelVersion 和 IndexVersion 关联。模型/Chunk 变化产生新 Vector，不原地混用不同空间。

### 15.4 Chunk Strategy

Chunk 保留文档层级、标题/章节、语义边界、Source、Rights、Language、School、Version 和 Stable Locator。具体大小、Overlap 和策略需通过 Retrieval Evaluation，不在本文设定数值。

### 15.5 Personal Data

正式持久化 Embedding 以 Published Knowledge 为主。用户问题、Birth、Conversation 或 Report 的持久 Embedding 默认禁止，除非有明确 Purpose、Consent、Retention、Deletion 和重识别评审。

### 15.6 Query Embedding

若对用户意图生成临时 Query Embedding，应先去标识化、最小化、使用批准 Model/Region，并按请求/短期生命周期处理，不进入跨用户 Cache。

### 15.7 Reindexing

新 Embedding/Chunk/Index Version 通过离线构建、质量评估、Shadow/双索引比较和原子切换方向上线；旧索引按 Retention/回退到期删除。

### 15.8 Embedding Evaluation

覆盖中文术语、同义词、流派/范围、相似但不适用内容、零结果、Rights 和 Injection Chunk。指标包括 Recall、Precision、NDCG/排序质量候选、Latency 和 Cost；最终指标/阈值待评审。

---

## 16. Retrieval Strategy

### 16.1 Hybrid Retrieval

默认架构支持 Structured Filter + Lexical + Vector 的混合候选，最终是否全部启用由实测决定。单一向量相似度不构成正式检索策略。

### 16.2 Candidate Generation

各召回器使用明确 Top-K/预算候选，具体值按 Task、Context 和 Evaluation 配置。禁止无界检索整个知识库。

### 16.3 Ranking Signals

| Signal | Role |
|---|---|
| Hard Eligibility | Published、Rights、Language、Version、Scope |
| Semantic Relevance | 向量/语义相似度 |
| Lexical Match | 术语、规则名、主题直接匹配 |
| Source Quality | 审核状态、来源等级、可引用性 |
| Evidence Alignment | 是否解释当前 Finding/Evidence |
| Diversity | 避免重复 Chunk/单一来源占满预算 |
| Recency/Effective Version | 仅在适用且不覆盖历史版本时使用 |

### 16.4 Reranking

可使用规则或批准的 Reranker。若 Reranker 是模型调用，也需 Registry、Version、Privacy、Cost、Timeout 和 Evaluation，不可成为隐藏 Provider Call。

### 16.5 Thresholds

Minimum Relevance、Citation Quality 和 Zero-Result 阈值按 Evaluation Set 设定、版本化并可回滚。阈值不为追求回答率而降低到无依据。

### 16.6 Result Diversity

按 Article、Source、Viewpoint/School 和 Section 去重/多样化，保留争议观点，不强行选择唯一正确答案。

### 16.7 Retrieval Cache

只缓存版本完整、权限安全的候选结果。Key 包含 Query Intent Hash、Knowledge/Index Version、Language、Scope、Rights View；不包含明文敏感问题。

### 16.8 Evaluation and Drift

Knowledge/Index/Embedding/Reranker 变化比较固定 Query Set、Zero Result、Irrelevant、Rights、Citation、Latency 和 Cost。显著回归阻断发布。

---

## 17. Context Assembly

### 17.1 Context Sources

| Source | Authority | Priority |
|---|---|---|
| Security/Task Constraints | Approved Policy/PromptVersion | 最高，不可由数据覆盖 |
| CalculationSnapshot | Deterministic Fact | 高 |
| RuleFinding/Frozen Evidence | Formal Analysis Evidence | 高 |
| Timeline | Approved Kind/Version | 按任务 |
| Knowledge Citations | Published Explanation Material | 补充 |
| Conversation/User Question | Intent/Request | 不作为事实来源 |

### 17.2 Context Manifest

保存 Source Identity/Version、Purpose、Scope、Language、Selection Reason、Token Estimate、Truncation/Summary 和 Citation Mapping。Manifest 不复制不必要正文。

### 17.3 Context Window

Model Registry 声明可用 Context Window，但平台不以最大窗口为目标。超过预算先减少无关 Knowledge、重复内容和 Conversation 历史；不能删除关键 Evidence、冲突或风险提示。

### 17.4 Context Budget

Context Budget 按 Task 划分：Policy/Output Contract、Facts、Evidence、Knowledge、Conversation、Response Reserve。具体比例/Token 数为可配置评估项，不在本文固定。

### 17.5 Token Budget

每个 AIAnalysis 有 Input、Output、Retry 和 Total Cost Token Budget。Tokenizer/估算误差留安全余量；超预算时缩小范围、分段或拒绝，不自动截断 Citation/风险信息。

### 17.6 Ordering and Labeling

Context 明确标识来源类型、Authority 和引用键。User/Knowledge 内容作为引用数据，不能改变 Task/Security Instruction。

### 17.7 Summarization

Conversation/Knowledge Summary 是可验证的上下文 Artifact，不是 Source of Truth。Summary 记录来源和 Version，不能省略不确定性、冲突、否定或时间范围。

### 17.8 Sensitive Data

在 Assembly 前移除直接身份、详细地址、工单、其他 Chart 和无关 Message；应用最终 Provider Payload Scan。任何 Redaction 失败阻断调用。

### 17.9 Deterministic Assembly

在相同 Plan、Source Manifest 和版本下，选择/排序/裁剪策略尽量确定，便于复核。Provider Output 仍可能非确定，须诚实记录。

---

## 18. AI Conversation Context

### 18.1 Conversation Scope

MVP Conversation 仅围绕当前 Chart、未来三年和已支持主题。每个 Conversation 绑定 Chart/Subject 权限、Language、Scope 和当前安全政策。

### 18.2 Message Flow

User Message → Protocol/Security/Topic Validation → Context Selection → Plan AIAnalysis → Generate/Validate → Complete/Reject AIMessage。Message Handler 不直接调用 Provider 或修改 Chart。

### 18.3 Conversation Memory

Memory 来源于已授权 Message、Completed AIAnalysis 和受控 Summary。不得跨 Conversation/Chart/User 共享。Memory 不替代 Frozen Evidence 或正式 Source。

### 18.4 Context Selection

按当前问题选择必要历史，不默认发送完整 Conversation。旧问题涉及其他主题/时间范围时不自动扩大当前 Scope。

### 18.5 Message Idempotency

同客户端 Message Intent 重复提交复用同 Message/Operation；技术重试保持 Analysis 版本。用户改变问题/范围是新 Message/Analysis。

### 18.6 Consent and Deletion

每次 Message 检查当前 Consent/Purpose/Ownership。撤回/删除后停止新处理、清理 Cache/Memory/Provider 副本并按 Saga 处置历史。

### 18.7 Conversation Safety

越界、高风险、Injection/Jailbreak、身份提取和其他 Chart 请求安全拒绝。拒绝仍记录最小 Risk/Result，不保存不必要恶意全文。

### 18.8 Length and Pagination

单条回答上限继承 SRS 8,000 Unicode 字符。长主题使用结构化分段/继续意图，不无限扩展一个 Message。

---

## 19. AI Output Validation

### 19.1 Validation Stages

| Stage | Validates | Failure Outcome |
|---|---|---|
| Transport | Provider Result、Size、Encoding、Finish | Retryable/Failed |
| Structural Parse | Expected Output Contract/Required Sections | Repair Candidate/Rejected |
| Scope | Chart、Theme、Time、Language | Rejected |
| Fact | Snapshot/Timeline 确定性事实一致 | Rejected/Failed |
| Rule/Evidence | Finding、Evidence Status、Conflict | Rejected |
| Citation | Source/Version/Chunk 存在且支持 | Repair/Rejected |
| Risk/Safety | 高风险、绝对化、专业替代、隐私 | Rejected/Safe Result |
| Injection/Leakage | Prompt/Secret/Other User/Tool Leakage | Rejected + Security Signal |
| Length/Presentation | 上限、风险提示、i18n | Repair/Rejected |

### 19.2 Deterministic Validators First

能用结构、Identity、Version、枚举、引用图和规则确定验证的内容优先使用确定性 Validator。不能仅让另一个模型判断“是否正确”。

### 19.3 Model-Based Validators

若使用模型辅助语义检查，必须独立 ModelReference/PromptVersion、Evaluation、Cost 和不确定性，不能覆盖确定性失败，也不能成为唯一安全 Gate。

### 19.4 Fact Validation

候选中的 FourPillars、Stem/Branch、时间范围、RuleFinding 和 Timeline Node 必须与 Source Manifest 对齐。模型新增的“事实”不在 Source 中则删除、拒绝或重生成。

### 19.5 Citation Validation

验证 Citation Identity、Version、Rights、引用内容存在、Claim Support 和 Scope。只存在来源但不支持 Claim 不算有效。

### 19.6 Conflict Validation

EvidenceStatus=`Conflict/Limited` 时，输出不能改写为唯一确定结论。验证观点边界、条件和不确定语言。

### 19.7 Risk Disposition

RiskDisposition 明确 Allow、AllowWithNotice、Limit、Refuse、HumanReview 等批准语义。具体枚举继承/待安全基线，不在本文新增 Domain Value Object。

### 19.8 Terminal State

只有全部必需 Gate 通过才进入 AIAnalysis Completed。Rejected/Failed 不含可冒充正式结果的隐藏候选；Raw Output 受限保留或不保留，按隐私/调试策略决定。

---

## 20. Hallucination Mitigation

### 20.1 Prevention Layers

1. 确定性事实在模型外计算；
2. Scope/Output Contract 明确；
3. Frozen Evidence 和 Published Knowledge Grounding；
4. Context Authority 标签；
5. Structured Candidate；
6. Fact/Citation/Conflict/Risk Validation；
7. Abstention/Insufficient Evidence；
8. Human Review 与持续 Evaluation。

### 20.2 Unsupported Claims

重要 Claim 无 Source/Evidence 时必须移除、弱化为一般性传统文化说明（若允许且明确）或拒绝生成。不得通过添加模糊 Citation 掩盖。

### 20.3 Uncertainty Language

使用批准等级和条件语言；禁止“必然、一定、准确预测”等绝对表达，也不使用伪精确概率。

### 20.4 Input Ambiguity

Birth Time/Boundary 不确定时携带 TimePrecision/Ambiguity，阻断受影响结论或明确条件。模型不能自行选择候选 Chart。

### 20.5 Contradictory Evidence

保留不同流派/规则观点，说明条件和冲突。MVP 主规则优先展示不等于宣称唯一正确；完整多流派对比仍属 V1。

### 20.6 Regeneration

Regeneration 不是事实修复默认方案。若 Source/Prompt/Model/Scope 变化创建新 AIAnalysis；技术重试只处理可修复生成失败。

### 20.7 Hallucination Metrics

Fact Error、Unsupported Claim、Invalid Citation、Conflict Collapse、Scope Expansion、Absolute Claim 和 Human Found Issue；不把用户主观“准不准”当唯一质量指标。

---

## 21. Citation Strategy

### 21.1 Citation Types

| Citation | Supports |
|---|---|
| Calculation Fact Reference | 四柱/派生/流运等确定性事实 |
| RuleFinding Reference | 规则结果、适用条件、流派、冲突 |
| Evidence Reference | Claim 与事实/规则的正式支持链 |
| Knowledge Citation | 术语、传统观点、解释背景和来源 |
| TimelineNode Reference | 时间节点事实/分析说明 |

### 21.2 Citation Identity

Citation 使用稳定 Source Identity、Version、Locator/Chunk 和 Rights/Status。UI 展示可以简化，但专业展开可定位完整依据。

### 21.3 Claim-to-Citation Mapping

输出结构将重要 Claim 映射一个或多个 Citation，不只在末尾列参考资料。Claim/引用支持关系可验证。

### 21.4 Citation Quality

| Status | Meaning |
|---|---|
| Valid and Supporting | 来源存在、版本正确、内容支持 Claim |
| Existing but Weak | 来源相关但支持有限，需弱化表达 |
| Conflicting | 多来源/规则冲突，需呈现冲突 |
| Invalid | 不存在、版本/权利不符或不支持 |

具体正式 EvidenceStatus 仍以 Domain Model 为准，本表是验证语义，不新增 Value Object。

### 21.5 Rights Withdrawal

停止新引用 Withdrawn 内容；历史 Frozen Report 处理由 Knowledge Rights/Legal Governance 决定，不由 AI 重写。再生成使用当前允许版本并创建新 Report/Analysis。

### 21.6 Citation Display

普通用户先看到通俗依据，专业依据可展开。不得显示受限全文、内部 Prompt 或其他用户 Evidence。

### 21.7 Citation Metrics

Citation Coverage、Existence、Support、Rights、Version、Orphan、Duplicate 和 User Expand/理解度。Coverage 高不等于支持有效。

---

## 22. AI Cache

### 22.1 Cache Categories

| Cache | Allowed Content | Source of Truth |
|---|---|---|
| Retrieval Cache | Ranked Candidate References/Score Metadata | Knowledge/Index |
| Embedding Cache | Approved Knowledge/临时去标识 Query Vector | Knowledge/Embedding Registry |
| Context Assembly Cache | Version-complete Source Manifest/安全摘要 | Upstream Sources |
| Validated AI Result Cache | 同主体/同正式意图的已验证结果引用 | AIAnalysis |
| Provider Prefix/Capability Cache | 非敏感稳定上下文/能力（如 Provider 支持） | Registry/Policy |

### 22.2 Key Completeness

Key 至少包含 Task、Scope、Snapshot、RuleRun、EvidenceBundle、Timeline、Knowledge/Index、Prompt、Model、Route、Validation/Risk、Language、Subject/Tenant View 和 Output Contract Version。

### 22.3 Privacy Isolation

私人 Conversation、Report 和 Analysis 不跨 User/Tenant 复用。Key 不含明文 Birth、Question 或 Prompt。缓存命中后仍验证 Ownership、Purpose 和 Consent。

### 22.4 Cache Eligibility

只有完成验证的结果、可重建检索投影或明确无敏感内容的前缀可缓存。Raw Output、Rejected Candidate、Prompt Secret（本就禁止）和未知 Rights 内容不缓存为正式结果。

### 22.5 Invalidation

Consent/Deletion、Knowledge Rights、Policy/Prompt/Model Status、Security Incident、Source Version 和 Authorization 变化触发失效或自然 Version Miss。Frozen 历史不因新版本被覆盖。

### 22.6 TTL and Retention

按 Classification、Purpose、Operation 和 Source 生命周期设置；具体数值待隐私/成本评审。Cache 不是绕过正式 Retention 的副本。

### 22.7 Cache Failure

Cache 不可用时重新构建/调用或降级，不能丢失正式 AIAnalysis。Cache Poisoning 通过完整 Key、Integrity、Tenant Isolation 和 Validation 防护。

### 22.8 Cache Metrics

Hit/Miss、Validated Reuse、Stale/Invalid、Latency Saved、Cost Saved、Cross-Scope Denial 和 Eviction；不记录敏感 Key 内容。

---

## 23. AI Cost Management

### 23.1 Cost Units

按 AIAnalysis/Message/Report Section、Model、Provider、Route、Input/Output Token、Retrieval/Embedding、Retry、Validation 和最终有效结果统计。

### 23.2 AI Cost Budget

每个 Task/Plan 具有最大 Input/Output Token、Provider Calls、Retry、Fallback、Latency 和货币成本候选预算。具体数值待商业/运营确认。

### 23.3 Budget Enforcement

Planning 前估算，Assembly 后复核，Gateway 前强制。超预算时依序：减少无关 Context、压缩重复 Evidence、缩小非必需 Knowledge、选择已批准低成本 Route、分段/延后或明确拒绝。

### 23.4 Non-Negotiable Controls

不得为降本跳过 Fact、Citation、Risk、Privacy、Security、Consent 或 Audit；不得用更便宜但未 Approved/未评估模型。

### 23.5 Retry Cost

Retry 共享同一 Analysis 总预算。Parse/Citation 修复有有限次数；Provider Timeout 先确认 Operation/Usage，避免未知重复计费。

### 23.6 Fallback Cost

Fallback 创建新 AIAnalysis 时单独记录预算和原失败关联；用户/套餐是否消耗额度由产品规则待确认，不能重复扣减同一技术故障。

### 23.7 Cost Allocation

按 Environment、Task、Model、Provider、Product Version、Plan/Tenant（V2）和 Validated Outcome 分配。Metric 不使用 User 敏感属性。

### 23.8 Cost Anomaly

Token、Retry、Context、Provider Price、Queue 和 Valid Result Unit Cost 异常触发告警/Route Block。价格变化进入 Registry/Route Review。

---

## 24. AI Reliability

### 24.1 Reliability Objectives

可靠性包括：请求可靠受理、版本不漂移、有限完成时间、有效输出率、无重复正式结果、Provider 故障隔离和安全降级，而不仅是模型 HTTP Availability。

### 24.2 Reliability Patterns

| Pattern | AI Use |
|---|---|
| Durable Operation | 长任务状态持久化 |
| Idempotency | 同意图不重复正式 Analysis/扣减 |
| Timeout | Provider/Retrieval/Validation 分阶段预算 |
| Retry | 仅 Retryable 且版本不变 |
| Circuit Breaker | Provider/Model/Embedding/Reranker 独立隔离 |
| Bulkhead | AI 与 Calculation、Provider/Task Queue 隔离 |
| Backpressure | Queue/Quota/429/Accepted 状态 |
| Fallback | 新 AIAnalysis、Approved Route、完整记录 |
| Degradation | 无 AI/无 RAG/延迟生成的明确结果 |

### 24.3 Timeout

设置连接、首字节/首有效结果、总生成、Retrieval、Validation 和 Operation 总预算。上游 Approved AI 首个有效响应 P95 目标 ≤15 秒、完整 AI Report P95 目标 ≤60 秒是测试基线，不等于单次硬超时或正式 SLO。

### 24.4 Circuit Breaker

按 Provider/Model/Region/Capability 维护 Circuit，基于错误率、Timeout、Rate Limit、Invalid Output 和最小样本。Open 后停止新 Route，保留确定性能力；Half-Open 小流量验证。

### 24.5 Bulkhead

Conversation、Report、Evaluation、Embedding/Index 和高风险人工任务分 Queue/Concurrency/Quota，防一个 Task 耗尽所有 AI 资源。

### 24.6 Durable State

Planned/Generating/Validating/Completed/Rejected/Failed 状态持久化。Worker 崩溃、Broker 重投或部署不丢正式进度，不从 Raw Provider 状态猜 Completed。

### 24.7 Dependency Failure

Knowledge、Vector、Provider、Cache、Broker、Object 和 Observability 分别有降级；必需 Evidence/Validation 不可用时阻断正式输出。

---

## 25. AI Retry Strategy

### 25.1 Retry Eligibility

| Failure | Auto Retry | Rule |
|---|---|---|
| Network/Transient Provider | 是，有限 | 同 Model/Prompt/Plan/Idempotency |
| Provider Rate Limit | 是，遵守 Retry-After/预算 | 不切换模型 |
| Timeout | 条件性 | 先确认是否已产生结果/Usage |
| Structural Parse | 有限修复/重生成 | 不改变事实/Scope |
| Invalid Citation/Fact | 仅批准修复次数 | 再失败 Rejected |
| Authorization/Consent | 否 | 终止/等待新用户决定 |
| Scope/Risk Prohibited | 否 | Safe Refusal/Rejected |
| Model Blocked/Retired | 否（同 Analysis） | 新 Fallback Analysis 或失败 |
| Budget Exhausted | 否 | 降级/拒绝/新意图 |

### 25.2 Retry Identity

技术 Retry 保持同 AIAnalysisId、AnalysisPlan、PromptVersion、ModelReference、EvidenceBundle、Knowledge Version 和 Output Contract。只增加 Attempt 技术记录。

### 25.3 Retry Budget

限制 Max Attempts、Total Time、Token 和 Cost；具体数值按 Task/Provider 评估。多层 SDK/Gateway/Worker 只有一个 Retry Owner，防重试乘法。

### 25.4 Backoff

使用有限指数退避与抖动，遵守 Provider Retry-After。用户可查询 Operation，不通过重复点击创建新 Analysis。

### 25.5 Repair

结构/Citation 修复使用最小失败信息和原 Source Manifest，不把完整错误/Prompt 发送到未批准模型。Repair Output 重新通过全部 Gate。

### 25.6 Exhaustion

达到预算进入 Failed/Rejected/Degraded 或 Manual Review，记录 Safe Error、Attempts、Cost 和 Root Category。禁止无限 Retry。

---

## 26. AI Degradation

### 26.1 Degradation Levels

| Level | Available | User Semantics |
|---|---|---|
| Full | RAG + AI + Validation + Citation | 完整受支持 AI 解读 |
| No Knowledge Enhancement | Facts/Evidence + AI，若政策允许 | 明确不含扩展知识，不伪造 Citation |
| Rule/Evidence Only | Deterministic Facts、RuleFinding、Evidence | 无 AI 生成，展示结构化依据 |
| Saved Assets Only | 已保存 Chart/Report/Conversation History | 新生成暂不可用 |
| AI Disabled | 确定性排盘与基础服务 | 明确 AI 不可用/稍后重试 |

### 26.2 Trigger

Provider/Model Circuit、Retrieval/Index、Budget/Quota、Security/Privacy Incident、Validation Regression、Prompt/Model Blocked、Region/Compliance 或 Queue Overload。

### 26.3 Fallback Model

只有 Approved、兼容 Prompt/Output/Risk/Region、通过 Evaluation 的 Fallback Model 可用。切换创建新 AIAnalysis，不改变原 Analysis ModelReference。

### 26.4 User Communication

显示 Accepted/Waiting/Degraded/Rejected/Failed 和可用替代，不披露内部 Prompt、Provider Secret 或攻击细节。禁止把 Rule-only 模板称为 AI Completed。

### 26.5 Report Behavior

若正式 Report 必需 AIAnalysis 而不可用，则 Awaiting/Failed，不冻结伪完整报告；若产品批准无 AI Report 类型，则其 Manifest/类型明确区分。

### 26.6 Recovery

依赖恢复后 Canary、Evaluation 和 Circuit Half-Open，逐步处理新任务。积压任务重新验证 Consent、Authorization、Version、Budget 和用户是否已删除。

### 26.7 Degradation Governance

每个 Level 有 Owner、Trigger、Runbook、Metric、用户文案和解除条件。Emergency 降级审计并事后 Review。

---

## 27. AI Observability

### 27.1 Observability Scope

覆盖 Planning、Retrieval、Assembly、Gateway、Generation、Parsing、Validation、Cache、Retry、Fallback、Degradation、Queue、Cost 和 Human Review。

### 27.2 Safe Dimensions

Environment、Task、RouteVersion、ModelReference、PromptVersion、Knowledge/Index Version、Risk Class、Result、Error Family、Attempt、Cache Status、Language 和 Release。禁止 User/Birth/Question/Prompt/Raw Output 高敏感或高基数 Label。

### 27.3 Logs

记录阶段、Identity/Version 安全引用、Duration、Token/Cost、Result、Safe Error、Correlation。不得记录完整 Prompt、Context、Conversation、Provider Raw Output 或 Report。

### 27.4 Metrics

Metrics 是质量和运行信号，不成为 AIAnalysis Source of Truth。No Data 与 Healthy 分离。

### 27.5 Traces

Span 覆盖 Retrieval、Gateway、Provider、Validation 和 Cache，Attribute 去敏。Provider Request ID 受控映射，不把 Payload 放入 Trace。

### 27.6 Dashboards

| Dashboard | Focus |
|---|---|
| AI Reliability | Queue、Availability、Timeout、Circuit、Retry |
| AI Quality | Fact/Citation/Risk/Structure、Drift、Human Review |
| Retrieval | Zero Result、Ranking、Rights、Index Lag |
| Cost | Token、Valid Result Unit Cost、Provider/Task |
| Security/Privacy | Injection、Leakage、Consent/Region、Provider |
| Release | Prompt/Model/Route Canary 与回归 |

### 27.7 Incident Correlation

通过 AIAnalysisId、OperationId、CorrelationId、Prompt/Model/Route Version 和 Safe Provider Request ID 调查。查看 Raw Content 需 JIT、Purpose、Masking 和 Audit，默认不可用。

### 27.8 Retention

AI Telemetry 保留按安全/隐私/成本确认，短于正式 Audit/AIAnalysis 的默认方向。删除流程覆盖可识别 Log/Trace/Cache。

---

## 28. AI Metrics

### 28.1 Reliability Metrics

- Planned/Completed/Rejected/Failed/Degraded Rate；
- Queue Depth/Oldest Age、Generation/Validation Time；
- Provider Error/Timeout/Rate Limit/Circuit；
- Retry/Fallback/Manual Review；
- Duplicate Prevented/Stuck Operation。

### 28.2 Quality Metrics

- Structural Parse Success；
- Fact Consistency/Unsupported Fact；
- Citation Existence/Support/Coverage；
- Conflict Preservation；
- Scope Compliance；
- Risk/Safety Pass/Refusal；
- Hallucination/Absolute Claim；
- User Understanding/Explanation Feedback。

### 28.3 Retrieval Metrics

Candidate/Selected Count、Zero Result、Recall/Precision/Ranking Evaluation、Rights Filter、Duplicate/Diversity、Index Lag、Latency 和 Cache Hit。

### 28.4 Cost Metrics

Input/Output Token、Provider Calls、Retry Waste、Cache Saving、Task/Model/Route Cost、Cost per Validated Result、Budget Exceeded。

### 28.5 User Metrics

AI 完成率、首个有效响应、对话继续/退出、Evidence 展开、理解度、投诉和安全拒绝。不得将“命中人生事件”或用户主观认同包装成预测准确率。

### 28.6 Security/Privacy Metrics

Injection/Jailbreak、Prompt Leakage、Cross-Scope Denial、Redaction Failure、Unapproved Provider/Region Attempt、Consent Block、Sensitive Log Finding。

### 28.7 Metric Interpretation

单指标不代表整体质量：低 Refusal 可能是防护弱，高 Citation Coverage 可能引用无支持内容，高 User Satisfaction 可能来自迎合。使用平衡 Scorecard 与人工复核。

### 28.8 Cardinality

不把 UserId、Question、Birth、Citation Text 或 Raw Error 作为 Metric Label。个案调查使用受控 AIAnalysis/Audit 引用。

---

## 29. AI Quality Evaluation

### 29.1 Evaluation Layers

| Layer | Purpose |
|---|---|
| Deterministic Unit | Parser、Fact、Citation、Scope、Budget |
| Offline Golden Set | 固定事实/Evidence 下质量回归 |
| Adversarial/Safety | Injection、Jailbreak、Leakage、高风险 |
| Retrieval Evaluation | Chunk/Embedding/Ranking/Rights |
| Model/Prompt Matrix | Provider、Model、Prompt、Language 兼容 |
| Human Review | 通俗性、克制、术语、支持度和风险 |
| Shadow/Canary | 真实分布的去敏/受控比较 |
| Online Monitoring | Drift、投诉、质量与成本趋势 |

### 29.2 Evaluation Dataset

包含专家批准命例、输入不确定、边界、规则冲突、证据有限、多主题、未来三年、零检索、高风险和攻击样例。数据来源、Consent、Version、Rights 和 Retention 可追踪。

### 29.3 Evaluation Dimensions

Fact Accuracy Against Source、Groundedness、Citation Support、Conflict Handling、Uncertainty、Risk Safety、Scope、Readability、Terminology、Localization、Latency、Cost 和 Stability。

### 29.4 No Scientific Accuracy Claim

评估“是否忠实于已批准规则与证据、是否易懂安全”，不评估或宣传命理能否科学预测未来。

### 29.5 Automated Evaluators

确定性检查优先。Model-as-Judge 若使用，记录 Model/Prompt/Version、Bias/Agreement 与人工校准，不作为唯一发布门禁。

### 29.6 Human Review

命理专家评 Rule/Evidence 表达，内容/产品评易懂性，安全/法律评高风险与隐私。Reviewer 使用去标识化最小数据并受 Audit。

### 29.7 Release Gate

新 Prompt/Model/Embedding/Retrieval/Route 必须在核心质量维度不低于批准门槛，Critical Fact/Citation/Safety 回归为阻断。具体阈值待评估基线确认。

### 29.8 AI Drift

监控同 ModelReference 行为、Output Distribution、Validation Failure、Citation、Refusal、Token、Latency 和 Cost。Provider 静默变化、知识分布或用户输入变化都可能导致 Drift。

### 29.9 Drift Response

验证 Telemetry → 隔离 Provider/Route → 固定样例复测 → Block/Canary/Rollback Prompt 或 Route → 新 Version 发布。不能用调整指标口径掩盖。

---

## 30. AI Governance

### 30.1 Governance Assets

Provider、Model、Embedding、Prompt、Route、Retrieval/Index、Validation、Risk Policy、Evaluation Set、Cost Policy、Cache Policy 和 Human Review Standard。

### 30.2 Governance Roles

| Role | Responsibility |
|---|---|
| AI Product Owner | 用例、用户价值、范围和版本 |
| AI Architect | Gateway、Routing、Context、Reliability |
| Domain Expert | 规则/Evidence/术语/冲突表达 |
| Knowledge Owner | Source、Rights、Chunk、Citation |
| Prompt Owner | Definition、Version、Review、Rollback |
| Model Owner | Registry、Provider、Evaluation、Drift |
| Security/Privacy | Data、Injection、Provider、Incident |
| Evaluation Owner | Dataset、Metric、Threshold、Human Review |
| Cost/Operations | Budget、SLO、Capacity、Incident |
| Publisher/Auditor | 职责分离、发布、追溯 |

### 30.3 Lifecycle

Proposed → Evaluating → Approved/Published → Canary → Stable → Deprecated/Blocked → Retired。不同资产使用其 Approved 状态机；本文生命周期是治理视图，不重定义 Domain Entity。

### 30.4 Release Package

包含 Purpose、Version、Compatibility、Dataset/Evaluation、Security/Privacy、Cost/Latency、Canary、Rollback、Drift Metrics、Owner 和 Change Summary。

### 30.5 Change Separation

应用部署、Prompt、Model Route、Knowledge/Index、Risk Policy 和 Provider Credential 是独立 Change。可协调发布，但不能互相绕过 Gate。

### 30.6 Emergency Block

安全、隐私、质量或供应商事件可立即 Block Model/Prompt/Route/Knowledge 新使用；已完成历史不改写。恢复需根因、评估和批准。

### 30.7 User Feedback Governance

反馈按 Consent、去标识化和 Purpose 使用，仅形成评估/改进候选。不自动修改生产资产，不宣传为“预测准确率训练”。

### 30.8 Audit

记录 Author/Reviewer/Publisher、Version、Evaluation、Route、Block/Rollback、Provider、Cost Policy 和人工例外，不记录完整敏感 Prompt/Context 于普通 Audit。

### 30.9 Technology Lifecycle

无 Owner、EOL、无法锁定版本、隐私条款不合格或持续 Drift 的模型/Provider 进入 Constrained/Retired。退出计划保留历史 Reference。

### 30.10 Governance Cadence

每个 Milestone、Prompt/Model Release、重大 Incident、法律/Provider 变化复审质量、安全、隐私、成本、Drift、投诉和债务。

---

## 31. AI ADR Reference Matrix

| Topic | ADR Required | Trigger Example |
|---|---|---|
| Provider Strategy | Yes | 单/多 Provider、Region、Exit 或直连边界变化 |
| Model Gateway | Yes | 绕过 Gateway 或改变核心调用/验证责任 |
| Provider Abstraction | Yes | Provider 类型进入 Domain/API |
| Model Registry | Yes | Identity、状态、版本/漂移模型变化 |
| Model Routing | Yes | Routing Inputs、Planning Time 或 Fallback 语义变化 |
| Prompt Strategy | Yes | Prompt Pipeline、资产边界或内容执行能力变化 |
| Prompt Version | Yes | Identity/Version、Published/回滚语义变化 |
| Prompt Governance | Yes | Review、职责分离、Evaluation Gate 变化 |
| RAG Strategy | Yes | RAG 变为事实/Evidence 来源或新数据边界 |
| Embedding Strategy | Yes | Model、个人数据 Embedding、Index/Storage 变化 |
| Chunk Strategy | Yes | Chunk Identity、Rights、Source/Version 变化 |
| Retrieval Strategy | Yes | Hybrid/Ranking/Threshold/Filter 责任变化 |
| Citation Strategy | Yes | Claim Mapping、Support、Rights 或历史策略变化 |
| Context Assembly | Yes | Authority、Scope、Budget 或敏感数据边界变化 |
| AIConversation Memory | Yes | 跨 Conversation/Chart Memory 或长期 Embedding |
| AI Output Validation | Yes | 删除/替换 Fact/Citation/Risk Gate |
| AI Cache | Yes | 跨用户复用、Raw Output Cache 或 Source-of-Truth 变化 |
| AI Cost Policy | Yes | Budget、Quota、成本与质量取舍原则变化 |
| AI Reliability | Yes | Retry、Circuit、Fallback、Degradation 语义变化 |
| AI Evaluation | Yes | Dataset、Metric、Human/Model Judge 或 Gate 变化 |
| AI Observability | Yes | 记录内容、Retention、Metric/Drift 责任变化 |
| AI Governance | Yes | Asset Lifecycle、Emergency Block、发布责任变化 |
| AI Tool Use | Yes | 任何 Database/Internet/Code/File/Action Tool |

任何涉及以上主题的修改，都不得直接修改本文档。必须先通过 ADR，记录背景、候选、Domain/Data/API/Security 影响、Evaluation、Cost、迁移、回退、Owner 和验证；批准后才能更新 AI Architecture Baseline。

---

## 32. AI Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐做法 |
|---|---|---|---|
| Giant Prompt | 把所有规则、知识、历史塞入单 Prompt | 超窗口、冲突、成本、难评审 | 分层 Pipeline、RAG、Context Budget、模块化资产 |
| Hardcoded Prompt | Prompt 固定在代码中 | 无版本/审核/回滚 | Prompt Registry、Published Version、Reference |
| Direct Provider Call | 业务模块绕过 Gateway | 安全、成本、版本和观测失控 | 统一 Model Gateway + Adapter |
| No Citation | 输出无来源 | 不可追溯、Hallucination | Claim-to-Evidence/Citation Mapping 与验证 |
| No Validation | Raw Output 直接正式展示 | 事实/风险/结构错误 | 多阶段 Output Validation |
| Hallucination Accepted | 将模型自信当事实 | 用户误导、报告污染 | Deterministic Source、Unsupported Claim Gate、Abstain |
| Unlimited Context | 尽可能发送全部数据 | 隐私、成本、Injection、注意力稀释 | 最小 Context、Budget、Scope Manifest |
| Unlimited Retry | 无总次数/时间/成本 | 重试风暴、重复费用 | 单 Retry Owner、有限预算、Circuit/DLQ |
| Single Provider | 核心代码绑定一个 Provider | Outage、合规、成本锁定 | Provider Abstraction、Exit Plan、受控 Multi-Provider |
| No Prompt Version | “最新 Prompt”覆盖历史 | 无法复现/回滚 | Prompt Identity + Immutable Version |
| No Model Version | 只记市场模型名 | Drift、历史不可解释 | Model Registry + Actual ModelReference |
| No Cost Control | 无 Token/Calls/Budget | Denial of Wallet、不可持续 | Plan Budget、Quota、Cost per Valid Result |
| No Quality Evaluation | 只看能否生成 | Fact/Citation/Safety 回归 | Offline/Human/Canary/Drift Evaluation |
| No Fallback | Provider 故障全平台 AI 中断 | 可用性差 | Approved Fallback Policy + 新 AIAnalysis |
| Prompt in Code | Prompt 与部署强绑定 | 内容治理绕过、变更慢 | Registry/Review/Independent Release |
| AI Computes Chart | 让模型推算四柱/流运 | 不可复现、事实错误 | Deterministic Calculation Engine |
| AI Creates Evidence | 模型自称依据 | 循环证明、伪引用 | EvidenceBuilder/Bundle 在 AI 之前冻结 |
| Vector Similarity as Truth | 高相似度直接决定结论 | 无关/错误知识变事实 | Filter、Ranking、Citation、Rule/Evidence Authority |
| Cross-User Cache | 私人输出/上下文跨用户复用 | 严重隐私泄漏 | Subject/Tenant/Version 隔离、默认不共享 |
| Silent Fallback | 同 Analysis 偷换模型/Provider | ModelReference 失真、质量漂移 | 新 AIAnalysis、Route/Fallback Audit |
| Silent Model Upgrade | Provider “latest”自动替换 | 行为/合规不可控 | Locked Reference、Drift Monitor、Registry |
| Model Self-Validation Only | 让模型判断自己是否正确 | 共同偏差、漏错 | 确定性 Validator + 独立/人工校准 |
| RAG without Rights Filter | 检索未发布/撤下内容 | 版权/合规和虚假依据 | Published/Rights Hard Filter |
| Conversation as Source of Truth | Summary/Memory 覆盖事实 | 错误累积、跨会话污染 | Snapshot/Evidence Authority、Memory 仅辅助 |
| Token Truncation Blindly | 直接截断末尾 | 丢 Citation/风险/冲突 | Priority-aware Assembly、分段或拒绝 |
| Metrics as Accuracy Claim | 将用户认同/模型一致宣传为预测准确 | 误导产品定位 | 衡量 Grounding/理解/安全，不宣称科学预测 |
| User Feedback Auto-Training | 反馈自动改 Prompt/Rule | 投毒、偏差、无审核 | Consent、去标识、Evaluation、人工发布 |
| Secret in Prompt | Prompt 携带 Key/内部敏感 | Leakage/Provider 暴露 | Secret Manager、Prompt 无 Secret |
| Unrestricted Tool Calling | 模型可任意执行外部动作 | 越权、SSRF、数据破坏 | 默认无 Tool；未来 Allowlist/Approval/Sandbox/ADR |

---

## 33. Review Checklist

### 33.1 Baseline and Boundaries

- [ ] 文档是否为 Review 0.9。
- [ ] 是否严格继承 01–12 Approved 基线。
- [ ] 是否未修改 Domain、Aggregate、Entity、Value Object、Event、API、Data、Technology、Engineering 或 Security Baseline。
- [ ] AI 是否不计算事实、不创建 Evidence、不扩大 Scope、不修改 Report/Chart。
- [ ] 是否没有 Prompt 内容、代码、SDK、模型配置、Tool 实现或部署资产。
- [ ] 是否未进入编码阶段。

### 33.2 Provider and Model

- [ ] 所有生产调用是否经过 Model Gateway。
- [ ] Provider Adapter 是否隔离 SDK/Payload/Error。
- [ ] Model Registry 是否记录 Version、Region、Privacy、Evaluation、Cost 和 Status。
- [ ] ModelReference 是否在 Planned 前锁定。
- [ ] 技术 Retry 是否不切换 Model/Prompt/Bundle。
- [ ] Fallback 是否创建新 AIAnalysis 并保留原失败历史。
- [ ] Multi-Provider 是否基于真实需求而非无治理扩张。

### 33.3 Prompt and Context

- [ ] Prompt 是否 Registry/Version/Review/Published/回滚。
- [ ] Published Prompt 是否不可原地修改。
- [ ] Prompt 与 Model/Output/Validation 是否有兼容矩阵。
- [ ] Context Authority、Manifest、Window/Budget/Token 是否明确。
- [ ] 是否移除身份、详细地址、工单和无关 Conversation。
- [ ] Conversation Memory 是否不跨 User/Chart 且不成 Source of Truth。

### 33.4 RAG and Citation

- [ ] RAG 是否只用 Published、Rights 有效 Knowledge。
- [ ] Embedding/Chunk/Index 是否版本化且可重建。
- [ ] 是否默认不持久化个人数据 Embedding。
- [ ] Structured/Lexical/Vector、Ranking、Threshold 和 Zero Result 是否治理。
- [ ] Vector Similarity 是否未被当作事实/Evidence。
- [ ] Claim-to-Citation、Existence、Support、Rights 和 Version 是否验证。

### 33.5 Validation, Security and Privacy

- [ ] Raw Output 是否始终不可信。
- [ ] Structure、Scope、Fact、Evidence、Citation、Conflict、Risk、Leakage、Length 是否全部 Gate。
- [ ] Prompt Injection/Jailbreak/Leakage 和 Tool 风险是否覆盖。
- [ ] Provider 是否仅接收去标识化最小 Context。
- [ ] Consent/Authorization/Deletion/Region 是否在调用和重放时重验。
- [ ] Observability/Cache 是否不含完整 Prompt/Context/Raw Output。

### 33.6 Reliability, Cost and Governance

- [ ] Timeout、Retry Budget、Circuit、Bulkhead、Backpressure 和 Degradation 是否明确。
- [ ] Cost 是否按 Validated Result、Task、Model、Retry 统计。
- [ ] 成本优化是否不跳过质量/安全 Gate。
- [ ] Evaluation 是否覆盖 Golden、Adversarial、Retrieval、Human 和 Canary。
- [ ] Drift 是否有 Detection、Block、Rollback/新版本流程。
- [ ] Prompt/Model/Route/Knowledge/Risk 是否职责分离和可审计。
- [ ] ADR Matrix 是否覆盖重大 AI 变化。
- [ ] Beta/RC/GA Scope Freeze 是否继续生效。

---

## 34. Open Questions

### 34.1 Provider and Model

1. MVP 是否生产启用一个主 Provider + 预验证备用，还是实际 Multi-Provider Active Routing。
2. 首批 Provider/Model 的 Region、Retention、Training、Subprocessor、备案/登记和 SLA。
3. Provider 无稳定版本标识时，如何定义 ModelReference 与 Drift 阻断。
4. Fallback Model 的 Task/Language/Risk 兼容矩阵和产品用户语义。
5. 是否需要独立 Validation Model/Reranker，以及其成本/安全边界。

### 34.2 Prompt

1. Prompt Registry 的物理归属、访问和发布工具。
2. PromptVersion 的版本规则、兼容矩阵和 Emergency Rollback 时限。
3. 中文首批 Prompt 的 Evaluation Set、Reviewer 和发布阈值。
4. 英文/阿拉伯语 Prompt/术语的人工复核流程。
5. 完整 Prompt 对 Auditor/Support 的可见边界。

### 34.3 RAG and Knowledge

1. 首批 Knowledge Source、Rights、Chunk 类型和正式 Citation 范围。
2. Chunk 大小/Overlap、Lexical/Vector Candidate、Rerank 和 Threshold 数值。
3. Embedding Model/Region、Index Version、重建窗口和 Retrieval SLO。
4. 是否需要独立 Reranker，还是规则/混合 Ranking 足够。
5. Rights Withdrawal 后历史 Frozen Report Citation 的展示政策。
6. 何种规模/质量证据触发独立 Search Engine。

### 34.4 Context and Conversation

1. 各 Task 的 Context/Token/Output/Cost Budget。
2. Conversation Summary 何时生成、保留多久、如何验证否定/冲突不丢失。
3. 一个 Chart 是否允许多个 Conversation 及跨会话引用策略。
4. 多候选 Birth Time 的 AI 阻断/比较流程；不得改变 Chart Boundary。
5. AI Conversation 中 Timeline 月/年粒度与三年范围细节。

### 34.5 Validation and Evaluation

1. AI Output Contract、Validation Policy 和 RiskDisposition 的正式版本/枚举。
2. Fact/Citation/Conflict/Risk 各发布阈值与允许 Repair 次数。
3. Model-as-Judge 的使用边界、校准和人工一致性要求。
4. Human Review 比例、角色、JIT 数据访问和 SLA。
5. AI Drift 的窗口、阈值、Block 和 Incident Severity。
6. 用户理解度/帮助反馈如何进入 Evaluation 而不成为准确率。

### 34.6 Reliability and Cost

1. Provider/Gateway/Retrieval/Validation Timeout 与 Retry Budget。
2. AI Valid Result Rate、First Valid Response 和 Report 的正式 SLO。
3. Queue/Worker 并发、Provider Quota、Circuit 和 Half-Open 参数。
4. Task/Plan/Tenant 的 Token/Cost Budget 和超限用户体验。
5. 技术故障 Fallback/Retry 是否消耗用户额度。
6. AI Cache 的 TTL、Eligibility 和 Validated Reuse 范围。

### 34.7 Security, Privacy and Legal

1. Provider Payload、Raw Output、Prompt/Context 和 Telemetry 的保留策略。
2. AI Content Labeling 对在线回答、Report、打印、PDF、复制/分享的要求。
3. Prompt Injection/Jailbreak/Leakage 的监控数据与隐私边界。
4. 高风险健康/婚姻/投资主题最终允许、限制与拒绝规则。
5. 是否/何时允许任何 AI Tool；当前默认不允许。
6. 研究/优化 Evaluation 数据的 Consent、去标识和撤回流程。

### 34.8 ADR Candidates

- ADR-CANDIDATE-AI-001：Multi-Provider、Model Gateway 与 Provider Exit。
- ADR-CANDIDATE-AI-002：Model Registry、ModelReference、Routing 与 Fallback 新 AIAnalysis 语义。
- ADR-CANDIDATE-AI-003：Prompt Registry、Version、Compatibility、Review 和 Rollback。
- ADR-CANDIDATE-AI-004：RAG、Chunk、Embedding、Hybrid Retrieval、Reranking 和 Citation。
- ADR-CANDIDATE-AI-005：Context Assembly、Token/Cost Budget 和 Conversation Memory。
- ADR-CANDIDATE-AI-006：Output Contract、Validation、Hallucination、Risk 和 Human Review。
- ADR-CANDIDATE-AI-007：AI Cache、Privacy Isolation、Retention 和 Reuse。
- ADR-CANDIDATE-AI-008：Timeout、Retry、Circuit、Fallback、Degradation 和 SLO。
- ADR-CANDIDATE-AI-009：Evaluation Set、Model-as-Judge、Drift 和 Release Gate。
- ADR-CANDIDATE-AI-010：AI Security、Content Labeling、Provider Region 和 Tool Policy。

---

## 35. Risks

| Risk | Manifestation | Impact | Mitigation / Gate |
|---|---|---|---|
| AI 事实越权 | 模型计算/补造 Chart | 不可复现、错误报告 | Deterministic Source + Fact Gate |
| Evidence 循环 | 模型生成自己的依据 | 伪 Citation、信任损失 | Bundle 先冻结、AI 不建 Evidence |
| Provider Lock-In | 业务直接用 SDK/Payload | 合规/成本/故障难迁移 | Gateway、Adapter、Registry、Exit |
| Silent Model Change | Provider 更新同名模型 | Drift、历史不可解释 | ModelReference、Continuous Eval、Block |
| Silent Fallback | 同 Analysis 换模型 | Version Manifest 失真 | 新 AIAnalysis + Fallback Audit |
| Giant Context | 全部历史/知识送模型 | 成本、泄漏、质量下降 | Manifest、Budget、Priority Assembly |
| Prompt Drift | 代码/配置临时改 Prompt | 无审核/回滚 | Registry、Immutable Version、Gate |
| Prompt Injection | User/Knowledge 操纵指令 | 泄漏/越权/错误 | Data Isolation、Tool Gate、Validation |
| Prompt Leakage | System/他人 Context 输出 | 安全/隐私事件 | No Secret、Scope Isolation、Leak Gate |
| RAG Rights Failure | 撤下/未发布内容被引用 | 版权/合规风险 | Hard Filter、Rights Event、Reindex |
| Retrieval Irrelevance | 高相似但不适用 | 误导 Citation | Hybrid、Rerank、Threshold、Zero Result |
| Invalid Citation | 来源存在但不支持 Claim | 虚假可信感 | Claim-Support Validation |
| Hallucination | 无 Source Claim | 用户误解 | Grounding、Abstention、Fact/Citation Gate |
| Conflict Collapse | 多观点被写成唯一结论 | 违背产品/领域基线 | Conflict Validator、等级语言 |
| Privacy Leakage | Birth/Identity 发送 Provider | 敏感数据事件 | Redaction、Manifest、Payload Scan |
| Cross-User Memory | Cache/Summary 串用户 | 严重隐私泄漏 | Tenant/Chart Isolation、Deletion |
| Unlimited Retry | Provider/Parser 循环 | 成本/Queue/重复 | Single Retry Owner、Budget、Circuit |
| No Reliable Fallback | Provider Outage 全 AI 中断 | 可用性下降 | Pre-approved Model、Rule-only Degrade |
| Fallback Quality Gap | 备用模型不兼容 Prompt | 错误/风险回归 | Compatibility Matrix、Eval、新 Analysis |
| Cost Runaway | Token/Context/Retry 激增 | 商业不可持续 | Plan Budget、Cost per Valid Result |
| Evaluation Bias | 固定集太窄/模型 Judge 偏差 | 假质量、漏风险 | Diverse Set、Human Calibration、Online Drift |
| Feedback Poisoning | 用户反馈自动影响生产 | 偏差/攻击 | Consent、Isolation、Human Governance |
| Observability Leakage | Prompt/Raw Output 进 Log/Trace | 二次数据泄漏 | Safe Metadata、JIT Investigation |
| AI Metric Gaming | 追求回答率/低拒绝 | 安全/证据质量下降 | Balanced Scorecard、Non-negotiable Gates |
| Security Tool Expansion | 模型获得任意外部动作 | SSRF/数据破坏 | Default No Tool、ADR、Allowlist/Sandbox |
| Content Compliance | 标识/高风险文案不合规 | 上线/法律风险 | Legal Gate、Labeling、Risk Policy |
| Scope Creep | 提前多流派/无界时间/Research | MVP 延期、风险扩大 | Scope Manifest、Roadmap Freeze |

---

## 36. 进入下一阶段《14-TESTING-STRATEGY.md》所需输入条件

- [ ] `13-AI-ARCHITECTURE.md` 已完成评审并成为 Approved 1.0 AI Architecture Baseline。
- [ ] AI Context Ownership、AIAnalysis/Conversation/Message 与上游 Context 边界已确认。
- [ ] Model Gateway、Provider Adapter、Multi-Provider 和 Direct Call 禁令已确认。
- [ ] Model Registry、ModelReference、状态、Routing、Planning Time Lock 和 Fallback 新 AIAnalysis 语义已确认。
- [ ] Prompt Registry、PromptVersion、Review、Evaluation、Published、Compatibility 和 Rollback 已确认。
- [ ] RAG、Knowledge Rights、Chunk、Embedding、Index、Hybrid Retrieval、Ranking、Threshold 和 Citation 已确认。
- [ ] Context Manifest、Context Window/Budget、Token Budget、Authority、Redaction 和 Conversation Memory 已确认。
- [ ] Output Structure、Fact、Evidence、Citation、Conflict、Risk、Injection/Leakage 和 Length Validation 已确认。
- [ ] Hallucination、Uncertainty、Conflict 和 Unsupported Claim 处置已确认。
- [ ] AI Cache 的 Eligibility、Key、Tenant Isolation、TTL、Invalidation 和 Deletion 已确认。
- [ ] AI Cost Budget、Token/Retry/Fallback、Quota、Cost per Valid Result 和告警已确认。
- [ ] Timeout、Retry、Circuit、Bulkhead、Backpressure、Degradation 和 Recovery 已确认。
- [ ] AI Logs/Metrics/Traces/Dashboard 的去敏和 Retention 已确认。
- [ ] Evaluation Dataset、Golden/Adversarial、Retrieval、Human Review、Canary、Drift 和 Gate 已确认。
- [ ] Provider Region、Retention、Training、Subprocessor、Content Labeling 和高风险主题已有安全/隐私/法律结论或明确阻断。
- [ ] ADR Reference Matrix 中影响测试策略的决策已批准，或 14 继续保持候选而不擅自实现。
- [ ] Beta、RC、GA Scope Freeze 继续生效。
- [ ] 下一阶段只生成 Testing Strategy，不生成测试代码、Prompt、评测脚本、模型配置、SDK 或部署资产。

只有本 AI 架构通过评审后，才可以生成 `14-TESTING-STRATEGY.md`。本次不得生成该文件，也不得进入编码阶段。

