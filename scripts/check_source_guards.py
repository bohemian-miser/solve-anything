#!/usr/bin/env python3
"""Hard CI source hygiene guard for all `.lean` files under `<lean_root>/` from `problem.toml`."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import tempfile
import tomllib

FORBIDDEN = [
    (re.compile(r"\bsorry\b"), "sorry"),
    (re.compile(r"\badmit\b"), "admit"),
    (re.compile(r"\baxiom\b"), "axiom"),
    (re.compile(r"\bnative_decide\b"), "native_decide"),
    (re.compile(r"\bLean\.ofReduceBool\b"), "Lean.ofReduceBool"),
    (re.compile(r"\bLean\.trustCompiler\b"), "Lean.trustCompiler"),
    (re.compile(r"\bimplemented_by\b"), "implemented_by"),
    (re.compile(r"\bextern\b"), "extern"),
    (re.compile(r"\bset_option\b"), "set_option"),
    (re.compile(r"\berw\b"), "erw"),
    (re.compile(r"\b(?:meta|unsafe)\b"), "meta/unsafe"),
    (re.compile(r"\brun_tac\b|\brun_cmd\b|\bby_elab\b"), "metaprogramming escape hatch"),
]
DECL_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)*(?:(?:public|private|protected|noncomputable|partial)\s+)*"
    r"(?:lemma|theorem|def)\s+(\S+)"
)


def load_config(root_dir: pathlib.Path = pathlib.Path(".")) -> tuple[pathlib.Path, int, int, int]:
    """Load Lean source root and guard limits from `problem.toml`."""
    cfg_path = root_dir / "problem.toml"
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    lean_root_cfg = pathlib.Path(cfg.get("problem", {}).get("lean_root", "Problem"))
    lean_root = lean_root_cfg if lean_root_cfg.is_absolute() else (root_dir / lean_root_cfg)
    guards = cfg.get("guards", {})
    return (
        lean_root,
        int(guards.get("max_line_length", 100)),
        int(guards.get("max_file_lines", 1000)),
        int(guards.get("max_proof_lines", 50)),
    )


def _strip_line_comments_and_strings(
    line: str, comment_depth: int, in_string: bool
) -> tuple[str, int, bool, bool]:
    """Strip Lean comments, mask string bodies, and report any `"` inside comments."""
    out: list[str] = []
    quote_in_comment = False
    i = 0
    n = len(line)
    while i < n:
        if comment_depth > 0:
            if line[i] == '"':
                quote_in_comment = True
            if line[i : i + 2] == "/-":
                comment_depth += 1
                i += 2
                continue
            if line[i : i + 2] == "-/":
                comment_depth -= 1
                i += 2
                continue
            i += 1
            continue

        if in_string:
            if line[i] == "\\":
                if i + 1 < n:
                    out.append("  ")
                    i += 2
                else:
                    out.append(" ")
                    i += 1
                continue
            if line[i] == '"':
                in_string = False
                out.append('"')
                i += 1
                continue
            out.append(" ")
            i += 1
            continue

        if line[i] == '"':
            in_string = True
            out.append('"')
            i += 1
            continue
        if line[i : i + 2] == "--":
            if '"' in line[i:]:
                quote_in_comment = True
            break
        if line[i : i + 2] == "/-":
            comment_depth += 1
            i += 2
            continue
        out.append(line[i])
        i += 1
    return "".join(out), comment_depth, in_string, quote_in_comment


def check_file(
    path: pathlib.Path, max_line_len: int, max_file_lines: int, max_proof_lines: int
) -> list[str]:
    """Check a single Lean file against line/file/proof caps and forbidden escape hatches."""
    errs: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) > max_file_lines:
        errs.append(f"{path}: {len(lines)} lines exceeds {max_file_lines}-line limit")

    comment_depth = 0
    in_string = False
    cur_decl: tuple[str, int] | None = None

    for idx, line in enumerate(lines, 1):
        if len(line) > max_line_len:
            errs.append(f"{path}:{idx}: line length {len(line)} > {max_line_len}")

        code_part, comment_depth, in_string, quote_in_comment = _strip_line_comments_and_strings(
            line, comment_depth, in_string
        )
        if quote_in_comment:
            errs.append(f"{path}:{idx}: double quote inside comment/docstring")

        if not code_part.strip():
            continue

        for pat, label in FORBIDDEN:
            if pat.search(code_part):
                errs.append(f"{path}:{idx}: forbidden construct `{label}`")

        m = DECL_RE.match(code_part)
        if m:
            if cur_decl is not None:
                dname, dstart = cur_decl
                if idx - dstart > max_proof_lines:
                    errs.append(
                        f"{path}:{dstart}: `{dname}` spans {idx - dstart} lines (> {max_proof_lines})"
                    )
            cur_decl = (m.group(1), idx)

    if cur_decl is not None:
        dname, dstart = cur_decl
        if len(lines) + 1 - dstart > max_proof_lines:
            errs.append(
                f"{path}:{dstart}: `{dname}` spans {len(lines) + 1 - dstart} lines (> {max_proof_lines})"
            )
    return errs


def run_self_test() -> int:
    """Verify forbidden constructs, line/file/proof length limits, and comment/string parsing."""
    with tempfile.TemporaryDirectory(prefix="source_guards_selftest_") as tmp:
        root = pathlib.Path(tmp)

        clean = root / "Clean.lean"
        clean.write_text(
            "\n".join(
                [
                    "/-! Clean header mentioning `sorry` and `native_decide` safely. -/",
                    "def msg : String := \"sorry and axiom inside string literal\"",
                    "/- single-line block comment with Lean.ofReduceBool -/",
                    "theorem ok_thm : True := by trivial -- inline comment with erw",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        clean_errs = check_file(clean, max_line_len=100, max_file_lines=50, max_proof_lines=10)
        if clean_errs:
            raise AssertionError(f"Unexpected errors on clean file: {clean_errs}")

        cases = [
            ("sorry", "theorem t : True := by sorry"),
            ("admit", "theorem t : True := by admit"),
            ("axiom", "axiom bad_ax : False"),
            ("native_decide", "theorem t : True := by native_decide"),
            ("Lean.ofReduceBool", "theorem t := Lean.ofReduceBool"),
            ("Lean.trustCompiler", "theorem t := Lean.trustCompiler"),
            ("implemented_by", "@[implemented_by fast_impl] def slow : Nat := 0"),
            ("extern", "@[extern \"c_fn\"] opaque ext_fn : Nat → Nat"),
            ("set_option", "set_option maxHeartbeats 0 in\ntheorem t : True := by trivial"),
            ("erw", "theorem t : True := by erw []"),
            ("meta/unsafe", "private unsafe def bad : Nat := 0"),
            ("meta/unsafe", "meta def bad_meta : Nat := 0"),
            ("metaprogramming escape hatch", "theorem t : True := by run_tac pure ()"),
        ]
        for expected_label, snippet in cases:
            bad = root / "Bad.lean"
            bad.write_text(snippet + "\n", encoding="utf-8")
            errs = check_file(bad, max_line_len=100, max_file_lines=50, max_proof_lines=10)
            if not any(f"forbidden construct `{expected_label}`" in e for e in errs):
                raise AssertionError(f"Failed to catch `{expected_label}` in {snippet!r}: {errs}")

        quote_doc = root / "QuoteDoc.lean"
        quote_doc.write_text("/-- Bad \"quote\" in docstring -/\ntheorem t : True := by trivial\n", encoding="utf-8")
        if not any("double quote inside comment/docstring" in e for e in check_file(quote_doc, 100, 50, 10)):
            raise AssertionError("Failed to catch double quote inside docstring")

        long_line = root / "LongLine.lean"
        long_line.write_text("-- " + ("x" * 100) + "\n", encoding="utf-8")
        if not any("line length" in e for e in check_file(long_line, 100, 50, 10)):
            raise AssertionError("Failed to catch max_line_length violation")

        long_file = root / "LongFile.lean"
        long_file.write_text("\n".join(["theorem t0 : True := by trivial"] * 6) + "\n", encoding="utf-8")
        if not any("exceeds 5-line limit" in e for e in check_file(long_file, 100, 5, 10)):
            raise AssertionError("Failed to catch max_file_lines violation")

        long_proof = root / "LongProof.lean"
        long_proof.write_text(
            "theorem long_p : True := by\n" + "\n".join(["  have h := trivial"] * 6) + "\n  exact trivial\n",
            encoding="utf-8",
        )
        if not any("spans 8 lines (> 5)" in e for e in check_file(long_proof, 100, 50, 5)):
            raise AssertionError("Failed to catch max_proof_lines violation")

    print("PASS: scripts/check_source_guards.py self-test passed (all escape hatches & limits enforced).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Hard CI source hygiene guard for Lean files")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path("."), help="Repo root containing problem.toml")
    parser.add_argument("--self-test", action="store_true", help="Run built-in unit self-tests")
    args = parser.parse_args()
    if args.self_test:
        return run_self_test()

    root, max_line_len, max_file_lines, max_proof_lines = load_config(args.root)
    files = sorted(root.rglob("*.lean")) if root.exists() else []
    all_errs: list[str] = []
    for f in files:
        all_errs.extend(check_file(f, max_line_len, max_file_lines, max_proof_lines))
    if all_errs:
        for e in all_errs:
            print("FAIL:", e, file=sys.stderr)
        return 1
    print(f"PASS: Checked {len(files)} Lean file(s) under {root}/ — 0 hygiene violations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
