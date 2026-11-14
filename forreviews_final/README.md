# forreviews_final — index

Final reviews of the repo, one folder per agent/worktree. This file is the map; each folder is the review.

**Repo:** `eltonaguiar/TSOM-Salesforce-DevOps-Learning`
**Indexed:** 2026-11-14 04:20 UTC · `main` @ `721542f`

---

## The seven entries

| Folder | Files | Reviewed *this* repo? | Scope |
|---|---|---|---|
| `2026-11-14T041300Z_spice-hyena/` | 5 | **Yes** | All 18 `forreviews/` entries, 4 branches, 5 guide pages. Error-propagation map, entry inventory, publish plan |
| `2026-11-14T030820Z_salesforceagain/` | 5 | **Yes** | 7 bundles, 51-defect register, guide `file:line` corrections, merge plan |
| `2026-11-14T031220Z_chill-egg/` | 5 | **Yes** | Branch inventory, guide alignment, corrections, release-engineering redline |
| `2026-11-14T030826-salesforceyetagain.md` | 1 | **Yes** | Consolidated cross-reference of `forreviews/` items against the guides |
| `2026-11-14T03-09-09Z_nova-currency/` | 1 | **No** — domain repo | Cross-branch review of `findtorontoevents_antigravity.ca` |
| `20261114T031017Z_jet-slime/` | 5 | **No** — domain repo | Cross-branch review of `findtorontoevents_antigravity.ca` |
| `2026-11-14T03-18-59Z_modern-venom/` | 10 | **No** — domain repo | Cross-branch review of `findtorontoevents_antigravity.ca` |

## Read this before using the folder

**Three entries review a different repository.** `nova-currency`, `jet-slime` and `modern-venom` each
declare `findtorontoevents_antigravity.ca` as the repo under review and cite its branch tip `1d9354ab9e2`.
That is the trading/domain repo, not this one. Their content is not wrong on its own terms — it is a
competent review of a different codebase — but it is **not a review of this repo** and should not be
merged into this repo's pages.

This is recorded per entry in the table above rather than silently relabelling anyone's work.

**Four entries review this repo** and are the ones a merge round should read: `spice-hyena`,
`salesforceagain`, `chill-egg`, and the `salesforceyetagain` single file.

## Where the substantive agreement is

The four on-target reviews converge on the same two or three findings, which is the strongest signal in the
folder:

| Finding | `spice-hyena` | `salesforceagain` | `chill-egg` |
|---|---|---|---|
| Heap `6/12 MB` is wrong (real: `10/25 MB`) | Yes, with root cause | Yes | Yes |
| Coverage "1%" rule does not exist | Yes | Yes | — |
| `forreviews/` contains duplicate drops of the same research | Yes | — | Yes, stated as the headline |
| Published pages have absorbed the useful material already | — | — | Yes |

`spice-hyena` adds the root cause: `6/12 MB` are the **callout request/response size** limits, a different
row of the same governor-limits table, applied to heap. `chill-egg` independently reaches the structural
conclusion that the corpus is "mostly duplicate drops of the same Scotiabank requisition 276046 research".

Both are describing the same underlying problem from different ends: the same research was performed
several times, and the errors were copied along with it.

## Where they disagree

| Question | Positions |
|---|---|
| Is "no official Salesforce DevOps cert" a defect? | `salesforceagain` says **yes** (cites Development Lifecycle and Deployment Architect). `spice-hyena` says **no** — the claim is narrower and matches the published guide's own wording |

Unresolved. Settle it against the official credential page before it enters a curriculum. Neither reviewer
verified the architect credential against the primary source in this session.

## Suggested reading order for a merge round

1. `spice-hyena/03_error_propagation_map.md` — which wrong claim lives where
2. `salesforceagain/03-defect-register.md` — the per-defect checklist
3. `chill-egg/04-feedback.md` — the release-engineering framing
4. `spice-hyena/04_publish_recommendation.md` — what to ship, in order

## What is missing from the folder

- No entry reviews the **guide repo** (`ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`) as a codebase.
  All five published pages are only read as source material.
- No entry attempts the four labs in `labs-design.md`. They need Developer Edition orgs.
- No entry verifies the vendor tool click paths (Gearset / Copado / AutoRABIT). The guide itself says these
  stay at category level, which may be the right call — but nobody has confirmed it.

## Conventions

- One folder per agent, named `<ISO-8601 timestamp>_<worktree>`.
- A single-file review is acceptable (`salesforceyetagain`), named `<timestamp>.md`.
- Each folder carries its own `README.md` with the worktree, timestamp, repo and scope.
- Do not edit another agent's folder. Corrections go in your own, with a reply to theirs.
- This index is append-only: add a row, never rewrite another agent's.