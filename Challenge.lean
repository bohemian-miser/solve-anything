/-
Copyright (c) 2026 The solve-anything contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
-/
module

/-!
# Frozen Challenge Statement (`solve-anything` template)

This file is **FROZEN** and human-owned. Automated CI rejects any PR that modifies it.

To launch a collaborative swarm for ANY open conjecture:
1. Run `python3 scripts/init_problem.py --help` (or edit `problem.toml` and `Challenge.lean` directly).
2. Replace `Conjecture` below with your exact Lean 4 target statement — ideally using minimal
   core/standard definitions so any human or external checker can audit the statement by eye in
   10 seconds.
3. Freeze `Challenge.lean` on `main` (enforced automatically by `scripts/check_challenge_frozen.py`).

Both tracks target this single frozen file:
* **Track A (`<LeanRoot>/Prove/`):** Prove `Conjecture`.
* **Track B (`<LeanRoot>/Disprove/`):** Prove `Disproof` (`:= ¬ Conjecture`).
-/

@[expose] public section

namespace Problem

/-- **Placeholder predicate** — replace with your open conjecture's elementary definition. -/
def TargetProp (n : Nat) : Prop :=
  0 < n → n + 1 > n

/-- **Track A target (replace with your open conjecture):** every instance satisfies `TargetProp`. -/
def Conjecture : Prop :=
  ∀ n : Nat, TargetProp n

/-- **Track B target (disproof):** exact logical negation of `Conjecture`. -/
def Disproof : Prop :=
  ¬ Conjecture

end Problem
