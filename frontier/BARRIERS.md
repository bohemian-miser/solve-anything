# Known Mathematical Barriers (`frontier/BARRIERS.md`)

Every serious open conjecture has **relativization / variant barriers** — closely related problems where the analogous statement is **FALSE**. Any Track A (`Prove/`) argument that fails to distinguish the true problem from these false variants is automatically suspect.

## How to Use This File (When Initializing a New Conjecture)

List 3–6 concrete barriers for your problem and, wherever possible, **formalize the counterexample variants directly in Lean (`<LeanRoot>/Core/Barriers.lean`)** plus an automated millisecond red-team script in `search/`:

| Barrier | Nearby Variant / Obstruction | Known Failure / Counterexample | What a Valid Track A Proof Must Use |
|---|---|---|---|
| **B1 (Variant counterexample)** | *(Replace with a natural perturbed version of your conjecture that is false)* | *(Concrete Lean-verified counterexample)* | *(Exact property of the true conjecture broken in B1)* |
| **B2 (Density / heuristic barrier)** | *(Almost-all / probabilistic / local-only methods that cannot rule out sparse counterexamples)* | *(Sparse or local counterexamples)* | *(Global / rigid obstruction)* |
| **B3 (Known impossibility / undecidability)** | *(Generalization known to be undecidable or false)* | *(Published theorem)* | *(Exact specialization avoiding the general class)* |

See `bohemian-miser/solve-collatz` for a complete worked example (`3n - 1` cycle at `5`, `5n + 1` cycle at `13`, `ℤ_{<0}` cycle at `-5`, `ℤ₂` rational periodic points, and Conway undecidability).
