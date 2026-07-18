# AI 八字命理分析平台：统一术语与架构附录

**文档编号：** 16  
**文档类型：** Glossary, Documentation Governance & Architecture Appendix  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md` 至 `15-ARCHITECTURE-DECISION-RECORDS.md`（按当前正式决策均为 Approved 1.0）  
**目标读者：** 产品、命理专家、架构、设计、研发、测试、安全、隐私、法律、AI、数据、平台、运维、内容与项目治理人员

---

## Version 0.9 Change Log

- 首次建立 01～15 文档体系的统一阅读顺序、结构、依赖和交叉引用。
- 建立需求、领域、数据、应用、API、技术、安全、AI、测试和 ADR 的追踪矩阵。
- 建立统一 Glossary、Acronyms、命名和版本规范。
- 建立文档 Ownership、Review、Version History、Architecture Timeline 和完整索引。
- 汇总架构原则、约束、安全、AI、测试、ADR、风险、待确认事项和未来改进。
- 记录 `DOC-NOTE-001`：当前正式输入已确认 01～15 为 Approved 1.0，但部分文件头仍保留早期工作状态；本文件不修改这些文件。
- 本文件不包含代码、配置、脚本、目录或技术实现。

---

## 1. Document Purpose

### 1.1 目标

本文档是 AI 八字命理分析平台架构文档体系的导航、统一语言和治理附录。它帮助不同角色在不改变任何 Approved Baseline 的前提下，理解同一术语在产品、领域、数据、应用、API、技术、安全、AI、测试和 ADR 中的准确含义。

### 1.2 权威边界

本文档是索引和摘要，不替代来源文档。若摘要与来源基线出现差异，以相应 Approved 来源文档为准，并将差异记录为 `Documentation Note` 或 `Open Question`，不得在本文件中重定义领域或架构。

### 1.3 适用用途

- 新成员入门和角色化阅读；
- 需求到架构、测试和治理的追踪；
- 术语、缩写、命名与版本一致性检查；
- 文档 Owner、评审与变更入口查找；
- ADR、风险、待确认和未来改进索引；
- 开发前 Architecture Baseline 完整性检查。

### 1.4 不包含内容

本文不包含：

- 对 Product、SRS、Domain、Data、Application、API、Technology、Operations、Security、AI、Testing 或 ADR Baseline 的修改；
- 新领域对象、状态、关系、API、技术选型或测试阈值；
- 对命理争议、法律问题或 ADR Candidate 的擅自决定；
- 代码、配置、脚本、项目目录或执行资产；
- 编码阶段授权。

### 1.5 冲突处理

发现问题时只使用：

- `Open Question`：仍需产品、专家、法律、架构或工程输入；
- `Future Improvement`：不改变当前基线的后续文档治理增强；
- `Documentation Note`：格式、标题、状态元数据或引用层面的说明。

本文不创建或裁决新的 `Baseline Conflict`；重大架构冲突应按 15 的 ADR 治理处理。

---

## 2. How to Read This Documentation

### 2.1 先问“我要回答什么”

| 问题 | 首选文档 | 辅助文档 |
|---|---|---|
| 产品为什么存在、为谁服务 | 01 | 02、06 |
| 系统必须做什么、如何验收 | 02 | 14 |
| 系统总体如何分层与协作 | 03 | 07、09 |
| 业务对象和不变量是什么 | 04 | 05、07 |
| 数据如何标识、版本、删除 | 05 | 12 |
| 何时实施和发布 | 06 | 11、14 |
| Use Case、Command、Saga 如何组织 | 07 | 04、08 |
| API 契约遵循什么规则 | 08 | 07、12 |
| 技术能力与基础设施边界 | 09 | 11 |
| 工程实现应遵循什么规范 | 10 | 09、14 |
| 如何部署、运行、恢复 | 11 | 09、12 |
| 如何保护身份、权限与隐私 | 12 | 05、08、11 |
| AI、Prompt、RAG、模型如何治理 | 13 | 04、12、14 |
| 如何证明质量和发布可接受 | 14 | 02、06、11、13 |
| 如何改变架构基线 | 15 | 所有受影响基线 |
| 术语、索引和交叉引用在哪里 | 16 | 对应来源文档 |

### 2.2 规范强度

- `Must`：MVP 或对应版本不可缺少的需求；
- `Should`：重要但可在明确权衡后延期；
- `Could`：有价值但非当前发布阻断；
- `Won’t`：当前版本明确不做，不代表永久禁止；
- `Approved Baseline`：已经评审通过、后续设计必须继承；
- `Open Question`：尚未批准，不得作为实现事实；
- `ADR Candidate`：需要正式架构决策，不代表已选择方案。

### 2.3 摘要不替代上下文

Architecture Principles Summary、Glossary 和矩阵用于导航。实施、评审或争议判断必须回到相关来源章节读取完整 Context、限制和后果。

### 2.4 版本读取规则

阅读时同时确认：Document Version、Domain/Data Version、API/Event Version、Algorithm/Rule/Knowledge/Prompt/Model/Validation Version。名称相似不代表版本含义相同。

### 2.5 决策变化入口

发现现有设计不再适用时，先查 15 的 Current Decision Register 和 Candidate Register。重大变化先提交 ADR，不能直接编辑 Approved Baseline 或以实现替代决策。

---

## 3. Reading Order

### 3.1 全量架构阅读顺序

1. `01-PRODUCT-VISION.md`：定位、用户、版本与成功边界；
2. `02-SRS.md`：可测试需求、流程、异常与非功能基线；
3. `03-SYSTEM-ARCHITECTURE.md`：系统结构、Context 与主要数据流；
4. `04-DOMAIN-MODEL.md`：唯一正式领域模型；
5. `05-DATA-MODEL.md`：领域到逻辑数据模型映射；
6. `06-ROADMAP.md`：阶段、依赖、里程碑和范围冻结；
7. `07-APPLICATION-ARCHITECTURE.md`：Use Case、Command、Query、Saga 与事务；
8. `08-API-DESIGN.md`：资源、协议语义、错误与兼容；
9. `09-TECHNOLOGY-ARCHITECTURE.md`：技术栈与基础设施边界；
10. `10-IMPLEMENTATION-GUIDE.md`：工程结构、实现与协作规范；
11. `11-DEPLOYMENT-OPERATIONS.md`：环境、发布、运行、恢复与运维治理；
12. `12-SECURITY-PRIVACY.md`：身份、权限、数据生命周期和威胁；
13. `13-AI-ARCHITECTURE.md`：AI Gateway、Prompt、RAG、验证与评估；
14. `14-TESTING-STRATEGY.md`：测试体系、质量门禁和发布证据；
15. `15-ARCHITECTURE-DECISION-RECORDS.md`：决策治理与登记；
16. `16-GLOSSARY-AND-APPENDIX.md`：统一语言、索引和附录。

### 3.2 产品与业务角色

推荐：01 → 02 → 06 → 04 的统一语言/高风险边界 → 12 的 Consent/用户权利 → 14 的验收门禁 → 16。

### 3.3 命理专家

推荐：01 → 02 的待专家确认项 → 04 的 Chart/Rule/Evidence/争议表达 → 13 的 AI Grounding → 14 的黄金命例 → 16。

### 3.4 架构与研发

推荐：03 → 04 → 05 → 07 → 08 → 09 → 10 → 12 → 13 → 14 → 15 → 16，同时回查 01/02 的目标与验收。

### 3.5 安全、隐私与法律

推荐：01/02 的产品边界 → 05 的分类/删除 → 07/08 的授权边界 → 11 的运行访问 → 12 全文 → 13 的 Provider 数据 → 14 的验证 → 15 的决策 Gate。

### 3.6 测试与发布

推荐：02 → 04/05 不变量 → 06 Release Gate → 07/08 契约 → 11 可运行性 → 12/13 专项风险 → 14 → 15。

### 3.7 快速定位顺序

遇到术语先查本文件 Glossary；遇到“为什么这样决定”查 15；遇到“现在是否必须”查 02/06；遇到“怎样才算通过”查 14。

---

## 4. Documentation Structure

### 4.1 文档分层

| 层级 | 文档 | 主要回答 |
|---|---|---|
| Product | 01、02、06 | 为什么、做什么、何时交付 |
| Core Architecture | 03、04、05 | 系统、领域、数据是什么 |
| Interaction Architecture | 07、08 | 用例与外部契约如何协作 |
| Technology & Engineering | 09、10、11 | 用什么能力、如何组织和运行 |
| Cross-Cutting | 12、13、14 | 安全隐私、AI、质量如何约束全部层级 |
| Governance | 15、16 | 如何改变、索引和解释文档体系 |

### 4.2 权威主题

- Product Positioning：01；
- Executable Requirements：02；
- Overall System Boundary：03；
- Domain Model：04；
- Logical Data Model：05；
- Delivery Sequence：06；
- Application Use Case & Consistency：07；
- API Contract Principles：08；
- Technology Baseline：09；
- Engineering Rules：10；
- Deployment & Operations：11；
- Security & Privacy：12；
- AI Architecture：13；
- Testing & Quality Gate：14；
- Architecture Decision Governance：15；
- Terminology & Index：16。

### 4.3 继承方向

后序文档继承前序 Approved Baseline，但不自动拥有修改权限。跨层重大变化由 ADR 授权并显式更新受影响基线。

### 4.4 Document Set Boundary

01～16 共同构成当前 Architecture Documentation Set。本文的完成不代表可以进入编码；编码授权必须由用户另行明确确认。

---

## 5. Document Dependency Matrix

### 5.1 直接依赖与输出

| No. | Document | Primary Inputs | Primary Outputs / Consumers |
|---:|---|---|---|
| 01 | Product Vision | 正式产品决策 | 02、03、06、12、13 |
| 02 | SRS | 01 | 03～14 的需求与验收输入 |
| 03 | System Architecture | 01、02 | 04、05、07、09、11 |
| 04 | Domain Model | 01～03 | 05、07、08、10、12、13、14 |
| 05 | Data Model | 01～04 | 07～12、14 |
| 06 | Roadmap | 01～05 | 阶段、Gate、07～14 实施顺序 |
| 07 | Application Architecture | 01～06 | 08～14 的用例与一致性输入 |
| 08 | API Design | 01～07 | 09～12、14 的契约输入 |
| 09 | Technology Architecture | 01～08 | 10、11、12、14 |
| 10 | Implementation Guide | 01～09 | 工程与 11、14 实施规范 |
| 11 | Deployment & Operations | 01～10 | 12、14 的运行与恢复输入 |
| 12 | Security & Privacy | 01～11 | 13、14 的安全隐私 Gate |
| 13 | AI Architecture | 01～12 | 14 的 AI/RAG 测试输入 |
| 14 | Testing Strategy | 01～13 | 发布质量证据与 15 治理输入 |
| 15 | ADR Governance | 01～14 | 未来所有重大基线变更入口 |
| 16 | Glossary & Appendix | 01～15 | 全体系导航、术语和索引 |

### 5.2 依赖类型

| Dependency Type | 含义 | 示例 |
|---|---|---|
| Normative | 下游不得违反上游规范 | 07 不得改变 04 Aggregate |
| Traceability | 下游证明上游需求 | 14 验证 02 NFR |
| Explanatory | 提供背景但不授权变化 | 16 摘要 15 ADR |
| Governance | 定义如何改变规范 | 15 管理 01～14 变更 |
| Operational | 将设计转为运行规则 | 11 承接 09 Runtime |

### 5.3 Circular Dependency Guard

后序文档可以引用前序，但不得反向改写来源。若 14 测试发现 04 不可实现，应登记问题/ADR，而不是在测试策略中重新定义 Aggregate。

---

## 6. Cross Reference Matrix

### 6.1 架构主题到文档

| Topic | Authoritative | Supporting | Governance/Test |
|---|---|---|---|
| Product Positioning | 01 | 02 | 12、13、14 |
| MVP/V1/V2 Scope | 01、02 | 06 | 14 |
| System Boundary | 03 | 01、02 | 15 |
| Bounded Context | 04 | 03、07 | 05、14、15 |
| Aggregate / Entity / VO | 04 | 05 | 07、10、14 |
| Identity / Version | 05 | 04 | 08、13、15 |
| Immutable History | 04、05 | 07、12 | 14、15 |
| Use Case / Command / Query | 07 | 02、04 | 08、14 |
| Saga / Eventual Consistency | 07 | 03、05 | 09、11、14 |
| REST / API Contract | 08 | 07 | 12、14、15 |
| Runtime / Infrastructure | 09 | 03 | 10、11、15 |
| Engineering Practice | 10 | 04、07、09 | 14 |
| Deployment / SLO / DR | 11 | 09 | 12、14、15 |
| Authentication / Authorization | 12 | 07、08 | 14、15 |
| Consent / Retention / Delete | 12 | 04、05、07 | 11、14 |
| AIAnalysis / Model Gateway | 13 | 04、07、12 | 14、15 |
| Prompt / RAG / Citation | 13 | 04、05、12 | 14 |
| Test Pyramid / Quality Gate | 14 | 02、06、10 | 15 |
| ADR Lifecycle / Decisions | 15 | 06～14 Governance | 16 |
| Glossary / Index | 16 | 01～15 | 来源文档优先 |

### 6.2 核心对象跨文档

| Concept | Domain | Data | Application | API | Security/AI/Test |
|---|---|---|---|---|---|
| Chart | 04 | 05 | 07 | 08 | 12、13、14 |
| CalculationSnapshot | 04 | 05 | 07 | 08 | 13、14 |
| RuleRun | 04 | 05 | 07 | 08 | 13、14 |
| EvidenceBundle | 04 | 05 | 07 | 08 | 13、14 |
| AIAnalysis | 04 | 05 | 07 | 08 | 12～14 |
| Report | 04 | 05 | 07 | 08 | 11～14 |
| SubjectConsent | 04 | 05 | 07 | 08 | 12、14 |
| AuditEvent | 04 | 05 | 07 | 08 | 11、12、14 |
| AnalysisProgress | 04（概念边界） | 05（非真相源） | 07（正式 Projection） | 08 | 13、14 |

### 6.3 决策交叉引用

31 项 `ADR-BL-*` 的正式摘要位于 15；来源分布在 03～14。任何替代必须创建未来 `ADR-NNNN`，不能修改本文件术语表以达到同等效果。

---

## 7. Traceability Matrix

### 7.1 产品目标到架构和测试

| Product / Requirement Theme | SRS | Architecture | Data/Application | Security/AI | Test Evidence |
|---|---|---|---|---|---|
| 普通用户最好用 | UC/FR 可用性、NFR 主旅程 | 03 移动优先 | 07 Use Case | 12 默认安全 | 14 E2E/可用性 |
| 三分钟首次排盘 | UC-002、NFR | 03 性能/旅程 | 07 首次流程 | 12 最小化 | 14 用户旅程基线 |
| 匿名试算 | User/Birth FR | 03 Identity Boundary | 05 匿名 Subject | 12 Retention | 14 E2E/Privacy |
| 确定性排盘 | FR-020～024、NFR-025 | 03 Calculation | 04 Chart、05 Snapshot | 13 AI 不计算 | 14 Golden/Boundary |
| 多观点与冲突 | Rule/Evidence FR | 03 Rule/Evidence | 04 RuleRun | 13 Conflict Validation | 14 Rule/AI Regression |
| 证据化 AI | AI/Evidence FR | 03 AI Flow | 04 EvidenceBundle/AIAnalysis | 13 Citation | 14 AI/RAG Validation |
| 当前命盘与未来三年 | AI/Timeline FR | 03 Timeline | 04/07 Scope | 13 Context Manifest | 14 E2E/Scope Test |
| 冻结历史报告 | Report FR | 03 Report | 04/05 Immutable | 12 Access | 14 Regression |
| 数据最小化 | Privacy FR/NFR | 03 Privacy | 05 Classification | 12 Privacy by Design | 14 Privacy Test |
| Consent 可撤回 | Consent FR | 03 Consent Flow | 04/05/07 SubjectConsent | 12 Purpose/Scope | 14 Lifecycle Test |
| 用户删除 | Privacy FR | 03 Delete Flow | 07 Deletion Saga | 12 Legal Hold | 14 Recovery/Delete |
| i18n/RTL 架构 | i18n NFR | 03 i18n | 07/08 Locale | 12 Content Safety | 14 Locale/E2E |
| 性能容量 | NFR-025～030 | 03/09 | 07 Async | 13 AI Budget | 14 Load/Stress |
| 风险内容控制 | Risk FR/NFR | 03 Governance | 04 RiskLevel | 12/13 Output Gate | 14 Adversarial/Human |
| AI 成本 | NFR-020 | 03/09 Cost | 07 Usage | 13 Cost Budget | 14 Cost per Valid Result |

### 7.2 领域不变量到验证

| Invariant | Source | Application Enforcement | Test |
|---|---|---|---|
| Chart 只管理确定性计算 | 04 | 07 Command/Context Boundary | 14 Aggregate/Architecture Test |
| RuleRun Completed 后不增 Finding | 04、05 | 07 Lifecycle | 14 Aggregate Test |
| EvidenceBundle Frozen 后不增 Evidence | 04、05 | 07 Evidence Flow | 14 Domain/Integration |
| AIAnalysis Completed 不回 Generating | 04、05 | 07 AI Use Case | 14 Lifecycle Test |
| Frozen Report 不回 Draft/Generating | 04、05 | 07 Report Flow | 14 Domain/E2E |
| Published 定义不原地修改 | 04、05 | 07 Governance | 14 Regression |
| 跨 Context 只引用 Root Identity/Snapshot/Event | 05 | 07 Collaboration | 14 Boundary Test |
| AnalysisProgress 只读可重建 | 04、05、07 | 07 Projection | 14 Projection Test |
| ConsentRecord 只追加 | 04、05 | 07 Consent Commands | 12/14 Audit & Privacy Test |

### 7.3 ADR 追踪

追踪链为：`Requirement → ADR-BL/ADR → Baseline Section → Implementation Change → Test Evidence → Release → Metric/Incident → Review`。本文件只建立关系，不生成实现或测试资产。

---

## 8. Glossary

### 8.1 使用规则

- 英文术语作为稳定架构名称时保留英文，中文解释用于沟通；
- 同一术语不得在不同 Context 中悄然改变含义；
- 若某词在日常语言与领域语言不同，以本表和 04 为准；
- 本表摘要不得覆盖 04/05 的详细生命周期与所有权。

### 8.2 Core Domain and DDD

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| Aggregate | 聚合；需要在一个一致性边界内共同变化的一组领域对象 | 不是任意对象集合；外部通过 Root 访问 | 04 |
| Aggregate Root | 聚合根；聚合唯一外部入口和身份载体 | 跨 Context 长期关系只引用 Root Identity | 04、05 |
| Entity | 实体；由稳定 Identity 区分、具有生命周期的领域对象 | 相同属性不代表同一 Entity | 04 |
| Value Object | 值对象；由全部值定义、通常不可变、可按值比较 | 不拥有独立生命周期或 Identity | 04 |
| Domain Event | 领域事件；某 Aggregate 中已经发生且对领域有意义的事实 | 不是 Command；跨 Context 时转换为 Integration Event | 04、07 |
| Domain Service | 领域服务；无法自然归属单一 Entity/VO、但属于领域的无状态业务行为 | 不承担跨 Context 编排或基础设施实现 | 04 |
| Repository | 聚合集合访问抽象 | 以 Aggregate Root 为边界；不是全库查询工具 | 04、09、10 |
| Factory | 创建复杂领域对象并确保初始不变量的领域构造角色 | 不承担持久化或用例协调 | 04 |
| Bounded Context | 限界上下文；统一语言、模型、数据所有权与一致性的边界 | 本文简称 Context 时通常指此概念 | 04 |
| Context | 上下文；除非明确为 Request/AI Context，默认指 Bounded Context | 不等同模块目录或部署单元 | 03、04 |
| Ubiquitous Language | 统一语言；业务、产品、架构、研发和测试共同使用的精确定义 | 变更核心术语需领域评审 | 04、16 |
| Invariant | 不变量；聚合或领域在允许状态下必须始终满足的规则 | 不因应用方便、重试或缓存而放宽 | 04、14 |
| Identity | 稳定身份；全局或规定范围内唯一、不可重用 | 不包含地区、时间、版本或业务含义 | 05 |
| Snapshot | 快照；某一时点/版本不可变的业务事实集合 | 可跨 Context 发布但不授予内部 Entity 修改权 | 04、05 |
| Projection | 投影；从权威事实构建的可重建只读视图 | 可延迟，不是 Source of Truth | 05、07 |
| Source of Truth | 权威真相源；对某类正式状态拥有最终解释权的对象/存储 | Cache、RAG Index、Read Model 不是业务真相源 | 05、09、13 |

### 8.3 Core Business Objects

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| User | 注册账户主体的身份实体 | 不等同命例 Subject；匿名用户可无 User | 04、05 |
| Subject | 数据所描述的人或授权决定主体 | Actor 不必等于 Subject | 12 |
| Actor | 发起访问或行为的人/系统身份 | 授权需结合 Subject、Purpose、Resource | 07、12 |
| BirthProfile | 出生资料容器 Aggregate Root | 创建容器不代表 BirthInput 已确认 | 04 |
| BirthInput | 用户确认的不可变出生输入 | `BirthInputConfirmed` 才正式触发时间标准化/排盘 | 04、05 |
| Chart | 围绕已确认 BirthInput 的确定性命盘 Aggregate Root | 不管理 RuleRun、Evidence、AIAnalysis、Report 状态 | 04 |
| CalculationSnapshot | Chart 内已验证的不可变计算事实快照 | 下游按 Snapshot 契约只读引用 | 04、05 |
| AlgorithmVersion | 可识别、可发布、可复现的排盘算法定义版本 | 与 SnapshotId、ChartId 不同 | 04、05 |
| RuleSet | 规则集合 Aggregate Root | 新正式运行只使用批准/发布版本 | 04 |
| RuleRun | 某 RuleSetVersion 对某 CalculationSnapshot 的单次执行 Aggregate Root | 管理 RuleFinding、冲突和完整性 | 04、05 |
| RuleFinding | RuleRun 内部实体；表达规则适用、结论、冲突或信息不足 | 不被其他 Context 直接装载或修改 | 04 |
| EvidenceBundle | 同一分析范围的一组证据 Aggregate Root | 锁定上游版本；Frozen 后供 AI/Report 引用 | 04、05 |
| Evidence | EvidenceBundle 内部实体；说明 Finding/Claim 的依据 | AI 不创建 Evidence | 04 |
| Knowledge | 经来源、权利、版本、语言、流派和发布治理的知识内容体系 | 不等同模型记忆或检索结果 | 04、13 |
| KnowledgeArticle | Knowledge Aggregate Root | Published/Rights 有效版本才进入正式检索 | 04、05 |
| Timeline | 时间轴 Aggregate Root | 基础时间轴不依赖 Evidence；分析时间轴可附加 Finding/Evidence 引用 | 04 |
| TimelineNode | 时间轴中的稳定节点身份概念 | Evidence 可引用节点身份，不形成循环依赖 | 04 |
| Report | 正式报告 Aggregate Root | Frozen 后不可原地修改；再生成创建新 Report | 04、05 |
| SubjectConsent | Consent Context 唯一同意 Aggregate Root | 管理 Purpose/Scope 当前决策视图和追加历史 | 04、12 |
| ConsentRecord | SubjectConsent 内部追加式决定记录 | Granted/Declined/Revoked 等变化不覆盖历史 | 04、05 |
| AuditEvent | 追加式、不可原地修改的审计事实 | 最小正文、独立权限、防篡改 | 04、05、12 |
| AnalysisProgress | 汇总跨 Context 公开状态的只读查询投影 | 不是 Entity、Aggregate、Saga 或流程触发器 | 04、07 |

### 8.4 Application and Integration

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| Use Case | 由 Actor 目标、前置、授权、事务、结果和失败定义的应用行为 | 不等同单一 Endpoint | 07 |
| Command | 请求系统执行一次业务意图 | 由目标 Context 处理；不返回拼装查询视图 | 07 |
| Query | 读取授权范围内数据或 Projection 的请求 | 不触发 Command 或副作用 | 07 |
| Application Service | 单一 Context 的用例入口与协调角色 | 不实现领域规则或拥有跨 Context 状态 | 07 |
| Command Handler | 校验上下文、加载 Root、调用领域行为并提交的角色 | 不直接修改第二个 Aggregate | 07 |
| Process Manager | 基于事件协调跨 Context 长流程的应用组件 | 不是 Domain Aggregate | 07 |
| Saga | 多步骤、可恢复、可能补偿的跨 Context 流程模式 | 每步保持本地事务与最终一致 | 07 |
| Operation | 长耗时异步业务请求的持久化处理身份和状态概念 | 支持受理、轮询、失败、重试；不是临时线程状态 | 07、08 |
| Idempotency | 同一业务意图重复提交只产生一个正式效果 | 同 Key 不同意图必须冲突，不静默覆盖 | 07、08 |
| Outbox | 保证已提交业务事实对应待发布事件不丢失的逻辑职责 | 不宣称 Exactly Once | 07、09 |
| Inbox | 记录消费者已处理事件身份与结果的逻辑职责 | 支持去重、重放和恢复 | 07、09 |
| Integration Event | Context 对外发布的稳定事件契约 | 与内部 Domain Event 分离、独立版本 | 07、08 |
| Eventual Consistency | 跨 Context 状态在事件处理后最终收敛 | 延迟必须可见，不用全局事务消除 | 07 |
| Transaction Boundary | 一次原子提交所覆盖的一致性范围 | 默认单 Aggregate/单 Context，不跨 Context | 07 |
| CorrelationId | 关联同一业务流程多个请求/事件的追踪身份 | 不作为 Domain Identity、Version 或授权依据 | 07、08 |
| CausationId | 指向直接触发当前事件/操作的身份 | 用于因果链，不等于 CorrelationId | 07 |

### 8.5 API and Versioning

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| Resource | API 中具有稳定 Identity、状态与允许操作的业务表示 | 不泄漏内部 Aggregate 结构 | 08 |
| Command API | 对外表达业务意图的 API | 不等同任意 RPC 方法集合 | 08 |
| Query API | 读取 Resource 或 Projection 的 API | 服务端执行权限与字段遮蔽 | 08 |
| Problem Details | 统一 API 错误语义 | 包含安全消息、稳定错误码和关联信息，不暴露内部细节 | 08 |
| API Version | 外部 API Contract 的兼容版本 | 不等于 Domain、Resource、Event 或内容版本 | 08 |
| Breaking Change | 会使现有合法消费者无法继续按原语义工作的变化 | 需要新版本、迁移和 Sunset | 08 |
| Pagination | 有界、稳定地遍历资源集合的契约 | 权限过滤先于分页；避免重复/遗漏 | 08 |
| Rate Limit | 按身份、资源、操作、风险或成本限制请求的控制 | 超限提供稳定错误和 Retry-After 语义 | 08、12 |
| RequestId | 单次请求的技术关联身份 | 可由平台校验/生成，不参与业务授权 | 08 |
| TraceId | 分布式追踪身份 | 不包含业务含义或敏感数据 | 09、11 |

### 8.6 AI, Prompt and RAG

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| AIAnalysis | 一次独立 AI 结构化分析任务及正式结果的 Aggregate Root | 不同于 Conversation；不计算事实、不创建 Evidence | 04、13 |
| AIConversation | 围绕授权 Chart 的受限对话 Aggregate Root | MVP 受当前命盘、未来三年和支持主题限制 | 04、13 |
| AIMessage | AIConversation 内部消息实体 | 不作为命盘事实或正式 Evidence | 04 |
| AnalysisPlan | AIAnalysis 的主题、范围、语言、输出和风险计划 | 后续步骤不得静默扩大 | 04、13 |
| Model Gateway | 所有正式模型/Embedding/Reranker 调用的唯一平台入口 | 集中去标识、路由、计量、可靠性和审计 | 13 |
| Provider Adapter | 隔离供应商 SDK、Payload、错误与能力差异的适配器 | 核心不直接依赖 Provider | 13 |
| Model Registry | 管理可用模型能力、版本、区域、隐私、成本和状态的注册表 | 物理实现仍为 Candidate | 13 |
| ModelReference | 一个 AIAnalysis 锁定的模型身份/版本引用 | Fallback 不改写原 ModelReference | 04、13 |
| Prompt Registry | 受控管理 Prompt 定义、评审、发布和回滚的逻辑注册表 | 不等同 Prompt 内容或代码常量 | 13 |
| PromptVersion | 不可变 Prompt 版本身份及兼容信息 | Published 后不原地修改 | 13 |
| Prompt Pipeline | 从计划、上下文组装、模板选择到调用前检查的受控流程 | 本文档体系不包含具体 Prompt 内容 | 13 |
| RAG | Retrieval-Augmented Generation；先检索受控知识再辅助生成 | 不是事实或 Evidence 的 Source of Truth | 13 |
| Embedding | 将允许内容表示为用于相似检索的向量 | 模型、Chunk 与 Index 均需版本化；不等于语义真相 | 13 |
| Chunk | 从 KnowledgeVersion 切分的稳定检索片段 | 保留来源、限定、权利、语言和流派元数据 | 13 |
| Retrieval | 从受控知识候选中按 Filter、Lexical、Vector 等取回内容 | 无结果时允许明确不足 | 13 |
| Reranker | 对候选检索结果重新排序的规则或模型能力 | 若使用模型，同样经过 Gateway、Registry 和 Evaluation | 13 |
| Citation | Claim 对具体来源版本/片段的可追踪引用 | 存在不等于支持，必须做 Claim-to-Citation Validation | 13 |
| Validation | 对结构、事实、引用、冲突、风险、泄漏和长度的正式检查 | 模型 Raw Output 未通过前不属于正式结果 | 13 |
| Hallucination | 模型生成缺少授权事实/证据支持或与事实冲突的内容 | 通过 Grounding、拒绝、降级和 Validation 缓解 | 13 |
| Context Assembly | 按 Authority、Scope、隐私和 Budget 组装模型输入 | 不等于任意拼接全部历史 | 13 |
| Context Budget | 对 Context 类型、优先级和容量的上限 | 与 Token Budget、Cost Budget 相关但不相同 | 13 |
| Token Budget | 单任务输入/输出/重试的 Token 使用边界 | 成本优化不能绕过质量与安全 | 13 |
| AI Cache | 对符合资格、严格隔离、版本完整结果的受控缓存 | 不跨用户复用私人 Context，不是 Source of Truth | 13 |
| Fallback Model | 主路由失败后经批准、兼容且已评估的替代模型 | 切换创建新 AIAnalysis，不静默覆盖 | 13 |
| Model Drift | 同一或相关模型行为随时间/版本变化 | 触发评估、阻断、回滚或新版本 | 13、14 |

### 8.7 Security, Privacy and Operations

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| Authentication | 验证 Actor 身份的过程 | 具体协议仍为 ADR Candidate | 12 |
| Authorization | 判断 Actor 对 Resource 在 Purpose/Scope 下是否允许行动 | 每个所属 Context 最终重验 | 12 |
| RBAC | Role-Based Access Control；基于角色授予基础权限 | 不能单独表达所有资源、Purpose 和风险条件 | 12 |
| ABAC | Attribute-Based Access Control；基于主体、资源、环境等属性判断 | 与 RBAC 组合，默认拒绝 | 12 |
| Least Privilege | 最小权限；只授予完成当前目的所必需的能力 | 适用于人、服务和供应商 | 12 |
| Zero Trust | 零信任；不因网络位置或内部身份自动信任 | 每次访问验证 Context 与风险 | 12 |
| Privacy by Design | 从设计开始落实最小化、目的限制和用户权利 | 不依赖上线后补救 | 12 |
| Consent | 主体对明确 Purpose、Scope、Policy 的决定 | 不等同隐私政策或所有处理的唯一法律依据 | 04、12 |
| Purpose | 数据处理的明确目的 | 实质变化需新告知/授权或法律判断 | 12 |
| Scope | 授权或操作允许的数据、资源、主题和范围 | 与 Role、Purpose、Ownership 共同判断 | 07、12 |
| PII | 可识别或可关联自然人的信息 | 出生信息即使无姓名仍需高保护 | 12 |
| Data Minimization | 只收集、传输和保留完成目的所需的数据 | 日志、AI Provider、测试同样适用 | 12 |
| Legal Hold | 法律要求下暂停正常删除/处置的受控状态 | 需理由、权限、期限和 Audit | 05、12 |
| Audit | 对关键行为和决策的可追踪、防篡改记录体系 | AuditEvent 追加，不等同普通日志 | 05、12 |
| Session | 已认证交互的受控生命周期 | 失效、撤销与风险变化需传播 | 12 |
| Secret | Credential、Key 等必须保密的运行材料 | 不进入源码、Prompt、日志或测试 Fixture | 09、12 |
| Encryption at Rest | 对持久化介质和适用字段的静态加密 | 字段级范围仍待 ADR | 12 |
| Encryption in Transit | 传输过程的加密与对端验证 | 内部流量也不默认可信 | 12 |
| SLI | Service Level Indicator；服务表现的可测指标 | 指标定义需稳定且可审计 | 11 |
| SLO | Service Level Objective；对 SLI 的正式内部目标 | 现有性能测试基线不自动等于正式 SLO | 11、14 |
| RPO | Recovery Point Objective；允许的数据恢复点损失目标 | 具体数值待正式 ADR/批准 | 11 |
| RTO | Recovery Time Objective；恢复能力的目标时间 | 具体数值待正式 ADR/批准 | 11 |
| Circuit Breaker | 依赖故障达到条件后暂停新调用并受控探测恢复 | 不能替代 Timeout、Retry 或降级 | 09、13 |
| Degradation | 在依赖故障或容量压力下保留安全、较低能力的服务 | AI 不可用时保留确定性排盘 | 03、11、13 |

### 8.8 Version and Governance

| Term | 中文/定义 | 边界与注意事项 | Primary Source |
|---|---|---|---|
| Version | 内容或契约演进的明确标识 | Identity ≠ Version | 05 |
| Version Manifest | 正式结果锁定的全部语义相关 Identity/Version 清单 | 包括 Snapshot、Rule、Evidence、Knowledge、Prompt、Model、Validation 等 | 05、13 |
| Document Version | 文档内容治理版本 | 不等于产品版本或 API Version | 15、16 |
| Product Version | MVP、V1、V2 等能力范围 | 不等同 SemVer 或发布制品版本 | 01、02、06 |
| ADR | Architecture Decision Record；重大架构决定的上下文、选项、结论和后果 | 不替代实现、法律或预算批准 | 15 |
| ADR Candidate | 尚需决策的架构事项 | 不代表推荐或批准 | 15 |
| Baseline | 已批准、后续设计必须继承的正式文档/规则集合 | 重大变化先 ADR 再修订 | 06、15 |
| Baseline-Inherited Decision | 从 Approved 文档归纳的既有决定摘要 | `ADR-BL-*` 不伪造历史独立 ADR | 15 |
| Review Trigger | 促使 ADR/架构重新评审的事实或事件 | 不是自动失效日期 | 15 |
| Quality Gate | 基于证据决定能否进入下一阶段/发布的门禁 | 关键门禁不因日程静默跳过 | 06、14 |

---

## 9. Acronyms

| Acronym | Full Form | 中文说明 |
|---|---|---|
| ABAC | Attribute-Based Access Control | 基于属性的访问控制 |
| ADR | Architecture Decision Record | 架构决策记录 |
| AI | Artificial Intelligence | 人工智能 |
| API | Application Programming Interface | 应用编程接口/系统契约边界 |
| BCP | Business Continuity Plan | 业务连续性计划 |
| CD | Continuous Delivery / Deployment | 持续交付/部署；本文件不定义实现 |
| CI | Continuous Integration | 持续集成；本文件不定义实现 |
| CSRF | Cross-Site Request Forgery | 跨站请求伪造 |
| DDD | Domain-Driven Design | 领域驱动设计 |
| DLQ | Dead Letter Queue | 不可正常处理消息的受控队列概念 |
| DR | Disaster Recovery | 灾难恢复 |
| DTO | Data Transfer Object | 数据传输对象；不属于 Domain Model |
| E2E | End-to-End | 端到端 |
| FR | Functional Requirement | 功能需求 |
| GA | General Availability | 正式发布 |
| HTTP | Hypertext Transfer Protocol | 超文本传输协议 |
| IDOR | Insecure Direct Object Reference | 不安全的直接对象引用/对象级越权 |
| i18n | Internationalization | 国际化架构 |
| JWT | JSON Web Token | Token 候选形式；是否采用尚未决定 |
| KMS | Key Management Service/System | 密钥管理能力 |
| MFA | Multi-Factor Authentication | 多因素认证 |
| MVP | Minimum Viable Product | 最小可行产品 |
| NFR | Non-Functional Requirement | 非功能需求 |
| OIDC | OpenID Connect | 身份协议候选；尚未选型 |
| ORM | Object-Relational Mapping | 对象关系映射；仅限基础设施层原则 |
| PII | Personally Identifiable Information | 个人可识别信息 |
| P95/P99 | 95th/99th Percentile | 第 95/99 百分位 |
| PR | Pull Request | 变更评审单元 |
| RAG | Retrieval-Augmented Generation | 检索增强生成 |
| RBAC | Role-Based Access Control | 基于角色的访问控制 |
| RC | Release Candidate | 发布候选版本 |
| RPO | Recovery Point Objective | 恢复点目标 |
| RTO | Recovery Time Objective | 恢复时间目标 |
| RTL | Right-to-Left | 从右向左书写/布局 |
| SDK | Software Development Kit | 软件开发工具包 |
| SLI | Service Level Indicator | 服务等级指标 |
| SLO | Service Level Objective | 服务等级目标 |
| SRS | Software Requirements Specification | 软件需求规格说明书 |
| SSRF | Server-Side Request Forgery | 服务端请求伪造 |
| TLS | Transport Layer Security | 传输层安全 |
| UC | Use Case / User Story identifier | 用例/用户故事编号语境 |
| URI | Uniform Resource Identifier | 统一资源标识符 |
| VO | Value Object | 值对象 |
| WAF | Web Application Firewall | Web 应用防护能力 |
| XSS | Cross-Site Scripting | 跨站脚本 |

### 9.1 Acronym Rule

首次出现不常见缩写时写全称；不得为内部方便创造与现有领域术语冲突的新缩写。`AIAnalysis`、`RuleRun` 等是正式领域名称，不缩写为含义不明的 AA/RR。

---

## 10. Naming Convention

### 10.1 Document Files

正式架构文档采用 `NN-UPPER-KEBAB-NAME.md`，编号两位、名称稳定。文件重命名属于文档治理变更，需更新全部引用。

### 10.2 Requirement IDs

| Prefix | Meaning |
|---|---|
| FR | 功能需求 |
| NFR | 非功能需求 |
| BR | 业务规则 |
| UC | 用户故事/用例 |
| BF | 业务流程 |
| EF | 异常流程 |
| EC | 边界情况 |

编号稳定且不可重用；废弃项保留历史和替代关系。

### 10.3 Domain Names

- Entity/Aggregate/Value Object 使用单数 PascalCase 英文正式名称，如 `Chart`、`EvidenceBundle`；
- Aggregate Root 与 Aggregate 名称一致时明确写 `Chart Aggregate`；
- 内部 Entity 不以外部 Context 名称伪装为 Root；
- 领域事件使用已发生事实的过去式语义，如 `ChartCalculated`；
- Domain Service 使用清晰领域行为名称，如 `EvidenceBuilder`。

### 10.4 Command and Query Names

- Command 使用动词开头的业务意图，如 Grant、Revoke、Calculate、Freeze；
- Query 使用 Get/List/Search 等读取语义；
- Query 不使用暗示副作用的名称；
- Process Manager 名称表达流程，如 User Deletion，而非通用 Manager。

### 10.5 Identity Names

Identity 使用 `{Object}Id`，不编码地区、时间、版本或业务含义。`SnapshotId` 不等于 `SnapshotSequence`，`ReportId` 不等于 `ReportOrdinal`。

### 10.6 Version Names

内容版本使用明确对象名，如 `RuleSetVersion`、`PromptVersion`；API、Event、Document、Algorithm、Knowledge、Model 和 Validation Version 不使用一个通用 `version` 字段混淆语义。

### 10.7 Event and Correlation Names

`EventId`、`CorrelationId`、`CausationId`、`RequestId`、`TraceId`、`IdempotencyKey` 分别表达事件身份、流程关联、直接因果、请求、追踪和业务去重，不可互换。

### 10.8 Status Names

状态使用已批准生命周期术语并保持 Context 所有权。不得用全局 `Completed` 代替 Chart、RuleRun、EvidenceBundle、AIAnalysis 和 Report 各自状态。

### 10.9 Security and Privacy Names

授权语义显式包含 Actor、Subject、Resource、Action、Purpose、Scope 和 Decision；避免使用含义不清的 `isAdmin` 或 `hasAccess` 作为完整模型名称。

### 10.10 AI Names

区分 Provider、Model、Prompt、Analysis、Conversation、Message、Evidence、Knowledge 和 Citation。禁止把模型 Raw Output 命名为正式 `AIAnalysisResult` 后绕过 Validation。

### 10.11 User-Facing Language

面向普通用户优先通俗中文；专业术语可展开。有效性使用“证据充分、一般、有限、存在冲突”等克制等级，不使用伪精确预测概率或绝对化未来断言。

---

## 11. Versioning Convention

### 11.1 Identity ≠ Version

Identity 表示“是哪一个对象”，Version 表示“内容如何演进”。二者不能编码、推断或互相替代。

### 11.2 Document Version

| Version | Meaning |
|---|---|
| 0.x | Draft/Review 工作版本，不属于正式基线 |
| 1.0 | 首次 Approved Baseline |
| 1.x | 向后兼容的澄清或治理增强；是否允许需文档治理确认 |
| 2.0+ | 重大语义或结构变化，必须由 ADR/正式变更授权 |

Approved 文档不得原地改变内容而保持同一版本。状态变化、版本变化与 Change Log 必须一致。

### 11.3 Domain and Data Versions

- Entity Identity 永久稳定；
- Snapshot/Report 等具有独立 Identity 与 Sequence/Ordinal；
- Published/Frozen/Completed 对象不原地修改；
- 新语义产生新 Version 或新对象，历史继续可引用。

### 11.4 API and Event Versions

API Version 与 Event Contract Version 独立；同一主版本不改变既有字段/错误/时间/Identity 语义。Breaking Change 需要新版本、迁移和 Sunset。

### 11.5 AI Versions

Prompt、Model、Embedding、Chunk、Index、Retrieval、Validation、Risk Policy 分开版本化。正式结果使用 Version Manifest，不用“当前版本”推断历史。

### 11.6 ADR Versions

正式 ADR Identity 永久；Accepted 结论不原地改写。实质变化创建新 ADR 并 Supersede。`ADR-BL-*` 是基线继承摘要，不占正式 `ADR-NNNN`。

### 11.7 Product Versions

MVP、V1、V2 表示产品能力范围，不等同文档版本、发布制品版本或 API 版本。

---

## 12. Document Ownership

### 12.1 Ownership Matrix

| No. | Document | Accountable Owner Role | Required Co-Owners / Reviewers |
|---:|---|---|---|
| 01 | Product Vision | Product Owner | CTO、Expert、Design、Legal |
| 02 | SRS | Product / Requirements Owner | Architecture、QA、Expert、Legal |
| 03 | System Architecture | CTO / System Architect | Domain、Data、Security、Ops |
| 04 | Domain Model | Domain Architect | Product、Expert、Data、QA |
| 05 | Data Model | Data Architect | Domain、Security、Privacy、Legal |
| 06 | Roadmap | Product / Program Owner | CTO、Release、All Gate Owners |
| 07 | Application Architecture | Application Architect | Domain、API、Security、QA |
| 08 | API Design | API Architect | Application、Security、Client、Ops |
| 09 | Technology Architecture | Technology Architect | Data、Platform、Security、Cost |
| 10 | Implementation Guide | Engineering Lead | Architects、QA、Security、Developers |
| 11 | Deployment & Operations | Operations / SRE Lead | Technology、Security、Data、Release |
| 12 | Security & Privacy | Security & Privacy Owners | Legal、Data、Product、AI、Ops |
| 13 | AI Architecture | AI Architect / AI Quality Owner | Knowledge、Security、Privacy、Expert、Cost |
| 14 | Testing Strategy | Test / Quality Architect | All Context Owners、Security、Release |
| 15 | ADR Governance | CTO / Architecture Council | Baseline Custodians、Gate Owners |
| 16 | Glossary & Appendix | Documentation Governance Owner | All Document Owners |

### 12.2 Owner Responsibilities

Owner 负责准确性、版本、评审、引用、待确认项、Change Log 和 Review Trigger。Owner 角色不是唯一编辑者，也不能单独越过必需法律、专家、安全或架构审批。

### 12.3 Ownership Transfer

角色变化时显式移交未决问题、风险、候选 ADR、评审证据和下一触发点。个人离开不使文档失去 Owner。

### 12.4 Custodianship

Documentation Governance Owner 维护索引与格式；各主题 Owner 维护语义。治理 Owner 不得通过术语表修改领域事实。

---

## 13. Review Process

### 13.1 标准流程

1. Owner 提交 Review 版本和 Change Summary；
2. 确认上游基线与影响矩阵；
3. 指定产品、架构、专家、安全、隐私、法律、AI、测试或运维 Reviewer；
4. 记录评论、决议和未决项；
5. 执行跨文档一致性与术语检查；
6. 必需 Gate Owner 给出批准、拒绝或附条件批准；
7. 状态与版本更新为 Approved 1.0 或后续版本；
8. 更新 Change Log、Review History、Dependency 和 Index；
9. 受影响的下游文档显式确认继承。

### 13.2 Review Types

| Review | Focus |
|---|---|
| Product Review | 用户、范围、价值、成功指标 |
| Expert Review | 命理规则、术语、争议、黄金命例 |
| Architecture Review | 边界、依赖、一致性、可演进性 |
| Data Review | Identity、Version、Delete、Audit、Migration |
| Security/Privacy/Legal Review | 威胁、权限、Purpose、区域、保留、权利 |
| AI Review | Provider、Prompt、RAG、Validation、Cost、Risk |
| Test Review | 可验收、覆盖、门禁、证据 |
| Operations Review | 可部署、可观察、容量、恢复、支持 |
| Documentation Review | 术语、引用、状态、版本、索引一致性 |

### 13.3 Approval Evidence

记录文档、版本、Outcome、Reviewer Role、条件和日期。当前基线未统一提供个人姓名与评审日期时，不在本文件虚构；见 Appendix Review History。

### 13.4 Change after Approval

非实质格式修订可走文档治理流程；重大语义变化先走 15 的 ADR。任何变更不得保持相同版本并静默覆盖。

### 13.5 Documentation Note Process

元数据、标题、引用或索引不一致可登记 `DOC-NOTE-NNN`。Note 不改变架构；若影响规范含义，升级为 Open Question/ADR。

---

## 14. Architecture Principles Summary

| Principle | Summary | Source |
|---|---|---|
| Business First | 技术服务普通用户、自我反思和克制表达 | 01、06 |
| Domain First | 领域语义先于框架和数据表 | 03、04、10 |
| Data First | Identity、Version、Snapshot、Delete、Audit 先明确 | 05、06 |
| Modular Monolith First | MVP 不提前微服务化 | 03、09、15 |
| Context Isolation | Context 拥有自己的模型、数据和一致性 | 04、05、07 |
| Aggregate Root Access | 外部不绕过 Root 修改内部 Entity | 04、05 |
| Deterministic Before AI | 命盘事实由确定性算法生成 | 03、04、13 |
| Evidence before Explanation | RuleRun→EvidenceBundle→AI | 04、13 |
| Immutable History | Frozen/Published/Completed 历史不原地改写 | 04、05 |
| Version Everything | 影响语义的版本完整记录 | 05、13、15 |
| Infrastructure as Adapter | 核心不依赖供应商/框架私有语义 | 09、10 |
| Eventual Consistency Explicit | 跨 Context 用 Event/Saga，不用全局事务 | 07、09 |
| Read Model Is Not Truth | Projection 可重建、可延迟、不回写源 | 05、07 |
| Incremental Delivery | 每阶段独立验证，范围可缩而质量不降 | 06 |
| Traceability | 需求、版本、证据、测试、发布可关联 | 02、14、15 |
| Governance by ADR | 重大变化先决定再更新基线 | 06、15 |

### 14.1 Summary Boundary

本节仅摘要。任何原则冲突、例外或演进必须回到来源文档和 ADR。

---

## 15. Architecture Constraints Summary

### 15.1 Product Constraints

- 首发中国大陆简体中文用户；18 岁以上；
- 定位为传统文化分析与自我反思工具，不宣称科学预测；
- 匿名试算默认不长期保存；MVP 不接真实支付；
- 普通用户最好用优先于功能最多；
- MVP 当前命盘、未来三年和已支持主题；
- 正式 PDF、分享、完整时间轴、多流派完整对比后移。

### 15.2 Domain Constraints

- Chart 只负责确定性计算；
- RuleRun、EvidenceBundle、AIAnalysis、Report 分属自治 Context；
- AnalysisProgress 只读；
- Frozen/Completed/Published 对象不可回到可编辑状态；
- 争议命理规则保留不同观点；待专家确认项不得擅自固化。

### 15.3 Data Constraints

- Identity 无业务含义且不可重用；
- Identity 与 Version 分离；
- 跨 Context 只使用 Root Identity、Snapshot、Event 或 Root 发布引用；
- 历史报告保存完整版本快照；
- 删除、匿名化、归档、Legal Hold 和 Audit 分开治理。

### 15.4 Technology Constraints

- 第一阶段模块化单体；
- PostgreSQL 为主要事务真相源，Redis 不是 Source of Truth；
- PostgreSQL 向量扩展优先，独立 Search 需证据与 ADR；
- 基础设施不泄漏入 Domain；
- AI 与 Report 采用受控异步操作；
- 具体 Provider、Vendor、Orchestration、正式跨区域仍未决定。

### 15.5 Governance Constraints

- Approved Baseline 不通过聊天、实现或 Roadmap 静默改变；
- 重大变化必须 ADR；
- Beta/RC/GA Scope Freeze 生效；
- 未批准候选不得成为默认实现；
- 当前仍未授权进入编码阶段。

---

## 16. Security Principles Summary

| Principle | Meaning | Source |
|---|---|---|
| Zero Trust | 不因内部网络、登录或管理员自动信任 | 12 |
| Least Privilege | 人与服务只获当前目的所需权限 | 12 |
| Defense in Depth | Edge、API、Application、Data、AI 多层控制 | 12 |
| Secure by Default | 新能力默认拒绝，显式批准后开放 | 12 |
| Privacy by Design | 从架构开始控制数据全生命周期 | 12 |
| Data Minimization | 不默认收集姓名、详细地址或无关数据 | 01、12 |
| Purpose Limitation | 按明确 Purpose/Scope 处理与 Consent | 12 |
| Encryption | 传输与静态加密；字段级范围待 ADR | 12、15 |
| Secret Hygiene | Secret 不入源码、Prompt、日志、测试数据 | 09、12、14 |
| Sensitive Masking | 日志、API、后台和 AI 输出按权限脱敏 | 08、12 |
| Auditability | 关键行为追加、防篡改、最小正文 | 05、12 |
| User Rights | 导出、撤回、删除、Legal Hold 可验证 | 07、12 |
| AI Security | Injection、Leakage、Jailbreak、输出风险受控 | 12、13 |
| Incident Readiness | 分级、监控、响应、恢复和复盘 | 11、12 |

### 16.1 Undecided Security Choices

Authentication Protocol、JWT/Opaque、字段级加密、具体 IAM/WAF/Key Vendor 等仍是 Candidate，不在本文件选择。

---

## 17. AI Principles Summary

| Principle | Meaning | Source |
|---|---|---|
| Deterministic Facts First | AI 不计算或补造 Chart 事实 | 13 |
| Evidence Grounded | 重要解释基于 Frozen Evidence/批准知识 | 13 |
| Scope Bound | 当前 Chart、未来三年、批准主题 | 01、13 |
| Gateway Only | 正式 Provider 调用只经 Model Gateway | 13、15 |
| Provider Abstraction | 核心不依赖供应商 SDK/Payload | 13 |
| Version Everything | Model、Prompt、Knowledge、Validation 等完整锁定 | 13 |
| Raw Output Untrusted | 正式结果前完成多层 Validation | 13 |
| Claim-to-Citation | 引用必须存在、合法且支持 Claim | 13、14 |
| RAG Not Truth | Retrieval 是候选知识获取，不定义事实 | 13 |
| Privacy Minimized | Provider 只收去标识最小 Context | 12、13 |
| No Cross-User Cache | 私人 Context/输出不跨用户复用 | 13、15 |
| No Silent Fallback | 换 Model 创建新 AIAnalysis | 13、15 |
| Controlled Cost | Token、Retry、Fallback、Validated Result 有预算 | 13 |
| Reliability & Degradation | Timeout、Retry、Circuit、Fallback、确定性降级 | 13 |
| Evaluation & Human Review | Golden、Adversarial、Drift 和人工校准 | 13、14 |
| No Scientific Overclaim | AI 一致/用户认同不等于预测准确 | 01、13、14 |

### 17.1 Undecided AI Choices

具体 Provider、Primary Model、Embedding、Reranker、Active Routing、Model-as-Judge、Tool Calling 和 Prompt Registry 物理存储保持 Candidate。

---

## 18. Testing Principles Summary

| Principle | Meaning | Source |
|---|---|---|
| Risk Based | 深度按影响、概率、检测和恢复风险 | 14 |
| Shift Left | 设计阶段确认不变量、契约和安全 | 14 |
| Deterministic Core | 控制 Clock、Identity、Version、外部依赖 | 14 |
| Test Pyramid | Domain/Unit 多，Contract/Integration 中，E2E 少而关键 | 14 |
| Real Boundary Verification | Mock 不证明真实兼容 | 10、14 |
| Negative Paths | 失败、撤回、越权、重试、删除同等重要 | 14 |
| AI as Untrusted | Raw Output 需评估和平台 Validation | 14 |
| Version Reproducibility | Test Dataset/Environment/Manifest 锁定 | 14 |
| Coverage as Signal | 不用单一百分比替代风险分析 | 10、14 |
| Flaky Is a Defect | 不以重跑到绿掩盖失败 | 10、14 |
| Production Is Not Test | 生产受控验证不替代测试环境 | 14 |
| Quality Gate over Calendar | 范围可缩，关键门禁不降 | 06、14 |
| No Accuracy Claim | 黄金/AI 测试不证明命理科学有效 | 14 |

### 18.1 Approved Performance Test Baseline

确定性排盘 P95 ≤ 2 秒/P99 ≤ 5 秒；常规已认证 API P95 ≤ 500 毫秒/P99 ≤ 1.5 秒；AI 首次有效响应 P95 目标 ≤ 15 秒；完整 AI 报告 P95 初始目标 ≤ 60 秒；100 并发交互、20 并发 AI、持续 10 请求/秒至少 30 分钟。它们是测试基线，不自动等于正式 SLO。

---

## 19. ADR Summary

### 19.1 Governance

- 正式未来 ADR 使用 `ADR-NNNN`；
- `ADR-BL-*` 是 Baseline-Inherited 摘要，不伪造历史独立 ADR；
- Candidate 不代表推荐；
- Accepted ADR 不原地修改，变化通过 Superseding ADR；
- ADR 包含 Context、Options、Consequences、Risk、Migration、Rollback、Testing 和 Review Trigger；
- ADR Accepted 后仍需显式更新受影响 Baseline。

### 19.2 Approved Decision Families

| Family | ADR-BL Range / Themes |
|---|---|
| Architecture Style | Modular Monolith、DDD、Context Isolation |
| Domain/Data | Root Reference、Deterministic、Rule/Evidence、Version、PostgreSQL/Redis |
| Application/API | Async、Outbox/Inbox、Idempotency、Version/Problem Details |
| Security/Privacy | Zero Trust、Privacy、Consent、Audit、Deletion Saga |
| AI | Gateway、Abstraction、Prompt、RAG、Citation、Cache、Fallback |
| Quality/Governance | Test Pyramid、Release Gates、No Silent Changes |

### 19.3 Candidate Families

Authentication/Token/Encryption；Provider/Model/Embedding/Reranker/Prompt Storage；Search/Active Routing/Model-as-Judge/Tool；Runtime Platform；正式 SLO/RPO/RTO；Test Framework；Observability/Object Storage Vendor；Cross-Region。

### 19.4 Change Rule

本文件不复制 31 项完整内容；正式 Decision、Rationale、Alternatives、Consequences、Owner 和 Trigger 以 15 为准。

---

## 20. Risks Summary

### 20.1 Top Risk Register

| Risk Area | Primary Risk | Guardrail | Owner Documents |
|---|---|---|---|
| Product | 误导性科学/未来承诺 | 克制定位、风险文案、Legal Review | 01、02、12 |
| Domain | Chart/Rule/Evidence/AI 混合 | Context/Aggregate Boundary | 04、07 |
| Algorithm | 历法或争议规则错误 | 版本、黄金/边界命例、专家 Gate | 02、04、14 |
| Data | 历史被覆盖、Identity/Version 混用 | Immutable/Snapshot/Manifest | 05 |
| Integration | 重复、乱序、跨事务 | Outbox/Inbox、Idempotency、Saga | 07、09 |
| API | Breaking 或错误泄漏 | Version、Compatibility、Problem Details | 08 |
| Technology | 单体变泥球、共享数据库 | Module/Data Ownership、ADR | 09、10 |
| Operations | 无恢复、错误 SLO、供应商故障 | Backup/Restore、Runbook、Degradation | 11 |
| Security | 越权、Secret、注入 | Zero Trust、Least Privilege、Testing | 12、14 |
| Privacy | 过度收集、撤回/删除失效 | Purpose、Consent、Deletion Saga | 12 |
| AI | 幻觉、引用失配、Prompt Injection | Evidence、Validation、Citation、Risk Gate | 13、14 |
| RAG | 撤权内容/相似度误当真相 | Rights Filter、Index Rebuild、Citation | 13、14 |
| Cost | Token/Retry/Provider 成本失控 | Budget、Quota、Cost per Valid Result | 13 |
| Quality | Flaky、Mock 漂移、假绿 | Pyramid、Contract、Release Gate | 14 |
| Governance | 候选泄漏、静默基线变化 | ADR、Index、Audit、Scope Freeze | 15 |

### 20.2 Risk Interpretation

本表仅为入口。严重度、触发、缓解、残余风险与 Owner 以各来源文档为准。

---

## 21. Future Improvements

所有项目均为文档治理或未来评估，不改变当前基线。

### FI-001 Metadata Reconciliation

经正式授权后，使 01～15 文件头的状态、版本和 Change Log 与当前 Approved 1.0 登记一致；不得在本轮修改。

### FI-002 Machine-Checkable Cross References

未来可建立只读文档检查，发现失效文件名、重复 ID、缺失版本、孤立 ADR 和未映射 Must 需求；工具选择属于实施阶段。

### FI-003 Requirement Trace Coverage

把 02 的每个 FR/NFR/BR/UC 映射至架构 Owner、测试和 Release Gate，形成更细粒度矩阵；不改变需求内容。

### FI-004 Domain Language Lint

建立禁用同义词和正式名称检查，防止把 AIAnalysis、Report、Evidence、Knowledge 或 Snapshot 混为一体。

### FI-005 ADR Index Separation

当正式 ADR 数量增长且用户授权创建独立文件后，把 15 的治理规则与 ADR Index/记录分离，保留历史和双向引用。

### FI-006 Review Evidence Registry

建立 Reviewer Role、日期、条件、版本和批准证据的统一登记，避免仅凭对话历史判断状态。

### FI-007 Reference Integrity

为文档章节建立稳定 Anchor/Section ID，减少标题变更导致引用失效；具体格式需治理评审。

### FI-008 Open Question Ownership

把分散在 01～15 的 Open Question 汇总到有 Owner、Due Gate 和 Resolution Document 的注册表，不在汇总中作决定。

### FI-009 Multilingual Terminology

在英文/阿拉伯语进入正式范围前建立人工复核的中英阿术语库、RTL 例句和禁止误译表。

### FI-010 Architecture Onboarding Views

为 Product、Expert、Engineering、Security、AI、QA 创建角色化只读导航，仍以 01～16 为权威来源。

---

## 22. Open Questions

### 22.1 Product and Expert

1. 具体旺衰、格局、调候、用神、喜神、忌神规则。
2. 起运顺逆与时间、子时换日、真太阳时最终口径。
3. 首批神煞、多流派冲突优先级和黄金命例。
4. 健康、婚姻、投资等高风险主题的最终边界。
5. 首次排盘完成率、三分钟完成率、理解度和引用有效率阈值。

### 22.2 Legal and Privacy

1. 正式数据保留期限、删除/匿名化与 Legal Hold 细节。
2. 目标地区上线、AI 内容标识、Provider、跨境与用户权利结论。
3. 命例用于优化的 Consent、撤回、去标识与研究保留流程。
4. 英文和阿拉伯语内容的法律与术语复核流程。

### 22.3 Architecture and Technology

1. Authentication Protocol、JWT/Opaque、字段级加密。
2. AI Provider、Primary Model、Embedding、Reranker、Prompt Registry Storage。
3. 独立 Search、Active Routing、Model-as-Judge、Tool Calling。
4. Production Orchestration、Observability/Object Storage Vendor。
5. 正式 SLO/RPO/RTO 与 Cross-Region Deployment。
6. Test Framework 与文档自动检查工具。

### 22.4 Documentation Governance

1. Architecture Council 成员、法定人数、代理和时限。
2. 文档 Review History 的统一证据、日期和 Reviewer 身份来源。
3. 现有文件头元数据的正式修订批次与批准方式。
4. 16 通过后文档体系是否冻结为 Architecture Baseline Set 1.0。
5. 编码阶段由谁、以何种明确指令授权；当前尚未授权。

---

## 23. References

### 23.1 Internal Normative References

| Ref | Document | Use |
|---|---|---|
| REF-01 | `01-PRODUCT-VISION.md` | 产品定位、用户、范围、指标 |
| REF-02 | `02-SRS.md` | 需求、流程、验收、NFR |
| REF-03 | `03-SYSTEM-ARCHITECTURE.md` | 系统结构与总体数据流 |
| REF-04 | `04-DOMAIN-MODEL.md` | 唯一正式领域模型 |
| REF-05 | `05-DATA-MODEL.md` | 正式逻辑数据模型 |
| REF-06 | `06-ROADMAP.md` | 阶段、里程碑和 Gate |
| REF-07 | `07-APPLICATION-ARCHITECTURE.md` | Application、Use Case、Saga |
| REF-08 | `08-API-DESIGN.md` | API 设计与契约原则 |
| REF-09 | `09-TECHNOLOGY-ARCHITECTURE.md` | 技术架构与基础设施 |
| REF-10 | `10-IMPLEMENTATION-GUIDE.md` | 工程实现规范 |
| REF-11 | `11-DEPLOYMENT-OPERATIONS.md` | 部署、运行、恢复与治理 |
| REF-12 | `12-SECURITY-PRIVACY.md` | 安全与隐私架构 |
| REF-13 | `13-AI-ARCHITECTURE.md` | AI、Prompt、RAG 与评估 |
| REF-14 | `14-TESTING-STRATEGY.md` | 测试体系与质量门禁 |
| REF-15 | `15-ARCHITECTURE-DECISION-RECORDS.md` | ADR 治理与决策登记 |
| REF-16 | `16-GLOSSARY-AND-APPENDIX.md` | 术语、索引与治理附录 |

### 23.2 External Reference Policy

本文档不新增外部规范引用。各主题若未来引用法律、标准或供应商材料，应记录版本、发布日期、适用地区、访问日期、授权和具体支撑范围；外部资料不能自动覆盖内部 Approved Baseline。

### 23.3 Citation Rule

文档引用优先使用文件名、章节和稳定 Requirement/Decision ID。避免只写“见上文”或依赖易变化的行号。

---

## 24. Appendix

### 24.1 全部文档索引

当前正式治理输入声明 01～15 均为 Approved 1.0；16 为本轮 Review 0.9。

| No. | File | 中文名称 | Type | Governing Status | Version | Primary Relationship |
|---:|---|---|---|---|---:|---|
| 01 | `01-PRODUCT-VISION.md` | 产品愿景 | Product Vision | Approved | 1.0 | 全体系产品根输入 |
| 02 | `02-SRS.md` | 软件需求说明书 | SRS | Approved | 1.0 | 将 01 转为可验收需求 |
| 03 | `03-SYSTEM-ARCHITECTURE.md` | 总体系统架构 | System Architecture | Approved | 1.0 | 将 01/02 转为总体结构 |
| 04 | `04-DOMAIN-MODEL.md` | 领域模型 | Domain Model | Approved | 1.0 | 唯一正式领域模型 |
| 05 | `05-DATA-MODEL.md` | 数据模型 | Data Model | Approved | 1.0 | 映射 04 至逻辑数据结构 |
| 06 | `06-ROADMAP.md` | 项目路线图 | Roadmap | Approved | 1.0 | 组织 01～05 的实施顺序 |
| 07 | `07-APPLICATION-ARCHITECTURE.md` | 应用架构 | Application Architecture | Approved | 1.0 | 落实 Use Case 与一致性 |
| 08 | `08-API-DESIGN.md` | API 设计规范 | API Design | Approved | 1.0 | 定义外部契约原则 |
| 09 | `09-TECHNOLOGY-ARCHITECTURE.md` | 技术架构 | Technology Architecture | Approved | 1.0 | 定义技术能力边界 |
| 10 | `10-IMPLEMENTATION-GUIDE.md` | 工程实现规范 | Engineering Guide | Approved | 1.0 | 定义工程组织规范 |
| 11 | `11-DEPLOYMENT-OPERATIONS.md` | 部署与运维规范 | Deployment & Operations | Approved | 1.0 | 定义运行与恢复 |
| 12 | `12-SECURITY-PRIVACY.md` | 安全与隐私架构 | Security & Privacy | Approved | 1.0 | 约束全生命周期安全隐私 |
| 13 | `13-AI-ARCHITECTURE.md` | AI 架构 | AI Architecture | Approved | 1.0 | 定义 AI/RAG/Prompt 治理 |
| 14 | `14-TESTING-STRATEGY.md` | 测试策略 | Testing Strategy | Approved | 1.0 | 定义验证与发布 Gate |
| 15 | `15-ARCHITECTURE-DECISION-RECORDS.md` | ADR 治理与登记册 | ADR Governance | Approved | 1.0 | 管理未来重大变化 |
| 16 | `16-GLOSSARY-AND-APPENDIX.md` | 统一术语与架构附录 | Documentation Governance | Review | 0.9 | 汇总索引，不修改来源 |

### 24.2 Documentation Note Register

| Note ID | Observation | Classification | Current Treatment | Future Action |
|---|---|---|---|---|
| DOC-NOTE-001 | 当前正式输入声明 01～15 均为 Approved 1.0，但部分本地文件头仍显示早期 Review/0.9 或待评审/0.1 | Documentation metadata inconsistency | 本索引按当前正式批准声明记录；不修改来源文件；不视为架构语义冲突 | 获授权后做仅元数据一致性修订并保留 Change Log |

### 24.3 Version History — Documentation Set

由于来源文档未统一记录全部审批日期和 Reviewer 身份，本表不虚构日期。

| Set Version | Scope | Status | Date | Evidence / Note |
|---|---|---|---|---|
| 0.x | 各文档逐份生成和评审 | Historical Working State | 未统一记录 | 各文件早期 Change Log/头部 |
| 1.0 | 01～15 | Approved Baseline Set | 未统一记录 | 当前正式输入明确确认全部 Approved 1.0 |
| 0.9 | 16 | Review | 本轮生成 | 等待用户评审，不属于 Approved Baseline |

### 24.4 Version History — Individual Documents

| No. | Review Version History Known from Process | Current Governing Version | Date |
|---:|---|---:|---|
| 01 | 0.x Review → Approved | 1.0 | 未统一记录 |
| 02 | Review → Approved | 1.0 | 未统一记录 |
| 03 | 0.x Review → Approved | 1.0 | 未统一记录 |
| 04 | 0.2 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 05 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 06 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 07 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 08 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 09 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 10 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 11 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 12 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 13 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 14 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 15 | 0.9 Review → 1.0 Approved | 1.0 | 未统一记录 |
| 16 | 0.9 Review | 0.9 | 本轮生成 |

### 24.5 Review History

| No. | Review Outcome | Reviewer Evidence | Approval Date | Documentation Note |
|---:|---|---|---|---|
| 01～15 | Approved 1.0 | 当前正式输入确认；具体个人/角色记录未统一附于文件 | 未统一记录 | 不虚构姓名或日期 |
| 16 | Pending Review | 等待用户正式评审 | Pending | 不得自行标记 Approved |

### 24.6 Architecture Timeline

本时间线表达依赖顺序，不表达实际日历日期。

| Sequence | Architecture Stage | Documents | Outcome |
|---:|---|---|---|
| T0 | Product Definition | 01 | 产品定位、用户与版本 |
| T1 | Requirements Baseline | 02 | 可验收需求与系统边界 |
| T2 | Overall Architecture | 03 | 模块、数据流、部署方向 |
| T3 | Domain Baseline | 04 | Context、Aggregate、Event |
| T4 | Data Baseline | 05 | Identity、Version、Delete、Audit |
| T5 | Delivery Governance | 06 | Phase、Milestone、Release Freeze |
| T6 | Application Behavior | 07 | Use Case、Command、Query、Saga |
| T7 | Contract Architecture | 08 | REST、Error、Version、Async |
| T8 | Technology Baseline | 09 | Runtime、Data Access、Infrastructure |
| T9 | Engineering Baseline | 10 | Project/DDD/Review/Test Practice |
| T10 | Operations Baseline | 11 | Deploy、Observe、Recover、Incident |
| T11 | Security & Privacy | 12 | Identity、Authorization、Data Rights |
| T12 | AI Baseline | 13 | Gateway、Prompt、RAG、Validation |
| T13 | Quality Baseline | 14 | Pyramid、Evaluation、Release Gate |
| T14 | Decision Governance | 15 | ADR Lifecycle、Register、Candidates |
| T15 | Documentation Closure | 16 | Glossary、Matrices、Index、Appendix |

### 24.7 Architecture Index by Context

| Bounded Context | Domain Definition | Key Data | Application/API | Cross-Cutting |
|---|---|---|---|---|
| Identity | 04 | User | 07、08 | 12、14 |
| Consent | 04 | SubjectConsent、ConsentRecord | 07、08 | 12、14 |
| Birth | 04 | BirthProfile、BirthInput | 07、08 | 12、14 |
| Calendar & Time | 04 | Time/Boundary VO | 07 | 03、14 |
| Chart Calculation | 04 | Chart、Snapshot、Algorithm | 07、08 | 03、14 |
| Rule Evaluation | 04 | RuleSet、RuleRun、Finding | 07、08 | 13、14 |
| Evidence | 04 | EvidenceBundle、Evidence | 07、08 | 13、14 |
| Knowledge | 04 | KnowledgeArticle | 07、08 | 09、13、14 |
| AI | 04 | AIAnalysis、Conversation、Message | 07、08 | 12～14 |
| Report | 04 | Report | 07、08 | 11、14 |
| Timeline | 04 | Timeline | 07、08 | 13、14 |
| Governance | 04 | Rule/Knowledge/Version governance | 07 | 12～15 |
| Audit | 04 | AuditEvent | 07、08 | 11、12、14 |

### 24.8 Architecture Index by Lifecycle

| Lifecycle | Primary Source | Related Control |
|---|---|---|
| BirthProfile / BirthInput | 04、05 | Consent、Deletion |
| Chart / CalculationSnapshot | 04、05 | AlgorithmVersion、Verification |
| RuleSet / RuleRun | 04、05 | Publish、Regression |
| EvidenceBundle | 04、05 | Frozen、Citation |
| KnowledgeArticle | 04、05 | Rights、Publish、Index |
| AIAnalysis | 04、13 | Model/Prompt/Validation |
| AIConversation | 04、13 | Scope、Retention、Consent |
| Report | 04、05 | Frozen、Regenerated、Archived |
| SubjectConsent | 04、05、12 | Append-only decisions |
| User Deletion | 07、12 | Saga、Legal Hold、Tombstone |
| ADR | 15 | Candidate→Active→Superseded |

### 24.9 Reference Matrix — Requirement IDs

| ID Family | Defined In | Primary Consumers |
|---|---|---|
| UC | 02 | 06、07、14 |
| FR | 02 | 03～14 |
| NFR | 02 | 03、09、11～14 |
| BR | 02 | 04、07、14 |
| BF | 02 | 07、14 |
| EF | 02 | 07、11、14 |
| EC | 02 | 04、14 |
| ADR-BL | 15 | 未来设计与评审 |
| ADR-CANDIDATE | 15 | 未来 ADR Triage |
| DOC-NOTE | 16 | 文档治理 |
| FI | 16 | Future Improvement backlog |

### 24.10 Reference Matrix — Version Types

| Version Type | Owner | Must Not Be Confused With |
|---|---|---|
| Document Version | Document Owner | Product/API Version |
| Product Version | Product Owner | Release Artifact Version |
| API Version | API Owner | Domain/Event Version |
| Event Contract Version | Producer/Consumer Owners | Domain Event identity |
| AlgorithmVersion | Calculation Owner | SnapshotId |
| RuleSetVersion | Rule Owner | RuleSetId/RuleRunId |
| KnowledgeVersion | Knowledge Owner | ArticleId/IndexVersion |
| PromptVersion | Prompt Governance | Code/Model Version |
| ModelReference | AI Governance | Provider display name alone |
| ValidationVersion | AI/Security Quality | PromptVersion |
| IndexVersion | Knowledge/Search Owner | EmbeddingModel alone |
| Version Manifest | Result Aggregate | 单一通用 Version |

### 24.11 MVP / V1 / Future Quick Index

| Horizon | Included Direction | Explicitly Deferred / Guarded |
|---|---|---|
| MVP | 简中、匿名试算、确定性排盘、基础规则、证据、受限 AI、在线报告、打印、未来三年、模块化单体 | 真实支付、完整多流派、PDF 分享、完整 0～100 时间轴、第三方插件代码 |
| V1 | 多流派完整对比、正式 PDF、分享链接、完整时间轴等经批准能力 | 英/阿正式上线仍需人工/专业复核 |
| Future/V2 | Developer API、插件生态、独立 Search/服务拆分等按证据与 ADR | 不因路线图自动批准具体技术或供应商 |

### 24.12 Document Set Completion Criteria

- 01～15 Approved 1.0 的语义已被索引；
- 16 通过评审后可成为文档体系导航基线；
- Open Question、Candidate 和 Documentation Note 不被误作已批准结论；
- 任何编码必须等待用户单独明确授权；
- 实施前仍需解决 Phase 0/MVP 阻断 ADR、法律与命理专家事项。

---

## 25. Review Checklist

### 25.1 Document Governance

- [ ] 文档状态是否为 Review、版本是否为 0.9。
- [ ] 是否严格继承 01～15 Approved 1.0。
- [ ] 是否未修改任何已有文件或 Architecture Baseline。
- [ ] 是否没有代码、配置、脚本、目录或实现资产。
- [ ] 是否没有自行进入编码阶段。
- [ ] 问题是否只记录为 Open Question、Future Improvement 或 Documentation Note。

### 25.2 Reading and Structure

- [ ] 是否提供全量和角色化 Reading Order。
- [ ] 文档分层、权威主题和继承方向是否清晰。
- [ ] Dependency Matrix 是否覆盖 01～16。
- [ ] Cross Reference 是否覆盖主要架构主题和核心对象。
- [ ] Traceability 是否从产品/需求连接到架构与测试。

### 25.3 Glossary and Acronyms

- [ ] Aggregate、Aggregate Root、Entity、Value Object 是否与 04 一致。
- [ ] Domain Event、Domain Service、Repository、Snapshot、Projection、Context 是否一致。
- [ ] AIAnalysis、EvidenceBundle、RuleRun、PromptVersion、Knowledge 是否准确。
- [ ] Embedding、RAG、Citation、Validation、Operation、Consent、Audit、Version Manifest 是否准确。
- [ ] AnalysisProgress 是否明确为只读 Projection。
- [ ] AI、API、安全、运维缩写是否完整且未把候选误作决定。

### 25.4 Naming and Versioning

- [ ] Document、Requirement、Domain、Command、Query、Event、Identity 命名是否统一。
- [ ] Identity 是否与 Version 分离。
- [ ] API/Event/Document/Product/Model/Prompt Version 是否未混淆。
- [ ] Frozen/Published/Completed 历史是否保持不可变。
- [ ] ADR-BL、正式 ADR 和 Candidate 是否区分。

### 25.5 Ownership and Review

- [ ] 16 份文档是否都有 Accountable Owner Role。
- [ ] Review Process 是否覆盖产品、专家、法律、安全、AI、测试和运维。
- [ ] 是否没有虚构个人 Reviewer 或审批日期。
- [ ] Metadata 不一致是否仅记录为 DOC-NOTE-001。
- [ ] Approved 文档变化是否需 ADR/正式版本修订。

### 25.6 Summaries

- [ ] Architecture、Constraints、Security、AI、Testing、ADR 摘要是否与来源一致。
- [ ] 测试性能基线是否未被误称正式 SLO。
- [ ] AI 测试和用户认同是否未被误称命理预测准确率。
- [ ] Candidate 选型是否保持未决。
- [ ] 风险摘要是否可追踪回来源 Owner 文档。

### 25.7 Appendix

- [ ] 全部文档索引是否包含编号、文件、关系、状态和版本。
- [ ] Governing Status 是否按当前正式批准声明记录。
- [ ] Version History 是否避免虚构日期。
- [ ] Architecture Timeline 是否只表达依赖顺序而非虚构日历。
- [ ] Context、Lifecycle、Requirement ID、Version Type 索引是否完整。
- [ ] MVP/V1/Future 边界是否保持已批准口径。

### 25.8 Final Gate

- [ ] `16-GLOSSARY-AND-APPENDIX.md` 经评审后才可标记 Approved 1.0。
- [ ] 文档体系完成不自动授权编码。
- [ ] 编码前 Product/Expert/Legal/ADR 阻断项已有明确 Owner 与处理计划。
- [ ] 后续任何重大变化遵循 15 的 ADR 和 Baseline Revision 流程。

本文件完成后立即停止。不得生成其他文件，不得创建项目目录，不得进入编码阶段。
