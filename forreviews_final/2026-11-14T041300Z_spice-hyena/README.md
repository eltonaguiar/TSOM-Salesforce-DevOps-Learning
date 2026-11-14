# forreviews_final — cross-reference of all bundles, branches and guide pages

| Field | Value |
|---|---|
| Folder | `forreviews_final/2026-11-14T041300Z_spice-hyena/` |
| Worktree | `spice-hyena` · **Agent:** kilo |
| Repo | <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning> |
| Reviewed at | `main` @ `6d0d44c` · 2026-11-14 04:13 UTC |
| Scope | 18 `forreviews/` entries (85 files) · 4 research branches · 5 published guide pages · the existing `forreviews_final/` |
| Method | Independent verification against primary sources, not a re-read of the peer review |

---

## What is in here

| File | Contents |
|---|---|
| `README.md` | This file — scope, method, headline findings |
| `01_inventory.md` | Every entry and branch, with size, state and verdict |
| `02_verified_findings.md` | Findings I confirmed against primary sources, with the evidence |
| `03_error_propagation_map.md` | Which wrong claim lives in which bundle — the cross-reference matrix |
| `04_publish_recommendation.md` | What to publish, what to fix, what to drop, and in what order |

---

## Headline findings

### 1. The heap error has a root cause, and it is not "the number is wrong"

Five bundles publish `6 MB sync / 12 MB async` for heap. The published crash course says it too. The peer
review correctly flagged the figure as wrong (real value 10 MB / 25 MB) — but the more useful finding is
**where 6/12 came from**.

`6 MB` and `12 MB` are **real Salesforce limits**. They belong to a different row of the same governor-limits
table, verified verbatim from the Apex Developer Guide:

| Limit | Sync | Async |
|---|---|---|
| **Total heap size** | **10 MB** | **25 MB** |
| **Maximum size of callout request or response** | **6 MB** | **12 MB** |

So the crash course did not invent a number. It took the **callout request/response size** row and applied it
to the **heap** row. That is a conflation, not a typo — and it explains why five independent bundles
reproduced it faithfully. They copied a plausible-looking pair of numbers from the page that was supposed to
be the authority.

**Why the diagnosis matters:** if you "fix" this by replacing 12 with 25 and stop there, the same class of
error will reappear, because the page still invites the reader to attach 6/12 to whichever limit they happen
to be reasoning about. The fix is to state the two limits separately and label them.

**Evidence:** `apex-gov-limits.html`, "Total heap size … 10 MB / 25 MB" and "Maximum size of callout request
or response (HTTP request or Web services call) … 6 MB for synchronous Apex or 12 MB for asynchronous Apex".

### 2. There is no 1% coverage rule, and it propagated through four files in three bundles

| Location | Claim |
|---|---|
| `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:222` | "ApexTrigger — Requires at least 1% test coverage on the trigger itself" |
| `2026-11-14_salesforceagain-v3_devops-metadata-dependencies-deep-dive.md:225` | "at least 1% per trigger, 75% org-wide" |
| `2026-11-14_salesforceagain-v3_devops-github-cicd-pipeline.md:241` | "Trigger coverage: 1% minimum per trigger" |
| `20261114-020852-salesforcemore/SALESFORCE_LIMITS_DEEP_DIVE.md:84` | "75% org-wide coverage … 1% per class minimum" |
| `20261114-020852-salesforcemore/salesforce-principles/KEY_PRINCIPLES.md:103` | "each Apex class needs ≥1% coverage" |
| `20261114-020852-salesforcemore/SALESFORCE_LIMITS_DEEP_DIVE.md:295` | "each class ≥ 1%" |

The official requirement, verified from `apex_code_coverage_intro.htm`:

> "To deploy Apex or package it for the Salesforce AppExchange, unit tests must cover at least **75%** of your
> Apex code, and those tests must pass."

There is no per-class or per-trigger 1% floor. The real constraint is subtler and worth stating properly:
**each class and trigger must have *some* coverage or the payload fails** — but the number is not 1%, and
"1%" reads like a documented threshold because it is a specific-looking number.

Note that `2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:69` gets this right and
flags its own uncertainty: *"Every trigger needs some coverage `[Verify the 1% trigger rule]`."* That is the
correct behaviour, and it is the only one of the seven sites that has it.

### 3. The deploy payload ceiling is out by an order of magnitude in two bundles

| Location | Claim | Real |
|---|---|---|
| `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:184` | "Total deploy zip size — 400 MB (recommended); hard limits vary" | **≈39 MB compressed** |
| `2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:66` | "Max compressed payload ~400 MB `[Verify current byte cap]`" | **≈39 MB compressed** |

`salesforceagain-v4` has a third variant at `comprehensive-devops-research.md:109`. Meanwhile
`2026-11-14T023507_salesforcemore-v2` states it correctly (≈39 MB compressed / ≈600 MB uncompressed) **and
documents that it corrected its own earlier 400 MB figure** in `08-cross-bundle-notes.md:21`. That bundle is
the only one that shows its work.

A 10× error on a payload ceiling is the kind that changes a design decision — a team sizing a deployment
against 400 MB will not think about splitting it.

### 4. One bundle tells you to install a deprecated CLI

`20261114-020852-salesforcemore/SALESFORCE_DEVOPS_DEEP_DIVE.md:599`:

```
npm install -g sfdx-cli || true  # prefer official sf installer in practice
```

`sfdx-cli` is the deprecated predecessor of `@salesforce/cli`. The `|| true` is the worse half — it
suppresses the failure, so a broken install proceeds silently. The peer's own bundle gets this right
(`20261114-020300-salesforceagain-kilo/04-github-actions-salesforce-cicd.md:179`) and names the replacement.

### 5. A claim I checked and believe is correct — and the peer review disputes it

The peer's defect register (D21, D32) records "No official Salesforce DevOps cert" as a **defect**, on the
grounds that the "Development Lifecycle and Deployment Architect" credential exists.

I think that correction over-reaches. The published guide says, in its own Certifications section:

> "A Salesforce 'DevOps Engineer' cert — **There is not an official one to list as if it existed.** Copado,
> Gearset, and AutoRABIT offer their own certificates. Those show tool time. They do not replace PD1."

The bundles' claim is narrower and correct: there is no credential *named* "DevOps Engineer". A credential
called "Development Lifecycle and Deployment Architect" is a different thing, and its existence does not make
the narrower claim false. Two bundles being wrong about the same number is a defect; two reviewers
disagreeing about scope is a discussion.

**Recommendation:** keep the bundles' claim, add the architect credential as a related-but-distinct item, and
verify it against the official credential page before it enters a curriculum. I did not verify it in this
session and am not asserting it.

---

## What I did not do

- **I did not re-derive all 51 defects** in the peer's `03-defect-register.md`. That register is good work and
  duplicating it would waste the merge round. This folder covers what I could verify independently, plus the
  structural analysis nobody had done (entry inventory, branch state, error-propagation map).
- **I did not attempt the labs.** They need Developer Edition orgs.
- **I did not verify the gearset/Copado/AutoRABIT click paths.** The guide is explicit that vendor button
  paths differ and stay at the category level; so do I.

## Reproduce

```bash
git clone https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning.git
cd TSOM-Salesforce-DevOps-Learning
grep -rn "6 MB\|12 MB" forreviews/ | grep -i heap
grep -rn "1%" forreviews/ | grep -iE "cover|trigger|class"
curl -sSL https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html
```