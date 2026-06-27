# app/agents/base.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import perf_counter
from typing import Any, Callable, Protocol


class AgentStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    WARNING = "warning"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class AgentIssue:
    code: str
    message: str
    severity: str = "warning"
    field: str | None = None


@dataclass
class AgentContext:
    request_text: str
    language: str = "auto"
    material: str = "PLA"
    quality_mode: str = "production"
    printer: str = "Bambu Lab A1"
    nozzle_mm: float = 0.4
    data: dict[str, Any] = field(default_factory=dict)
    assumptions: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    trace: list[dict[str, Any]] = field(default_factory=list)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def add_warning(self, message: str) -> None:
        if message not in self.warnings:
            self.warnings.append(message)

    def add_error(self, message: str) -> None:
        if message not in self.errors:
            self.errors.append(message)

    def add_assumption(self, message: str) -> None:
        if message not in self.assumptions:
            self.assumptions.append(message)


@dataclass
class AgentResult:
    name: str
    status: AgentStatus
    output: dict[str, Any] = field(default_factory=dict)
    issues: list[AgentIssue] = field(default_factory=list)
    elapsed_ms: float = 0.0

    @property
    def ok(self) -> bool:
        return self.status in {AgentStatus.PASSED, AgentStatus.WARNING, AgentStatus.SKIPPED}


class Agent(Protocol):
    name: str

    def run(self, context: AgentContext) -> AgentResult:
        ...


def run_agent(name: str, context: AgentContext, fn: Callable[[AgentContext], dict[str, Any]]) -> AgentResult:
    started = perf_counter()
    try:
        output = fn(context)
        status = AgentStatus.WARNING if context.warnings and not context.errors else AgentStatus.PASSED
        result = AgentResult(name=name, status=status, output=output)
    except Exception as exc:
        context.add_error(f"{name} failed: {exc}")
        result = AgentResult(
            name=name,
            status=AgentStatus.FAILED,
            issues=[AgentIssue(code="agent_exception", message=str(exc), severity="error")],
        )
    result.elapsed_ms = round((perf_counter() - started) * 1000, 3)
    context.trace.append(
        {
            "agent": result.name,
            "status": result.status.value,
            "elapsed_ms": result.elapsed_ms,
            "issues": [issue.__dict__ for issue in result.issues],
            "output_keys": sorted(result.output.keys()),
        }
    )
    return result
