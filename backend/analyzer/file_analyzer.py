from __future__ import annotations

import ast
from pathlib import Path

from backend.analyzer.collector import CallCollector
from backend.common.models import CallEdge, FileGraph, Symbol
from backend.indexer.symbol_index import SymbolIndex


def analyze_file(repo_root: Path, target_file: Path, symbol_index: SymbolIndex) -> FileGraph:
    repo_root = Path(repo_root).resolve()
    target_file = Path(target_file).resolve()
    rel_path = symbol_index.rel_path(target_file)
    source = target_file.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(target_file))
    local_symbols = symbol_index.symbols_for_file(rel_path)
    local_symbol_ids = {symbol.symbol_id for symbol in local_symbols if symbol.symbol_type in {"function", "method"}}
    nodes_by_id: dict[str, Symbol] = {symbol.symbol_id: symbol for symbol in local_symbols if symbol.symbol_type != "class"}
    edges: list[CallEdge] = []
    unresolved_ids: list[str] = []
    local_functions = {symbol.name: symbol.symbol_id for symbol in local_symbols if symbol.symbol_type == "function"}
    local_classes = {symbol.name: symbol.symbol_id for symbol in local_symbols if symbol.symbol_type == "class"}

    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            caller_id = f"{rel_path}::{node.name}"
            collector = CallCollector(symbol_index, rel_path, local_functions, local_classes, None)
            function_edges = collector.collect(node, caller_id)
            for edge in function_edges:
                edges.append(edge)
                if not edge.resolved:
                    if edge.status == "unresolved":
                        unresolved_ids.append(edge.callee_id)
                    nodes_by_id.setdefault(
                        edge.callee_id,
                        make_uncertain_symbol(edge.callee_id, rel_path, edge.line, edge.call_expr, edge.status),
                    )
                else:
                    nodes_by_id.setdefault(edge.callee_id, symbol_index.get_symbol(edge.callee_id))
        elif isinstance(node, ast.ClassDef):
            class_id = f"{rel_path}::{node.name}"
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    caller_id = f"{rel_path}::{node.name}.{child.name}"
                    collector = CallCollector(symbol_index, rel_path, local_functions, local_classes, class_id)
                    function_edges = collector.collect(child, caller_id)
                    for edge in function_edges:
                        edges.append(edge)
                        if not edge.resolved:
                            if edge.status == "unresolved":
                                unresolved_ids.append(edge.callee_id)
                            nodes_by_id.setdefault(
                                edge.callee_id,
                                make_uncertain_symbol(edge.callee_id, rel_path, edge.line, edge.call_expr, edge.status),
                            )
                        else:
                            nodes_by_id.setdefault(edge.callee_id, symbol_index.get_symbol(edge.callee_id))

    center_ids = sorted(local_symbol_ids)
    return FileGraph(
        center_file=rel_path,
        center_symbol_ids=center_ids,
        nodes=list(nodes_by_id.values()),
        edges=edges,
        unresolved_ids=unresolved_ids,
    )


def make_uncertain_symbol(symbol_id: str, file_path: str, line: int, expr: str, status: str) -> Symbol:
    return Symbol(
        symbol_id=symbol_id,
        name=expr,
        qualname=expr,
        file_path=file_path,
        start_line=line,
        end_line=line,
        signature=expr,
        symbol_type="ambiguous" if status == "ambiguous" else "unresolved",
        docstring=None,
        source="",
    )
