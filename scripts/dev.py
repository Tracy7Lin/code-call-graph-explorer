from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLE_REPO = REPO_ROOT / "fixtures" / "sample_repo"
SAMPLE_TARGET = SAMPLE_REPO / "pkg" / "main.py"


def run_command(argv: list[str]) -> int:
    completed = subprocess.run(argv, cwd=REPO_ROOT)
    return completed.returncode


def cmd_test() -> int:
    return run_command([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])


def cmd_serve_sample() -> int:
    return run_command(
        [
            sys.executable,
            "run.py",
            "--repo-root",
            str(SAMPLE_REPO),
            "--target-file",
            str(SAMPLE_TARGET),
        ]
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Developer helpers for the Python Call Graph Explorer.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("test", help="Run the full unit test suite.")
    subparsers.add_parser("serve-sample", help="Run the local app against the bundled sample repository.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "test":
        return cmd_test()
    if args.command == "serve-sample":
        return cmd_serve_sample()
    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
