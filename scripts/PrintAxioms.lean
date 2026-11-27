import Problem

/-!
Verify that exported Track A / Track B core theorems depend ONLY on standard Lean axioms
(`propext`, `Classical.choice`, `Quot.sound`) — no `sorryAx`, no `Lean.ofReduceBool`.
-/

#print axioms Problem.disproof_of_counterexample
#print axioms Problem.Disprove.CounterexampleCert.disproves
