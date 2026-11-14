# 03 — Error propagation map

The point of this file: these are not 51 independent defects. They are a small number of upstream errors,
each copied into several bundles. Fixing the upstream page and the earliest bundle prevents the rest.

## 1. Propagation chains

### Chain A — heap `6 / 12 MB`

```
crash-course.md:345,425,434        (upstream: callout row applied to heap row)
   ├─ salesforceyetagain-v2/02_crash-course.md:327
   ├─ salesforceagain-v2.md:331, :344, :416, :440, :806        (5 sites)
   ├─ salesforceagain-v3_devops-governor-limits-deep-dive.md:45, :63, :78, :172, :423
   └─ salesforceagain-v4/comprehensive-devops-research.md:88    (mutated: "2 MB async")
```

Five bundles, 14 sites, **one upstream cause**. Note the mutation at the end: `salesforceagain-v4` wrote
"2 MB async" — not 12. That is independent invention, not copying, and it is the worst of the set (off by
12.5×).

### Chain B — the 1% coverage rule

```
20261114-020852-salesforcemore/
   ├─ SALESFORCE_LIMITS_DEEP_DIVE.md:84, :295
   └─ salesforce-principles/KEY_PRINCIPLES.md:103
2026-11-14_salesforceagain-v3/
   ├─ devops-governor-limits-deep-dive.md:222
   ├─ devops-metadata-dependencies-deep-dive.md:225
   └─ devops-github-cicd-pipeline.md:241
```

Two bundles, six sites. **Both bundles appear to have invented it independently** — the phrasing differs
("1% per class minimum" vs "1% minimum per trigger"). That is worse than copying: it means the wrong number
is *attractive*, which is why it will keep coming back unless the real rule is stated clearly somewhere
prominent.

`2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:69` is the sole site that flags it
as unverified. That bundle is the model.

### Chain C — `400 MB` payload

```
2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:184
2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:66   (flagged [Verify])
salesforceagain-v4/comprehensive-devops-research.md:109                        (mutated: "10 MB")
```

Correct value (≈39 MB compressed) appears in `2026-11-14T023507_salesforcemore-v2`, which **documents its own
earlier 400 MB error** at `08-cross-bundle-notes.md:21`. That is the healthiest pattern in the repo: state the
number, then record that you corrected it.

### Chain D — deprecated CLI

```
20261114-020852-salesforcemore/SALESFORCE_DEVOPS_DEEP_DIVE.md:599   (sfdx-cli + `|| true`)
```
Single site. Corrected form exists in `20261114-020300-salesforceagain-kilo`.

## 2. Bundle-by-bundle scorecard

| Bundle | Heap | 1% rule | 400 MB | CLI | Self-documents corrections? |
|---|---|---|---|---|---|
| `20261114-020300-salesforceagain-kilo` | **correct** | **correct** | — | **correct** | Yes (`08-cross-bundle-delta.md`) |
| `2026-11-14T023507_salesforcemore-v2` | **correct** | **correct** | **correct** | hedged | **Yes** (`08-cross-bundle-notes.md`) |
| `20261114-020852-salesforcemore` | wrong | **wrong** | — | **wrong** | No |
| `2026-11-14T023241_salesforceagain-v2` | wrong ×5 | — | — | — | Partial (`[Verify]` tags) |
| `2026-11-14T023312_salesforcemore-v3` | — | flagged | flagged | — | **Yes** — best epistemic hygiene |
| `2026-11-14T0210Z-salesforceyetagain-v2` | wrong | — | — | — | No |
| `2026-11-14_salesforceagain-v3` (loose) | wrong ×5 | wrong ×3 | wrong | — | No |
| `salesforceagain-v4-2026-11-14-0230` | **wrong (2 MB)** | — | wrong (10 MB) | wrong flag | No |
| `forreviews_final/2026-11-14T030820Z_salesforceagain` | correct | correct | — | — | Yes (12 self-defects) |

**Reading the scorecard:** the two bundles with self-correction records are the two that are correct on the
numbers. That is not a coincidence. A bundle that records its own uncertainty gets checked; a bundle that
does not, does not.

## 3. The authority question the merge round needs

For each contested fact, who is right:

| Fact | Authoritative source | Bundles that agree | Bundles that disagree |
|---|---|---|---|
| Heap 10 MB / 25 MB | `apex-gov-limits.html` | `salesforceagain-kilo`, `salesforcemore-v2` | 5 bundles |
| Callout size 6 / 12 MB | same page | `salesforceagain-kilo` (correctly labelled as callout) | — |
| Coverage 75% org-wide, no per-item floor | `apex_code_coverage_intro.htm` | `salesforceagain-kilo`, `salesforcemore-v2` | 3 bundles |
| Deploy payload ≈39 MB compressed | Metadata API `deploy()` | `salesforcemore-v2`, `salesforceagain-kilo` | 3 bundles |
| `sf limits api display`, not `sf org list limits` | CLI plugin inventory | `salesforceagain-kilo`, `salesforcemore-v2` (partly) | `salesforceagain-v4` |
| Five test levels incl. `RunRelevantTests` | CLI messages | `salesforceagain-kilo`, `salesforcemore-v2` | bundles listing four |

**The pattern is consistent:** `salesforceagain-kilo` and `salesforcemore-v2` are right on every contested
number, and both maintain correction logs. Treat those two as the reference set for the merge round.

## 4. What this means for the merge

Do not merge 18 entries. Merge two, and use them to overwrite the rest.

1. **`20261114-020300-salesforceagain-kilo`** is the best-organised: JD cross-reference matrix, source log,
   system-properties table, and a self-delta file.
2. **`2026-11-14T023507_salesforcemore-v2`** is the most epistemically careful: correct numbers and a written
   record of its own corrections.

Everything else either duplicates those two or contradicts them on a number that the official docs settle.

The peer's `04-merge-plan.md` reaches the same conclusion from the page-structure side. The two recommendations
are compatible: their plan says how to lay out the published page, this says which bundle wins each section.

## 5. Residual risk after the merge

Even with the two good bundles, three things need a human decision because no bundle settles them:

1. **Exam weights.** No bundle cites an exam guide. Publish domain names only, never percentages.
2. **Vendor tool click paths.** The guide says these stay at category level. Do not publish a button path
   nobody has clicked.
3. **The architect credential.** Disputed between the peer and me (see `02_verified_findings.md` §7). Verify
   against the official credential page before it enters a curriculum.