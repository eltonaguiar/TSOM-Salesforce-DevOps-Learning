# 04 — Publish recommendation

Ordered so each step is independently shippable.

## Step 1 — Fix the published page (highest value, smallest diff)

`docs/salesforce/crash-course.md` in the guide repo. Three edits plus one addition:

| Line | Change |
|---|---|
| 345 | `6 MB (sync) / 12 MB (async)` → `10 MB (sync) / 25 MB (async)` |
| 425 | `6 MB Synchronous / 12 MB Asynchronous` → `10 MB Synchronous / 25 MB Asynchronous` |
| 434 | `the heap limit doubles to 12 MB` → `the heap limit rises to 25 MB and CPU to 60,000 ms` |
| 85 | delete the `Setup > Monitor > Logs > Debug Logs` row (line 84 already covers it) |
| new | add `\| Max callout request or response size \| 6 MB (sync) / 12 MB (async), counts toward heap \|` |

**Why first:** this page is the upstream source for 14 wrong sites across 5 bundles. Fixing it stops the
propagation, and it is the page a beginner reads first. The peer's review independently reached the same
conclusion, which is good corroboration.

**Do not** simply swap 12 for 25 and stop. Add the callout row, or the 6/12 figures remain orphaned and will
get re-attached to whatever limit a future reader is reasoning about.

## Step 2 — Deduplicate `forreviews/`

Five entries exist as both a folder and a loose consolidated `.md`. A reader cannot tell which is
authoritative, and a fix applied to one stays live in the other.

**Action:** delete the loose twins. They are in git history, so nothing is lost.

| Delete | Keep |
|---|---|
| `2026-11-14T023507_salesforcemore-v2.md` | `2026-11-14T023507_salesforcemore-v2/` |
| `2026-11-14T023241_salesforceagain-v2.md` | `2026-11-14T023241_salesforceagain-v2/` |
| the 4 loose `2026-11-14T0210Z-salesforceyetagain-v2*.md` | `2026-11-14T0210Z-salesforceyetagain-v2/` |
| `salesforceagain-v4`'s folder stays (no twin) | — |

Add `forreviews/README.md` naming which entry belongs to which agent. Right now nothing states it, and the
folder names alone do not tell you whether `salesforceagain-v2` and `salesforceagain-v3` are the same author.

## Step 3 — Delete the four redundant branches

Verified: all four are behind `main` and hold no unique content.

```bash
git push origin --delete research/salesforceagain-2026-11-14T020300Z
git push origin --delete research/salesforceagain-v2-20261114
git push origin --delete research/salesforcemore-v2-2026-11-14T021057Z
git push origin --delete salesforceagain-v3
```

This is the cleanest available win: four branches deleted, zero content lost, and the "what is unpublished?"
question goes away.

**Do this before the merge round.** Stale branches make every inventory wrong.

## Step 4 — Merge two bundles, retire the rest

| Keep as reference | Why |
|---|---|
| `20261114-020300-salesforceagain-kilo` | Best organised. JD matrix, source log, self-delta |
| `2026-11-14T023507_salesforcemore-v2` | Most careful. Correct on every contested number, documents its own corrections |

Move the others to `forreviews/_archive/` rather than deleting — the peer's register cites them by path, and
the corrections in it are still useful as a record of what was checked.

## Step 5 — Fix the wrong numbers at source, not per-bundle

Do not edit 14 sites. Fix the two reference bundles and state that they supersede the rest.

| Error | Sites | Fix |
|---|---|---|
| Heap 6/12 | 14 across 5 bundles | Page fix (step 1) + state 10/25 in the two reference bundles |
| 1% coverage | 6 across 2 bundles | State 75% org-wide with no per-item floor |
| 400 MB payload | 3 sites | State ≈39 MB compressed |
| `sfdx-cli` + `\|\| true` | 1 site | `@salesforce/cli@<pinned>`, no `\|\| true` |
| `--validated-deploy-request-id` | 1 site | `sf project deploy quick --job-id` |
| `sf org list limits` | 4 sites | `sf limits api display` — and drop the Storage row it cannot serve |

## Step 6 — Leave these alone

- **The `1%` sites that already hedge.** `2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:69`
  flags its own uncertainty correctly. Do not "fix" it by deleting the flag; keep the flag as the pattern.
- **The bundles' "no official DevOps Engineer cert" claim.** I believe it is correct and narrow (see
  `02_verified_findings.md` §7). The peer's correction over-reaches. Verify the exact wording before changing.
- **The peer's `03-defect-register.md`.** 51 defects, already written, no duplication needed. Use it as the
  per-defect checklist; this folder is the structural layer.

## Definition of done

- [ ] `crash-course.md` heap figures correct in all three places, and the callout row added
- [ ] `crash-course.md:85` deprecated path removed
- [ ] `forreviews/` has one copy of each entry, with a root `README.md` naming owners
- [ ] Four redundant branches deleted
- [ ] Two reference bundles named as authoritative
- [ ] No bundle publishes a number the official docs contradict
- [ ] Nothing in the published pages asserts an exam weight, a vendor click path, or an unverified credential

## What I did not verify

Recorded so the merge round does not assume coverage I do not have: vendor tool click paths, exam weight
percentages, the `RunRelevantTests` API version gate, Metadata API intra-payload ordering, and whether a
masking checklist matches the current Salesforce Data Mask UI. See `02_verified_findings.md` §8.