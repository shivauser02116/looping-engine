#!/usr/bin/env python3
"""Looping Engine v1.3: bounded command evaluation and repair runner."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_TIMEOUT_SECONDS = 120
DEFAULT_MAX_ATTEMPTS = 1


@dataclass
class CheckResult:
    passed: bool
    message: str


@dataclass
class AttemptResult:
    attempt: int
    command: str
    exit_code: int | None
    duration_seconds: float
    stdout: str
    stderr: str
    checks: list[CheckResult] = field(default_factory=list)
    timed_out: bool = False

    @property
    def passed(self) -> bool:
        return (not self.timed_out) and all(check.passed for check in self.checks)

    def to_dict(self) -> dict[str, Any]:
        return {
            "attempt": self.attempt,
            "command": self.command,
            "exit_code": self.exit_code,
            "duration_seconds": round(self.duration_seconds, 3),
            "timed_out": self.timed_out,
            "passed": self.passed,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "checks": [check.__dict__ for check in self.checks],
        }


def load_cases(path: Path) -> list[dict[str, Any]]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Cases file not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc

    if isinstance(payload, dict):
        cases = payload.get("cases")
    else:
        cases = payload

    if not isinstance(cases, list):
        raise SystemExit("Cases payload must be a list or an object with a 'cases' list.")

    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise SystemExit(f"Case #{index} must be an object.")
        if not case.get("name"):
            raise SystemExit(f"Case #{index} is missing 'name'.")
        if not case.get("command"):
            raise SystemExit(f"Case '{case['name']}' is missing 'command'.")

    return cases


def run_command(command: str, cwd: Path, timeout_seconds: int) -> tuple[int | None, str, str, float, bool]:
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
        duration = time.perf_counter() - start
        return completed.returncode, completed.stdout, completed.stderr, duration, False
    except subprocess.TimeoutExpired as exc:
        duration = time.perf_counter() - start
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        return None, stdout, stderr, duration, True


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise SystemExit("Expected a string or list of strings in case assertions.")


def evaluate_case(case: dict[str, Any], repo_root: Path) -> dict[str, Any]:
    name = str(case["name"])
    command = str(case["command"])
    cwd = repo_root / str(case.get("cwd", "."))
    timeout_seconds = int(case.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS))
    max_attempts = int(case.get("max_attempts", DEFAULT_MAX_ATTEMPTS))
    expected_exit_code = int(case.get("expected_exit_code", 0))
    repair_command = case.get("repair_command")
    attempts: list[AttemptResult] = []

    if max_attempts < 1:
        raise SystemExit(f"Case '{name}' has invalid max_attempts: {max_attempts}")
    if not cwd.exists():
        raise SystemExit(f"Case '{name}' cwd does not exist: {cwd}")

    for attempt_number in range(1, max_attempts + 1):
        exit_code, stdout, stderr, duration, timed_out = run_command(command, cwd, timeout_seconds)
        result = AttemptResult(
            attempt=attempt_number,
            command=command,
            exit_code=exit_code,
            duration_seconds=duration,
            stdout=stdout,
            stderr=stderr,
            timed_out=timed_out,
        )

        result.checks.append(
            CheckResult(
                passed=(not timed_out),
                message="Command completed before timeout.",
            )
        )
        result.checks.append(
            CheckResult(
                passed=(exit_code == expected_exit_code),
                message=f"Expected exit code {expected_exit_code}, got {exit_code}.",
            )
        )

        for fragment in as_list(case.get("stdout_contains")):
            result.checks.append(
                CheckResult(
                    passed=(fragment in stdout),
                    message=f"stdout contains {fragment!r}.",
                )
            )

        for fragment in as_list(case.get("stderr_contains")):
            result.checks.append(
                CheckResult(
                    passed=(fragment in stderr),
                    message=f"stderr contains {fragment!r}.",
                )
            )

        for file_name in as_list(case.get("files_exist")):
            expected_path = repo_root / file_name
            result.checks.append(
                CheckResult(
                    passed=expected_path.exists(),
                    message=f"file exists: {file_name}",
                )
            )

        attempts.append(result)
        if result.passed:
            break

        if repair_command and attempt_number < max_attempts:
            run_command(str(repair_command), cwd, timeout_seconds)

    passed = attempts[-1].passed
    return {
        "name": name,
        "passed": passed,
        "attempts": [attempt.to_dict() for attempt in attempts],
    }


def build_report(cases: list[dict[str, Any]], repo_root: Path) -> dict[str, Any]:
    started_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    results = [evaluate_case(case, repo_root) for case in cases]
    passed = all(result["passed"] for result in results)
    return {
        "engine": "Looping Engine",
        "version": "1.3",
        "started_at": started_at,
        "passed": passed,
        "case_count": len(results),
        "results": results,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Looping Engine v1.3 evaluation runner")
    parser.add_argument("--cases", default="evals/test_cases.json", help="Path to evaluation cases JSON.")
    parser.add_argument("--report", default=None, help="Optional path to write the JSON report.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = Path.cwd()
    cases_path = (repo_root / args.cases).resolve()
    cases = load_cases(cases_path)
    report = build_report(cases, repo_root)
    indent = 2 if args.pretty else None
    output = json.dumps(report, indent=indent)

    if args.report:
        report_path = (repo_root / args.report).resolve()
        report_path.write_text(output + "\n", encoding="utf-8")

    print(output)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
