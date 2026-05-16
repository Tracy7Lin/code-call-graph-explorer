from __future__ import annotations

from pathlib import Path

from backend.app.pipeline import AnalysisPipeline
from backend.common.models import AdvisorySuggestion, FileGraph, FileGraphDelta, NodeDetail, NodeInsight, Symbol


class ExplorerService:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.pipeline = AnalysisPipeline(self.repo_root)
        self.symbol_index = self.pipeline.symbol_index
        self.graph_cache: dict[str, FileGraph] = {}

    def analyze_file(self, target_file: Path) -> FileGraph:
        target_file = Path(target_file).resolve()
        rel_path = self.symbol_index.rel_path(target_file)
        cached = self.graph_cache.get(rel_path)
        if cached:
            return cached
        graph = self.pipeline.analyze_file(target_file)
        self.graph_cache[rel_path] = graph
        return graph

    def get_node_detail(self, symbol_id: str, with_llm: bool) -> NodeDetail:
        symbol = self.symbol_index.get_symbol(symbol_id)
        graph = self.analyze_file(self.repo_root / symbol.file_path)
        inbound_edges = [edge for edge in graph.edges if edge.callee_id == symbol_id]
        outbound_edges = [edge for edge in graph.edges if edge.caller_id == symbol_id]
        callers = [edge.caller_id for edge in inbound_edges]
        callees = [edge.callee_id for edge in outbound_edges]
        insight = self._build_insight(symbol, callees) if with_llm else None
        advisory_suggestions = self._build_advisory_suggestions(outbound_edges) if with_llm else []
        return NodeDetail(
            symbol=symbol,
            callers=callers,
            callees=callees,
            inbound_edges=inbound_edges,
            outbound_edges=outbound_edges,
            advisory_suggestions=advisory_suggestions,
            insight=insight,
        )

    def expand_node(self, symbol_id: str) -> FileGraphDelta:
        symbol = self.symbol_index.get_symbol(symbol_id)
        graph = self.analyze_file(self.repo_root / symbol.file_path)
        nodes = [node for node in graph.nodes if node.symbol_id != symbol_id]
        relevant_ids = {node.symbol_id for node in nodes}
        edges = [
            edge
            for edge in graph.edges
            if edge.caller_id == symbol_id or edge.callee_id == symbol_id or edge.callee_id in relevant_ids
        ]
        unresolved_ids = [node.symbol_id for node in nodes if node.symbol_type == "unresolved"]
        return FileGraphDelta(symbol_id=symbol_id, nodes=nodes, edges=edges, unresolved_ids=unresolved_ids)

    def _build_insight(self, symbol: Symbol, callees: list[str]) -> NodeInsight:
        summary = symbol.docstring or f"{symbol.qualname} appears to coordinate {len(callees)} downstream call(s)."
        responsibilities = [f"Defined in {symbol.file_path}:{symbol.start_line}"]
        if callees:
            responsibilities.append(f"Calls {len(callees)} other symbol(s)")
        side_effects = []
        if "return " in symbol.source:
            side_effects.append("Returns a computed value")
        if "open(" in symbol.source or "write(" in symbol.source:
            side_effects.append("Touches I/O")
        suggested = callees[:3]
        return NodeInsight(
            summary=summary,
            responsibilities=responsibilities,
            side_effects=side_effects,
            suggested_next_nodes=suggested,
        )

    def _build_advisory_suggestions(self, outbound_edges: list) -> list[AdvisorySuggestion]:
        suggestions: list[AdvisorySuggestion] = []
        for edge in outbound_edges:
            if edge.status not in {"unresolved", "ambiguous"}:
                continue
            summary = (
                f"Static analysis could not confirm `{edge.call_expr}` because `{edge.reason}`."
                if edge.status == "unresolved"
                else f"`{edge.call_expr}` has multiple plausible targets under static analysis."
            )
            suggestions.append(
                AdvisorySuggestion(
                    edge_status=edge.status,
                    call_expr=edge.call_expr,
                    reason=edge.reason,
                    summary=summary,
                    candidate_symbol_ids=edge.candidate_symbol_ids,
                )
            )
        return suggestions
