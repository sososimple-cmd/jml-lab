# JML Capstone — Validation Log

**Exercise date:** 2026-10-10  
**Environment:** All Things Identity / OrangeHRM + Authentik hosted lab  
**Author:** [Add GitHub display name if desired]

This is a record of expected and observed results. Do not mark an outcome as verified until you have observed it in the dashboard or script output.

## Checkpoints

| Checkpoint | Guide's expected result | My actual result | Evidence |
|---|---|---|---|
| Before HR changes | 11 rows, 0 findings | **[Fill in]** | [Optional baseline screenshot] |
| After five HR changes | 13 rows, 3 findings | **[Fill in]** | [01 — Board](../screenshots/01-hr-changes-board.png) |
| After joiner.py | Sam and Carol provisioned; Jessica enabled | **[Fill in]** | [02 — Joiner](../screenshots/02-joiner-output.png) |
| After mover.py | Department access aligned; stale memberships removed | **Illyana's issue resolved after TODO 3 indentation fix** | [05 — Mover](../screenshots/05-mover-output.png) |
| After leaver.py | Billy disabled, groups removed | **[Fill in]** | [06 — Leaver](../screenshots/06-leaver-output.png) |
| Final reconciliation | 13 rows, 0 findings | **[Fill in]** | [07 — Final](../screenshots/07-final-dashboard.png) |

> Note: The guide's row-count assumptions may not match labs with extra test accounts. Findings and actual group state matter more than matching the default row count exactly.

## Employee-level acceptance

| Employee | Expected state | Verified? | Notes |
|---|---|---|---|
| Sam Wilson | Active account; `dept-avengers` | [ ] | |
| Carol Danvers | Active account; `dept-cosmic-division` | [ ] | |
| Illyana Rasputin | Active; only correct managed department group `dept-defenders` | [x] | `dept-x-men` remained at first; corrected `mover.py` indentation and reran. |
| Billy Kaplan | Terminated in HR; disabled in Authentik; groups removed | [ ] | |
| Jessica Jones | Rehired; account enabled; `dept-defenders` restored | [ ] | |

## Actual debugging record — mover.py

**Observed failure:** Illyana had both `dept-x-men` and `dept-defenders`, while HR recorded Defenders as her department. This is documented by the actual screenshot at [`03-mover-finding.png`](../screenshots/03-mover-finding.png).

**Root cause:** The stale-group removal loop was not indented within the per-employee loop, preventing it from consistently removing obsolete access for each employee.

**Fix:** Move the `for old in has_now:` loop inside `for emp in hr_employees():`, compare every current group to `should_have`, and call `ak_remove_from_group(user, old)` for mismatches.

**Retest:** User confirmed the revised code worked. Save screenshot and final dashboard observation above.

## Notes and next steps

- [ ] Enter final finding count and timestamp.
- [ ] Replace screenshot placeholders with genuine lab images where available.
- [ ] Confirm no credentials or environment secrets appear in public files.
