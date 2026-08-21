---
name: looping-engine
description: Run bounded build-evaluate-repair loops for coding, data, and hardware-adjacent validation tasks.
version: 1.3
---

# Looping Engine v1.3

Use this skill when a task benefits from repeated execution, evaluation, and targeted repair.

## Core Loop

1. Define the goal and the smallest evidence that proves it works.
2. Create or update an evaluation case in `evals/test_cases.json`.
3. Run `scripts/loop_runner.py` from the repository root.
4. Inspect the failing check, make the smallest necessary correction, and rerun.
5. Stop when the evaluation passes or the configured attempt limit is reached.

## Rules

- Keep each loop bounded with `max_attempts`.
- Prefer objective checks: exit code, output text, required files, and JSON report status.
- Make one correction per loop when practical.
- Do not hide failures. Preserve the final report and summarize remaining risk.
- For hardware-adjacent projects, include physical assumptions, tamper risks, and sensor failure modes in the evaluation notes.

## Command

```bash
python3 scripts/loop_runner.py --cases evals/test_cases.json --report loop-report.json
```

## Expected Case Shape

Each case can define:

- `name`: Human-readable case name.
- `command`: Command to execute.
- `cwd`: Optional working directory relative to the repository root.
- `timeout_seconds`: Optional command timeout.
- `max_attempts`: Optional loop limit.
- `expected_exit_code`: Expected process exit code.
- `stdout_contains`: Text fragments required in standard output.
- `stderr_contains`: Text fragments required in standard error.
- `files_exist`: Paths that must exist after execution.
- `repair_command`: Optional command to run after a failed attempt before retrying.
