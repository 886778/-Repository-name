# M1 Platform Foundation

## Scope

M1 establishes technical platform boundaries only. It contains no Bazi calculation, rules,
evidence, AI, identity, payment, report, business schema, repository, prompt, or provider code.
The approved documents 01–17 remain the architecture baseline.

## Runtime composition

- `apps/api` is the HTTP composition root. It owns FastAPI middleware, safe Problem Details,
  request/correlation identifiers, health endpoints, and runtime startup/shutdown.
- `apps/worker` is the process composition root. It owns signal handling and delegates ordered
  startup and reverse-order graceful shutdown to the platform worker framework.
- `packages/backend/platform` contains technical ports and replaceable adapters. Domain modules
  must not import runtime composition or adapter details.
- `packages/backend/bootstrap` validates settings and wires only enabled dependencies.

## Configuration and secrets

Configuration is typed, validated at startup, and sourced from the process environment. Local and
test environments may run with PostgreSQL and Redis disabled. Staging and production fail closed
without PostgreSQL and an explicit release identifier. Connection URLs are excluded from object
representations and must never be logged. `.env.example` contains names only; real values remain in
an approved secret store or ignored local environment file.

## Logging and observability

Logs are structured JSON with service, environment, release, event name, safe result/error fields,
and validated RequestId/CorrelationId. Known credential patterns are redacted at emission. Logs,
metrics, traces, audit, and domain events remain separate concepts. The metrics port uses bounded,
non-sensitive labels; a null adapter is the safe default until an observability backend is approved.

## API base and errors

The public platform surface remains limited to `/health/live` and `/health/ready`. All responses
carry accepted RequestId and CorrelationId values plus baseline safety headers. Errors map to safe
Problem Details and stable `SYSTEM-*` codes; stack traces and dependency details are never returned.
Liveness never probes dependencies. PostgreSQL is readiness-critical when configured; Redis is
degradable and therefore does not independently make the API unready.

## PostgreSQL boundary

M1 provides a bounded async connection pool, health probe, explicit transaction context, timeouts,
startup, and graceful shutdown. It creates no tables and executes no startup migration. The driver
adapter is infrastructure-only and cannot enter Domain or Application contracts.

The ORM, migration framework, persistence mapping, Repository implementation, schema ownership,
Outbox/Inbox schema, and field-level encryption remain gated by the approved ADR process. No choice
in M1 changes Aggregate, Data Model, transaction semantics, or immutable-object rules.

## Redis boundary

The cache contract exposes byte-oriented get/set/delete operations with mandatory positive TTL and
bounded opaque namespaced keys. The disabled adapter is a safe cache miss. Redis is never a source
of truth, never carries authorization by itself, and cannot be used to recover formal state.

## Worker boundary

The worker framework manages lifecycle components only. It contains no broker, scheduler, handler,
retry, task payload, Outbox/Inbox, or business dispatch. Broker and task-framework selection remains
an M4 decision.

## Failure behavior

| Condition                      | Behavior                                                |
| ------------------------------ | ------------------------------------------------------- |
| Invalid required configuration | Fail startup with a safe configuration error            |
| PostgreSQL startup failure     | Fail startup; do not accept formal traffic              |
| PostgreSQL health failure      | Readiness returns not ready                             |
| Redis failure                  | Cache miss/degraded signal; readiness remains available |
| Partial component startup      | Stop already-started components in reverse order        |
| Unhandled API exception        | Safe 500 Problem Details and correlated internal log    |

## Verification

- Unit tests cover configuration fail-closed rules, redaction, identifiers, Problem Details,
  readiness semantics, cache-key safety, and worker cleanup.
- Architecture tests continue to prevent API/Worker cross-imports and Domain module dependence on
  platform adapters.
- CI performs locked installs, format, lint, strict typing, tests with coverage, architecture checks,
  and the Web build.

## Deferred gates

- ORM/Migration/Repository/Unit of Work combination: ADR required before persistence mapping.
- Field-level encryption scope: security decision required before sensitive fields are persisted.
- Broker and task framework: M4 decision; no broker is introduced here.
- Observability backend/vendor and formal SLO values: remain open governance decisions.
