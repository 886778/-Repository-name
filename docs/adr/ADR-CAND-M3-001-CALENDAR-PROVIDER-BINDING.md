# ADR-CAND-M3-001：Calendar Provider Production Binding

**Status：** Proposed / Pending

**Date：** 2026-07-18

**Owner：** Calendar & Time Owner / Algorithm Governance Owner

## Context

M3 已定义 Calendar、Time Zone Rules 与 Solar Term Provider 契约，并要求每次结果锁定 SourceId、Version、Checksum 与 Capability。01～17 和 M2 ADR 没有批准生产历法数据集、历史时区数据源、节气算法或供应商。

## Problem

正式 FR-020/FR-021 需要覆盖历史时区、夏令时、公农历转换及节气边界。若直接在代码中绑定宿主机时区库、未版本化系统数据或任意第三方库，将破坏复现、审计与回滚能力。

## Decision Drivers

- 可复现和历史版本可读；
- 历史时区与 DST gap/fold 覆盖；
- 公农历、闰月和节气黄金样例；
- 数据授权、更新、校验、回滚与离线运行；
- 不允许 AI 或网络成为计算时依赖。

## Options

1. 使用宿主机隐式时区与历法数据；
2. 绑定单一第三方库但不快照数据；
3. 引入经过专家、法律与技术评审的版本化离线数据包，通过现有 Provider 契约绑定；
4. 自建并维护全部数据。

## Proposed Direction

方向倾向 Option 3，但本文件不批准具体数据源、库、供应商、节气算法或版本。正式 Decision 必须在黄金样例、授权、覆盖范围、独立交叉验证和回滚演练完成后作出。

## Consequences

- M3 可完成 Provider-independent Engine 和测试 Fake；
- 生产农历转换、历史时区与节气结果继续阻断；
- 未来 Provider 替换不改变 Calendar & Time Domain Contract；
- 需要维护数据包 Manifest、Checksum、兼容清单和历史可读策略。

## Risks

- 数据源范围或授权不足；
- 不同数据源在历史边界产生差异；
- 数据升级造成未识别语义变化；
- 把测试 Fake 或宿主机 tzdata 误用为生产来源。

## Security / Privacy / AI Impact

数据包不得包含用户出生资料；运行时不联网；AI 不参与解析、补全或差异裁决。供应链来源、Checksum 与许可证必须可审计。

## Testing Requirements

正式批准前必须具备专家黄金命例、DST gap/fold、历史偏移、闰月、节气边界、海外地点、范围边界、交叉实现差异与回滚测试。

## Migration and Rollback

新数据版本不得覆盖历史 Manifest。新计算显式选择新版本；旧结果继续通过原版本或受控归档快照解释。回滚只改变新任务绑定，不修改旧快照。

## Approval

Pending：命理专家、Algorithm Governance、Data/Legal、Security、QA、Architecture Owner。

## Review Trigger

选择生产 Calendar/Time Zone/Solar Term Provider、引入外部数据包、扩大日期或地区范围，或准备实现 FR-021 时必须评审。

## Related Documents

- 02-SRS.md：FR-020、FR-021、FR-026、FR-027、EF-002、EC-001～EC-011；
- 03-SYSTEM-ARCHITECTURE.md：§10；
- 04-DOMAIN-MODEL.md：Calendar & Time Context；
- docs/adr/M2-DOMAIN-DECISIONS.md：ADR-CAND-M2-001～009；
- docs/M3-CALENDAR-TIME-ENGINE.md。
