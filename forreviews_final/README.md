# forreviews_final — index

Final reviews of the repo, one folder per agent/worktree. This file is the map; each folder is the review.

**Repo:** `eltonaguiar/TSOM-Salesforce-DevOps-Learning`
**Indexed:** 2026-11-14 04:25 UTC

---

## All entries

| Folder | Files | Reviews *this* repo? | Scope |
|---|---|---|---|
| `2026-11-14T041300Z_spice-hyena/` | 5 | **Yes** | All 18 `forreviews/` entries, 4 branches, 5 guide pages. Error-propagation map, entry inventory, publish plan |
| `2026-11-14T030820Z_salesforceagain/` | 5 | **Yes** | 7 bundles, 51-defect register, guide `file:line` corrections, merge plan |
| `2026-11-14T031220Z_chill-egg/` | 5 | **Yes** | Branch inventory, guide alignment, corrections, release-engineering redline |
| `2026-11-14T030826-salesforceyetagain/` | 6 | **Yes** | Cross-tree audit: inventory, guide-coverage matrix, fidelity corrections, gap register, merge plan |
| `2026-11-14T030826-salesforceyetagain.md` | 1 | **Yes** | Short index of the folder above. Not a duplicate |
| `2026-11-14T0316Z-cooing-son/` | 1 | **Both** | Declares both repos as source. Cross-reference of domain `main` *and* this repo |
| `2026-11-14T03-25-00Z_spice-hyena/` | 8 | **No** — domain repo | Cross-branch + PR review of `findtorontoevents_antigravity.ca`. Cites branch tip `1d9354ab9e2` |
| `2026-11-14T03-09-09Z_nova-currency/` | 1 | **No** — domain repo | Cross-branch review, cites `1d9354ab9e2` |
| `20261114T031017Z_jet-slime/` | 5 | **No** — domain repo | Cross-branch review, cites `1d9354ab9e2` |
| `2026-11-14T03-18-59Z_modern-venom/` | 10 | **No** — domain repo | Cross-branch review, cites `1d9354ab9e2` |

**10 entries, 51 files.** Four review this repo, one covers both, four review the domain repo, and one is
the short index of another entry.

## Read this before using the folder

**Four entries review a different repository.** `03-25-00Z_spice-hyena`, `nova-currency`, `jet-slime` and
`modern-venom` each cite `findtorontoevents_antigravity.ca` and its branch tip `1d9354ab9e2`. That is the
trading/domain repo, not this one.

Their content is not wrong on its own terms — it is a competent review of a different codebase — but it is
**not a review of this repo** and should not be merged into these pages.

Recorded per entry in the table above rather than relabelling anyone's work.

**One worktree has two folders.** `spice-hyena` appears twice, with different scopes:

| Folder | Repo | Note |
|---|---|---|
| `2026-11-14T041300Z_spice-hyena/` | this repo | The on-target review |
| `2026-11-14T03-25-00Z_spice-hyena/` | domain repo | Declares its own scope in its `00_index.md` |

Both are honest about which repo they cover. Keeping both, distinguished by timestamp, is better than
deleting either — the domain-repo review is a real artifact, just aimed elsewhere.

## Where the on-target reviews agree

The four on-target entries converge on the same findings, which is the strongest signal in the folder:

| Finding | `spice-hyena` | `salesforceagain` | `chill-egg` | `salesforceyetagain` |
|---|---|---|---|---|
| Heap `6/12 MB` is wrong (real: `10/25 MB`) | Yes, with root cause | Yes | Yes | — |
| Coverage "1%" rule does not exist | Yes | Yes | — | — |
| `forreviews/` is duplicate drops of one research effort | Yes | — | Yes, as headline | Yes |
| Published pages already absorbed the useful material | — | — | Yes | Yes |

`spice-hyena` adds the root cause: `6/12 MB` are the **callout request/response size** limits — a different
row of the same governor-limits table, applied to heap. `chill-egg` independently calls the corpus "mostly
duplicate drops of the same Scotiabank requisition 276046 research". `salesforceyetagain` reaches the same
conclusion from the tree-inventory side.

Three independent routes to the same diagnosis: the same research was performed several times, and the
errors were copied with it.

## Where they disagree

| Question | Positions |
|---|---|
| Is "no official Salesforce DevOps cert" a defect? | `salesforceagain` says **yes** (cites Development Lifecycle and Deployment Architect). `spice-hyena` says **no** — the claim is narrower and matches the published guide's own wording |

Unresolved. Settle against the official credential page before it enters a curriculum. Neither reviewer
verified the architect credential against the primary source in this session.

## Suggested reading order for a merge round

1. `spice-hyena/03_error_propagation_map.md` — which wrong claim lives in which bundle
2. `salesforceagain/03-defect-register.md` — the per-defect checklist (51 items)
3. `salesforceyetagain/02-guide-coverage-matrix.md` — guide-side coverage
4. `chill-egg/04-feedback.md` — the release-engineering framing
5. `spice-hyena/04_publish_recommendation.md` — what to ship, in order

## What is missing from the folder

- No entry reviews the **guide repo** (`ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`) as a codebase.
  All five published pages are read as source material only.
- No entry attempts the four labs in `labs-design.md`. They need Developer Edition orgs.
- No entry verifies the vendor tool click paths (Gearset / Copado / AutoRABIT). The guide itself says these
  stay at category level — possibly the right call, but unconfirmed.
- No entry verifies the "Development Lifecycle and Deployment Architect" credential against the official
  credential page, which is the one factual dispute in the folder.

## Conventions

- One folder per agent, named `<ISO-8601 timestamp>_<worktree>`.
- A short single-file index alongside a folder is acceptable (`salesforceyetagain`), provided it is an index
  and not a second copy.
- Each folder carries its own `README.md` with worktree, timestamp, repo and scope.
- **Declare which repo you reviewed.** Two folders here review a different repo; the scope line is what
  makes that discoverable instead of confusing.
- Do not edit another agent's folder. Corrections go in your own, with a reply to theirs.
- This index is append-only: add a row, never rewrite another agent's.