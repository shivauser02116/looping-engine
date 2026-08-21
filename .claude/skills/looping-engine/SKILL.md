---
name: looping-engine
description: Runs any task through a strict 4-phase self-correcting cycle — Context Boundary & Acceptance Region, Execution & Drafting, Internal Audit, Exit Condition — instead of delivering a first-pass answer. Use whenever the user invokes "Looping Engine" by name, or asks for a high-stakes deliverable (spec, PRD, code, strategy doc, plan, pitch, hackathon submission) to be run through repeated draft-audit-refine cycles against explicit and inferred acceptance criteria. Capped at 3 iterations to prevent runaway refinement. Do not use for quick factual questions, casual conversation, or tasks where a single clean pass is obviously sufficient.
---
 
# Looping Engine (v1.3)
 
A self-auditing execution protocol. Every output is checked against criteria fixed *before* the draft exists, and revised up to 3 times if it fails that check. Phase 3 exists to find what's wrong with Phase 2's work — a pass on iteration 1 is only valid if it's actually true, not because a clean single pass is more convenient.
 
## Activation line
 
If invoked with no task attached yet, output **only**:
 
> Looping Engine v1.3 Active. Send task.
 
Nothing else. Wait for the task.
 
## Phase 1 — Context Boundary & Acceptance Region
 
1. Ingest the request.
2. Formulate the **Acceptance Region** in two tiers:
   - **Explicit Criteria** — direct requirements the user stated.
   - **Inferred Criteria** — baseline technical and operational standards required for completeness that the user didn't state but would expect (e.g. for code: handles empty input, no unhandled exceptions; for a document: internally consistent, no unsupported claims). Invent the strictest reasonable set for genuine gaps only — don't pad the list.
3. Display the Acceptance Region upfront, split into the two tiers. This is the one piece of the process that's always visible — without it the user can't judge whether a later "pass" was checked against something real.
4. If missing data or a logical contradiction makes execution impossible: output a **HALT** notice with the specific clarification question(s). Stop completely — no draft, no audit.
5. **Post-HALT re-entry:** once the user answers, merge the answer into the locked context boundary and jump directly to Phase 2. Do not re-evaluate ambiguity a second time — one clarification round only, then the boundary is locked regardless.
6. If nothing is missing, skip the HALT and proceed to Phase 2 in the same response.
## Phase 2 — Execution & Drafting
 
1. Select the optimal method to fulfill the locked context boundary.
2. Draft the solution internally — this and Phase 3 don't get printed turn-by-turn; the user sees the final draft plus the Engine Log, not a transcript of every attempt.
3. If a higher-efficiency alternative exists, isolate it into an **Alternatives Considered** section at the end of the response. It informs; it never silently replaces the requested approach.
## Phase 3 — Internal Audit
 
1. Audit the internal draft strictly against the Phase 1 Acceptance Region — both tiers, checked separately. Don't invent new criteria post-hoc; that moves the goalposts.
2. Log specific failures: missing components, logic flaws, or edge-case vulnerabilities.
3. Be exhaustive even when the draft looks clean — a rubber-stamp audit isn't an audit.
## Phase 4 — Exit Condition & Output Generation
 
Evaluate current iteration count (N) against the draft state, in this order:
 
1. **Explicit == PASS AND Inferred == PASS** → Exit Status: `CONVERGED`. Break loop.
2. **Explicit == PASS AND Inferred == FAIL AND N == 3** → Exit Status: `SAFETY_CAP_EXHAUSTED (Inferred Gap)`. Break loop. Output best available draft. Log unfulfilled inferred criteria.
3. **Explicit == FAIL AND N == 3** → Exit Status: `SAFETY_CAP_EXHAUSTED (Explicit Gap)`. Break loop. Output best available draft. Log the exact failed explicit criteria, why they failed, and what user input would be needed to resolve them.
4. **Criteria == FAIL (either tier) AND N < 3** → Increment N by 1. Pass the Phase 3 critique directly into Phase 2's execution context and regenerate the draft internally. This is the only branch that loops — an Inferred-only failure iterates too, it doesn't wait silently for the cap.
These four conditions are mutually exclusive and exhaustive across every (Explicit, Inferred, N) state — there is no unhandled combination.
 
### Output Standard
 
Render in this structure:
 
1. **[Final Refined Output]** — the deliverable itself, first.
2. **Alternatives Considered** — only if Phase 2 surfaced one; omit the heading if empty.
3. **Engine Log**:
   - Total Iterations: N
   - Exit Status: `CONVERGED` | `SAFETY_CAP_EXHAUSTED (Inferred Gap)` | `SAFETY_CAP_EXHAUSTED (Explicit Gap)`
   - Logged Failures / Unmet Criteria: specific items, why they failed, and (if Explicit Gap) what user input would resolve them — only populated when the safety cap was triggered.
Keep the log to an audit trail, not a second copy of the reasoning. If the user wants the full draft-by-draft transcript, they'll ask for it explicitly.
