import Problem

/-!
# Kernel Axiom Audit (`scripts/PrintAxioms.lean`)

Every exported Track A (`Prove/`) and Track B (`Disprove/`) theorem — as well as all shared
`Core/` and `Known/` results — MUST depend ONLY on Lean's standard foundational axioms:

  `[propext, Classical.choice, Quot.sound]`

Forbidden in all exported theorems (enforced by `.github/workflows/verify.yml` and
`scripts/check_source_guards.py`):
- `sorryAx` (`sorry` / `admit`)
- `Lean.ofReduceBool` (`native_decide`)
- `Lean.trustCompiler`
- Custom `axiom` declarations, `@[implemented_by]`, `@[extern]`, or `unsafe` escape hatches

Downstream problem repositories should list every exported flagship theorem, certificate verifier,
and formalized barrier theorem below so CI audits them automatically on every PR.
-/

#print axioms Problem.disproof_of_counterexample
#print axioms Problem.Disprove.CounterexampleCert.disproves
