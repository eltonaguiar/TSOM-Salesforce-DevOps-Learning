# 04 — Prioritized actions

Consolidated from `01` (cross-reference), `02` (guide accuracy), and `03` (work update). De-duplicated; the
same finding is not repeated across sections.

## P0 — Fix the published guides (learner-facing, blocks labs)

| # | Action | File | Why |
|---|--------|------|-----|
| 1 | Replace `Crypto.getRandomInteger().abs()` with `Math.abs(Crypto.getRandomInteger())` | `docs/salesforce/labs-design.md` Lab 2 | Apex `Long` has no `abs()` — the lab does not compile (F-01) |
| 2 | Replace `sf project generate component -n projectCard -l lwc` with `sf template generate lightning component --name projectCard --output-dir force-app/main/default/lwc` | `docs/salesforce/labs-design.md` Lab 3 | The command does not exist (F-02) |
| 3 | Replace the four invented "system properties" with the real organization settings / session / password controls | `docs/salesforce/labs-design.md` | `setup.locked`, `apex.pageLimit`, `session.timeout`, `login.lockout` are not real (F-03) |
| 4 | Fix Lab 4's "Remote Site Setting fallback" wording to state that Named Credentials remove the requirement | `docs/salesforce/labs-design.md` | Contradicts `crash-course.md` and teaches the wrong model (F-05) |

## P1 — Fold in the work update

| # | Action | Where |
|---|--------|-------|
| 5 | Copy the four new notes into the Salesforce review bundle | `forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/` (or the merge round's successor) |
| 6 | Apply `corrections_to_existing_notes.md` — the three fake credentials above all | `certifications.md` |
| 7 | Add the four missing `crash_course.md` sections (integration types, Named Credentials, other limits, resources) | `crash_course.md` |
| 8 | Update `research_index.md` so the four Pending rows read Complete | `research_index.md` |
| 9 | Apply the `labs-design.md` source fixes in the **learning repo**, not just the notes | `eltonaguiar/ServiceNow_Learning_…` |

## P2 — Repository hygiene (cross-reference findings)

| # | Action | Evidence |
|---|--------|----------|
| 10 | Decide the fate of the two mermaid-test commits (`4294fd835f`, `1d9354ab9e`) before `modern-venom` is promoted — they are scaffolding, not product | `01` §1 |
| 11 | Review the 19 recent PRs (#735–#766) first; none has a review decision | `01` §5 |
| 12 | Triage or close the 9 stale June–July PRs (#562, #564, #581, #595, #600, #657, #665, #666, #667) | `01` §5 |
| 13 | Land or close PR #713 (backup-verify false failures) — it is the fix for the 30-issue spam | `01` §6 |
| 14 | Assign an owner to issue #748 (resolver predates `_priceless_close`); it is the only real data-correctness bug open | `01` §6 |
| 15 | Review #761 / #700 / #696 together with the Mercury-retirement commit — same secret-handling surface | `01` §5 |

## P3 — Coordinate

| # | Action |
|---|--------|
| 16 | Do not edit `forreviews/salesforceyetagain-v4/…` on `main` from this worktree while the concurrent agent is active; fold both sets in a merge round instead. |
| 17 | The learning repo's non-main branches do not touch the Salesforce track — `main` is the only source of truth, so guide fixes go to `main` there. |
| 18 | Re-verify the six Trailhead trail IDs in `crash-course.md` before publishing (F-09). |

## Suggested order

1 → 2 → 3 → 4 (unblock the labs) → 5 → 6 → 7 → 8 (fold in the notes) → 9 (fix the source) → 10 → 11/12 →
13/14 → 15 → 16/17/18.
