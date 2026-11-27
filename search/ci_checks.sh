#!/usr/bin/env bash
# Problem-specific barrier red-team & search smoke checks run automatically by `.github/workflows/verify.yml`.
# Replace or extend this script in downstream problem repos (e.g. barrier_redteam.py, hunter tools).
set -euo pipefail

if [ -f scripts/check_source_guards.py ]; then
  python3 scripts/check_source_guards.py --self-test
  python3 scripts/check_source_guards.py
fi

if [ -f scripts/native_cache.py ]; then
  python3 scripts/native_cache.py --self-test
fi

if [ -f scripts/build_dashboard.py ]; then
  python3 scripts/build_dashboard.py --self-test
fi

if [ -f search/verify_json_artifacts.py ]; then
  python3 search/verify_json_artifacts.py --self-test
  if [ -d search/logs ]; then
    python3 search/verify_json_artifacts.py search/logs
  fi
fi

echo "PASS: Default solve-anything search CI hook (add problem-specific red-team & search smoke tests here)."
