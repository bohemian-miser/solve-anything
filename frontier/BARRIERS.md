# Known Mathematical Barriers (`frontier/BARRIERS.md`)

Every serious open conjecture sits beside **barrier regimes** — closely related variants, relaxed domains, or weaker obstructions where the analogous statement is **FALSE** or **provably insufficient**. Any Track A (`Prove/`) argument that fails to distinguish the true conjecture from these false or obstructed regimes is automatically suspect.

## The Five-Tier Barrier Checklist (Mandatory for New Conjecture Forks)

When initializing a new conjecture, populate all five tiers below (`B1`–`B5`) and, wherever possible, **formalize concrete counterexample variants directly in Lean (`<LeanRoot>/Core/Barriers.lean`)** alongside a millisecond red-team script in `search/`:

| Tier | Barrier Class | Failure Mode / Obstruction | What a Valid Track A Proof Must Establish |
|---|---|---|---|
| **B1** | **Perturbed-Problem / Variant Counterexamples** | Nearby parameter, sign, coefficient, or boundary perturbations where the analogous statement is **FALSE**. | Pinpoint the exact structural property of the true conjecture that breaks in every false variant. |
| **B2** | **Density / Probabilistic-vs-Universal Obstruction** | "Almost-all", statistical, ergodic, or measure-1 arguments that cannot exclude zero-density or sparse counterexamples. | Supply a deterministic global mechanism ruling out thin exceptional sets (not merely positive/full density). |
| **B3** | **Domain-Boundary / Sign / Completion Counterexamples** | Counterexamples that emerge on enlarged or boundary domains (e.g., signed integers vs `ℕ⁺`, rationals/reals vs integers, degenerate base cases). | Explicitly invoke positivity, integrality, discreteness, or boundary side-conditions absent from the larger domain. |
| **B4** | **Local-vs-Global / Completion Obstructions** | Statements satisfied locally (modulo `m`, in `p`-adic completions `ℤ_p`, or by finite-state automata) where local counterexamples or dense periodic points still exist. | Combine local constraints with an archimedean, global integrality, or height-rigidity obstruction. |
| **B5** | **Computability / Finite-Horizon Limits** | Generalizations known to be undecidable, intractable, or unresolvable by bounded finite-horizon verification alone. | Isolate the exact specialization that escapes the undecidable class and cannot be proved by purely syntactic/uniform schemas. |

## How Swarms Must Use This File

1. **Formalize witnesses in Core:** Prove concrete `B1`/`B3` counterexamples in `<LeanRoot>/Core/Barriers.lean` (zero `sorry`, zero `native_decide`) and audit them in `scripts/PrintAxioms.lean`.
2. **Red-team before proving:** Run `bash search/ci_checks.sh` (and any problem-specific red-team harness in `search/`) against proposed invariants, bounds, or predicates *before* spending Lean prover compute.
3. **Require explicit disposition in PRs:** Every Track A PR's `Quality pass: Q3` MUST state which tiers (`B1`–`B5`) apply and exactly where the argument fails on the excluded barrier regimes.
