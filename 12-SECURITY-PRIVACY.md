# AI 八字命理分析平台：安全与隐私架构

**文档编号：** 12  
**文档类型：** Security & Privacy Architecture  
**文档状态：** Review  
**当前版本：** 0.9  
**上游基线：** `01-PRODUCT-VISION.md`、`02-SRS.md`、`03-SYSTEM-ARCHITECTURE.md`、`04-DOMAIN-MODEL.md` 1.0、`05-DATA-MODEL.md` 1.0、`06-ROADMAP.md` 1.0、`07-APPLICATION-ARCHITECTURE.md` 1.0、`08-API-DESIGN.md` 1.0、`09-TECHNOLOGY-ARCHITECTURE.md` 1.0、`10-IMPLEMENTATION-GUIDE.md` 1.0、`11-DEPLOYMENT-OPERATIONS.md` 1.0（均已 Approved）  
**目标读者：** CTO、产品与安全负责人、隐私与法律负责人、领域/数据/API/技术架构师、研发与测试、平台工程、运维、审计及事件响应人员

---

## Version 0.9 Change Log

- 首次定义 Identity、Authentication、Authorization、RBAC、ABAC、Session 与 Token 安全架构。
- 定义 API、Transport、数据分类、加密、Key、Secret、PII、Masking 和 Consent 架构。
- 定义 Retention、Export、Deletion、Audit、Threat Modeling、AI Security 和 Prompt Injection 防护。
- 定义 Supply Chain、Dependency、Vulnerability、Monitoring、Incident、Compliance、安全与隐私治理。
- 本文件不包含任何代码、IAM/WAF/OAuth/JWT 配置、云资源或执行脚本。

---

## 1. Document Purpose

### 1.1 目标

本文档定义 AI 八字命理分析平台如何识别主体、验证身份、授权访问、保护敏感出生资料和派生内容、约束第三方 AI、响应威胁，并在数据全生命周期内落实 Privacy by Design。

安全目标不是“隐藏实现细节”，而是通过明确身份、最小权限、分层防御、可审计决定、不可变历史和可验证删除，降低未经授权访问、数据泄露、模型滥用、内容风险和供应链风险。

### 1.2 适用范围

本文覆盖：

- 用户、管理员、DeveloperClient、Workload 和匿名会话身份；
- Authentication、RBAC/ABAC、Session、Token 和 API Security；
- 数据分类、加密、Key/Secret、PII、Masking、Consent 和 Retention；
- Data Export、Deletion、Legal Hold、Audit 与不可抵赖性支持；
- Threat Modeling、AI Security、Prompt Injection、Jailbreak 和输出验证；
- Supply Chain、Dependency、Vulnerability、Security Monitoring 和 Incident；
- Security Governance、Privacy Governance 和合规评审输入。

### 1.3 不包含内容

本文不包含：

- Python、TypeScript、SQL、FastAPI 或 Next.js 代码；
- JWT、OAuth、IAM、WAF、KMS、Secret Manager 或云配置；
- Docker、Kubernetes、Terraform、CI/CD 或部署脚本；
- 具体加密算法、密钥长度、Token 字段或协议 Payload；
- OpenAPI、Controller、DTO、数据库表或 Policy-as-Code；
- 对法律适用性的最终意见；
- Domain、Aggregate、Entity、Value Object、Domain Event、API、Data 或 Technology Baseline 变更；
- 进入编码阶段的授权。

### 1.4 Security and Privacy Boundary

安全与隐私架构决定“谁可以在何种目的、条件和期限内做什么”，但不决定命理事实、规则结论或 AI 是否科学准确。安全工具不得直接修改 Aggregate 或把安全判定写成新的领域状态。

### 1.5 Conflict Handling

若安全/隐私要求需要改变已批准的 Context、Aggregate、Data Model、Application Flow、API Contract、Technology 或 Engineering Baseline，只登记 `ADR Candidate` 或 `Open Question`。需要立即降低风险时，优先关闭能力、缩小数据或阻断发布，而不是未经批准改写基线。

### 1.6 Legal Disclaimer

本文件是架构与治理输入，不构成法律意见。正式上线前必须由目标地区合格法律与隐私专家确认适用法律、敏感个人信息、同意、影响评估、备案/安全评估、跨境、内容标识、事件通知、保留和未成年人边界。

---

## 2. Security Principles

### SEC-P-001 Zero Trust

不因网络位置、登录状态、管理员身份或内部服务而自动信任。每次访问根据 Actor、Client、Resource、Purpose、Scope、环境和风险验证。

### SEC-P-002 Least Privilege

权限只覆盖完成当前任务所需资源、动作、数据字段、环境和时间；不使用默认全能角色。

### SEC-P-003 Defense in Depth

Edge、Identity、Authorization、Application、Data、Runtime、Observability 和 Operations 多层控制，任一层失效不应直接暴露正式数据。

### SEC-P-004 Secure by Default

资源、对象、日志、接口、管理操作和第三方传输默认拒绝；必须显式满足授权条件才能开放。

### SEC-P-005 Strong Identity

高权限人员、Workload、DeveloperClient 与普通用户身份分离。共享账户、共享生产凭据和身份冒用禁止。

### SEC-P-006 Server-Side Enforcement

所有关键授权、输入、状态和风险判断在服务端执行。前端隐藏、不可猜 ID 或网络位置不是安全边界。

### SEC-P-007 Minimize Secrets and Trust

减少长期 Credential、静态 Key 和信任关系；使用短期、可轮换、可撤销的身份与 Secret。

### SEC-P-008 Fail Securely

认证、授权、Consent、Audit、Key 或风险检查失败时拒绝或降级，不默认放行，不把失败伪装为成功。

### SEC-P-009 Explicit Boundaries

Identity、Birth、Chart、AI、Audit、Vendor、Environment 和 Tenant 之间有明确隔离；Context 间只传稳定 Identity、Snapshot 或批准 Event。

### SEC-P-010 Verifiable Controls

关键安全要求有测试、Metric、Audit、Runbook 和 Owner；只有文档声明而不可验证的控制不视为完成。

### SEC-P-011 Assume Breach

设计考虑 Credential、Provider、Client 或单层控制可能失陷，通过最小权限、分段、检测和快速撤销限制影响。

### SEC-P-012 No Security Through Obscurity

不依赖私有 URL、隐藏字段、未公开算法或 Prompt 保密作为唯一防护。安全来自认证、授权、加密和验证。

### SEC-P-013 Immutable Security History

安全事件、授权变化、Consent、发布、删除和敏感访问保留可追踪记录；Correction 追加而不覆盖历史。

### SEC-P-014 Governed Change

Authentication、Authorization、Token、Encryption、Key、Audit、AI Security 和 Monitoring 重大变化先走 ADR 与安全评审。

---

## 3. Privacy Principles

### PRI-P-001 Privacy by Design and Default

从产品、领域、数据、API、技术到运维默认采用更少收集、更少共享、更短保留和更严格访问。

### PRI-P-002 Purpose Limitation

每次处理绑定明确 Purpose。排盘服务、AI 解读、命例优化、研究、支持、审计和法律保留不能相互默认授权。

### PRI-P-003 Data Minimization

不默认收集姓名和详细地址，只处理计算与服务必需信息。第三方 AI 只接收去标识化命盘事实、Evidence 和必要 Scope。

### PRI-P-004 Transparency

用户清楚知道收集什么、为何处理、是否保存、是否使用第三方 AI、如何撤回、导出和删除，以及输入不确定性如何影响结果。

### PRI-P-005 User Control

匿名试算、保存、命例优化、研究和分享具有清晰控制；可选授权拒绝不影响基础服务。

### PRI-P-006 Consent Integrity

Consent 明确、可证明、按 Purpose/Scope/Policy 管理；撤回与授予同样容易，不用暗示或捆绑取得。

### PRI-P-007 Storage Limitation

数据按类别、目的和法律要求配置保留，不因为存储便宜无限保存。匿名数据默认不长期保存。

### PRI-P-008 Accuracy and Uncertainty

用户输入按原精度保存，不擅自补全。更正通过新输入/版本表达，不静默改写 Frozen 历史。

### PRI-P-009 Separation and Pseudonymization

Identity 与传统算法参数分离；跨系统使用目的限定的假名/一次性分析标识，避免第三方直接关联平台用户。

### PRI-P-010 Data Subject Rights

访问、导出、更正、删除、撤回和投诉由可追踪流程支持；Partial、Legal Hold 和 Backup Expiry 不伪报完成。

### PRI-P-011 Privacy Accountability

处理活动、数据流、供应商、影响评估、Consent、Retention、访问和事件有 Owner、记录与复审。

### PRI-P-012 No Accuracy Marketing from Personal Data

不得以未经科学验证的“预测准确率”诱导用户提供更多敏感信息或贡献命例。

---

## 4. Identity Architecture

### 4.1 Identity Types

| Identity | Represents | Security Boundary |
|---|---|---|
| UserId | 注册账户主体 | 不含地区、时间或业务语义 |
| Anonymous Session Identity | 受限匿名试算会话 | 短期、不可访问注册资源 |
| SubjectId | 数据所涉及的自然人/主体 | 与 Actor 可不同，需授权关系 |
| Actor Identity | 当前执行动作的人或系统 | 用于授权与 Audit |
| Client/Tenant Identity | V2 DeveloperClient/租户 | Scope、Quota、数据隔离 |
| Workload Identity | API、Worker、Scheduler 等运行单元 | 不冒充 User；最小机器权限 |
| Support/Admin Identity | 内部受控人员 | 强认证、JIT、Purpose、Audit |
| External Provider Identity | AI、地点、通知等供应商调用方/接收方 | Adapter、Credential、数据最小化 |

### 4.2 Separation of Identity and Birth Data

账户身份、认证渠道、Credential 与 BirthProfile/BirthInput 分离存储和授权。第三方 AI、Search、Cache、Log 和 Message 不使用 UserId 作为不必要关联键。

### 4.3 Identity Proofing

不同用例需要不同身份保证：匿名试算最低、常规账户中等、导出/删除/恢复/高权限操作更强。具体核验方式与保证等级待产品、安全和法律确认。

### 4.4 Actor and Subject

Actor 不一定等于 Subject。保存他人命盘、法定代理、支持调查或企业 Client 访问时，必须有明确关系、Purpose、Scope、期限和 Audit。不能因为 Actor 拥有账户就默认可处理任意 Subject 数据。

### 4.5 Workload Identity

- 每个 Runtime/Service Role 使用独立 Workload Identity。
- 按环境和能力授权，不共享生产 Credential。
- API 与 Worker 只能访问其用例所需资源。
- Workload 权限变化、使用和异常访问可观察。

### 4.6 Identity Lifecycle

Create/Verify → Active → Restricted/Suspended → Recovery → Deactivated/Deleted。该安全生命周期不能重定义 User Aggregate；具体业务状态仍由 Identity Context 管理。

### 4.7 Account Enumeration Protection

注册、登录、恢复、授权和对象访问对外使用一致安全响应，避免泄露账户或资源存在性；内部保留真实拒绝原因与安全事件。

---

## 5. Authentication Model

### 5.1 Authentication Surfaces

| Surface | Authentication Direction | Additional Controls |
|---|---|---|
| Anonymous Trial | 受限、短期、设备/风险辅助会话 | Rate Limit、无长期保存默认 |
| Registered User | 安全用户会话 | Session Rotation、Recovery、Risk Detection |
| Privileged Staff | 强认证 | MFA、JIT、Re-authentication、Audit |
| DeveloperClient V2 | 受控 Client Credential | Scope、Tenant、Rotation、Quota |
| Workload | Workload Identity / 短期机器 Credential | Environment、Audience、Least Privilege |
| Webhook/Callback | 独立完整性与接收身份 | Replay Protection、Target Registration |

### 5.2 Authentication Requirements

- Credential 不出现在 URI、日志、Report、Error 或普通配置。
- 登录和恢复防暴力尝试、Credential Stuffing、Session Fixation 和账户枚举。
- 身份验证成功后仍需 Authorization。
- 新设备、异常位置、Credential 变更和高风险操作可触发 Step-Up。
- 用户退出、密码/认证因子变更和安全事件使相关 Session 失效。

### 5.3 MFA

- 高权限 Staff 和 Break-Glass 必须使用 MFA。
- Developer/Operations 高风险 Credential 管理需强认证与 MFA。
- 普通用户 MFA 是否强制或可选待产品与风险评估。
- 恢复流程不得弱于 MFA，否则形成绕过。
- MFA 因子、备用码和恢复材料按 Secret/敏感数据保护。

### 5.4 Authentication Protocol Boundary

具体用户认证协议、联合身份、Passwordless、OAuth/OIDC 等选型尚未批准。架构要求标准兼容、可撤销、Audience/Issuer 验证、短期 Credential 和安全恢复；选型需 ADR。

### 5.5 Re-Authentication

Data Export/Delete、Credential/Consent 高风险变更、管理员敏感访问、发布、Secret 和 Break-Glass 需要近期强认证或 Step-Up。有效 Session 不自动满足所有高风险操作。

### 5.6 Recovery

账户恢复使用多信号、速率限制、通知、冷却或人工复核（按风险），不泄露原认证材料。恢复完成撤销旧 Session/Token 并审计。

### 5.7 Authentication Events

成功/失败、MFA、Recovery、Session Revocation、Credential Create/Rotate/Revoke、异常和 Lockout 产生安全记录；不记录 Password、Token 或完整因子。

---

## 6. Authorization Model

### 6.1 Decision Formula

授权决策为多条件合取：Authenticated/Allowed Anonymous Capability + RBAC Permission + Resource Ownership/Delegation + ABAC Conditions + Purpose + Consent + Resource State + Environment/Risk。任一必需条件失败即拒绝。

### 6.2 Decision Context

| Attribute Group | Examples |
|---|---|
| Actor | User/Staff/Client/Workload Identity、Role、Assurance |
| Subject | SubjectId、Actor-Subject Relationship |
| Resource | Context、Owner、Classification、Lifecycle、Tenant |
| Action | Read、Create、Manage、Publish、Export、Delete、Audit |
| Purpose | Core Service、Support、Security、Research、Optimization |
| Consent | Current Decision、PolicyReference、Scope、Revoked |
| Environment | Production/Staging、Network/Device/Risk |
| Governance | Ticket、Approval、Time Limit、Legal Hold |

### 6.3 Enforcement Points

- Edge/API：基础认证、Rate Limit、Route Scope；
- Interface：建立可信 ActorContext；
- Application Service：最终用例授权、Purpose、Consent、Ownership；
- Repository/Query：数据域和 Tenant 过滤、防止越权枚举；
- Object/Search/Cache：再次执行资源与字段级边界；
- Operations：JIT、MFA、Session Audit。

### 6.4 Default Deny

未知 Role、Scope、Purpose、Resource State、Consent 或 Policy Version 默认拒绝。配置/Policy 加载失败不得回退到允许。

### 6.5 Resource Ownership

User 只能访问本人或明确获授权资源。Chart 权限不自动授予关联 Subject 的其他 Chart；Report 分享不授予 BirthInput 或 Conversation 权限。

### 6.6 Cross-Context Authorization

调用方 Context 不能代替目标 Context 最终授权。跨 Context 只传最小、可验证的 Actor/Purpose/Correlation，目标 Application Service 重新检查。

### 6.7 Field-Level Authorization

专业参数、Evidence、知识正文、Support 数据、Audit 和安全信息按 Role/Purpose/Classification 过滤。字段缺失可能表示 Masking，不向客户端暴露内部策略。

### 6.8 Authorization Caching

只缓存短期辅助决策，Key 包含 Subject/Actor/Policy/Resource/Version。Consent/Role 撤回主动失效并短 TTL；高风险操作查询权威状态。

---

## 7. RBAC Strategy

### 7.1 Role Purpose

RBAC 定义“某类 Actor 可以尝试哪些动作”，不单独决定具体资源访问。

### 7.2 Approved Role Families

| Role Family | Allowed Direction | Mandatory Restrictions |
|---|---|---|
| Anonymous | 受限试算与公开内容 | 无注册资源、短期、Rate Limit |
| RegisteredUser | 本人 Chart/Report/Conversation/Consent/Data Rights | Ownership、Purpose、Consent |
| ProfessionalUser | 展开批准专业参数/依据 | 不获得他人数据或治理权限 |
| ContentEditor | 创建知识/术语/Prompt Draft | 不可自行 Published |
| DomainExpert | 审核命理规则/内容 | 不自动获得生产发布/用户数据 |
| Reviewer/Publisher | 独立审核与发布 | 职责分离、MFA、Audit |
| SupportAgent | 处理批准工单 | JIT、Masking、Purpose、限时 |
| Administrator | 受控平台管理 | 非全局数据所有者、最小权限 |
| Auditor | 只读调查 Audit/Version | 不修改业务数据 |
| DeveloperClient | V2 Scope 内 API | Tenant、Quota、Credential、Version |
| Security/Operations | 安全与运行处置 | JIT、MFA、Break-Glass、Audit |

具体 Role 名称与权限矩阵需与 SRS 最终 Role Catalog 对齐；本文不新增 Domain Role Entity。

### 7.3 Role Hierarchy

不默认采用“管理员继承所有角色”。角色组合显式评估，避免隐式权限膨胀。高风险发布、Audit、Security 和 Support 保持职责分离。

### 7.4 Role Assignment

角色授予有申请、批准、范围、环境、期限、Owner 和 Audit。Privileged Role 定期复审；无 Owner、无使用或过期角色撤销。

### 7.5 Separation of Duties

- Draft 创建与高风险 Published 分离；
- Secret/Access 申请与批准分离；
- Audit 调查与源数据修改分离；
- Backup 管理与 Restore/Production 激活分离（按风险）；
- Emergency Break-Glass 使用与事后 Review 分离。

### 7.6 Role Testing

每个 Role 执行 Allow/Deny、Cross-User、Cross-Tenant、Field Mask、Expired/JIT、Consent 和 State 测试。新增权限默认阻断直到测试和审批完成。

---

## 8. ABAC Strategy

### 8.1 ABAC Purpose

ABAC 在 RBAC 基础上处理资源、主体、目的、环境和风险上下文，避免为每个条件创建角色。

### 8.2 Attribute Sources

| Attribute | Authoritative Source |
|---|---|
| Actor/Role/Assurance | Identity/Security Context |
| Subject/Ownership | Resource-owning Context |
| Consent/Purpose | SubjectConsent Aggregate / Policy Catalog |
| Resource State/Classification | Owning Aggregate/Approved Metadata |
| Tenant/Client Scope | Identity/API Credential Governance |
| Ticket/Approval/Expiry | Governance/Operations System |
| Legal Hold | Approved Data Governance Record |
| Risk Signal | Security Risk Engine/Policy |

### 8.3 Policy Rules

- Policy 使用稳定、版本化术语和明确 Owner。
- 未知/缺失 Attribute 默认拒绝。
- Policy Decision 与执行分离；Application 仍验证领域状态。
- 高风险 Policy 变化经过双人 Review、测试、Canary 和 Audit。
- 不允许客户端自报 Role、Ownership、Consent 或 Risk 作为权威。

### 8.4 Contextual Conditions

支持时间限制、环境、网络/设备风险、Purpose、Ticket、Field View、Operation State 和 Legal Hold。不得使用未经审查的敏感推断属性进行歧视性授权。

### 8.5 Policy Decision Logging

记录 Policy Version、Decision、Reason Code、Actor/Resource 安全引用和 Correlation，不记录完整敏感 Attribute。拒绝记录用于安全调查但防止账户枚举。

### 8.6 Policy Testing

使用决策表覆盖 Allow/Deny、属性缺失、撤回、冲突、时间边界、跨 Tenant 和 Policy Version。策略改变执行回归与影响分析。

### 8.7 RBAC + ABAC Boundary

RBAC 决定动作类别，ABAC/Ownership/Purpose/Consent 决定具体请求。两者均不能绕过 Aggregate 不变量或 API Contract。

---

## 9. Session Management

### 9.1 Session Types

| Session | Scope | Lifetime Direction |
|---|---|---|
| Anonymous Trial | 单次/短期试算 | 短、最小状态、默认不长期保存 |
| User Browser | 第一方 Web | 受控 Idle/Absolute Timeout |
| Privileged Staff | Governance/Support/Operations | 更短、MFA、JIT、Re-auth |
| Developer Console | Credential 管理/Usage | 强认证、独立于 API Credential |

### 9.2 Session Properties

- 高熵、不透明、Secure/HttpOnly/SameSite 等浏览器安全方向；具体配置后续实现。
- 登录、Privilege Change、MFA、Recovery 后 Session Identifier 轮换。
- Session 只存必要安全状态，不存完整 Birth/Report/Prompt。
- Server 端可撤销、可列出活动 Session（如产品批准）并审计。

### 9.3 Expiration

Idle Timeout、Absolute Lifetime、Remembered Device 和 Re-auth Window 按风险分层，具体数值为 Open Question。Privileged Session 不使用长期“记住登录”默认。

### 9.4 Revocation

Logout、Password/Factor Change、Account Suspend/Delete、Credential Compromise、Role/Consent 高风险变化和 Security Incident 触发相关 Session 撤销。撤销传播有 SLO 候选，待安全评审。

### 9.5 Session Fixation and Hijacking

登录前后轮换、Cookie 安全、CSRF、防 XSS、异常检测、并发 Session Policy 和高风险 Step-Up 共同防护。不得把 IP 作为唯一身份绑定。

### 9.6 Anonymous Upgrade

匿名升级注册时明确选择哪些数据保存、绑定哪个 Subject 和 Purpose；不自动扩大 Retention 或 Optimization Consent。

### 9.7 Session Audit

记录创建、认证强度、轮换、撤销、异常和高风险操作，不记录原 Session Secret。

---

## 10. Token Lifecycle

### 10.1 Token Categories

Access Token、Refresh/Session Token、API Credential、Workload Token、Share Credential、Webhook Secret 和 Password Reset Token 相互分离，不能跨用途复用。

### 10.2 General Lifecycle

Issue → Validate → Use → Rotate/Renew → Revoke/Expire → Audit/Retire。每类 Token 有 Issuer、Audience、Subject/Client、Scope、Lifetime、Key Version 和 Revocation 策略。

### 10.3 JWT Principles

若采用 JWT：

- Access JWT 短生命周期，并严格验证签名、Issuer、Audience、Expiry/Not-Before、Algorithm Policy 和 Key Identifier；
- Claims 最小化，不包含 BirthInput、姓名、详细地址、Consent 细节、Prompt 或其他敏感正文；
- JWT 不是实时授权 Source of Truth，高风险操作查询 Role/Consent/Resource 权威状态；
- 不接受无签名、弱/错误算法或由客户端决定验证算法；
- Key Rotation 支持受控重叠和旧 Key 退役；
- Token 泄漏通过短生命周期、Revocation/Session Version、Risk Control 和 Scope 限制影响。

是否采用 JWT、Opaque Token 或混合模式必须通过 ADR。

### 10.4 Refresh Token

Refresh Token 更严格保存、轮换并检测重用；每次使用可发行新 Token 并撤销旧 Token Family。异常重用触发 Session Family 撤销和安全事件。

### 10.5 API Credential

V2 API Credential 仅保存不可逆摘要或受控材料，绑定 Client/Tenant、Scope、Environment、Status 和 Rotation。不得在 Browser、URI 或日志公开。

### 10.6 Workload Token

使用短期、Audience 限定的 Workload Identity，避免长期静态机器 Key。Workload 不以 User Token 执行后台管理。

### 10.7 Share and Reset Tokens

Share/Reset Token 单用途、短期、可撤销、不可枚举，使用后按策略失效。Share 只授予 Frozen Report 等明确资源，不授予关联 Birth/Conversation。

### 10.8 Token Storage

Browser、Server、CI/CD、Mobile（未来）使用各自安全存储方向。Token 不进入 Local Storage 的默认决定需结合认证协议评审；任何选择必须防 XSS/CSRF 并有 ADR。

---

## 11. API Security

### 11.1 Security Controls

| Control | Purpose |
|---|---|
| Authentication | 验证 User/Client/Workload |
| Authorization | Role、Scope、Ownership、Purpose、Consent、State |
| Rate Limiting | 防暴力、枚举、滥用、容量和 AI 成本 |
| WAF | 常见攻击、异常 Payload、Bot 与 DDoS 辅助防护 |
| Schema/Size Validation | 拒绝畸形、过大和未知输入 |
| Idempotency | 防重复正式对象和副作用 |
| Error Safety | 不泄露 Stack、SQL、Provider Raw 或资源存在性 |
| Audit/Trace | 关键调用可追踪且去敏 |

### 11.2 Rate Limiting

Edge 粗粒度 + Application 细粒度，按 IP 风险、Anonymous Session、User、Client、Tenant、Credential、Endpoint、Operation、AI 成本和并发组合。Redis 失败时保守化，不无限开放。

### 11.3 WAF Principles

- 作为 Defense in Depth，不替代安全编码/授权。
- 规则先观察/测试再阻断，避免大面积误伤。
- 保护登录、恢复、Export/Delete、Webhook 和高成本 AI Endpoint。
- WAF Event 去敏并有 Owner/Runbook。
- 本文件不生成 WAF 配置。

### 11.4 CSRF

使用 Cookie/Browser Session 的状态变更请求必须有 CSRF 防护、SameSite 策略、Origin/Referer 验证方向和不可预测 Token/等价机制。GET/Query 无副作用。

### 11.5 XSS

所有 User/AI/Knowledge 内容视为不可信：上下文输出编码、安全渲染、CSP、禁止不受控 HTML/Script、URL Sanitization。AI 生成 Markdown/链接不能绕过渲染边界。

### 11.6 SSRF

Webhook/Callback、File Import、Image/Link、AI Tool 和 Provider URL 使用预登记/Allowlist、DNS/IP 复核、Redirect 限制、私网/Metadata 阻断、Egress Control 和响应大小/超时。

### 11.7 SQL Injection

使用参数化数据访问、ORM/Query Adapter 边界、输入白名单和最小数据库权限。客户端不能提交数据库字段名、任意表达式或 SQL。WAF 不是唯一防护。

### 11.8 IDOR / Object Authorization

每个 Resource Identity 在服务端验证 Ownership/Tenant/Scope。列表在数据源端授权过滤；无权对象采用统一 403/404 防枚举策略。

### 11.9 Mass Assignment

API 只接受用例允许意图，不把任意客户端字段自动绑定 Aggregate/ORM。Client 不能直接设置 Owner、Role、Published、Frozen、Completed 或 Consent 历史。

### 11.10 File Upload

若 V1/V2 开放上传，限制类型、大小、数量，隔离扫描、内容探测、安全重命名和受控渲染。未通过检查不能进入 Knowledge/Report。

### 11.11 CORS and Headers

CORS 默认拒绝未知 Origin；安全 Header、Cache-Control、Content-Type、Referrer 与下载策略继承 API Design。具体配置待实现评审。

---

## 12. Transport Security

### 12.1 Encryption in Transit

所有外部和敏感内部通信使用行业通行的安全传输协议。禁止明文传输 Credential、Birth、Chart、Conversation、Report、Audit 或 Secret。

### 12.2 TLS Principles

- 只允许受支持协议/密码套件方向，具体版本由安全标准维护；
- 证书可信、自动到期监控和轮换；
- HSTS 在完整域名/HTTPS 治理后启用；
- 禁止跳过证书验证；
- 内部服务按风险使用双向身份或 Workload Identity。

### 12.3 Certificate Lifecycle

Issue、Inventory、Renew、Revoke、Expire、Incident 有 Owner、自动监控和 Break-Glass。证书私钥进入 Key/Secret Management，不进入源码或镜像。

### 12.4 External Provider

验证 Provider Host、Certificate、Endpoint 和 Egress；不跟随任意 Redirect。传输安全不代表 Provider 可以接收更多数据，仍需最小化和合同控制。

### 12.5 Internal Network

私有网络不是信任充分条件。API、Worker、Database、Redis、Broker、Object 和 Observability 使用最小网络路径、认证与授权。

---

## 13. Data Classification

### 13.1 Classification Levels

| Level | Definition | Examples | Default Controls |
|---|---|---|---|
| Public | 批准公开，泄露无实质个人风险 | 公共产品说明、已批准公开知识摘要 | 完整性、发布审核 |
| Internal | 仅组织内部，泄露影响有限 | 聚合运营指标、一般工程文档 | 认证、最小访问 |
| Confidential | 商业/技术/用户相关，泄露有明显影响 | 未发布规则、供应商合同、去标识化分析集 | 加密、Role/Purpose、审计 |
| Restricted Sensitive | 个人敏感或高风险组合数据 | BirthInput、Chart、Conversation、Report、Consent、Support、Audit | 强加密、最小字段、JIT/Mask、严格保留 |
| Critical Security | 可直接取得高权限或破坏保护 | Secret、Key、Token、Break-Glass、签名材料 | 专用管理、MFA、短期、实时告警 |

### 13.2 Conservative Classification

出生日期、时间、地点及其派生命盘/报告虽然法律分类需专业确认，但因组合可识别性、信仰/偏好推断和用户期待，工程上默认按 `Restricted Sensitive` 保护。

### 13.3 Data Object Mapping

| Object / Data | Classification Direction |
|---|---|
| User Auth/Credential | Restricted / Critical Security |
| BirthProfile/BirthInput | Restricted Sensitive |
| Chart/CalculationSnapshot | Restricted Sensitive |
| RuleSet Published Definition | Internal/Confidential；公开部分另行批准 |
| RuleRun/EvidenceBundle | Restricted Sensitive when linked to Subject |
| KnowledgeArticle | Public/Internal/Confidential by Rights/State |
| AIAnalysis/Conversation/Message | Restricted Sensitive |
| Timeline/Report | Restricted Sensitive |
| ConsentRecord/Data Rights | Restricted Sensitive |
| Audit/Security Event | Restricted Sensitive |
| Aggregated De-identified Metric | Internal；重识别风险复审 |
| Secret/Key/Token | Critical Security |

### 13.4 Classification Metadata

数据对象/流具有 Classification、Owner、Purpose、Retention、Region、Legal Hold、Masking 和 Allowed Recipient 元数据。分类变化走 Data/Security Review。

### 13.5 Aggregation and Inference

多个低敏感字段组合可能提升等级。去标识化数据与辅助数据结合可重识别时，按更高等级处理。

### 13.6 Handling Rules

Classification 决定收集、显示、Cache、Log、Export、Backup、Provider、环境和删除控制。未知分类默认按较高等级保护，直到 Owner 确认。

---

## 14. Data Encryption

### 14.1 Encryption at Rest

PostgreSQL、Backup、Object Storage、Log/Audit、Search/Vector 和必要临时制品使用受控静态加密。平台/磁盘加密是基础，Restricted Sensitive 字段是否额外字段级/应用级加密按 Threat Model 决定。

### 14.2 Encryption in Transit

继承 Transport Security：外部、跨网络边界和敏感内部通信全程加密，禁止跳过验证。

### 14.3 Field-Level Protection

候选对象包括认证材料、BirthInput 的高敏感字段、Support/Legal Note 和 Provider Mapping。具体字段、查询影响、Key Rotation、Backup/Restore 和删除语义需 ADR 与性能验证。

### 14.4 Envelope Encryption

采用数据加密 Key 与主 Key/Key Encryption Key 分离的方向，便于轮换和最小权限。本文不规定具体算法或实现。

### 14.5 Context Separation

Identity 与 Birth/Analysis 可使用不同 Key Domain/访问策略，降低单一权限暴露完整用户画像。Environment、Region 和数据类别 Key 不复用。

### 14.6 Integrity

Frozen Report、Object、Backup、Audit 和发布制品需要 Hash/签名/完整性证据（按对象适用）。加密保密性不能替代完整性验证。

### 14.7 Encryption Limitations

加密不替代授权、最小化、Masking、Retention 或安全执行。应用读取后的明文仍需内存、日志、Trace 和第三方传输保护。

---

## 15. Key Management

### 15.1 Key Hierarchy

Key Management 使用专用 KMS/HSM-compatible 边界方向。主 Key、Data Key、Signing Key、Token Key、Webhook Key 和 Certificate Key 按用途分离。

### 15.2 Key Lifecycle

Generate → Activate → Use → Rotate → Deactivate → Revoke/Destroy → Audit。每个 Key 有 Owner、Purpose、Environment、Version、Status 和影响清单。

### 15.3 Key Rotation

- 定期与事件驱动轮换；
- 新写使用新 Key，旧 Key 在受控窗口仅用于读取/验证；
- 验证所有 Consumer/Backup/Restore 兼容；
- Rotation 失败不静默回退到不安全 Key；
- 具体周期待安全评审。

### 15.4 Access Control

Workload 只获 Encrypt/Decrypt/Sign/Verify 中所需动作，不获导出主 Key。人员使用 JIT、MFA、双人（高风险）和 Audit。

### 15.5 Key Backup and Recovery

验证 KMS 故障、Region/Account 恢复、Key Version 与 Backup Restore。不能因 Key 丢失导致合法历史永久不可读，也不能用恢复让已删除数据重新可见。

### 15.6 Compromise

疑似 Key 泄漏立即限制使用、轮换/撤销、评估受影响数据/Token/Artifact，并启动 Security Incident。销毁 Key 前验证 Legal Hold、Backup 和业务可读性。

### 15.7 Separation of Duties

Key Administrator、Application Operator、Security Auditor 和 Data User 权限分离。Break-Glass 有实时告警和事后 Review。

---

## 16. Secret Management

### 16.1 Secret Types

Database/Broker/Redis/Object Credential、AI/Location/Notification API Key、Webhook Secret、Certificate Private Key、Signing Material、CI/CD Credential 和 Break-Glass Material。

### 16.2 Storage

Secret 只存专用 Secret Management/KMS 能力，不进入源码、普通配置、数据库普通字段、镜像、日志、Report、工单或聊天。

### 16.3 Delivery

Workload 通过身份在运行时获取或安全注入，按 Environment/Service/Purpose 最小授权。不由人员复制到本地文件或共享频道。

### 16.4 Secret Rotation

支持受控双 Key 重叠、依赖健康验证、旧 Secret 撤销和失败回退。高风险 Secret 设最大寿命，具体值待批准。

### 16.5 Secret Detection

Source、Commit、Build、Artifact、Log 和 Ticket 持续扫描。命中按真实泄漏处理，不能仅删除文本；需撤销/轮换并评估使用。

### 16.6 Shared Secret Prohibition

禁止跨人员、环境、服务或供应商项目共享生产 Credential。无法区分调用方的 Secret 不适合作为长期关键认证方式。

### 16.7 Break-Glass Secret

离线/受控保存、双人获取、短期启用、实时告警、使用后轮换。不得被日常自动化依赖。

---

## 17. PII Protection

### 17.1 Terminology

`PII` 在本文作为工程总称；正式法律分类使用目标地区适用概念（个人信息、敏感个人信息等）并由法律顾问确认。

### 17.2 Collection Minimization

- 不默认收集姓名和详细地址；
- 地点优先保存计算所需标准化引用/精度；
- 不收集无关联系方式、职业、健康或家庭详情；
- 自由文本限制用途、长度与敏感提示；
- 匿名试算数据默认不长期保存。

### 17.3 Pseudonymization

内部用稳定但不含业务意义的 Identity；第三方 AI 使用一次性 Analysis Identity，移除 UserId、姓名、联系方式、详细地址、Support Ticket 和无关标签。

### 17.4 De-identification

去标识化不仅删除姓名，还评估 Birth 时间/地点、稀有组合、Free Text、Conversation 和外部数据重识别。研究/优化数据建立独立批准流程和重识别风险评估。

### 17.5 Data Flow Inventory

维护 Collection → Normalize → Chart → Rule/Evidence → AI → Report/Conversation → Log/Metric → Export/Delete 的字段级数据流、Purpose、Recipient、Region、Retention 和 Control。

### 17.6 Third-Party Processing

供应商只接收最小字段，合同限制用途、留存、训练、子处理者、地区、删除、Incident 通知和审计。技术上通过 Model Gateway、Redaction 和 Payload Review 执行。

### 17.7 Support and Operations

Support 默认看 Masked View，JIT/Purpose/工单后按最小范围解锁。Operations 使用 Identity/Correlation 排障，不浏览正文。

### 17.8 Re-identification Prohibition

未经批准不得将去标识化数据与 Identity、外部资料或其他命例重连。研究结果输出需防小样本和唯一组合泄漏。

---

## 18. Data Masking

### 18.1 Masking Views

| View | Default Visibility |
|---|---|
| End User | 本人资源与必要事实 |
| Professional User | 批准参数/Evidence，仍不见其他主体 |
| Support | 最小账户/状态，Birth/Conversation 默认遮蔽 |
| Operations | Resource/Correlation/State，无业务正文 |
| Auditor | Actor/Action/Result/Version，正文最小 |
| DeveloperClient | Scope/Tenant 允许字段 |
| Analytics | 聚合/去标识化，防小样本 |

### 18.2 Masking Techniques

隐藏、部分显示、Tokenization/Pseudonymization、聚合、泛化时间/地点、摘要、Hash 和字段移除。Hash 不自动等于匿名化。

### 18.3 Dynamic Masking

Masking 根据 Role、Purpose、Resource、Ticket 和 Environment 决定。客户端参数不能关闭。Query、Export、Log、Search 和 Cache 分别执行。

### 18.4 Unmasking

需要强身份、JIT、Purpose、Reason、最小字段、时限和 Audit。批量 Unmask 需要更高级批准和安全监控。

### 18.5 Screenshots and Downloads

用户打印/下载前提示隐私风险；Support/Operations 页面可采用防误复制、水印/标识或禁止导出方向，具体 UX 待产品确认。

### 18.6 Testing

覆盖 Role/Scope、字段、列表、Search、Cache、Error、Log、Export、Screenshot 和前端 Bundle，确保 Masking 不只存在 UI。

---

## 19. Consent Management

### 19.1 Domain Alignment

继承 Approved Domain Model：`SubjectConsent` 为 Aggregate Root，`ConsentRecord` 为内部追加式 Entity；同一 Subject、Purpose、Scope 在同一时刻只有一个有效决定视图。

### 19.2 Consent Dimensions

| Dimension | Meaning |
|---|---|
| SubjectId | 授权所涉及主体 |
| Purpose | 明确处理目的 |
| Scope | 数据类别、功能、Recipient/Region |
| Decision | Granted、Declined、Revoked 等批准语义 |
| PolicyReference | 用户看到的政策/告知版本 |
| Timestamp / Actor | 决定时间和操作主体 |
| Evidence | 展示、交互、语言和合法性记录 |

### 19.3 Purpose Catalog

至少区分核心排盘服务、第三方 AI 处理、账户保存、命例优化、研究、分享/导出和支持调查。哪些属于 Consent、合同必要、法定义务或其他处理基础由法律评审确认；工程上都需 Purpose 和记录。

### 19.4 Consent UX

- 简明、分层、清晰语言；
- 可选用途不预选、不捆绑、不用 Dark Pattern；
- 拒绝命例优化/研究不降低基础服务；
- 说明第三方 AI、保存和匿名试算差异；
- 记录语言、Policy Version 和交互证据。

### 19.5 Withdrawal

撤回与授予同样易操作。撤回立即阻止新可选处理，并通过 Saga 评估在途 AI、Research、Feedback、Index、Cache 和 Vendor。合法历史/Audit 不被改写。

### 19.6 Consent Propagation

Source of Truth 在 Consent Context。下游可以缓存当前决定但短 TTL/主动失效；高风险处理重查权威状态。传播失败保持阻断或 Partial，不默认允许。

### 19.7 Policy Changes

实质 Purpose/Recipient/Scope 变化需要新告知或重新授权（法律适用待确认），不能静默更新 PolicyReference。历史 ConsentRecord 保留原版本。

### 19.8 Minors

首发独立用户暂定 18 岁以上。年龄确认、误入、监护人授权和删除流程需上线前法律/产品确认；未确认前不主动面向未成年人。

---

## 20. Data Retention

### 20.1 Retention Principles

数据按 Purpose、Classification、Lifecycle、User Choice、Legal Hold、Security/Audit 和法律要求保留。期限可配置，正式数值上线前确认。

### 20.2 Retention Schedule

| Data Class | Default Direction | Final Status |
|---|---|---|
| Anonymous Trial | 短期、默认不长期保存 | 期限待产品/法律确认 |
| Account/Auth | 账户期间 + 必要安全/法律期 | 待确认 |
| Birth/Chart/Snapshot | 用户保存期间；删除请求按策略 | 待确认 |
| Frozen Report/Timeline | 用户控制 + 历史引用/法律 | 待确认 |
| Conversation/AIAnalysis | 最小必要、可配置 | 待确认 |
| ConsentRecord | 证明决定所需期限 | 待法律确认 |
| Security/Audit | 调查、合规、防篡改需求 | 待法律/安全确认 |
| Logs/Traces | 较短、按信号类别 | 待确认 |
| Backups | 周期到期、墓碑保护 | RPO/法律待确认 |
| Optimization/Research | 单独 Consent、撤回与计划期限 | 待伦理/法律确认 |

### 20.3 Retention Metadata

对象具备 Retention Class、Purpose、Created/Last Needed、Expiry、Legal Hold、Deletion Status 和 Source。期限不散落硬编码。

### 20.4 Expiry

到期由幂等任务发现并经各 Context 处置，覆盖 Database、Object、Search/Vector、Cache、Task、Projection 和 Vendor。失败进入 Partial/Manual Review。

### 20.5 Legal Hold

Hold 有法律依据、范围、Owner、起止/复审、访问限制与 Audit。Hold 不授权新用途；无关数据继续到期/删除。

### 20.6 Backup Retention

Backup 按周期到期，不从活动备份直接恢复已删除数据。Restore 重新应用 Tombstone 和 Retention。

### 20.7 Retention Review

每次新 Purpose、Vendor、Region、数据类别或法律变化更新数据清单、影响评估和 Schedule。减少期限优先，延长需明确依据。

---

## 21. Data Export

### 21.1 Scope

用户可请求其有权访问的数据导出。Export 是 Data Rights Operation，不通过通用 API Expand 绕过 Masking/Authorization。

### 21.2 Identity Verification

导出前 Step-Up/近期认证，评估账户风险与代理关系。不能把导出发送到未经验证的新地址或任意 Callback。

### 21.3 Data Collection

各 Context 提供授权、版本化导出投影，记录截止时间、来源、成功/失败和 Legal Hold/权利限制。应用流程记录不是新 Domain Aggregate。

### 21.4 Export Content

包含适用数据、版本、用户决定和必要说明；不包含其他主体信息、平台 Secret、受限知识全文、内部安全策略或供应商机密。具体格式与法律范围待确认。

### 21.5 Artifact Security

Export 加密/短期下载、不可猜 Identity、服务端授权、完整性、到期删除和访问 Audit。文件名不含敏感信息。

### 21.6 Partial and Failure

任何必要来源失败则保持 `Partial/Processing/Failed`，不标 Completed。用户得到安全状态和下一更新时间；超期进入 Manual Review/Incident。

### 21.7 Delivery and Retention

下载次数、有效期和 Artifact Retention 待产品/法律确认。到期后删除 Object、URL/Token 和 Cache，保留最小 Audit。

---

## 22. Data Deletion

### 22.1 Deletion Scope

支持账户删除、单一资源删除和 Consent 撤回相关停止处理。删除不等于 Archive；Archive 也不满足删除权。

### 22.2 Orchestration

继承 User Deletion Saga：Identity、Consent、Birth、Chart、Rule/Evidence 关联、AI/Conversation、Timeline、Report、Object、Search、Cache、Task/Projection 和适用研究副本分别处置。

### 22.3 Deletion Strategies

按 Data Model 使用 Physical Delete、Logical Delete、Archive、Anonymization 和 Legal Hold。选择由对象、引用、法律和可复现要求决定，不用一个通用 Hard Delete。

### 22.4 Pre-Deletion

- 强身份复核；
- 展示影响范围；
- 停止新活动/分享/Session；
- 发现所有资产、Vendor 和备份范围；
- 评估 Legal Hold、Fraud/Security 和他人权利；
- 创建可追踪 Request/Correlation。

### 22.5 Active Stores

删除或匿名化 PostgreSQL、Object、Search/Vector、Cache、Read Model、Queue/Task 和第三方 Provider 的适用副本。每一步幂等并返回结果。

### 22.6 Backup and Tombstone

不可立即逐项修改的 Backup 通过到期与 Tombstone 防复活。恢复后先重放删除状态再开放访问。用户完成表述需法律确认。

### 22.7 Legal Hold

Hold 数据保持最小、受限、不可新用途，并向用户提供法律允许的状态说明。Hold 解除后继续删除流程。

### 22.8 Partial Completion

失败步骤保持受限，有限重试后人工处置。不得因主要数据库已删就忽略 Object、Index、Cache、Vendor 或 Backup。

### 22.9 Verification

按 Subject/Resource 安全引用在各 Store、Index、Object、Vendor 和 Restore 流程验证；验证工具不得重建完整敏感数据副本。

### 22.10 User Communication

状态包括 Received、Processing、Partial、LegalReview/Hold、Completed、Failed。说明剩余范围和后续，不暴露内部安全/他人数据。

---

## 23. Audit Architecture

### 23.1 Audit Objectives

支持 Accountability、调查、职责分离和不可抵赖性证据：谁、何时、以何身份/权限/Purpose、对何对象、做何动作、结果如何、关联何批准/版本。

### 23.2 Audit Events

认证/MFA/Recovery、Role/Scope、Consent、敏感访问、发布、Config/Secret/Key、Export/Delete、Share、AI Provider/Policy 高风险变化、Break-Glass、Replay、Migration、Incident 和 Data Repair。

### 23.3 Immutability and Tamper Evidence

- Append-only；
- Correction 新增记录引用原事件；
- 限制普通管理员修改/删除；
- 使用完整性链、签名/Hash、WORM/受控归档等候选机制支持篡改检测；
- 具体不可抵赖技术与法律效力需 ADR/法律评审。

### 23.4 Audit Content

Actor/Subject 安全引用、Action、Resource、Purpose、Role/Scope、Decision、Result、Time、Request/Correlation、Policy/Version 和 Approval。最小化，不复制 Birth、Conversation、Prompt、AI Raw 或 Report 全文。

### 23.5 Time and Identity

统一可信时间，记录 Workload/User/Impersonation/Delegation。共享账户禁止，避免 Audit 无法归属。

### 23.6 Reliability

必需 Audit 与业务/管理动作可靠关联。关键 Audit 写失败阻断高风险操作或进入明确 Incident，不静默丢失。

### 23.7 Access and Investigation

Auditor/安全角色 JIT、Purpose、范围和 Session Audit。查询 Audit 本身被审计。取证导出保留 Hash、Chain of Custody 和到期。

### 23.8 Retention and Deletion

Audit 保留与用户删除的平衡由法律确认。保留必要法律/安全证据时最小化并限制访问，不把 Audit 当作永久保存业务正文的后门。

---

## 24. Threat Modeling

### 24.1 Method

每个重大 Feature/Flow 使用系统化方法识别身份欺骗、篡改、否认、信息泄露、拒绝服务、权限提升，以及隐私可关联、可识别、不可干预、过度披露等威胁。具体采用 STRIDE/LINDDUN 或等价方法可由安全团队标准化。

### 24.2 Assets

Credential/Key、Identity/Consent、BirthInput、Chart/Snapshot、Rule/Evidence、AI Conversation/Report、Knowledge Rights、Audit、Data Rights State、Algorithm/Prompt/Model Version、Build Artifact 和 Backup。

### 24.3 Trust Boundaries

Browser ↔ Edge、Edge ↔ API、API ↔ Module/Data、API ↔ Worker/Broker、Worker ↔ AI/Provider、App ↔ Object/Search/Observability、Staff ↔ Production、Environment/Region、DeveloperClient/Tenant。

### 24.4 Threat Scenarios

| Threat | Example | Primary Controls |
|---|---|---|
| Account Takeover | Credential Stuffing、Recovery Abuse | MFA、Rate Limit、Risk、Session Revoke |
| IDOR | 猜 Chart/Report ID | Server Ownership/ABAC、404 Policy |
| Privilege Escalation | Role/Scope/Policy 操纵 | Signed Context、Default Deny、Audit |
| Data Exfiltration | Export、Log、Object、Vendor 滥用 | DLP/Mask、JIT、Short URL、Monitoring |
| Prompt Injection | User/Knowledge 诱导越权 | Isolation、Tool Allowlist、Validation |
| Model Jailbreak | 绕过主题/风险边界 | Policy、Classifier、Output Gate、Rate Limit |
| Supply Chain | 恶意依赖/CI Artifact | Lock、SBOM、Signing、Least Privilege |
| Data Poisoning | 未审核 Knowledge/Rule 进入生产 | Governance、Published Version、Provenance |
| Ransom/Deletion | Key/Backup/Object 破坏 | MFA、Separation、Immutable Backup、DR |
| Insider Abuse | Support/Admin 批量查看 | JIT、Masking、Session Audit、Alert |
| Re-identification | 去标识数据关联 | Minimization、Aggregation、Access、Review |
| Denial of Wallet | AI 高成本滥用 | Quota、Rate Limit、Budget、Circuit |

### 24.5 Threat Register

每个 Threat 记录 Asset、Actor、Entry、Precondition、Impact、Existing Control、Residual Risk、Owner、Test、Detection、Response 和 Review Date。

### 24.6 Risk Treatment

Avoid、Reduce、Transfer、Accept。Accept 需要明确 Owner、期限/复审、理由和补偿；Critical Security/Privacy/Data Integrity 风险不能由普通产品 Owner 单独接受。

### 24.7 Modeling Triggers

新数据/Vendor/Region/API、Authentication、Role、AI Tool、File Upload、Share、Export/Delete、Migration、Model/Prompt 或重大 Incident 后更新 Threat Model。

---

## 25. AI Security

### 25.1 Security Boundary

AI 不计算八字事实、不创建 Evidence、不扩大 Scope、不决定授权。Provider 原始输出是不可信数据，只有经过平台 Validation 的结构化结果可成为正式 AIAnalysis/Message/Report 输入。

### 25.2 Model Gateway

所有 Provider 调用通过统一 Gateway/Adapter：去标识化、Model/Prompt Version、Timeout、Quota、Region、Policy、Input/Output Validation、Cost、Audit 和 Error Mapping。

### 25.3 Input Minimization

发送 Chart/Snapshot 事实、Frozen Evidence、必要 Timeline/Topic 和 Risk Context；移除 UserId、姓名、联系方式、详细地址、Support Ticket、无关 Conversation 和其他 Chart 标签。

### 25.4 Provider Controls

合同与技术限制 Retention、Training、Human Review、Subprocessor、Region、Deletion、Security、Incident Notification 和 Data Use。使用已批准 Model Reference，不自动切换“最新模型”。

### 25.5 Output Validation

依次验证：结构、Scope、Fact、Evidence/Citation、Conflict、Risk、Language/Length 和 Prohibited Claim。失败可有限修复/重试，但不能补造缺失上游。

### 25.6 Tool Use

MVP AI 不获得任意 Code Execution、Database、Internet、Secret 或跨用户 Tool。未来 Tool 必须最小 Allowlist、参数验证、Sandbox、Approval、Timeout、Result Validation 和 Audit，并需 ADR。

### 25.7 AI Data Leakage

防止 Prompt/Context/Response 进入 Provider Log、平台 Debug、Analytics 或其他 User Session。使用一次性 Analysis Identity 和 Tenant/Conversation 隔离。

### 25.8 Availability and Abuse

Rate Limit、Quota、Concurrency、Circuit、Timeout、Retry Budget 和 Degraded Mode 防 Denial of Wallet。AI 不可用时确定性排盘仍可用。

### 25.9 Model Change

新 Model/Version 经过安全、隐私、事实、引用、风险、成本与区域评估，Canary 后发布新 Route Version；旧 Frozen Report 不被改写。

---

## 26. Prompt Injection Defense

### 26.1 Threat Sources

用户问题、Birth Label、Knowledge 文本、网页/文件、Retrieved Chunk、Conversation 历史、Provider 输出和外部 Tool Result 都可能包含恶意指令。

### 26.2 Instruction Hierarchy

平台安全/系统规则、批准 Application Scope 和用户请求分层。Retrieved Content 与 User Content 明确标记为数据，不得覆盖高层指令。

### 26.3 Context Isolation

- 每次 Analysis 使用最小、明确 Scope；
- Conversation 只关联当前 Chart/允许主题与未来三年；
- 不跨用户/Chart 复用私人上下文 Cache；
- Knowledge Chunk 带来源、State、Rights、Version；
- 系统 Prompt 不包含 Secret 或高权限 Credential。

### 26.4 Input Controls

长度、编码、结构、附件、URL、语言和风险分类；检测已知越权/泄漏/工具操纵模式，但检测器不是唯一防护。

### 26.5 Retrieval Controls

只检索 Published、权利有效、Scope/语言/流派兼容内容；向量相似度只召回。Chunk 中的指令不自动执行，Citation 必须可验证。

### 26.6 Tool and Action Controls

模型不能直接决定授权、Tool Scope 或最终写入。所有 Tool 参数经服务端 Schema、ABAC、Purpose 和领域前置验证；高风险动作要求用户/人工显式确认。

### 26.7 Output Gate

结构化解析后进行 Fact/Evidence/Risk/Scope Validation。模型声称“已执行”“已删除”“已保存”不改变业务状态。

### 26.8 Prompt Leakage

- 不把 System Prompt 保密视为安全边界；
- 不在 Prompt 放 Secret、内部 Key 或未必要 Policy 细节；
- 拒绝提取系统/其他用户上下文；
- 输出扫描敏感片段和跨 Session 数据；
- 泄漏疑似事件进入 AI Security Incident。

### 26.9 Testing

维护 Injection/Jailbreak/Leakage/Encoding/Multilingual/Indirect Injection 评估集，覆盖用户、Knowledge、File 和 Tool。Model/Prompt/Route 变化必须回归。

---

## 27. Model Abuse Prevention

### 27.1 Abuse Categories

越权数据提取、无限高成本生成、Jailbreak、高风险健康/婚姻/投资裁决、欺骗/操纵、自动化批量命盘、Prompt/Model 探测、恶意分享和生成内容标识规避。

### 27.2 Controls

| Control | Use |
|---|---|
| Scope/Topic Policy | 限定当前 Chart、未来三年和批准主题 |
| Risk Classifier/Rules | 检测高风险和拒答/降级 |
| Rate/Quota/Concurrency | 防自动化滥用和成本攻击 |
| Evidence Requirement | 重要结论必须可引用 |
| Safe Completion | 明确不确定、冲突、有限证据 |
| Account/Client Risk | 异常行为限制与复核 |
| Share/Export Control | 防敏感内容扩散 |
| Monitoring | 模式、成本、拒绝和绕过趋势 |

### 27.3 Jailbreak

不依赖单一关键词。采用分层 Prompt、Policy、最小 Tool、Input/Output Gate、Conversation Scope、Rate Limit 和人工 Red Team。发现成功绕过先关闭/限制能力，再修复与回归。

### 27.4 High-Risk Topics

最终健康、婚姻、投资边界待法律/专家确认。未确认前不提供疾病诊断、投资保证、婚姻事件确定预测或绝对择日裁决；输出提示非专业建议和证据限制。

### 27.5 Content Labeling

AI 生成内容、下载/导出和未来传播功能的显式/隐式标识义务需按目标地区法律评审。标识不得被用户或 Pipeline 静默移除。

### 27.6 Abuse Response

Warn、Rate Limit、Temporary Restrict、Credential Revoke、Manual Review 或 Account Action，依据批准 Policy、证据和申诉流程。不能以命理观点差异作为滥用证据。

---

## 28. Supply Chain Security

### 28.1 Scope

Source、Dependency、Package Registry、Build Runner、CI/CD、Artifact、Container Base、Action/Plugin、Model/Prompt/Knowledge Source 和 Vendor。

### 28.2 Source Control

强身份/MFA、Branch Protection、Required Review、Signed/Traceable Change、Secret Scan 和最小 Bot 权限。敏感修复使用受控私密流程。

### 28.3 Build Security

- 隔离、短期 Workload Credential；
- 依赖锁定与可信来源；
- 不在不可信 PR 暴露生产 Secret；
- 生成 SBOM、Vulnerability/License 证据；
- Artifact 完整性/签名和 Provenance；
- 同一 Artifact 环境晋级。

### 28.4 Artifact Security

Registry 私有、最小 Push/Promote、不可变 Tag/Digest 方向、Retention 与 Quarantine。发现污染停止 Promotion、撤销 Credential 并 Incident。

### 28.5 Third-Party Actions and Plugins

固定受信版本、最小权限、审查维护/许可证，不允许任意第三方动态代码进入 MVP/V1 Production。Plugin Marketplace 不在当前范围。

### 28.6 Model and Knowledge Supply Chain

Model、Embedding、Prompt、Rule、Knowledge 来源、Version、Rights、Review 和 Hash 可追踪。下载模型/数据不得未经验证直接进入生产。

### 28.7 Supplier Assurance

关键 Vendor 评估 Security、Privacy、Compliance、Incident、BCP、Subprocessor、Region 和 Exit。评估不替代平台自身防护。

---

## 29. Dependency Security

### 29.1 Inventory

维护直接/传递依赖、Version、Owner、License、Source、Runtime/Build Scope、Known CVE、Support/EOL 和替代。

### 29.2 Admission

新增依赖说明必要性、维护状态、权限、大小、Telemetry、Data Access、License 和替代。微小功能不轻易引入高权限/复杂依赖。

### 29.3 Pinning and Verification

Lock 版本与完整性，禁止生产构建自动取“latest”。Registry/Source 受控，检测依赖混淆、Typosquatting 和恶意更新。

### 29.4 CVE Handling

按 Severity、Exploitability、Exposure、Data/Privilege 和可用修复分类。不能只看 CVSS；Critical 可利用问题触发 Emergency Change/能力隔离。

### 29.5 Update

安全 Patch 与常规 Upgrade 分开，小步、Contract/Regression、安全和性能测试。Breaking Upgrade 需要兼容/ADR 评估。

### 29.6 End of Life

EOL 依赖进入 Debt/Replacement Plan，有 Owner、Deadline 和风险控制。无维护关键依赖不得长期接受。

### 29.7 Exceptions

无法立即修复的 CVE 记录影响、不可利用证据、补偿控制、Owner、Expiry 和复测。永久忽略禁止。

---

## 30. Vulnerability Management

### 30.1 Lifecycle

Discover → Validate → Prioritize → Assign → Mitigate/Fix → Verify → Close → Learn。

### 30.2 Sources

SAST、DAST、Dependency/Container/Secret Scan、Penetration Test、Bug Report、Vendor Advisory、Threat Modeling、Incident 和安全研究。

### 30.3 Prioritization

考虑 Exploitability、Internet Exposure、Privilege、Data Classification、Blast Radius、Compensating Control 和 Business Criticality。身份、Export/Delete、AI Tool、Object、Secret 和 Supply Chain 优先。

### 30.4 Remediation SLA

具体 Critical/High/Medium/Low 时限需安全治理批准。超期自动升级；SLA 不能因“未被利用”无限延长。

### 30.5 Verification

修复后重新扫描、回归、攻击路径和生产信号验证。关闭 Finding 需要证据，不只依赖版本号变化。

### 30.6 Disclosure

建立负责任披露/安全联系、Safe Harbor（如适用）、报告接收、保密和用户通知流程。具体计划待法律/安全确认。

### 30.7 Penetration and Red Team

上线前及重大变化后覆盖 Auth、Authorization、API、Web、AI/Prompt、SSRF、Object、Supply Chain 和 Data Rights。测试使用批准环境与数据，避免影响用户。

---

## 31. Security Monitoring

### 31.1 Monitoring Domains

| Domain | Signals |
|---|---|
| Identity | Login/MFA/Recovery、Session、Credential Abuse |
| Authorization | Deny、IDOR、Role/Scope、JIT、Break-Glass |
| API/Edge | WAF、Rate Limit、Bot、Payload、SSRF Attempt |
| Data | Unusual Read/Export/Delete、Object Access、DB Privilege |
| AI | Injection/Jailbreak、Leakage、Policy Bypass、Cost Abuse |
| Supply Chain | Secret、Artifact、Dependency、CI Identity |
| Operations | Config Drift、Direct Access、Audit Failure |
| Privacy | Consent/Retention/Delete Partial、Cross-Border Route |

### 31.2 Detection Principles

- 基于风险和基线，不用单个弱信号自动重罚；
- Security/Privacy Signal 有 Owner/Runbook；
- No Data/Telemetry Failure 不是 Healthy；
- Detection 不记录完整敏感正文；
- 规则变化测试误报、漏报与攻击覆盖。

### 31.3 Anomaly Detection

候选场景：批量 Resource 枚举、异常 Export、Support Unmask、Secret 访问、AI Token 激增、跨 Tenant、Impossible Travel（谨慎）、DLQ Replay 和对象下载。行为分析需 Privacy Impact Review。

### 31.4 Alert Severity

继承 Operations SEV 模型。疑似敏感数据泄漏、系统性 Authorization Bypass、Key/Artifact Compromise、删除复活和 Critical Audit Loss 保守提升。

### 31.5 Evidence

保留最小必要事件、Correlation、Policy/Release、Actor 安全引用与 Integrity，不为调查无限采集业务正文。

### 31.6 Metrics

MTTD、False Positive、Coverage、Alert Owner、Investigation Time、Containment、Credential Revoke、Patch Aging 和 Repeat Finding。不能用“告警数量多”证明更安全。

---

## 32. Security Incident Response

### 32.1 Alignment

继承 `11-DEPLOYMENT-OPERATIONS.md` 的 SEV-1 至 SEV-4、Incident Commander、Operations Lead、Communications Lead、Security/Privacy Lead、Timeline、Mitigation、Recovery 和 PIR。

### 32.2 Security Incident Categories

Account/Session、Authorization Bypass、Data Exposure/Exfiltration、Secret/Key、Supply Chain、Malware、Prompt/Model Leakage、Vendor、Data Integrity、Audit、Deletion/Privacy 和 DoS/Cost Abuse。

### 32.3 Initial Response

1. Declare/Set Severity；
2. Assign Security/Privacy Lead；
3. Preserve Evidence/Timeline；
4. Contain（Revoke、Isolate、Block、Flag Off、Rate Limit）；
5. Assess Data/Subjects/Regions/Time；
6. Notify Legal/Leadership by trigger；
7. Eradicate and Recover；
8. Validate Security/Data/User Journeys；
9. Communicate and Review。

### 32.4 Containment

优先限制影响：撤销 Token/Key、禁用 Client/Account、隔离 Artifact/Worker、暂停 Export/Webhook、阻断 Egress、停止 Model Route。Containment 不能销毁 Audit/Forensic Evidence。

### 32.5 Privacy Assessment

确定数据类别、数量、主体、地区、加密/可识别、接收者、持续时间、可能伤害、删除/Consent 和法律通知义务。未知按保守假设，持续更新。

### 32.6 Notification

监管、用户、供应商和合同通知条件/时限由法律确认。Communications 不隐瞒、不猜测，不暴露攻击细节或其他用户数据。

### 32.7 Recovery

轮换 Credential/Key、修复漏洞、清理恶意 Artifact、验证权限/数据完整性、恢复受控流量并加强监测。组件 Up 不等于安全恢复。

### 32.8 Post-Incident

无责但有责任：Root/Contributing Factors、Control Gap、Detection/Response、Data Impact、Decision、Corrective Actions、Owner、Deadline 和验证。重复问题升级 Governance。

---

## 33. Privacy Governance

### 33.1 Roles

| Role | Responsibility |
|---|---|
| Privacy Owner | Privacy Program、Policy、Risk 和 Rights |
| Data Owner | Purpose、Classification、Retention、Access |
| Product Owner | Notice、Choice、UX、Minimization |
| Security Owner | Technical/Operational Controls |
| Legal Counsel | Applicable Law、Basis、Transfer、Notice |
| Vendor Owner | Contract、Subprocessor、Region、Deletion |
| Audit/Compliance | Evidence、Review、Finding |

### 33.2 Data Inventory / Record of Processing

记录 Data、Source、Purpose、Legal Basis Candidate、Subject、Recipient、System/Region、Retention、Consent、Transfer、Control 和 Owner。新 Feature/Vendor 前更新。

### 33.3 Privacy Impact Assessment

下列触发 PIA/PIPIA 候选：Restricted Sensitive、新 AI/Vendor、Cross-Border、Research/Optimization、Large-Scale Profiling、Share、File Upload、New Purpose、Minor、Security Monitoring/Behavior Analysis。

### 33.4 Privacy Review Gate

Product Discovery、Architecture、API/Data、Vendor、Pre-Production 和 GA 均有 Gate。未解决 High Privacy Risk 阻断发布或缩小范围。

### 33.5 Data Subject Rights

访问、复制/导出、更正、删除、撤回、解释和投诉（适用范围由法律确认）有验证、时限、状态、例外、Audit 和申诉。

### 33.6 Vendor Governance

Due Diligence、合同、数据流、Region、Subprocessor、Security、Retention、Training、Deletion、Incident、Audit 和 Exit。Vendor 变化触发 Review。

### 33.7 Privacy Metrics

Consent、Withdrawal Propagation、Export/Delete Completion、Partial/Hold、Retention Backlog、Unmask Access、Vendor Deletion、Incident 和 Finding Aging。指标不包含敏感正文。

### 33.8 Training and Awareness

开发、Support、Operations、Content、Expert 和 Incident Role 按职责培训。高权限与敏感访问需定期更新培训。

### 33.9 Complaints and Appeals

用户可投诉数据、AI 风险、授权和删除；处理不自动更改命理规则。支持流程最小访问、时限、升级和 Audit。

---

## 34. Compliance Considerations

### 34.1 Scope and Legal Review

首发面向中国大陆简体中文成年用户。以下仅为合规评审清单，不是适用性结论；上线前由法律顾问结合主体、部署、模型供应商、数据规模、功能和地区确认。

### 34.2 Primary Official References

- 《中华人民共和国个人信息保护法》：个人信息处理、敏感个人信息、个人权利、委托处理、影响评估和跨境等评审基础，可从[中国政府网](https://www.gov.cn/xinwen/2021-08/20/content_5632486.htm)核对正式文本。
- 《中华人民共和国数据安全法》：数据处理、安全义务和分类分级等评审基础，参见[中国人大网](https://www.npc.gov.cn/npc/c2/c30834/202106/t20210610_311888.html)。
- 《中华人民共和国网络安全法》及其现行有效修订状态：网络运营、安全保护和事件等评审基础，应在上线前从国家法律法规数据库核对最新文本。
- 《网络数据安全管理条例》及配套规则：网络数据处理、个人信息、重要数据和平台义务的评审输入，应核对届时现行官方文本。
- 《生成式人工智能服务管理暂行办法》：面向境内公众提供生成式 AI 服务的适用性、备案/评估和内容治理需专项确认，参见[国家互联网信息办公室](https://www.cac.gov.cn/2023-07/13/c_1690898327029107.htm)。
- 《人工智能生成合成内容标识办法》及配套强制性标准：显式/隐式标识、下载/导出和用户协议要求需专项确认；该办法自 2025 年 9 月 1 日施行，参见[国家互联网信息办公室](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm)。
- 数据跨境路径、阈值、个人信息保护影响评估和单独同意等需按现行业务事实确认，参见[《促进和规范数据跨境流动规定》官方文本](https://www.cac.gov.cn/2024-03/22/c_1712776611775634.htm)及届时最新申报/备案指南。

### 34.3 Compliance Workstreams

| Workstream | Questions Before GA |
|---|---|
| Personal Information | Controller/Processor 角色、Purpose、敏感分类、Notice、Rights |
| Cross-Border | AI/Cloud/Support/Logs 是否出境、路径、合同/评估/认证 |
| AI Service | 服务适用范围、备案/登记、安全评估、Provider Disclosure |
| AI Labeling | 在线文本、复制、打印、PDF、分享、Metadata 如何标识 |
| Cybersecurity | 等级保护/其他安全义务适用性、事件报告 |
| Data Security | 分类分级、重要数据识别、风险评估和应急 |
| Consumer Protection | 免责声明、订阅/额度、投诉、误导性宣传 |
| Content | 传统文化定位、高风险话题、生成内容和违法信息治理 |
| Copyright | Knowledge 来源、引用、模型输入输出和撤下 |
| Minors | 18+ 策略、年龄确认、误入与监护人流程 |

### 34.4 AI Content Labeling

产品应在 UI、报告、复制/下载/导出和未来分享中保留“AI 生成/辅助解释”透明度。显式标识位置、隐式 Metadata、日志保留和用户协议内容必须按现行办法与强制标准由法律/产品/技术联合确认。

### 34.5 Cross-Border

在选择境外 AI、Observability、Support 或 Cloud 前完成数据流、分类、数量、敏感性、Recipient、Region、Subprocessor、合同、影响评估和可用合规路径。未批准前优先不向境外传输直接身份或详细 Birth 数据。

### 34.6 High-Risk Content

健康、婚姻、投资等最终边界仍待法律/领域确认。平台不得宣称科学准确、必然预测未来或替代医疗/法律/投资专业意见。

### 34.7 Evidence and Change Monitoring

维护法律清单、Owner、适用性结论、控制映射、证据、复审日期和变更订阅。法规变化不直接在生产修改行为，先评估并走 Change/ADR。

---

## 35. Security ADR Reference Matrix

| Topic | ADR Required | Trigger Example |
|---|---|---|
| Authentication Strategy | Yes | 密码/无密码/联合身份信任模型变化 |
| Authorization Strategy | Yes | 改变 RBAC+ABAC+Ownership+Purpose 合取模型 |
| RBAC Model | Yes | 新增继承、超级管理员或职责分离变化 |
| ABAC Model | Yes | 新 Attribute、Policy Engine 或风险属性 |
| Token Strategy | Yes | JWT/Opaque、Access/Refresh、Revocation 模型变化 |
| Session Strategy | Yes | Cookie/Token Storage、Timeout、Revocation 变化 |
| MFA / Step-Up | Yes | 高权限/用户 MFA 和恢复策略变化 |
| API Security | Yes | WAF、Rate Limit、CORS/CSRF 或 Trust Boundary 变化 |
| Encryption Strategy | Yes | 字段级、Envelope、传输/静态加密模式变化 |
| Key Management | Yes | KMS/HSM、Key Hierarchy、Rotation/Recovery 变化 |
| Secret Management | Yes | Secret Delivery、Workload Identity 或 Break-Glass 变化 |
| Data Classification | Yes | Classification Level/Handling Rule 变化 |
| PII / Masking | Yes | 默认可见、去标识或 Unmask 模型变化 |
| Consent Model | Yes | Purpose、Decision、Policy/Withdrawal 语义变化 |
| Retention / Legal Hold | Yes | 正式期限、到期、Hold 或 Backup 语义变化 |
| Export / Deletion | Yes | Rights Scope、Completed、Tombstone 或 Vendor 删除变化 |
| Audit Strategy | Yes | 必需事件、不可变、保留或物理边界变化 |
| AI Security Strategy | Yes | Model Gateway、Tool Use、Validation 或 Provider 数据变化 |
| Prompt Injection Defense | Yes | Instruction/Tool/Retrieval Trust 模型变化 |
| Threat Model | Yes | 新 Trust Boundary、Asset 或正式方法变化 |
| Privacy Model | Yes | Purpose、Recipient、Region 或 Data Subject 权利变化 |
| Security Monitoring | Yes | 行为分析、Retention、Detection 或 Evidence 范围变化 |
| Incident Response | Yes | Severity、Notification、Forensics 或 Containment 变化 |
| Supply Chain | Yes | Build Trust、Signing、Registry 或 Third-Party Plugin 变化 |

任何涉及以上主题的修改，都不得直接修改本文档。必须先通过 ADR，记录 Threat、Data/Privacy、候选、取舍、兼容、迁移、Incident/Recovery、法律输入、Owner 和验证；批准后才能更新 Security & Privacy Baseline。

---

## 36. Security Anti-Patterns

| Anti-Pattern | 为什么属于反模式 | 风险 | 推荐做法 |
|---|---|---|---|
| Hardcoded Secret | Secret 进入源码/镜像/配置 | 泄漏、难轮换 | 专用 Secret Manager、扫描、Workload Identity |
| Shared Admin Account | 多人共享高权限身份 | 无法追责、撤销困难 | 个人身份、MFA、JIT、Session Audit |
| Long-lived Token | Token 长期有效且难撤销 | 泄漏后长期访问 | 短期 Access、Rotation、Revocation、Scope |
| Missing MFA | 高权限仅单因子 | Account Takeover | Staff/Break-Glass 强制 MFA、Step-Up |
| Trusting Client Input | 信任 Role、Owner、State、URL 或 AI 内容 | 越权、注入、SSRF | 服务端验证、Schema、ABAC、Allowlist |
| Logging Sensitive Data | 记录 Birth、Conversation、Prompt、AI Raw、Report | 隐私泄漏与保留扩大 | 禁记清单、Redaction、最小引用 |
| Prompt Injection Ignored | 把 Retrieved/User 文本当可信指令 | 泄漏、越权 Tool、策略绕过 | 指令分层、隔离、Tool Gate、输出验证 |
| AI Output Without Validation | Provider 输出直接展示/入库 | 事实编造、引用/风险失控 | 结构/事实/Evidence/Risk/Scope Gate |
| Direct Database Access | 人员/服务绕过 Application 修改数据 | 不变量、Audit、删除损坏 | JIT 只读、受控 Repair Use Case |
| Over-Privileged Service Account | Workload 拥有全库/全 Secret | 单点失陷大范围泄漏 | 每服务/环境最小 Role 和网络权限 |
| Shared Production Credential | 环境/人员/服务共用 Key | Blast Radius、无法归属 | 独立 Credential、Rotation、Audit |
| Missing Audit | 高风险操作无可靠记录 | 无调查、否认、合规失败 | 必需 Audit + Outbox/阻断策略 |
| Security Through Obscurity | 依赖隐藏 URL/Prompt/ID | 一旦发现即失守 | 强认证、授权、加密、验证 |
| Disabled TLS | 明文或跳过证书验证 | 窃听、中间人 | 强制安全传输、证书生命周期 |
| Ignoring Dependency CVEs | 不评估已知漏洞 | Supply Chain/远程利用 | Inventory、优先级、Patch/例外期限 |
| UI-Only Authorization | 只隐藏按钮/页面 | API 直接越权 | Application/Repository 服务端执行 |
| Super Admin by Default | 管理员继承全部数据权限 | Insider/误操作 | 职责分离、Purpose、JIT、Mask |
| Consent as Checkbox Only | 无 Purpose/Version/撤回传播 | 无法证明、继续未授权处理 | SubjectConsent、PolicyReference、Saga |
| Hash Equals Anonymous | 认为 Hash ID 即匿名 | 重识别和链接攻击 | 风险评估、Pseudonymization、Minimization |
| Encryption as Complete Privacy | 加密后无限收集/保留 | 合法使用和内部泄漏风险 | Purpose、Minimization、Access、Retention |
| Secrets in Prompt | 把 Key/内部策略放入模型上下文 | Prompt Leakage/Provider Exposure | Prompt 不含 Secret、Gateway 隔离 |
| Unrestricted AI Tools | 模型可访问 DB/Internet/Code | 越权、SSRF、数据破坏 | 最小 Tool Allowlist、Approval、Sandbox |
| Silent Model Upgrade | 自动使用“最新模型” | 安全/行为/合规漂移 | Locked Model Reference、评估、Canary |
| Permanent Data Retention | 无期限保存用户/日志 | 攻击面和法律风险 | Retention Schedule、Expiry、Deletion |
| Backup Resurrection | Restore 后恢复已删数据 | 违反用户权利 | Tombstone、Restore Validation、隔离 |
| Audit Contains Full Content | Audit 复制全部业务正文 | 高价值敏感数据库 | 最小 Actor/Action/Reference/Result |
| Blind Cross-Border Transfer | 未评估直接发境外 Provider | 合规与隐私事件 | Data Flow、Impact、合同/路径、最小化 |
| Alerting on Sensitive Payload | 将完整 Payload 放入告警/聊天 | 二次泄漏 | 安全摘要、Correlation、受控调查 |

---

## 37. Review Checklist

### 37.1 Baseline and Scope

- [ ] 文档是否为 Review 0.9。
- [ ] 是否严格继承 01–11 Approved 基线。
- [ ] 是否未修改 Domain、Aggregate、Entity、Value Object、Event、API、Data、Technology 或 Engineering Baseline。
- [ ] 是否没有代码、JWT/OAuth/IAM/WAF/Cloud 配置或部署脚本。
- [ ] 是否未进入编码阶段。

### 37.2 Identity and Access

- [ ] User、Subject、Actor、Client、Workload 和 Provider Identity 是否分离。
- [ ] Authentication 是否防枚举、暴力、Fixation 和恢复绕过。
- [ ] Privileged/Break-Glass 是否 MFA、JIT、限时和审计。
- [ ] RBAC、ABAC、Ownership、Purpose、Consent 是否合取且 Default Deny。
- [ ] 是否无共享账户/生产 Credential。
- [ ] Session/Token 是否短期、可轮换、可撤销、最小 Claim。
- [ ] JWT 若采用是否不作为实时授权 Source of Truth。

### 37.3 API and Infrastructure

- [ ] Rate Limit、WAF、CSRF、XSS、SSRF、SQLi、IDOR、Mass Assignment 是否覆盖。
- [ ] TLS/证书、Encryption at Rest/In Transit 是否明确。
- [ ] Key/Secret 是否分用途、环境、Workload 且可轮换恢复。
- [ ] Production/Database/Object/Search/Log 是否最小权限。
- [ ] Error/Log/Trace 是否不泄露敏感内容。

### 37.4 Privacy and Data Lifecycle

- [ ] Data Classification 是否覆盖 Birth、Chart、AI、Report、Consent、Audit 和 Secret。
- [ ] 是否不默认收集姓名/详细地址。
- [ ] Pseudonymization/De-identification 是否考虑组合重识别。
- [ ] Masking 是否在服务端且 Unmask 有 JIT/Purpose/Audit。
- [ ] SubjectConsent/ConsentRecord 是否与 Domain Model 一致。
- [ ] 可选授权是否不捆绑，撤回是否停止新处理。
- [ ] Retention、Legal Hold、Export、Deletion、Backup Tombstone 是否完整。
- [ ] Partial/Delete/User Communication 是否不伪报完成。

### 37.5 AI and Threats

- [ ] AI 是否不计算事实、不建 Evidence、不扩大 Scope。
- [ ] 第三方 AI 是否只接收去标识化必要上下文。
- [ ] Prompt Injection/Leakage/Jailbreak、Tool/Retrieval 是否分层防护。
- [ ] AI 输出是否经过结构、事实、Evidence、风险和 Scope 校验。
- [ ] Model/Prompt/Route 是否版本化、评估和 Canary。
- [ ] Threat Model 是否覆盖所有 Trust Boundary、Asset 和 Privacy Threat。

### 37.6 Governance and Response

- [ ] Supply Chain、Dependency、CVE、Artifact 和 Vendor 是否有 Owner。
- [ ] Security Monitoring 是否去敏、有 Runbook 和 No-Data 处理。
- [ ] Incident 是否与 SEV、IC、Security/Privacy Lead、Timeline、通知对齐。
- [ ] Audit 是否追加、防篡改、最小、可靠、受限访问。
- [ ] Compliance 适用性是否明确待法律确认并引用官方来源。
- [ ] ADR Matrix 是否覆盖重大安全/隐私变化。
- [ ] Beta/RC/GA Scope Freeze 是否继续生效。

---

## 38. Open Questions

### 38.1 Authentication and Identity

1. 用户认证采用何种标准协议、Password/Passwordless/联合身份组合。
2. 普通用户 MFA 是可选、风险触发还是强制；恢复如何不弱化。
3. Export/Delete/Recovery 的身份保证等级与 Step-Up 方式。
4. Anonymous Session 生命周期、设备信号和升级注册策略。
5. DeveloperClient 与 Workload Identity 的具体协议和 Credential 形式。

### 38.2 Session and Token

1. JWT、Opaque Token 或混合模式。
2. Access/Refresh/Session Idle/Absolute/Share Token 的正式期限。
3. Refresh Rotation、Reuse Detection 和 Revocation 传播 SLO。
4. Browser Token/Cookie Storage 与 CSRF/XSS 平衡。
5. 并发 Session、设备管理和异常登录通知规则。

### 38.3 Authorization

1. 最终 Role/Permission/Scope 矩阵与 Privileged Role 复审周期。
2. ABAC Policy Engine 是否需要独立技术能力，还是应用内受控 Policy。
3. Actor 处理他人 Birth Data 的授权证明和期限。
4. Support Unmask、Auditor、Security/Operations 的字段级视图。
5. Consent/Role/Policy Cache 最大 TTL 和撤销传播目标。

### 38.4 Encryption, Key and Secret

1. 哪些 Restricted Sensitive 字段需要应用/字段级加密。
2. KMS/HSM、Key Hierarchy、Region、Rotation 和 Recovery 技术方案。
3. Secret 最大寿命、双 Key 窗口和 Workload Identity 范围。
4. Audit/Object/Frozen Report 的完整性/签名机制。
5. Key 销毁与 Legal Hold/Backup/历史可读的协调。

### 38.5 Privacy and Consent

1. Birth/Chart/Report 在适用法律下的敏感个人信息分类结论。
2. 核心服务、第三方 AI、保存、优化、研究各自处理基础与 Consent 要求。
3. 用户保存他人命盘、代理和未成年人误入流程。
4. 匿名试算、Conversation、AI Provider、Logs/Traces 和 Audit 的保留期。
5. Export/Delete 时限、范围、Legal Hold 和 Backup 完成表述。
6. 去标识化研究/优化数据的重识别测试和撤回方案。

### 38.6 AI Security

1. 首批 Provider/Model 的地区、留存、训练禁用、Subprocessor 和备案状态。
2. Prompt/Model/Route 的安全评估集、阈值和人工 Red Team 频率。
3. 高风险健康/婚姻/投资主题的最终允许/拒绝边界。
4. 是否及何时允许任何 AI Tool；MVP 默认不允许任意 Tool。
5. AI 生成内容显式/隐式标识在在线、打印、PDF、分享中的实现要求。
6. Prompt Leakage/Injection 成功的 Incident Severity 与用户通知。

### 38.7 Monitoring and Incident

1. Security Log/Trace/Audit 保留期、访问和行为分析边界。
2. Security Incident 的通知阈值、时限、监管与用户流程。
3. JIT、Break-Glass、Access Review 和 Session Recording 的具体工具/周期。
4. Vulnerability Remediation SLA、Penetration/Red Team 周期。
5. Security Monitoring False Positive、No Data 和 Privacy Review 标准。

### 38.8 Compliance

1. 平台是否属于相关生成式 AI 服务、算法备案/登记或安全评估适用范围。
2. AI 生成合成内容标识办法与强制性标准对文本、打印、PDF、复制和分享的具体义务。
3. 网络安全等级保护、网络数据安全和事件报告义务的适用等级/范围。
4. 境外 AI/Cloud/Observability 的数据出境路径、阈值、影响评估和单独同意。
5. 知识版权、Consumer Protection、高风险内容和用户协议/隐私政策最终文本。

### 38.9 ADR Candidates

- ADR-CANDIDATE-SEC-001：用户/Staff/Developer/Workload Authentication 与 MFA。
- ADR-CANDIDATE-SEC-002：RBAC+ABAC Policy Decision/Enforcement 架构。
- ADR-CANDIDATE-SEC-003：Session、JWT/Opaque Token、Refresh 和 Revocation。
- ADR-CANDIDATE-SEC-004：Data Classification、字段加密、KMS 与 Key Hierarchy。
- ADR-CANDIDATE-SEC-005：Secret/Workload Identity、Rotation 和 Break-Glass。
- ADR-CANDIDATE-SEC-006：Consent Purpose、Retention、Export/Delete 和 Legal Hold。
- ADR-CANDIDATE-SEC-007：Audit Tamper Evidence、物理隔离、Retention 和 Forensics。
- ADR-CANDIDATE-SEC-008：AI Model Gateway、Prompt Defense、Output Gate 和 Tool Policy。
- ADR-CANDIDATE-SEC-009：Security Monitoring、Behavior Analytics、Retention 和 Incident Evidence。
- ADR-CANDIDATE-SEC-010：Cross-Border、AI Content Labeling 和 Compliance Control。

---

## 39. Risks

| Risk | Manifestation | Impact | Mitigation / Gate |
|---|---|---|---|
| Account Takeover | Credential Stuffing/Recovery Abuse | 用户敏感数据泄漏 | MFA/Rate Limit/Risk/Session Revoke |
| Authorization Bypass | IDOR、Role/Scope 错误 | 跨用户/租户访问 | Server RBAC+ABAC+Ownership、测试 |
| Super Admin Abuse | 永久全能权限 | Insider/误操作 | JIT、Separation、Masking、Audit |
| Long-Lived Credential | Token/Key 难撤销 | 长期入侵 | 短期、Rotation、Revocation、Scope |
| Birth Data Exposure | Log/Object/Support/Vendor 泄漏 | 高敏感隐私事件 | Classification、Encryption、Mask、Minimize |
| Re-identification | 去标识数据被组合识别 | 研究/供应商隐私风险 | Risk Test、Aggregation、Access、Consent |
| Consent Drift | 下游继续使用已撤回数据 | 未授权处理 | Source of Truth、Invalidate、Saga、Audit |
| Retention Creep | 默认长期保存 | 攻击面/法律风险 | Schedule、Expiry、Owner、Metrics |
| Delete Incomplete | Object/Index/Backup/Vendor 残留 | 用户权利和信任风险 | Saga、Tombstone、Verification、Manual Review |
| Audit Failure | 高风险操作无证据 | 调查/不可抵赖失败 | Reliable Audit、Block/Alert、DR |
| Key/Secret Leak | Source/CI/Log 暴露 | 全面系统/Provider 失陷 | Secret Manager、Scan、Rotate、Incident |
| Weak Recovery | 恢复绕过 MFA | Account Takeover | Step-Up、多信号、旧 Session 撤销 |
| Prompt Injection | 用户/知识操纵模型 | 泄漏、越权、错误内容 | Isolation、Tool Gate、Output Validation |
| Prompt Leakage | System/其他用户上下文输出 | 安全/隐私泄漏 | No Secrets、Context Isolation、Leak Scan |
| Jailbreak | 高风险绝对化/禁止内容 | 用户伤害/合规风险 | Policy、Evaluation、Rate Limit、Safe Refusal |
| AI Hallucination | 未验证输出进入 Report | 虚假事实/引用 | Fact/Evidence/Risk Gate、Freeze |
| Denial of Wallet | 自动化 AI 滥用 | 成本/可用性 | Quota、Rate Limit、Circuit、Budget |
| Vendor Cross-Border | 数据进入未批准地区 | 法律/隐私风险 | Data Flow、Contract、Minimize、Approval |
| Supply Chain Compromise | 恶意依赖/Artifact | 生产入侵 | Lock、SBOM、Signing、Isolation |
| CVE Backlog | 高风险漏洞超期 | 可利用攻击面 | SLA、Owner、Exception Expiry |
| Monitoring Blind Spot | No Data 显示正常 | 延迟发现 | Pipeline Health、Synthetic、No-Data Alert |
| Monitoring Overreach | 行为分析/日志过量 | 二次隐私风险 | PIA、Minimization、Retention、Access |
| TLS/Certificate Failure | 明文/过期/跳过验证 | MITM/不可用 | Lifecycle、Monitor、Fail Secure |
| SSRF | Callback/Tool 访问内网 | Secret/Metadata 泄漏 | Pre-register、Egress、IP/DNS Recheck |
| XSS | AI/Knowledge/User 内容执行 | Session/Data Theft | Encoding、Sanitize、CSP、No Raw HTML |
| Misclassified Data | Birth/Report 低等级保护 | 控制不足 | Conservative Default、Owner Review |
| Legal Change | 新标识/跨境/AI 规则未落实 | 上线/处罚风险 | Legal Inventory、Change Monitoring、Gate |
| Security Theater | 有工具无测试/Owner | 假安全感 | Verifiable Control、Metrics、Drill |

---

## 40. 进入下一阶段《13-AI-ARCHITECTURE.md》所需输入条件

- [ ] `12-SECURITY-PRIVACY.md` 已完成评审并成为 Approved 1.0 Security & Privacy Baseline。
- [ ] User、Subject、Actor、Client、Workload、Provider Identity 边界已确认。
- [ ] Authentication、MFA、Recovery、RBAC、ABAC、Ownership、Purpose 和 Consent 模型已确认。
- [ ] Session、Token/JWT 候选、Rotation、Revocation 和高风险 Step-Up 已批准或明确为 13/实施阻断项。
- [ ] API Rate Limit、WAF、CSRF、XSS、SSRF、SQLi、IDOR、File/Callback 安全原则已确认。
- [ ] Data Classification、PII、Masking、Encryption、Key/KMS、Secret 和 Workload Identity 已确认。
- [ ] SubjectConsent、ConsentRecord、Purpose、Withdrawal Propagation 和 Policy Version 已确认。
- [ ] Retention、Legal Hold、Export、Deletion、Backup Tombstone、Vendor 删除和用户状态已完成法律/隐私评审。
- [ ] Audit 必需事件、不可变/篡改证据、访问、Retention、Reliability 和 Forensics 已确认。
- [ ] Threat Model 的 Asset、Boundary、Threat、Risk Owner 和验证方法已确认。
- [ ] AI 只接收去标识化最小 Context、不计算事实、不建 Evidence、不扩大 Scope 的边界已确认。
- [ ] Prompt Injection/Leakage/Jailbreak、Retrieval、Tool、Output Validation 和 Model Abuse 防护已确认。
- [ ] Provider Region、Retention、Training、Subprocessor、Incident、备案/登记和内容标识事项已有法律结论或明确阻断。
- [ ] Supply Chain、Dependency、CVE、Security Monitoring、Incident 和 Privacy Governance 已确认。
- [ ] ADR Reference Matrix 中影响 AI Architecture 的决策已批准，或 13 继续保持候选而不改变基线。
- [ ] Beta、RC、GA Scope Freeze 继续生效。
- [ ] 下一阶段只生成 AI Architecture，不生成 Prompt、代码、模型配置、评测脚本、WAF/IAM/云配置或部署资产。

只有本安全与隐私架构通过评审后，才可以生成 `13-AI-ARCHITECTURE.md`。本次不得生成该文件，也不得进入编码阶段。

