# Review Packet

This directory contains tracked review artifacts for the Relational Substrate sandbox baseline.

- `sandbox-closure-summary.md`: closure milestone summary for external review.
- `external-ai-review-prompt.md`: prompt for an independent AI review of the closure milestone.
- `claude-progress-review-prompt.md`: comprehensive progress and drift-audit prompt for Claude before the next validation step.

The source of truth for generated report logic remains in `analysis/`. The ignored `analysis/out/` directory can be rebuilt with:

```bash
npm run reports
```
