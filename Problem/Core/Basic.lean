/-
Copyright (c) 2026 The solve-anything contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
module

public import Challenge

/-!
# Shared Core Definitions & Bridge Lemmas

Shared building blocks usable by **both** Track A (`Prove/`) and Track B (`Disprove/`):
- Equivalences and reductions between `Conjecture` and structured subgoals.
- Counterexample bridge lemmas reducing `Disproof` to a concrete witness.
- Formalized barrier counterexamples (nearby variants where the conjecture is FALSE) so Track A
  strategies can be red-teamed rigorously.
-/

public section

namespace Problem

/-- **Bridge Lemma (Track B):** exhibiting any counterexample `n` with `¬ TargetProp n` immediately
proves `Disproof`. -/
theorem disproof_of_counterexample {n : Nat} (h : ¬ TargetProp n) : Disproof :=
  fun hconj => h (hconj n)

end Problem
