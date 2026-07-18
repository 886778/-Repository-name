# M3 Calendar & Time Engine

## 1. Scope

M3 建立可复现、可版本化、可追溯的历法与时间计算内核。它完成民用日期验证、显式时区偏移转换、DST gap/fold 表达、Provider/Strategy 契约、计算时间线和稳定输出 Schema，但不实现完整四柱排盘或任何命理解释。

01～17 继续作为 Approved Architecture Baseline；M1 与 M2 是实施输入。本文件不修改基线，不批准任何 Pending 命理口径。

## 2. Baseline References

| 文档                                                                          | M3 继承的约束                                                                           |
| ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 01-PRODUCT-VISION.md §6、§11～12、§18、§21                                    | 确定性与 AI 分离；显示时区、真太阳时、换日与不确定性；不伪装精确                        |
| 02-SRS.md FR-012～016、FR-020～028、BR-002/007～010、EF-001～004、EC-001～011 | 时间精度、历史时区、DST、版本、边界和专家门禁                                           |
| 03-SYSTEM-ARCHITECTURE.md §3、§7.4、§10                                       | Calendar & Time 自治；输入规范化、时区、历法、可选修正、边界和验证分层                  |
| 04-DOMAIN-MODEL.md Calendar & Time Context、Chart Context、Timeline Aggregate | Calendar & Time 不产生命理结论；标准化结果单向提供给 Chart                              |
| 05-DATA-MODEL.md Identity/Version、Snapshot、Cross Context Rules              | Provider Identity 与 Data Version 分离；跨 Context 只交换稳定 Snapshot                  |
| 06-ROADMAP.md Domain/Data First、Traceability、ADR Gate                       | 风险驱动、专家样例和版本门禁先于正式算法                                                |
| 07-APPLICATION-ARCHITECTURE.md Application Service、Command、Consistency      | 应用层未来负责 Birth Snapshot 到 TimeNormalizationInput 的映射，不把业务规则放入 Engine |
| 08-API-DESIGN.md Resource Leakage、Compatibility                              | M3 不新增 API，不泄露内部 Provider 或领域对象                                           |
| 09-TECHNOLOGY-ARCHITECTURE.md Replaceable Adapter、Data Access、Reliability   | Provider 可替换；内核不访问网络、数据库、缓存或宿主隐式时区状态                         |
| 10-IMPLEMENTATION-GUIDE.md DDD、DI、Validation、Testing                       | 纯 Domain Port、显式依赖注入、类型化错误与自动门禁                                      |
| 11-DEPLOYMENT-OPERATIONS.md Configuration、Version、Observability             | 数据版本可观察但不含用户敏感信息；运行日志不替代推导链                                  |
| 12-SECURITY-PRIVACY.md Data Minimization、Supply Chain                        | Provider 数据包不包含用户数据；来源、Checksum 与许可证需治理                            |
| 13-AI-ARCHITECTURE.md AI Context Boundaries                                   | AI 不参与时间转换、数据补全、边界选择或差异裁决                                         |
| 14-TESTING-STRATEGY.md Domain、Boundary、Golden、Regression                   | 单元、属性、确定性、Schema、非法输入和架构测试                                          |
| 15-ARCHITECTURE-DECISION-RECORDS.md ADR Lifecycle / Baseline Change           | 数据源或策略绑定必须先经 ADR，不在实现中静默决定                                        |
| 16-GLOSSARY-AND-APPENDIX.md Naming、Identity≠Version、Timeline                | 统一术语；M3 TimeComputationTimeline 不冒充产品 Timeline Aggregate                      |
| 17-PROJECT-INITIALIZATION-PLAN.md DDD Module Bootstrap、Gates                 | 模块目录服从 Context；不创建业务 Schema、Repository 或 AI                               |
| docs/M1-PLATFORM-FOUNDATION.md                                                | Domain 不依赖 Platform；无 ORM、Migration、Broker 或业务表                              |
| docs/M2-DOMAIN-FOUNDATION.md                                                  | Raw/Validated/Canonical/Calculation 分层；推断显式；Kernel 无 IO/AI                     |
| docs/adr/M2-DOMAIN-DECISIONS.md                                               | 公农历、时区、DST、坐标、真太阳时、换日、未知时间和数据源仍 Pending                     |

## 3. Context Boundary

Calendar & Time 拥有 `TimeNormalizationInput`、Provider Port、CivilDate/LocalDateTime/UtcOffset、标准化结果和计算时间线。它不导入 Birth Aggregate；未来应用层从 `CanonicalBirthInputSnapshot` 映射到 `TimeNormalizationInput`。Chart Calculation 只能消费已发布的标准化 Snapshot，不得反向修改 Calendar & Time 状态。

## 4. Time Normalization

`TimeNormalizationEngine` 要求调用者显式提供：

- `CalendarProvider`；
- `TimeZoneRulesProvider`；
- `DayBoundaryStrategy`；
- `TrueSolarTimeStrategy`；
- RequestId、UTC performedAt、输入来源链和可选 OffsetSelection。

处理顺序为日期验证、时区确认、Provider Manifest 匹配、offset resolution、UTC 转换、真太阳时策略、日界策略和时间线冻结。没有默认 Provider，也不读取系统当前时间、宿主时区、网络或数据库。

结果状态：`Exact` 对应一个点，`Range` 对应两个有序点，`Indeterminate` 对应零个点。未知时间不会被填充。

## 5. Time Zone Conversion

Provider 返回 `Unique`、`Ambiguous`、`Gap` 或 `Unavailable`：

- Unique：使用唯一显式 offset；
- Ambiguous：必须提供属于 Provider Candidate 集合的 OffsetSelection；
- Gap：返回 `LOCAL_TIME_GAP`；
- Unavailable：返回 `TIME_ZONE_DATA_UNAVAILABLE`。

输入 TimeZoneReference 的 SourceId/Version、Provider Manifest 和每次 Resolution Manifest 必须一致。UTC 转换只执行 `local - explicit offset`，不调用 `zoneinfo` 或宿主 tzdata。超出支持日期范围返回类型化错误。

## 6. Provider Interfaces

`CalendarProvider` 负责支持能力声明与 CalendarDate 到 CivilDate 的转换。M3 只实现无外部数据的 `ProlepticGregorianProvider` 用于公历有效性验证；它不支持农历。

`SolarTermProvider` 只定义版本化边界查询契约。M3 没有节气数据、名称清单、公式或生产实现。

`CalendarDataManifest` 锁定 SourceId、DataVersion、Checksum 和 Capability。Provider 返回值必须携带同一 Manifest。

## 7. Day Boundary Strategy

`DayBoundaryStrategy` 是强制注入 Port。M3 的 `CivilMidnightBoundaryStrategy` 只表示普通民用日期午夜边界，用于验证机制；它明确不是子初换日、早晚子时或平台最终默认口径。任何命理日界策略在 ADR-CAND-M2-006/007 批准前不得实现或注册为生产策略。

## 8. True Solar Time Extension

`TrueSolarTimeStrategy` 接收 LocalDateTime 与显式坐标/缺失值，返回调整后的时间、秒差、是否应用、策略身份、版本和 Manifest。M3 只实现 `DisabledTrueSolarTimeStrategy`；测试 Fake 仅证明扩展可注入，不构成公式或生产决策。

## 9. Timeline Model

`TimeComputationTimeline` 是 Calendar & Time 内部的有序推导模型，不是 04/05 定义的产品 `Timeline` Aggregate。节点包含连续序号、稳定 DerivationId、Step、值、父引用、SourceId 和 SourceVersion。父节点必须先出现且身份唯一。

它只记录输入、日期验证、时区解析、UTC 转换、真太阳时策略和日界策略，不包含大运、流年、吉凶、规则发现、EvidenceBundle 或解释。

## 10. Validation and Error Model

类型化错误覆盖不支持日历、精度不足、非法日期、时区未确认、数据不可用、gap/fold、无效候选、Provider 版本不一致、UTC 越界和 Timeline 不变量。错误不包含用户身份或详细地点。

## 11. Stable Contract

`packages/contracts/schemas/m3/time-normalization-result.schema.json` 使用 JSON Schema Draft 2020-12，Schema Version 1.0.0。输出包含状态、显式执行时间、完整 Provider Manifest Id、标准化点和推导时间线。版本变化遵守 M2 Schema 兼容策略。

## 12. Requirements Traceability

| Requirement                 | M3 交付                                                      | 验证                            | 状态                                     |
| --------------------------- | ------------------------------------------------------------ | ------------------------------- | ---------------------------------------- |
| FR-012 / BR-007             | Exact、Range、Indeterminate；未知不补全                      | Unit / Schema                   | Implemented Foundation                   |
| FR-013 / FR-014             | TimeZoneReference 与 Manifest 必须匹配；歧义显式选择         | Unit / Negative                 | Implemented Foundation                   |
| FR-015 / BR-008             | TrueSolarTimeStrategy Port + Disabled 实现                   | Unit / Architecture             | Extension Only；公式 Pending             |
| FR-016 / BR-009             | DayBoundaryStrategy Port + Civil neutral strategy            | Unit / Architecture             | Extension Only；命理策略 Pending         |
| FR-020                      | 标准化流程、offset conversion、gap/fold 和历史 Provider Port | Unit / Property / Boundary      | Engine Implemented；生产数据 Pending     |
| FR-021                      | CalendarProvider/SolarTermProvider Port、公历验证            | Unit / Contract                 | Interface Implemented；农历/节气 Pending |
| FR-026 / BR-002             | Manifest、Checksum、performedAt、确定性结果                  | Repeat / Property / Schema      | Implemented                              |
| FR-027                      | Provider 可替换、差异可归因基础                              | Contract                        | Foundation Only；独立数据集 Pending      |
| EF-002 / EC-004～006        | gap/fold、候选偏移、Provider Version                         | Negative / Boundary             | Implemented Foundation                   |
| EC-001 / EC-009～011        | SolarTerm/TrueSolar/Calendar Provider Port                   | Contract                        | Pending Data / Expert                    |
| NFR-008 / NFR-016 / NFR-024 | 复现、纯 Domain、自动门禁                                    | Determinism / Architecture / CI | Implemented                              |

## 13. Determinism and Architecture Gates

- Engine 不导入 FastAPI、Pydantic、数据库、Redis、HTTP、网络、AI、`zoneinfo` 或随机模块；
- 禁止 `datetime.now`、`datetime.utcnow` 和 `date.today`；
- 相同 Request、Provider Manifest 和 Strategy Version 产生相等结果；
- Schema、序列化、属性、gap/fold、range、unknown、越界、父子引用和版本不匹配均自动测试；
- Secret Scan 与全部既有 Quality Gate 保持启用。

## 14. Decisions and Pending Items

已确定的是机制：显式 Provider、版本 Manifest、类型化 gap/fold、显式 offset selection、UTC 纯函数、策略 Port、不可变 Timeline 和输出 Schema。

仍待决定：生产 Calendar/Time Zone/Solar Term Provider、公农历转换、闰月、历史覆盖、节气算法与精度、真太阳时公式和最终默认、子初换日、早晚子时、未知时间候选策略、坐标来源及专家黄金样例。

新增 `ADR-CAND-M3-001` 只登记生产 Provider Binding 决策，不作最终选择。

## 15. Explicitly Not Implemented

- 年柱、月柱、日柱、时柱；
- 五行、十神、神煞、旺衰、格局、调候、用神、喜忌；
- 起运、大运、流年或产品 Timeline；
- 命理解读、Prompt、LLM、AI Provider；
- 账户、认证、支付、业务数据库 Schema、ORM、Repository 或 API；
- 未经批准的数据源、历法口径、节气公式、真太阳时或子时换日规则。
