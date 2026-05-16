from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from backend.app.service import ExplorerService


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


class ExplorerRequestHandler(BaseHTTPRequestHandler):
    service: ExplorerService | None = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._serve_file(FRONTEND_DIR / "index.html", "text/html; charset=utf-8")
            return
        if parsed.path == "/app.js":
            self._serve_file(FRONTEND_DIR / "app.js", "application/javascript; charset=utf-8")
            return
        if parsed.path == "/styles.css":
            self._serve_file(FRONTEND_DIR / "styles.css", "text/css; charset=utf-8")
            return
        if parsed.path == "/api/graph":
            self._handle_graph(parsed.query)
            return
        if parsed.path == "/api/node":
            self._handle_node(parsed.query)
            return
        if parsed.path == "/api/expand":
            self._handle_expand(parsed.query)
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def log_message(self, format: str, *args: object) -> None:
        return None

    def _handle_graph(self, query: str) -> None:
        params = parse_qs(query)
        target_file = self._required(params, "target_file")
        repo_root = params.get("repo_root", [None])[0]
        service = self._service_for(repo_root)
        graph = service.analyze_file(Path(target_file))
        self._write_json(graph.to_dict())

    def _handle_node(self, query: str) -> None:
        params = parse_qs(query)
        symbol_id = self._required(params, "symbol_id")
        with_llm = params.get("with_llm", ["0"])[0] == "1"
        detail = self._service_for(None).get_node_detail(symbol_id, with_llm)
        self._write_json(detail.to_dict())

    def _handle_expand(self, query: str) -> None:
        params = parse_qs(query)
        symbol_id = self._required(params, "symbol_id")
        delta = self._service_for(None).expand_node(symbol_id)
        self._write_json(delta.to_dict())

    def _service_for(self, repo_root: str | None) -> ExplorerService:
        if repo_root and (self.service is None or self.service.repo_root != Path(repo_root).resolve()):
            type(self).service = ExplorerService(Path(repo_root))
        if self.service is None:
            raise ValueError("Service not configured")
        return self.service

    def _required(self, params: dict[str, list[str]], name: str) -> str:
        value = params.get(name, [None])[0]
        if not value:
            raise ValueError(f"Missing required query parameter: {name}")
        return value

    def _serve_file(self, path: Path, content_type: str) -> None:
        body = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _write_json(self, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the Python Code Call Graph Explorer.")
    parser.add_argument("--repo-root", required=True, help="Repository root to analyze")
    parser.add_argument("--target-file", required=True, help="Initial file to analyze")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    ExplorerRequestHandler.service = ExplorerService(Path(args.repo_root))
    server = ThreadingHTTPServer((args.host, args.port), ExplorerRequestHandler)
    print(f"Serving explorer on http://{args.host}:{args.port}")
    print(f"Initial graph target: {args.target_file}")
    server.serve_forever()
