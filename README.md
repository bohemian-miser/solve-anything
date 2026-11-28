# `solve-anything`

**Drop in any Lean 4 conjecture and turn this repository into an open-source, kernel-verified dual-track (`Prove` + `Disprove`) crowd-swarm.**

Click **"Use this template"** (or clone with `git remote add upstream` so you can pull future framework upgrades with `git merge upstream/main`), drop your open conjecture into frozen `Challenge.lean`, and get a complete multi-agent mathematical collaboration engine out of the box:

- **One frozen ground truth (`Challenge.lean` + `problem.toml`):** Both tracks target the exact same Lean 4 statement (`Conjecture`) and its negation (`Disproof := ¬ Conjecture`). CI rejects any PR that modifies frozen files, introduces `sorry`/`native_decide`/escape hatches, or depends on anything outside `[propext, Classical.choice, Quot.sound]`.
- **Dual-Track Architecture (Prove + Disprove in one repo):**
  - **Track A (`<LeanRoot>/Prove/`):** Proving `Conjecture`, standing on formalized literature (`<LeanRoot>/Known/`).
  - **Track B (`<LeanRoot>/Disprove/` + `search/`):** Hunting for a counterexample (`Disproof`) with fast off-kernel Python/Rust/C++/GPU/SAT engines whose hits compile into **Lean-kernel-verified certificates** (`Cert.lean`).
  - Shared lemmas in `Core/` and `Known/` compound value for *both* directions simultaneously.
- **Built-in Mathematical Immune System (`frontier/BARRIERS.md` + `frontier/REFUTED.md`):**
  - Formalize nearby false variants as barrier counterexamples so Track A ideas are red-teamed in milliseconds before burning proof compute.
  - Record dead ends permanently in `frontier/REFUTED.md` so fresh swarms never loop on disproved ideas.
- **Zero-Friction Swarm Coordination & Live Dashboard (GitHub Actions + Pages):**
  - **Hard Verification Gate (`verify.yml`):** `.elan`/`.lake` caching, frozen-file guard, source hygiene guard (`<= 50`-line proofs, `<= 100`-char lines), `lake build` (`warningAsError = true`), strict axiom audit, and problem-specific `search/ci_checks.sh`.
  - **Zero-Friction Claims Bot (`claims.yml`):** Any outside human or agent claims an open node by commenting `/claim <NODE_ID>` on the pinned **Frontier Claims** issue (24h auto-expiring TTL, zero push access required).
  - **Live Frontier Dashboard (`dashboard.yml`):** Auto-publishes an interactive dark-mode Frontier DAG + machine-readable `frontier.json` to GitHub Pages on every merge.
  - **5 Adversarial Review Rubrics (`review/`):** Parallel multi-agent review gates (`correctness`, `nontriviality`, `barrier-check`, `proof-quality`, `quality-pass` `Q1`–`Q5`) + sandboxed self-hosted reviewer/worker blueprint (`docs/SELF_HOSTED_AGENT.md`).

---

## Launch a New Conjecture in 60 Seconds

1. **Create your repo from this template** (or fork/clone with `upstream` pointing here so you can run `git merge upstream/main` for framework upgrades):
   ```bash
   git clone https://github.com/bohemian-miser/solve-anything.git solve-goldbach
   cd solve-goldbach
   git remote rename origin upstream
   ```
2. **Initialize your problem metadata and Lean root in one command:**
   ```bash
   python3 scripts/init_problem.py \
     --name solve-goldbach \
     --title "Goldbach Conjecture" \
     --lean-root Goldbach \
     --namespace SolveGoldbach \
     --tagline "Every even integer > 2 is the sum of two primes."
   ```
3. **Drop your exact conjecture into `Challenge.lean`** (using minimal definitions so any human can inspect it in 10 seconds), add your problem's known barriers to `frontier/BARRIERS.md`, seed open subgoals in `frontier/FRONTIER.toml`, and add a fast red-team/search hook in `search/ci_checks.sh`.
4. **Verify locally and push:**
   ```bash
   python3 scripts/check_all.py   # same steps as CI: frozen files, guards, build, axioms, search hook
   ```
5. **Enable GitHub Pages** (`Settings -> Pages -> GitHub Actions`), create the `claims` label + pinned **Frontier Claims** issue, and enable branch protection requiring `verify`.

---

## Live Instances Built on `solve-anything`

- **`bohemian-miser/solve-collatz`** — Dual-track crowd-swarm for the Collatz ($3n+1$) conjecture (with Lean-proved `3n-1`, `5n+1`, and `ℤ_{<0}` barriers, Diophantine cycle hunter, and kernel-verified `NontrivialCycleCert`).

---

## Repository Layout

| Path | Owned By | Role |
|---|---|---|
| `problem.toml` | Problem (FROZEN) | Single manifest driving all CI workflows, guards, and dashboard generation. |
| `Challenge.lean` | Problem (FROZEN) | Canonical statements (`Conjecture`, `Disproof := ¬ Conjecture`). CI blocks PR edits. |
| `<LeanRoot>/Core/` | Problem | Shared core lemmas, bridge theorems, and formalized barrier counterexamples. |
| `<LeanRoot>/Known/` | Problem | Formalized published literature usable by both Track A and Track B. |
| `<LeanRoot>/Prove/` | Problem | Track A (TRUE): competing proof strategies, each barrier-checked. |
| `<LeanRoot>/Disprove/` | Problem | Track B (FALSE): kernel-verified counterexample certificate checkers (`Cert.lean`). |
| `search/` | Problem | Fast off-kernel search engines & barrier red-teaming (`search/ci_checks.sh`). |
| `frontier/` | Problem | Living DAG (`FRONTIER.toml`), barrier catalog (`BARRIERS.md`), dead-end log (`REFUTED.md`). |
| `review/` | Framework | 5 adversarial review rubrics (`correctness`, `nontriviality`, `barrier-check`, `proof-quality`, `quality-pass`). |
| `scripts/` | Framework | `check_challenge_frozen.py`, `check_source_guards.py`, `build_dashboard.py`, `init_problem.py`, `check_all.py`, `audit_axioms.py`. |
| `.github/` | Framework | Zero-secret `verify.yml`, `claims.yml`, `dashboard.yml`, `label-pr.yml`, PR template. |
| `docs/` | Framework | `SELF_HOSTED_AGENT.md` — sandboxed two-plane server setup for autonomous review & 24/7 workers. |

---

## Acknowledgments

Built from hard-won lessons collaborating on `leanprover-community/riemann-hypothesis` (`AGENTS.md`, readability norms, non-module kernel auditing) and `TauCetiProject/TauCeti` (multi-rubric adversarial AI review, `Q1`–`Q5` quality passes, cooperative swarm claiming).
