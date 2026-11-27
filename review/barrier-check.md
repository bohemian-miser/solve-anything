# Rubric 3: Known-Barrier Red-Teaming

## Mission
Open conjectures accumulate graveyards of approaches that accidentally prove too much — arguments that would ALSO apply to closely related variants where the conjecture is **known to be false**.

This rubric enforces an explicit **barrier check** against `frontier/BARRIERS.md` and `frontier/REFUTED.md` on every Track A strategy and Track B heuristic claim.

## Mandatory Checks

1. **Barrier Survival Test (`[S0]` for Track A strategy claims)**
   - Read `frontier/BARRIERS.md` and any formalized barrier counterexamples in `<LeanRoot>/Core/`.
   - For EVERY Track A lemma/strategy claiming progress toward `Conjecture`, verify it explicitly identifies **where the argument breaks** on each relevant barrier in `frontier/BARRIERS.md`.
   - Reject any argument whose hypotheses hold verbatim on a known false variant.
2. **Negative Knowledge Base Check (`[S0]`/`[S1]`)**
   - Read `frontier/REFUTED.md`. Verify the PR is not repeating an already-refuted approach without explicitly fixing the falsified hypothesis and citing the prior `REF-*` entry.
3. **Automated Red-Team & Search Hook (`[S1]`)**
   - Verify `bash search/ci_checks.sh` passes cleanly.
   - If the PR proposes a new invariant, bound, or heuristic, require extending the problem's red-team script to stress-test it against barrier variants.
4. **Track B Search Realism (`[S1]`)**
   - For Track B (`Disprove/` and `search/`), verify that searches respect published computational lower bounds and target structured danger zones rather than redundant naive brute force.

## Output Format
Explicitly identify which barriers in `frontier/BARRIERS.md` apply and whether the argument genuinely clears them. Tag findings `[S0]`/`[S1]`/`[S2]` and emit `PASS` or `REQUEST CHANGES`.
