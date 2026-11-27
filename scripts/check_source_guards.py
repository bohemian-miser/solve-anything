#!/usr/bin/env python3
"""Hard CI source hygiene guard for all `.lean` files under `<lean_root>/` from `problem.toml`."""

from __future__ import annotations

import pathlib
import re
import sys
import tomllib

FORBIDDEN = [
    (re.compile(r"\bsorry\b"), "sorry"),
    (re.compile(r"\badmit\b"), "admit"),
    (re.compile(r"\bnative_decide\b"), "native_decide"),
    (re.compile(r"^\s*set_option\b"), "set_option"),
    (re.compile(r"\berw\b"), "erw"),
    (re.compile(r"^\s*(?:meta|unsafe)\b"), "meta/unsafe"),
    (re.compile(r"\brun_tac\b|\brun_cmd\b|\bby_elab\b"), "metaprogramming escape hatch"),
]
DECL_RE = re.compile(
    r"^(?:@\[[^\]]*\]\s*)*(?:(?:private|protected|noncomputable)\s+)*(?:lemma|theorem|def)\s+(\S+)"
)


def load_config() -> tuple[pathlib.Path, int, int, int]:
    cfg_path = pathlib.Path("problem.toml")
    cfg = tomllib.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.exists() else {}
    lean_root = pathlib.Path(cfg.get("problem", {}).get("lean_root", "Problem"))
    guards = cfg.get("guards", {})
    return (
        lean_root,
        int(guards.get("max_line_length", 100)),
        int(guards.get("max_file_lines", 1000)),
        int(guards.get("max_proof_lines", 50)),
    )


def check_file(path: pathlib.Path, max_line_len: int, max_file_lines: int, max_proof_lines: int) -> list[str]:
    errs: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) > max_file_lines:
        errs.append(f"{path}: {len(lines)} lines exceeds {max_file_lines}-line limit")

    in_block_comment = False
    cur_decl: tuple[str, int] | None = None

    for idx, line in enumerate(lines, 1):
        if len(line) > max_line_len:
            errs.append(f"{path}:{idx}: line length {len(line)} > {max_line_len}")

        stripped = line.strip()
        if "/-" in line and "-/" not in line:
            in_block_comment = True
        if in_block_comment or stripped.startswith("--"):
            if '"' in line:
                errs.append(f"{path}:{idx}: double quote inside comment/docstring")
            if "-/" in line:
                in_block_comment = False
            continue

        code_part = line.split("--", 1)[0]
        for pat, label in FORBIDDEN:
            if pat.search(code_part):
                errs.append(f"{path}:{idx}: forbidden construct `{label}`")

        m = DECL_RE.match(line)
        if m:
            if cur_decl is not None:
                dname, dstart = cur_decl
                if idx - dstart > max_proof_lines:
                    errs.append(f"{path}:{dstart}: `{dname}` spans {idx - dstart} lines (> {max_proof_lines})")
            cur_decl = (m.group(1), idx)

    if cur_decl is not None:
        dname, dstart = cur_decl
        if len(lines) + 1 - dstart > max_proof_lines:
            errs.append(f"{path}:{dstart}: `{dname}` spans {len(lines) + 1 - dstart} lines (> {max_proof_lines})")
    return errs


def main() -> int:
    root, max_line_len, max_file_lines, max_proof_lines = load_config()
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
