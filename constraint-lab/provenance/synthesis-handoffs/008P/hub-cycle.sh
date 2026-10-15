#!/usr/bin/env bash
# Proposal only. Do not run in a CL worktree; never performs adoption.
set -eu
test -f research-synthesis/synth
branch="$(git branch --show-current)"
case "$branch" in
  research/constraint-lab-*) printf '%s\n' 'Stop: use a separate hub worktree.' >&2; exit 1 ;;
esac
test -z "$(git status --porcelain)"
target="${1:-99565d14e9c0fc172d925fd335965e127d950868}"
git cat-file -e "$target^{commit}"
python3 research-synthesis/synth audit
python3 research-synthesis/synth propose-pin --source CL --commit "$target" --note "Proposal only: preserve pending independent scientific review; inspect continuation branch configuration and 008P handoff."
printf '%s\n' 'Pending: independent scientific review and named-human reviewed hub adoption. No pin applied.'
printf '%s\n' 'After that decision, follow runbook apply-pin, generate/check twice, snapshot, round-close, PR/review. No private publication consent inferred.'
