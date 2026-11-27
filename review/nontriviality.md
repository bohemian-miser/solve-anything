# Rubric 2: Nontriviality & Genuine Frontier Progress

## Mission
Prevent progress theater: PRs that restate the conjecture in slightly different notation, prove elementary tautologies while claiming a frontier milestone, or churn code without advancing the DAG.

## Mandatory Checks

1. **Non-Equivalence / Genuine Reduction Test (`[S0]`/`[S1]`)**
   - If a Track A PR introduces a new intermediate conjecture or reduction `H -> Conjecture`, ask: *is `H` strictly easier or structurally richer than `Conjecture`, or is `H` just a disguised restatement?*
   - Trivial re-encodings belong in `Core/` ONLY if actually reused by downstream theorems — never as a frontier breakthrough.
2. **Frontier DAG Accounting (`[S1]`)**
   - Every PR MUST name the exact `frontier/FRONTIER.toml` node(s) it advances, closes, or refutes.
   - If a PR closes a node, verify the Lean theorem matches the node's mathematical target — not a weakened toy special case.
   - If an attempted approach fails, **negative results are valuable** — require a crisp, witness-backed entry in `frontier/REFUTED.md` rather than dead code.
3. **No Slop or Fake Diff Churn (`[S1]`)**
   - Reject PRs that add unused helper lemmas, duplicate existing/Mathlib lemmas under new names, or golf clear proofs into unreadable one-liners.
4. **Honest Scope & Attribution (`[S1]`)**
   - For `Known/`, cite the exact paper/theorem and clearly state any remaining dependencies or hypotheses.

## Output Format
Tag each finding `[S0]`/`[S1]`/`[S2]` with `file:line`, verify the frontier node delta, and conclude with `PASS` or `REQUEST CHANGES`.
