# M2 Domain Decision Register

**状态：** Proposed / Pending

**版本：** 0.1

**治理依据：** 15-ARCHITECTURE-DECISION-RECORDS.md §4～21

本文件是待决登记，不批准任何命理算法、数据源或默认值。每项在进入正式实现前必须形成符合 15 文档模板的 ADR，完成专家、产品、安全、隐私、测试及迁移影响评审。

| Candidate ID    | 议题                 | 当前状态           | 已批准约束                                             | 尚需决定                                              | Owner Role                       | 实现门禁                  |
| --------------- | -------------------- | ------------------ | ------------------------------------------------------ | ----------------------------------------------------- | -------------------------------- | ------------------------- |
| ADR-CAND-M2-001 | 公历与农历输入边界   | Proposed / Pending | 两种输入均需保留原值、来源和确认；不得静默转换         | 闰月表达、转换能力范围、失败/歧义处置、数据集         | Calendar & Time Owner + 命理专家 | FR-010、FR-021 正式转换前 |
| ADR-CAND-M2-002 | 时区来源             | Proposed / Pending | 保存标准化标识、来源和版本；歧义不得静默选择           | 权威数据集、历史覆盖、升级与回滚                      | Calendar & Time Owner            | FR-013、FR-020 实现前     |
| ADR-CAND-M2-003 | 夏令时处理           | Proposed / Pending | 无效/重复本地时间必须显式错误或候选                    | gap/fold 交互、确认语义、黄金样例                     | Calendar & Time Owner + QA       | FR-020 实现前             |
| ADR-CAND-M2-004 | 地理坐标来源         | Proposed / Pending | 仅保存计算必要精度，不默认保存详细地址                 | 数据供应源、精度策略、海外覆盖和授权                  | Data / Privacy Owner             | 地点解析接入前            |
| ADR-CAND-M2-005 | 真太阳时是否启用     | Proposed / Pending | MVP 可切换；基线记载默认关闭但最终策略与口径待专家确认 | 计算公式、默认值最终确认、经度/均时差来源             | 命理专家 + Product Owner         | 任何正式真太阳时计算前    |
| ADR-CAND-M2-006 | 子初换日规则         | Proposed / Pending | 可配置，不宣称唯一标准                                 | 平台默认、选项集合、版本兼容                          | 命理专家                         | 日柱计算前                |
| ADR-CAND-M2-007 | 早晚子时             | Proposed / Pending | 不得把争议观点写成唯一事实                             | 是否区分、与换日规则组合、展示方式                    | 命理专家                         | 日柱/时柱边界实现前       |
| ADR-CAND-M2-008 | 出生时间未知或不精确 | Proposed / Pending | 不静默补精确值；保留范围/未知和不确定性                | 多候选盘、部分结果或阻断策略                          | Product Owner + 命理专家         | 候选盘或降级计算前        |
| ADR-CAND-M2-009 | 历法数据来源及版本   | Proposed / Pending | 所有计算数据源必须版本化、可追溯、可复现               | 数据源、授权、覆盖范围、交叉验证、更新策略            | Algorithm Governance Owner       | 非 No-op Kernel 前        |
| ADR-CAND-M2-010 | 性别字段对规则的影响 | Proposed / Pending | 身份信息与算法参数分离；字段影响不可隐式               | 允许值、用途、非二元/未指定处置、受影响规则、法律说明 | Product + Legal + 命理专家       | 任何依赖该字段的规则前    |

## 共同影响分析要求

每项正式 ADR 必须说明 Context、Problem、Decision Drivers、Options、Decision、正负后果、风险、安全/隐私/AI/数据/API/运维/测试影响、迁移、回滚、可观察性、审批与复审触发器。任何 Pending 项都不能通过代码默认值、Fixture 名称或 No-op 示例被事实批准。

## 当前实现约束

- `CalendarType` 只表达用户声明的输入类型，不执行转换。
- `TimeZoneReference` 只表达 resolved/ambiguous/unresolved 与候选，不选择数据源。
- `RuleSexMarker` 只保留规则可能需要的显式输入，不授权任何规则使用它。
- `NoOpCalculationKernel` 不计算命盘，只返回输入快照推导记录。
- 示例中的 `pending`、`empty-ruleset`、`noop-kernel` 都是非生产占位身份，不是产品决策。
