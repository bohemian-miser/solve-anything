# `search/` — High-Speed Off-Kernel Search & Barrier Red-Teaming

Lean 4's kernel is the **judge**, not the search engine. Put fast off-kernel tools here (Python, Rust, C++, GPU, SAT/SMT, lattice reduction):

1. **Automated Barrier Red-Teaming (`Track A` immune system):**
   - Test candidate Track A conjectures, invariants, and bounds in milliseconds against known barrier variants and stress inputs *before* spending prover time formalizing a false lemma.
2. **Counterexample Hunting (`Track B` certificate emitter):**
   - Search structured danger zones at native speed; if a candidate counterexample is ever found, emit a compact Lean 4 certificate checked strictly by `<LeanRoot>/Disprove/Cert.lean` (zero `sorry`, zero `native_decide`).
3. **CI Integration (`search/ci_checks.sh`):**
   - `.github/workflows/verify.yml` automatically runs `search/ci_checks.sh` (configured via `problem.toml`). Keep CI smoke tests deterministic and fast (< 5 seconds).
