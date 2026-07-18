# M4.1 Four Pillars Engine（Foundation）

**状态：** Implemented — Engineering Foundation / Expert Gate Open

**版本：** 0.1

**范围：** Chart Calculation Context

**基线：** 01～17 Approved 文档、M2 Domain Foundation、M3 Calendar & Time Engine、全部现有 ADR

## 1. 目标与边界

M4.1 建立四柱结果的纯领域表达、确定性计算端口、逐柱规则版本、推导证据和契约边界。它验证“明确输入 + 明确规则版本 = 明确结果”的工程能力，但不擅自选定仍待专家确认的四柱算法。

本阶段仅允许输出：

- 年柱；
- 月柱；
- 日柱；
- 时柱；
- 每柱的规则身份、规则集版本、算法版本、ADR 引用；
- 每柱的 Calculation Evidence；
- 结构化输出契约。

本阶段不输出五行、十神、旺衰、格局、神煞、用神、大运、流年或任何自然语言命理解读；不接入 AI、用户、支付、数据库或网络。

## 2. 基线追踪

| Requirement | M4.1 响应                                      | 验证                               | 当前结论                                 |
| ----------- | ---------------------------------------------- | ---------------------------------- | ---------------------------------------- |
| FR-020      | 只消费 M3 显式标准化结果                       | 非 `EXACT` 输入拒绝测试            | Foundation                               |
| FR-021      | 不替代 Calendar/Solar Term Provider            | Provider/ADR Gate                  | Pending Provider                         |
| FR-022      | 四柱值、逐柱证据与确定性执行器                 | Domain/Deterministic/Contract Test | Engineering Foundation；生产正确性待专家 |
| FR-026      | 逐柱锁定 RuleSet、Rule、Algorithm、Source、ADR | Evidence/Serialization Test        | Foundation                               |
| FR-027      | 未伪造第二实现；保留正式门禁                   | ADR-CAND-M4-001                    | Pending Expert                           |
| BR-008      | 真太阳时沿用 M3 策略，不在 M4 静默启用         | Architecture Gate                  | Pending Expert                           |
| BR-009      | 子时换日不在 M4 内设默认                       | ADR Reference Gate                 | Pending Expert                           |
| EC-001～011 | 非精确、歧义、边界不得静默推断                 | Failure/Fixture Tests              | Partial；权威边界样例待专家              |

## 3. 四柱领域模型

### 3.1 Typed Values

- `HeavenlyStem`：十个稳定枚举值，只表达干的身份。
- `EarthlyBranch`：十二个稳定枚举值，只表达支的身份。
- `PillarKind`：`year`、`month`、`day`、`hour`。
- `PillarRuleVersion`：记录 RuleId、RuleSetId、RuleSetVersion、AlgorithmId、AlgorithmVersion 和 ADR References。
- `Pillar`：柱类型、天干、地支、规则版本和一个或多个 CalculationEvidenceId。
- `FourPillars`：按年、月、日、时固定顺序组成的不可变值。

这些对象不包含解释属性，也不把四柱扩展为 RuleRun、EvidenceBundle 或 AIAnalysis。

### 3.2 Invariants

1. FourPillars 必须且只能包含年、月、日、时四柱，并按固定顺序排列。
2. 每柱必须有非空 Evidence 引用。
3. 每柱必须有规则与算法版本。
4. 每柱规则必须引用治理 ADR；争议规则不能脱离 ADR 执行。
5. 输出引用的 Evidence 必须存在于同一 CalculationTrace。

## 4. 计算端口与执行流程

`FourPillarsProvider` 是纯计算端口，接收 M3 的 `NormalizedTimePoint`，返回四个有类型的 `PillarValue`。端口不允许访问网络、数据库、缓存、AI 或当前系统时间。

`FourPillarsEngine` 的流程：

1. 验证 M3 结果为单一 `EXACT` 点；
2. 验证规则权限与四个规则均为 `Published`；
3. 调用注入的 Provider；
4. 验证 Provider 按年、月、日、时返回完整结果；
5. 创建输入快照 Evidence；
6. 为每柱创建输出 Evidence，并锁定 Rule/RuleSet/Algorithm/Source；
7. 构建 FourPillars 与四个 CalculationOutput；
8. 校验所有输出 Evidence 引用。

所有时间、规则、算法和数据版本均为显式输入；执行器不读取当前时间、不使用随机性、不进行 IO。

## 5. 年、月、日、时柱覆盖

| Pillar | M4.1 已完成                              | M4.1 未决定                        |
| ------ | ---------------------------------------- | ---------------------------------- |
| Year   | 类型、端口、独立规则版本、Evidence、契约 | 年界、节气口径、生产算法与权威数据 |
| Month  | 类型、端口、独立规则版本、Evidence、契约 | 月界、月序、年干关联与节气边界     |
| Day    | 类型、端口、独立规则版本、Evidence、契约 | 日柱锚点、历史范围、数据源与纠错   |
| Hour   | 类型、端口、独立规则版本、Evidence、契约 | 时辰边界、日干关联、子时与早晚子时 |

因此，M4.1 完成的是四柱计算“基础能力与治理闭环”，不是生产算法正确性验收。

## 6. Evidence Integration

M4.1 复用 M2 `CalculationEvidence`，它属于 Chart Calculation 推导轨迹，不等同于 Evidence Context 的 `Evidence` Entity 或 `EvidenceBundle`。

每次执行产生：

- 1 个 `INPUT_SNAPSHOT` Evidence，引用 CalculationSnapshot 身份；
- 4 个 `OUTPUT_VALUE` Evidence，分别对应年、月、日、时柱；
- 4 个 CalculationOutput，分别只引用对应柱 Evidence；
- 每个输出 Evidence 记录 RuleId、RuleSetId、RuleSetVersion、AlgorithmId、AlgorithmVersion、Source、CalculatedAt 和父 Evidence。

未来 Evidence Context 只能引用冻结 CalculationSnapshot 的稳定事实，不得反向修改 Chart 或四柱推导轨迹。

## 7. Rule Authority Gate

M4.1 定义两类权限：

- `expert_approved`：仅供未来通过正式专家与 ADR 治理的 Provider；
- `engineering_fixture`：仅验证工程契约，默认路径拒绝执行，必须由测试显式开启。

权限字段本身不是专家审批凭证。未来 Application Composition 必须从受治理 Registry 装配 Provider，并验证审批记录、版本、校验和及适用范围。

所有四柱规则当前共同引用 `ADR-CAND-M4-001`；其中日界、真太阳时、时区、节气等还必须引用对应 M2/M3 ADR。Candidate 不是 Accepted 决策，不能赋予生产授权。

## 8. Candidate Golden Fixtures

首批提供 4 个工程候选样例，覆盖四个显式标准化时间点和不同四柱值。Fixture 文件包含：

- `authority: engineering_fixture`；
- `expertApproval: pending`；
- 明确声明只验证确定性契约和 Evidence 接线；
- 完整输入 Lookup Key 与四柱期望值；
- Schema Version 和 Fixture Set Identity。

这些样例不是专家批准黄金命例，不证明历法或命理正确性，不计入产品黄金命例通过率。未知 Lookup Key 直接失败，禁止推断。

正式黄金样例必须由专家提供/审核，记录来源、授权、适用口径、规则版本、边界分类、期望四柱与独立交叉验证结果。

## 9. Contracts

新增两个 Draft 2020-12 JSON Schema：

- `four-pillars-result.schema.json`：四柱、逐柱规则版本、ADR、Evidence 与 Output 引用；
- `candidate-golden-four-pillars.schema.json`：候选样例权限、审批状态、Lookup Key 与期望四柱。

Schema Version 与 Rule/Algorithm Version 相互独立。当前契约版本为 `1.0.0`；兼容扩展不得改变既有字段语义。

## 10. Failure Semantics

| Code / Failure                | 含义                        | 安全行为       |
| ----------------------------- | --------------------------- | -------------- |
| `normalized_time_not_exact`   | 未知时间、范围或多个候选点  | 不计算四柱     |
| `rule_authority_not_approved` | 工程 Fixture 被用于默认路径 | 拒绝执行       |
| `rule_not_published`          | 任一柱规则未发布            | 拒绝执行       |
| `provider_result_incomplete`  | 未返回完整有序四柱          | 拒绝结果       |
| `provider_result_mismatch`    | 返回柱类型与规则绑定不一致  | 拒绝结果       |
| Fixture LookupError           | 显式数据集中不存在该时间点  | 不推断、不回退 |

不允许静默回退到另一个规则版本、另一个 Provider、默认时区、默认日界或默认四柱。

## 11. Tests

M4.1 新增测试覆盖：

- 四柱领域顺序与完整性；
- 4 个工程候选样例的逐柱输出；
- 每柱 Evidence、Rule Version 与 ADR 引用；
- 相同输入和版本的确定性；
- 输出到 Evidence 的引用完整性；
- 工程 Fixture 默认拒绝；
- 未发布规则拒绝；
- Range/Indeterminate 标准化结果拒绝；
- 未知 Fixture 不推断；
- 规则 ADR 与 Manifest 完整性；
- JSON Schema 与版本身份；
- 既有架构依赖、无 IO/AI、格式、类型与全量回归门禁。

## 12. 已确定与待决事项

### 已确定

- Chart Calculation 是四柱确定性事实的唯一所属 Context。
- 四柱与每柱规则、算法和 Evidence 必须不可变且可追溯。
- AI、Rule Evaluation 和自然语言解释不能进入四柱计算路径。
- 非精确输入不得静默产生唯一四柱。
- 工程候选数据不能冒充专家黄金数据。

### Pending Expert / ADR

1. 年柱年界、节气与适用历法口径。
2. 月柱节气边界、月序和年干关联规则。
3. 日柱算法锚点、历史范围、数据集与纠错方式。
4. 时柱时辰边界、日干关联、子时换日与早晚子时。
5. 真太阳时最终策略及其在四柱中的应用位置。
6. 公历/农历转换、时区、DST、地理和节气生产 Provider。
7. 第一批专家批准黄金、边界、争议命例。
8. 独立交叉验证实现或权威数据源与差异处置。

## 13. M4.1 Completion Gate

- [x] 四柱纯领域模型已建立。
- [x] 年、月、日、时均具有独立规则绑定与 Evidence。
- [x] 相同显式输入和版本可复现。
- [x] 非精确输入和未批准权限被拒绝。
- [x] Candidate Fixture 明确非专家黄金样例。
- [x] JSON Schema 与自动测试已建立。
- [x] 计算路径不访问网络、数据库、缓存、AI、当前时间或随机源。
- [x] 未实现禁止的分析、AI、用户、支付能力。
- [ ] 专家批准生产四柱口径与 Provider。
- [ ] 专家批准第一批正式黄金与边界命例。
- [ ] 独立交叉验证达到 FR-027 门禁。

未完成的三项不阻止 M4.1 工程基础合并，但阻止将其声明为生产四柱算法，也阻止进入依赖 Valid CalculationSnapshot 的正式规则分析与 AI 验收。
