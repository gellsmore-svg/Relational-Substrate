# Adaptive-interface RRC — recovery, publication and automatic integration

**Date:** 26 October 2026

This handoff exists because the latest GitHub inspection found that the **adaptive-interface prompt had been merged into `main` but its new research results were not present**. The user reports the work may already exist locally and asks Codex to finish the publication/integration workflow.

The main instruction is [RESEARCH-RECOVERY-AND-PUBLISH.md](RESEARCH-RECOVERY-AND-PUBLISH.md). It is designed for execution **in the original local workspace**, where unpublished research and the intentionally untracked Atlas-019/020 outputs might be present.

It instructs Codex to:

1. Audit local and remote state and distinguish prompt merge from published scientific work.
2. Recover/verify and publish completed local work **or** finish the original independently selected inquiry.
3. Validate mathematical evidence, protect frozen results and accurate atlas counts.
4. Commit/push results to the RRC research branch, then use the standing `AGENTS.md` authority to merge validated work automatically to `main`.
5. Verify final CI and both branch heads, or state an exact blocker.

## Run in Codex

> Read and execute `relational-complexity/prompts/2026-10-26-adaptive-interface-recovery-publication/RESEARCH-RECOVERY-AND-PUBLISH.md` from your **existing local repository/worktree**. Investigate and finish or recover the adaptive-interface OTR research originally specified in `relational-complexity/prompts/2026-10-26-adaptive-relational-interfaces/RESEARCH-PROMPT.md`. Independently verify, commit and push real findings, then automatically merge validated research to main under `relational-complexity/AGENTS.md`. Report exact commit, CI and merge evidence. Do not treat the previously merged prompt as completed research.

Writing this instruction does **not** itself execute or accept any scientific increment.