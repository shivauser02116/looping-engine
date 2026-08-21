# Looping Engine (v1.3)

[![Agent Skill](https://img.shields.io/badge/Agent--Skill-Claude-purple.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A self-auditing execution protocol for Large Language Models (LLMs). The **Looping Engine** replaces single-pass generation with a 4-phase internal self-correcting loop. It enforces strict upfront **Acceptance Regions** (Explicit and Inferred criteria) and auto-corrects logical flaws up to a hard safety limit of 3 iterations.

---

## Operational Architecture

```text
  ┌─────────────────────────────────────────────────────────┐
  │ Phase 1: Context Boundary & Acceptance Region           │
  │ (Extract Explicit Criteria & Infer Baseline Standards)  │
  └──────────────────────────┬──────────────────────────────┘
                             │
                     [ Ambiguous Input? ] ─── YES ───► HALT & Clarify
                             │
                            NO
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │ Phase 2: Execution & Internal Drafting                  │
  └──────────────────────────┬──────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │ Phase 3: Internal Audit (Validate against Acceptance)   │
  └──────────────────────────┬──────────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────────┐
  │ Phase 4: Exit Condition & Output Generation             │
  │                                                         │
  │  IF All Pass               ──► Status: CONVERGED        │
  │  IF N < 3 & Criteria Fail  ──► Re-run Phase 2 (Loop)    │
  │  IF N = 3 & Criteria Fail  ──► Status: SAFETY_CAP_EXH   │
  └──────────────────────────┘
