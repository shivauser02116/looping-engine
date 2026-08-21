# Looping Engine v1.3

Looping Engine is a small, dependency-free evaluation runner for bounded build-evaluate-repair workflows. It is designed for coding tasks, data checks, and hardware-adjacent validation where every improvement should be backed by a repeatable test case.

## Repository Layout

```text
.claude/skills/looping-engine/SKILL.md
scripts/loop_runner.py
evals/test_cases.json
evals/hardware_tamper_case_study.md
README.md
```

## Quick Start

```bash
python3 scripts/loop_runner.py --cases evals/test_cases.json --report loop-report.json --pretty
```

The command exits with `0` when all cases pass and `1` when any case fails.

## Evaluation Cases

Cases are defined in JSON. A case can assert exit code, output text, required files, timeout behavior, and an optional repair command.

```json
{
  "name": "runner compiles under Python",
  "command": "python3 -m py_compile scripts/loop_runner.py",
  "timeout_seconds": 30,
  "max_attempts": 1,
  "expected_exit_code": 0
}
```

## Loop Policy

- Keep attempts bounded.
- Add the evaluation before relying on a fix.
- Make the smallest practical correction between attempts.
- Preserve the final report when a case still fails.

## Hardware-Adjacent Use

For Internet of Things and sensor workflows, place field-risk scenarios in `evals/` and include checks for operational metadata, not only normal-looking sensor values.
