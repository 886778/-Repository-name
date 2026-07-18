# M2 Requirements Traceability Matrix

**状态：** Implementation Baseline

**版本：** 1.0

**范围：** Domain Foundation and Traceability

## 1. 使用规则

本矩阵把已批准需求映射到 M2 工程制品和验证方式，不替代或修改 01～17。`Implemented` 仅表示 M2 基础契约已经实现，不表示对应 MVP 业务功能完成。任何命理口径仍以基线中的专家门禁为准。

状态定义：

- `Implemented`：M2 范围内的类型、契约或门禁已实现并有自动测试。
- `Foundation Only`：只具备接口或版本基础，业务规则尚未实现。
- `Pending Expert`：必须等待命理专家批准。
- `Pending ADR`：必须先完成 ADR。
- `Deferred`：不属于 M2。

## 2. 正式矩阵

| Requirement ID   | 来源文档与章节                  | 所属模块                       | 实现阶段 | 测试类型                   | 验收标准                                                                    | 当前状态        |
| ---------------- | ------------------------------- | ------------------------------ | -------- | -------------------------- | --------------------------------------------------------------------------- | --------------- |
| PV-CP-001        | 01 §6.2、§6.4                   | Chart Calculation              | M2       | Determinism / Architecture | 计算不依赖 AI；相同完整请求得到相同结果；版本与输入可追溯                   | Implemented     |
| PV-INPUT-001     | 01 §12 阶段 3～5                | Birth / Calendar & Time        | M2       | Unit / Schema              | 时间精度、时区、地点、来源、不确定性可显式表达，不静默补全                  | Implemented     |
| UC-003           | 02 §5 User Stories              | Birth                          | M2       | Unit / Schema              | 缺失或不精确时间进入显式类型并保留不确定性                                  | Implemented     |
| UC-004           | 02 §5 User Stories              | Calendar & Time                | M2       | Contract                   | 关键时间参数可被确认并进入版本化计算输入                                    | Foundation Only |
| UC-015           | 02 §5 User Stories              | Chart Calculation              | M2       | Contract                   | 计算输入、算法、规则和数据源版本可追溯                                      | Foundation Only |
| UC-023           | 02 §5 User Stories              | Audit / Traceability           | M2       | Trace test                 | 可从输出引用回溯计算输入、算法、规则集和来源                                | Foundation Only |
| FR-010           | 02 §7                           | Birth                          | M2       | Schema / Round trip        | 公历/农历边界、原始值、来源和确认状态可表达；不执行转换                     | Implemented     |
| FR-011           | 02 §7                           | Birth / Chart Calculation      | 后续     | —                          | 直接四柱输入需要专家确认后的专用契约与校验                                  | Deferred        |
| FR-012           | 02 §7                           | Birth                          | M2       | Unit / Schema              | 分钟、小时、范围、未知语义可区分；未知不填成事实                            | Implemented     |
| FR-013           | 02 §7                           | Calendar & Time                | M2       | Unit / Schema              | 坐标、精度、来源、时区候选和消歧状态可追踪                                  | Foundation Only |
| FR-014           | 02 §7                           | Birth / Chart Calculation      | M2       | Unit / Contract            | 自动决策有来源、版本、确认与可覆盖属性                                      | Implemented     |
| FR-015           | 02 §7                           | Calendar & Time                | 后续     | ADR / Expert regression    | 真太阳时策略和算法版本经批准后才实现                                        | Pending Expert  |
| FR-016           | 02 §7                           | Calendar & Time                | 后续     | ADR / Expert regression    | 子时换日方案经批准后才实现                                                  | Pending Expert  |
| FR-020           | 02 §8                           | Calendar & Time                | 后续     | Boundary / Golden case     | 历史时区、DST 和标准化算法待数据源与 ADR 决策                               | Pending ADR     |
| FR-021           | 02 §8                           | Calendar & Time                | 后续     | Golden / Cross-validation  | 公农历与节气计算待正式算法和数据版本批准                                    | Pending Expert  |
| FR-022           | 02 §8                           | Chart Calculation              | 后续     | Golden / Cross-validation  | 四柱计算不属于 M2，不得由 No-op Kernel 实现                                 | Pending Expert  |
| FR-023           | 02 §8                           | Chart Calculation              | 后续     | Domain / Golden            | 基础派生事实等待正式排盘口径                                                | Pending Expert  |
| FR-024           | 02 §8                           | Chart Calculation              | 后续     | Golden / Boundary          | 大运与流年算法等待专家确认                                                  | Pending Expert  |
| FR-026           | 02 §8                           | Chart Calculation              | M2       | Determinism / Trace        | 算法与数据版本是显式输入，禁止隐式时间、网络、数据库、随机与 AI             | Implemented     |
| FR-027           | 02 §8                           | Chart Calculation              | 后续     | Cross-validation           | 独立数据或实现的交叉验证尚未选择                                            | Deferred        |
| FR-030           | 02 §9                           | Rule Evaluation                | 后续     | Rule regression            | RuleRun 执行不在 M2；M2 只建立版本协议                                      | Foundation Only |
| FR-031           | 02 §9                           | Rule Evaluation                | 后续     | Expert regression          | 子平基础规则集需专家批准                                                    | Pending Expert  |
| FR-032           | 02 §9                           | Rule Evaluation                | M2       | Unit                       | EffectiveStatus、Compatibility、Supersedes 可表达                           | Implemented     |
| FR-033           | 02 §9                           | Chart Calculation / Evidence   | M2       | Trace / Schema             | 计算推导链可表达输入、中间值、规则、版本、父子和来源；不冒充 EvidenceBundle | Foundation Only |
| FR-034           | 02 §9                           | Evidence                       | 后续     | Expert / Product           | 正式 EvidenceStatus 阈值不在 M2                                             | Pending Expert  |
| FR-035           | 02 §9                           | Rule Evaluation / Evidence     | 后续     | Conflict regression        | 冲突保留策略已是基线，具体规则内容待专家确认                                | Foundation Only |
| FR-036           | 02 §9                           | Rule Evaluation / Governance   | M2       | Unit                       | Published 版本不可无治理来源；参数键唯一                                    | Foundation Only |
| BR-002           | 02 §18 Business Rules           | Chart Calculation              | M2       | Determinism                | 同一完整 KernelRequest 产生相等 KernelResult                                | Implemented     |
| BR-003           | 02 §18 Business Rules           | Rule Evaluation / Traceability | M2       | Unit / Trace               | 推导值带 RuleId、RuleSetId、版本和算法版本                                  | Foundation Only |
| BR-007           | 02 §18 Business Rules           | Birth                          | M2       | Unit / Schema              | 未知时间使用 MissingValue，不发生静默推断                                   | Implemented     |
| BR-008           | 02 §18 Business Rules           | Calendar & Time                | 后续     | ADR                        | 真太阳时最终策略保持 Pending                                                | Pending Expert  |
| BR-009           | 02 §18 Business Rules           | Calendar & Time                | 后续     | ADR                        | 子时换日最终口径保持 Pending                                                | Pending Expert  |
| BR-010           | 02 §18 Business Rules           | Rule Evaluation                | M2 Gate  | Static review              | M2 无旺衰、格局、调候、用神、喜忌、起运或神煞规则                           | Implemented     |
| BR-015           | 02 §18 Business Rules           | Rule Evaluation / Traceability | M2       | Unit / Schema              | Rule、RuleSet、Algorithm、Schema 和来源均有版本身份                         | Foundation Only |
| EC-001～011      | 02 §23 Edge Cases               | Birth / Calendar & Time        | M2       | Fixture / Schema           | 边界可表达；实际历法、DST、换日与真太阳时结果不在 M2                        | Foundation Only |
| EC-014           | 02 §23 Edge Cases               | Evidence / AI                  | 后续     | Validation                 | AI 引用校验不在 M2；计算输出已禁止未知推导引用                              | Foundation Only |
| NFR-006          | 02 §19                          | Domain                         | M2       | Unit                       | 冻结值对象不可变，引用完整性由构造时验证                                    | Implemented     |
| NFR-008          | 02 §19                          | Chart Calculation              | M2       | Determinism / Schema       | 输入、算法、规则和数据版本显式；序列化可往返                                | Implemented     |
| NFR-016          | 02 §19                          | Architecture                   | M2       | Architecture               | Domain 不依赖 Web、数据库、缓存、Worker 或平台适配器                        | Implemented     |
| NFR-024          | 02 §19                          | Quality                        | M2       | Full gate                  | 单元、Schema、属性、确定性、架构与 Secret 扫描进入 CI                       | Implemented     |
| SA-AP-001        | 03 §3 AP-001                    | Chart Calculation              | M2       | Architecture               | 确定性核心与 AI/IO 隔离                                                     | Implemented     |
| SA-TIME-001      | 03 §10                          | Calendar & Time                | M2       | Contract                   | 处理阶段和算法契约具备版本化输入边界                                        | Foundation Only |
| SA-EVID-001      | 03 §12                          | Chart Calculation / Evidence   | M2       | Trace                      | 计算推导不可被输出绕过；正式 EvidenceBundle 仍属 Evidence Context           | Implemented     |
| DM-XCTX-001      | 04 §6、§18                      | Birth / Chart Calculation      | M2       | Architecture               | Chart 仅消费 Birth 发布的不可变 CanonicalBirthInputSnapshot                 | Implemented     |
| DM-RULE-001      | 04 Rule Aggregate               | Rule Evaluation                | M2       | Unit                       | M2 不创建 RuleRun/RuleFinding，只定义版本协议                               | Implemented     |
| DATA-IMM-001     | 05 Immutable Object Rules       | Domain                         | M2       | Unit                       | frozen value objects 无原地状态修改                                         | Implemented     |
| ROAD-RP-005      | 06 §2 RP-005                    | Documentation                  | M2       | Review                     | RTM 链接需求、模块、阶段、测试和验收                                        | Implemented     |
| APP-CMD-001      | 07 §5                           | Application                    | 后续     | Application test           | M2 不实现 Command Handler 或跨 Context 流程                                 | Deferred        |
| API-BOUNDARY-001 | 08 Resource / Command rules     | API                            | 后续     | Contract                   | M2 不新增 API 或 DTO                                                        | Deferred        |
| TECH-PORT-001    | 09 Technology Principles        | Domain                         | M2       | Architecture               | Domain 只用 Python 标准库；技术能力是可替换适配器                           | Implemented     |
| ENG-DDD-001      | 10 DDD Implementation Rules     | Backend                        | M2       | Import Linter / AST        | 模块边界和依赖方向自动检查                                                  | Implemented     |
| OPS-TRACE-001    | 11 Observability / Audit        | Operations                     | 后续     | Operations                 | calculated_at 必须显式输入；M2 不将运行日志当证据                           | Foundation Only |
| SEC-MIN-001      | 12 Privacy Principles / PII     | Birth                          | M2       | Review                     | 无姓名、账户、详细地址、认证或持久化                                        | Implemented     |
| AI-BOUNDARY-001  | 13 AI Context Boundaries        | Chart Calculation              | M2       | Architecture               | Kernel 禁止 AI import 与 Provider 调用                                      | Implemented     |
| TEST-DOMAIN-001  | 14 Domain / Coverage / Gates    | Quality                        | M2       | Full gate                  | Domain、属性、Schema、非法输入、边界和架构测试齐备                          | Implemented     |
| ADR-GOV-001      | 15 ADR Creation Criteria        | Governance                     | M2       | Documentation review       | 十项未决时间/历法/身份议题登记为 Proposed/Pending                           | Implemented     |
| GLOSS-IDVER-001  | 16 §10～11                      | Domain                         | M2       | Unit / Review              | Identity 与 Version 分离，语义版本不作为对象身份                            | Implemented     |
| INIT-DDD-001     | 17 §7、§10                      | Engineering                    | M2       | Architecture / CI          | Context 骨架与 Day-One tests 建立，无业务 Schema                            | Implemented     |
| M1-DEFER-001     | M1 §PostgreSQL / Deferred gates | Platform                       | M2       | Git diff / Architecture    | 不引入 ORM、Migration、Repository 或业务表                                  | Implemented     |

## 3. 追踪结论

- M2 已覆盖输入语义、纯领域边界、版本协议、计算推导、Schema 和自动门禁。
- 所有完整排盘、规则运行、正式 EvidenceBundle、AI 与报告需求仍未实现。
- `Foundation Only` 不得在发布报告中被解释为业务能力已完成。
- 本矩阵的状态变化必须随实现与测试证据更新；不得反向修改批准基线。

## 4. 非 M2 需求保全登记

下表保证 02-SRS 中未进入 M2 实现的需求仍有阶段与验证去向。它不降低原验收标准；正式实施时应拆成逐项可执行测试案例。

| Requirement ID                                                                  | 来源文档与章节         | 所属模块                           | 实现阶段            | 测试类型                                             | 验收标准                                               | 当前状态                        |
| ------------------------------------------------------------------------------- | ---------------------- | ---------------------------------- | ------------------- | ---------------------------------------------------- | ------------------------------------------------------ | ------------------------------- |
| BF-001～BF-007                                                                  | 02 §4 Business Flows   | Application / 多 Context           | 后续端到端阶段      | E2E / Saga / Acceptance                              | 各流程按 SRS 原步骤、异常和冻结边界完成                | Deferred                        |
| UC-001～UC-002、UC-005～UC-014、UC-016～UC-022、UC-024                          | 02 §5 User Stories     | Product / 多 Context               | MVP / V1 / V2       | Acceptance / Usability / E2E                         | 每个 User Story 的 SRS 验收结果逐项满足                | Deferred                        |
| FR-001～FR-006                                                                  | 02 §6                  | Identity / Account                 | 后续 Identity 阶段  | Security / API / E2E                                 | 匿名、年龄、账户与删除按 SRS 验收                      | Deferred                        |
| FR-017～FR-018                                                                  | 02 §7                  | Birth / Chart                      | 后续                | Authorization / Parser / E2E                         | 资产隔离、授权、导入确认与来源保留                     | Deferred                        |
| FR-025、FR-028                                                                  | 02 §8                  | Chart Calculation                  | V1 / 后续           | Golden / Comparison                                  | 仅在批准算法与版本锁定后实现                           | Deferred                        |
| FR-037～FR-038                                                                  | 02 §9                  | Rule Evaluation                    | V1 / 后续           | Expert regression                                    | 神煞与多流派规则必须先经专家批准                       | Pending Expert                  |
| FR-040～FR-045                                                                  | 02 §10                 | Knowledge                          | 后续 Knowledge 阶段 | Rights / Search / Governance                         | 来源、授权、审核、检索和命例 Consent 按 SRS 验收       | Deferred                        |
| FR-050～FR-065                                                                  | 02 §11～12             | AI Analysis / Conversation         | 后续 AI 阶段        | AI evaluation / Security / Citation                  | 仅消费 Frozen Evidence，结构、事实、引用和风险检查通过 | Deferred                        |
| FR-070～FR-076                                                                  | 02 §13                 | Report                             | 后续 Report 阶段    | Snapshot / Print / Security / i18n                   | 冻结、复现、打印、PDF、分享和语言按版本验收            | Deferred                        |
| FR-080～FR-084                                                                  | 02 §14                 | Timeline                           | 后续 Timeline 阶段  | Domain / Evidence / E2E                              | Basic 与 Analytical Timeline 依赖方向保持基线          | Deferred                        |
| FR-090～FR-096                                                                  | 02 §15                 | Privacy / Consent / Data Rights    | 后续                | Privacy / Deletion / Audit                           | 查看、导出、删除、Consent、Retention 与访问记录可审计  | Deferred                        |
| FR-100～FR-105                                                                  | 02 §16                 | Authorization / Audit / Operations | 后续                | Permission / Audit / Operations                      | 最小权限、职责分离、审计和安全事件满足 SRS             | Deferred                        |
| FR-110～FR-114                                                                  | 02 §17                 | i18n / Accessibility               | MVP / V1            | i18n / RTL / Accessibility                           | 简体中文正式质量并预留完整 i18n/RTL                    | Deferred                        |
| FR-120～FR-124                                                                  | 02 插件与 API 章节     | Module Registry / API              | V2                  | Contract / Security                                  | MVP 不执行第三方动态代码；开放 API 需独立门禁          | Deferred                        |
| FR-130～FR-137                                                                  | 02 后台管理章节        | Governance / Admin                 | 后续                | Authorization / Audit / Acceptance                   | 所有管理操作按角色、职责分离和影响分析验收             | Deferred                        |
| BR-001、BR-004～BR-006、BR-011～BR-025                                          | 02 §18                 | 多 Context                         | 全阶段约束          | Static / Security / Acceptance                       | 作为持续不变量进入相应实现与发布门禁                   | Not Implemented in M2           |
| NFR-001～NFR-005、NFR-007、NFR-009～NFR-015、NFR-017～NFR-023、NFR-025～NFR-030 | 02 §19、性能补充       | Platform / 多 Context              | 对应功能阶段        | Performance / Security / Reliability / Accessibility | 保留 SRS 量化目标与待复核条件                          | Deferred                        |
| EF-001～EF-012                                                                  | 02 §22 Exception Flows | 多 Context                         | 对应功能阶段        | Negative / Recovery / Security                       | 每个异常必须显式失败、降级或人工处置，不伪装成功       | Deferred；M2 已覆盖输入表达基础 |
| EC-012～EC-025                                                                  | 02 §23 Edge Cases      | Rule / Evidence / AI / Data / i18n | 对应功能阶段        | Boundary / Regression / Security                     | 保留冲突、引用、范围、删除、版本与 RTL 边界            | Deferred                        |
