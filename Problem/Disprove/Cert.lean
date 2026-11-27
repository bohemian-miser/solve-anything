/-
Copyright (c) 2026 The solve-anything contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
module

public import Problem.Core.Basic

/-!
# Formal Counterexample Certificate Verifier (Track B: `Disprove/`)

Lean's kernel is the **judge**, not the search engine. Fast off-kernel search tools in `search/`
(Python, Rust, C++, GPU, SAT/SMT) hunt for counterexamples and emit compact certificates checked
directly by Lean's kernel here (with zero `sorry` and zero `native_decide`).
-/

@[expose] public section

namespace Problem.Disprove

/-- A self-contained kernel-verified counterexample certificate for `Problem.Conjecture`. -/
structure CounterexampleCert where
  /-- Concrete witness input. -/
  witness : Nat
  /-- Kernel-checked proof that `TargetProp witness` fails. -/
  refutes : ¬ TargetProp witness

/-- Any valid `CounterexampleCert` proves `Problem.Disproof` in Lean's kernel. -/
theorem CounterexampleCert.disproves (c : CounterexampleCert) : Disproof :=
  disproof_of_counterexample c.refutes

end Problem.Disprove
