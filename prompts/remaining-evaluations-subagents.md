# Remaining Evaluations via High-Reasoning Subagents

You are working in the `crest-insights` repo. Complete the remaining case study evaluations by delegating the analysis work to subagents with **high reasoning**.

## Goal

Create evaluation files in `evaluations/` for every case study in `markdown/` that does not already have a matching filename in `evaluations/`.

Each new evaluation must:

- Use the exact structure, headings, and tone used by the existing evaluation files in `evaluations/`
- Follow the YC evaluation framework in `prompts/office-hours-distilled.md`
- Be written as a standalone markdown file
- Use the same filename as the source case study
- Set `**Date Evaluated**: 2026-03-19`

## Required Workflow

1. Read `prompts/office-hours-distilled.md` in full and treat it as the evaluation rubric.
2. Identify the unreviewed case studies by comparing `markdown/` and `evaluations/` filenames.
3. Spawn multiple subagents to do the case-study analysis work in parallel.
4. Subagents must use `reasoning_effort: "high"`.
5. Give each subagent a disjoint file ownership set so they do not touch the same files.
6. Tell each subagent that they are not alone in the codebase and must not revert or overwrite others' work.
7. Instruct each subagent to create the evaluation files directly in its assigned write scope, using the repo's existing evaluation format exactly.
8. After the subagents finish, review every new file yourself and normalize any inconsistencies in:
   - section names
   - markdown formatting
   - tone
   - scoring calibration
   - category labels
   - em dash / double hyphen usage
9. Verify that every unreviewed source file now has a corresponding file in `evaluations/`.
10. Verify that each new file includes:
    - title
    - source filename
    - category
    - date evaluated
    - all required sections from the office-hours prompt
    - startup viability score
    - one-line verdict
    - PG-style comment
    - concrete assignment

## Delegation Instructions

Use subagents for the heavy analysis drafting. A good pattern is:

- Spawn 3-4 worker subagents with `reasoning_effort: "high"`
- Split the missing files into non-overlapping groups
- Give each subagent explicit ownership of its filenames
- Tell each subagent to:
  - read its assigned source files in `markdown/`
  - inspect 1-2 existing evaluations in `evaluations/` for style calibration
  - write the new evaluation files directly into `evaluations/`
  - keep scores honest; most files should likely land in the `3-5` range unless there is unusually strong evidence

## Output Quality Bar

- Be specific and reference actual details from each case study
- Most consulting engagements are not startups; say so clearly when true
- Look for the hidden startup wedge rather than taking the consulting scope at face value
- Do not be generic
- Do not soften weak conclusions
- Do not inflate scores

## Useful Checks

- Compare file counts between `markdown/` and `evaluations/`
- Spot-check that every new file starts with `# Evaluation:`
- Spot-check that every new file contains:
  - `## The Idea (In One Paragraph)`
  - `## Forcing Questions Assessment`
  - `## The Paul Graham Test`
  - `## Startup Quality`
  - `## Wild Card -- "But What If?"` or the repo's prevailing equivalent
  - `## Verdict`

## Final Deliverable

When finished:

- all previously unreviewed case studies should have evaluations in `evaluations/`
- formatting should match the existing evaluation corpus closely
- the final response should summarize which files were added and confirm verification

