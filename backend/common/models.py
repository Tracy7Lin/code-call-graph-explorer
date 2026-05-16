from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Symbol:
    symbol_id: str
    name: str
    qualname: str
    file_path: str
    start_line: int
    end_line: int
    signature: str
    symbol_type: str
    class_name: str | None = None
    docstring: str | None = None
    source: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CallEdge:
    edge_id: str
    caller_id: str
    callee_id: str
    call_expr: str
    line: int
    confidence: str
    resolved: bool
    cross_file: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NodeInsight:
    summary: str
    responsibilities: list[str]
    side_effects: list[str]
    suggested_next_nodes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NodeDetail:
    symbol: Symbol
    callers: list[str]
    callees: list[str]
    insight: NodeInsight | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "symbol": self.symbol.to_dict(),
            "callers": self.callers,
            "callees": self.callees,
            "insight": self.insight.to_dict() if self.insight else None,
        }
        return payload


@dataclass(frozen=True)
class FileGraph:
    center_file: str
    center_symbol_ids: list[str]
    nodes: list[Symbol]
    edges: list[CallEdge]
    unresolved_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "center_file": self.center_file,
            "center_symbol_ids": self.center_symbol_ids,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "unresolved_ids": self.unresolved_ids,
        }


@dataclass(frozen=True)
class FileGraphDelta:
    symbol_id: str
    nodes: list[Symbol]
    edges: list[CallEdge]
    unresolved_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol_id": self.symbol_id,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "unresolved_ids": self.unresolved_ids,
        }
