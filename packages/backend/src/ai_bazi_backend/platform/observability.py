import re
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from dataclasses import dataclass
from time import monotonic
from typing import Protocol
from uuid import uuid4

SAFE_IDENTIFIER = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
TRACEPARENT = re.compile(r"^[0-9a-f]{2}-([0-9a-f]{32})-[0-9a-f]{16}-[0-9a-f]{2}$")


@dataclass(frozen=True, slots=True)
class TraceContext:
    request_id: str
    correlation_id: str
    trace_id: str | None = None


_trace_context: ContextVar[TraceContext | None] = ContextVar("trace_context", default=None)


def new_identifier() -> str:
    return uuid4().hex


def accepted_identifier(candidate: str | None) -> str:
    if candidate and SAFE_IDENTIFIER.fullmatch(candidate):
        return candidate
    return new_identifier()


def trace_id_from_traceparent(traceparent: str | None) -> str | None:
    if traceparent is None:
        return None
    match = TRACEPARENT.fullmatch(traceparent.lower())
    if match is None or match.group(1) == "0" * 32:
        return None
    return match.group(1)


def current_trace_context() -> TraceContext | None:
    return _trace_context.get()


@contextmanager
def bind_trace_context(context: TraceContext) -> Iterator[None]:
    reset_handle: Token[TraceContext | None] = _trace_context.set(context)
    try:
        yield
    finally:
        _trace_context.reset(reset_handle)


class MetricsRecorder(Protocol):
    def increment(self, name: str, *, labels: dict[str, str] | None = None) -> None: ...

    def observe(
        self,
        name: str,
        value: float,
        *,
        labels: dict[str, str] | None = None,
    ) -> None: ...


class NullMetricsRecorder:
    def increment(self, name: str, *, labels: dict[str, str] | None = None) -> None:
        del name, labels

    def observe(
        self,
        name: str,
        value: float,
        *,
        labels: dict[str, str] | None = None,
    ) -> None:
        del name, value, labels


class InMemoryMetricsRecorder:
    """Deterministic recorder for tests and local diagnostics, not a metrics backend."""

    def __init__(self) -> None:
        self.counters: dict[tuple[str, tuple[tuple[str, str], ...]], int] = {}
        self.observations: dict[tuple[str, tuple[tuple[str, str], ...]], list[float]] = {}

    def increment(self, name: str, *, labels: dict[str, str] | None = None) -> None:
        key = (name, tuple(sorted((labels or {}).items())))
        self.counters[key] = self.counters.get(key, 0) + 1

    def observe(
        self,
        name: str,
        value: float,
        *,
        labels: dict[str, str] | None = None,
    ) -> None:
        key = (name, tuple(sorted((labels or {}).items())))
        self.observations.setdefault(key, []).append(value)


class Timer:
    def __init__(self) -> None:
        self._started = monotonic()

    @property
    def elapsed_seconds(self) -> float:
        return monotonic() - self._started


__all__ = [
    "MetricsRecorder",
    "InMemoryMetricsRecorder",
    "NullMetricsRecorder",
    "Timer",
    "TraceContext",
    "accepted_identifier",
    "bind_trace_context",
    "current_trace_context",
    "new_identifier",
    "trace_id_from_traceparent",
]
