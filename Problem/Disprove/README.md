# `Disprove/` — Track B (Proving `Disproof := ¬ Conjecture`)

Everything here works toward proving the frozen `Disproof` in `Challenge.lean`.

- `Cert.lean` defines the kernel-verified counterexample certificate interface so high-speed off-kernel search engines in `search/` only need to emit a compact certificate to produce a kernel-checked disproof.
- Never use `native_decide` or `Lean.ofReduceBool` to verify certificates.
- Ground all searches in published computational lower bounds so compute targets genuine danger zones.
