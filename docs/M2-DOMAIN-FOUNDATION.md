# M2 Domain Foundation and Traceability

## 1. Scope

M2 建立可复现、可追溯、可版本化的领域基础，不实现完整排盘、命理规则、自然语言解释、AI、账户、支付、业务持久化或业务 API。01～17 仍是批准的 Architecture Baseline；本文件只记录实施映射，不改变基线。

## 2. Baseline References Read

| 文档                                                                            | M2 采用的正式约束                                                                                       |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| 01-PRODUCT-VISION.md §6、§11～12、§18、§21                                      | 确定性计算与 AI 分离；输入、事实、规则、解释分层；不确定性不伪装为精确；专家待确认项保留                |
| 02-SRS.md §5、§7～9、§18～24                                                    | FR-010～016、FR-020～036、BR-002/003/007～010/015、NFR-006/008/016/024、异常和边界验收                  |
| 03-SYSTEM-ARCHITECTURE.md §3、§7～12                                            | 确定性核心隔离、Context 边界、算法契约、规则与证据分层                                                  |
| 04-DOMAIN-MODEL.md §5～18                                                       | Birth、Calendar & Time、Chart Calculation、Rule Evaluation、Evidence 的所有权与跨 Context Snapshot 规则 |
| 05-DATA-MODEL.md §3～12                                                         | Identity≠Version、不可变 Snapshot、跨 Context 只读引用、无内部 Entity 共享                              |
| 06-ROADMAP.md §2、§4～6、§15                                                    | Domain/Data First、Traceability、风险门禁与 ADR Gate                                                    |
| 07-APPLICATION-ARCHITECTURE.md §3～7                                            | 应用层只编排，不能重写计算或证据规则；M2 不实现 Saga/Command Handler                                    |
| 08-API-DESIGN.md Resource、Command、Compatibility                               | M2 不泄露 Aggregate、不新增 API 合同或 DTO                                                              |
| 09-TECHNOLOGY-ARCHITECTURE.md Layering、Repository、Infrastructure              | Domain 与基础设施隔离；基础设施保持可替换                                                               |
| 10-IMPLEMENTATION-GUIDE.md DDD、Domain Event、Testing                           | 纯领域实现、依赖方向、工程与测试规范                                                                    |
| 11-DEPLOYMENT-OPERATIONS.md Configuration、Observability、Audit                 | 不读取隐式运行时间；运行日志不替代领域证据                                                              |
| 12-SECURITY-PRIVACY.md Data Minimization、PII、Audit                            | 出生输入最小化；无账户、认证、详细地址或持久化                                                          |
| 13-AI-ARCHITECTURE.md AI Context Boundaries、Validation                         | AI 不进入计算路径；计算推导不接受模型输出                                                               |
| 14-TESTING-STRATEGY.md Domain、Contract、Test Data、Quality Gates               | 单元、属性/确定性、Schema、序列化、非法输入、架构测试                                                   |
| 15-ARCHITECTURE-DECISION-RECORDS.md Governance、Template、Baseline relationship | 未决历法/时间/身份议题登记为 Proposed/Pending，不静默决定                                               |
| 16-GLOSSARY-AND-APPENDIX.md Glossary、Naming、Versioning                        | 使用统一语言；Identity 与 Version 分离；Traceability 命名一致                                           |
| 17-PROJECT-INITIALIZATION-PLAN.md §7、§10、§13～15                              | Context 目录不是边界本身；Day-One test；专家和 ADR Gate                                                 |
| docs/M1-PLATFORM-FOUNDATION.md 全文                                             | Domain 不依赖 platform/bootstrap；M1 无业务 Schema；ORM、Migration、Broker 等仍受门禁                   |

## 3. Module Boundaries

- `modules/calendar_time`：发布日期、时间精度、时区解析状态、坐标、来源、缺失与不确定性值对象。它不做历法转换、DST 解析或真太阳时计算。
- `modules/birth`：拥有 Raw、Validated、Canonical Birth Input 领域阶段；对 Chart Calculation 仅发布不可变 `CanonicalBirthInputSnapshot`。
- `modules/chart_calculation`：拥有 `CalculationInput`、算法版本、推导链和纯 Kernel Port。它不访问 BirthInput 内部 Entity。
- `modules/rule_evaluation`：只发布规则身份、规则集身份、语义版本、状态、兼容性、替代、来源和确定性参数协议；不创建 RuleRun、RuleFinding 或规则内容。
- 正式 `EvidenceBundle` 与 `Evidence` 仍属于 Evidence Context，未在 M2 实现。`CalculationEvidence` 是 CalculationSnapshot 形成前后的推导记录值，不是 Evidence Entity。

## 4. Input Stages

1. `RawBirthInput`：保留用户原始文本与显式缺失原因。
2. `ValidatedBirthInput`：字段结构合法，但时区等仍可明确处于 ambiguous/unresolved。
3. `CanonicalBirthInput`：用户已确认，来源链和所有不确定性被锁定。
4. `CalculationInput`：Chart Calculation 消费的不可变 Snapshot，加上明确计算策略。

`BirthInputValidator` 与 `BirthInputCanonicalizer` 是确定性 Port。M2 不提供会作业务推断的实现。任何未来决策必须生成 `NormalizationDecision`，包含 DecisionId、字段、方法、原值、选择值、来源、版本、是否可覆盖与用户确认；非用户直接选择的决策未确认时构造失败。

## 5. Derivation and Evidence Boundary

每条 `CalculationEvidence` 包含计算推导 ID、类型、值、RuleId（输入快照可为空）、RuleSetId/Version、AlgorithmId/Version、数据来源、显式计算时间、父推导、警告和不确定性。父记录必须先于子记录，ID 唯一。每个 `CalculationOutput` 必须引用已存在的 CalculationEvidenceId，否则 `KernelResult` 无法构造。

这些记录用于证明确定性事实如何产生。后续 Evidence Context 只能引用 Chart Context 发布的冻结 CalculationSnapshot/公开推导引用，再构建正式 EvidenceBundle；解释层不能直接把计算推导冒充规则证据。

## 6. Rule Version Protocol

协议支持 RuleId、RuleSetId、SemanticVersion、EffectiveStatus、Compatibility、Supersedes、SourceReference 和有序确定性参数。Published 版本必须有治理来源，参数键必须唯一。M2 没有 Published 规则实例，也没有任何命理规则内容。

## 7. Calculation Kernel Port

`CalculationKernel.calculate(KernelRequest)` 只接受 Canonical Calculation Input、AlgorithmVersion、RuleSetId/Version、显式带时区计算时间和来源。返回 `KernelResult(outputs, trace)`。

自动门禁禁止 Kernel 引入网络、HTTP、数据库、Redis、平台适配器或 AI。当前 `NoOpCalculationKernel` 只生成一个输入快照推导记录和 `NO_OP_KERNEL` 警告，输出集合为空。相同完整请求产生值相等结果；时间是显式请求字段，不读取系统当前时间。

## 8. Schema and Fixtures

稳定 JSON Schema 位于 `packages/contracts/schemas/m2`，采用 Draft 2020-12 和显式 `schemaVersion=1.0.0`。兼容策略：新增可选语义使用 minor；删除、类型/语义变化或新增必填字段使用 major；被历史 Snapshot 引用的旧版本保持可读。

Fixtures 覆盖正常输入、缺失时间、不明确时区、边界日期、非法输入和推导链。Fixture 只验证表达能力，不声称任何命理计算结果。

## 9. ADR Gates

`docs/adr/M2-DOMAIN-DECISIONS.md` 登记公农历边界、时区来源、DST、坐标来源、真太阳时、子初换日、早晚子时、未知时间、历法数据源和性别规则影响。全部为 Proposed/Pending。

## 10. Automated Architecture Gates

- backend modules 不得依赖 bootstrap、platform 或 projections；
- Domain 不得导入 FastAPI、Pydantic、asyncpg、Redis、SQLAlchemy 或 apps；
- Calculation Kernel 不得导入网络、数据库、缓存、AI 或平台适配器；
- 输出必须经 `KernelResult` 验证其推导引用；
- Import Linter 与 AST architecture tests 同时执行。

## 11. Verification Scope

测试覆盖值对象不变量、非法输入、显式推断确认、序列化往返、SemanticVersion 属性测试、规则版本约束、No-op Kernel 确定性、推导父子完整性、输出引用完整性、Schema/Fixture、Schema 兼容清单和架构边界。仓库现有格式、Lint、Type、测试、Coverage、Import Linter、前端测试和构建门禁全部保留。

## 12. Explicitly Not Implemented

- 四柱、公农历转换、节气、五行、十神、神煞、旺衰、格局、调候、用神、喜忌、起运、大运或流年算法；
- RuleRun、RuleFinding、正式 EvidenceBundle/Evidence；
- 命理解读、Prompt、LLM、Provider 或 AI；
- 账户、认证、会员、支付、业务数据库 Schema、ORM 或 Repository；
- 任何待专家或 ADR 决策的默认口径。
