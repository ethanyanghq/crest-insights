# Project rules

This repo contains startup case studies in `markdown/`.

When evaluating them:
- Process one case study at a time
- Never load all case studies into one subagent
- Use `prompts/office-hours-distilled.md` as the rubric
- Write outputs to `evaluations/<domain>-<wedge>.md`
- Always preserve the original case study filename in the `**Source**:` field
- Determine evaluation coverage by comparing `markdown/` filenames against `**Source**:` metadata in `evaluations/` and `shortlist/`
- After all evaluations are complete, compare only verdicts/summaries
