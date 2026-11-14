# 04 — Merge plan for the published Salesforce guides

**Audience:** the merge-round agent.
**Inputs:** every bundle in `forreviews/` on `main`, plus the branches listed in §5.
**Output:** the five published pages under `docs/salesforce/` in
<https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM>.

---

## 1. The decision that matters most

**Do not merge everything into one page.** There are two different jobs:

| Job | Page | Voice | Length |
|---|---|---|---|
| Teach a beginner the platform | Crash Course, Navigation, Labs, User Management | ELI5, no jargon | keep as is |
| Prepare someone for a release-engineering interview | DevOps & Release Engineering | technical, precise | may grow 3–5× |

The instinct after five parallel bundles is to dump everything into the DevOps page. That page is
already 554 lines and it is the **entry point** for a specific job description. A 6,000-line page
is less usable than a 1,500-line one.

**Recommendation:**
- The DevOps page becomes a **long, well-collapsed** page — the user asked for collapsible
  sections, which is exactly the right instrument for depth that is valuable but not needed on
  first read.
- The *teaching* material stays in the other four pages, and the DevOps page **links** to it
  rather than restating it.
- Anything that is a crash-course-level correction goes to the crash course, **not** to the DevOps
  page. A release engineer does not need a second governor-limits table.

---

## 2. Target structure for `docs/salesforce/devops-engineer.md`

Keep the existing 12 sections and their numbering (existing links and any training material
pointing at anchors keep working). Fold the depth in as `<details>` blocks.

```
0.  How to use this page  (NEW — 10 lines: read §1-§4, then the rest is reference)

1.  Source of truth
      + details: the release lifecycle end to end; source tracking; what never goes in Git
2.  Metadata that breaks releases
      + details: error -> cause -> fix table
      + details: destructive changes; the Master-Detail Recycle Bin rule
2b. LIMITS, DEPENDENCIES AND CONSTRAINTS   (NEW — the highest-value addition)
      + details: governor limits, per transaction
      + details: governor limits, per org / per 24 h
      + details: platform allocations (API, storage)
      + details: Metadata API payload ceilings
      + details: the metadata types that force a full local test run
      + details: deployment constraints (locking, queueing, permissions)
3.  Environments and sandboxes
      + details: sandbox type table; the refresh -> mask gate
4.  Branching
      + details: hotfix topology; the GitHub branch-protection rules that enforce it
5.  CI/CD
      + details: the GitHub Actions pipeline (YAML); auth; validate -> quick deploy
      + details: Azure DevOps / GitLab equivalents; which one for a bank
6.  DevOps tools   (REWRITE as three vendor subsections)
6a. Gearset          + details: navigation, compare/deploy, CI jobs, pipelines, backup, masking
6b. Copado           + details: Pipeline Manager, promotions, quality gates, credentials, compliance
6c. AutoRABIT        + details: CI Job, deployment settings, release labels, approvals, Vault masking
6d. Choosing between them; the stale-label warnings ("do not say 'Work Rules'")
7.  Conflict clinic
      + details: profile decomposition; the record-type assignment chain; Flow versions
8.  Packages
      + details: file-count ceilings; the certified-namespace governor-limit interaction
9.  Tests and validation
      + details: the FIVE test levels; the test-forcing metadata list; coverage semantics
10. Releases, hotfixes, rollback
      + details: three speeds; the runbook with owners; the rollback decision tree
11. Banking change control
      + details: the evidence pack; segregation of duties; the org settings that enforce them
12. Design patterns you coach
      + details: pattern -> deployability consequence  (LINK to Labs & Design, do not restate)
13. Certifications   (EXPAND)
      + details: current names; prerequisites; curricula; the vendor certs; study order
```

**Do not** renumber the existing sections. Insert `2b` rather than renumbering §3 onwards.

### 2.1 The collapsible-section syntax is already decided by the page

`docs/salesforce/devops-engineer.md` currently contains **26** `<details markdown="1">` blocks and
**zero** plain `<details>`. The `markdown="1"` attribute is what tells kramdown to process the
Markdown inside an HTML block; without it, headings, tables and lists inside the block render as
literal text. **Every new collapsible block must use `<details markdown="1">`.**

(The rest of the repo uses 128 plain `<details>` blocks, but those are short one-line quiz answers
where there is no Markdown to process. Do not copy that form for the DevOps page.)

Verified across the repo on 2026-11-14:

| Pattern | Count in `docs/` | Use for |
|---|---|---|
| `<details markdown="1">` | 26 — all in `salesforce/devops-engineer.md` | **Any block containing headings, tables, lists or code** |
| `<details>` | 128 — quiz answers elsewhere | Single-line plain text only |

---

## 3. What goes where, by source bundle

| Target section | Take from | Notes |
|---|---|---|
| §1 Source of truth | any bundle | All agree. Use the most compact wording. |
| §2 Metadata that breaks releases | my `02 §4` (dependency map), my `02 §4.3` (destructive changes) | The **Master-Detail Recycle Bin rule** is unique to my bundle and is the most-missed deploy hazard on the page. |
| §2b Limits | my `02` (whole artifact) + `20261114-020852-salesforcemore/SALESFORCE_LIMITS_DEEP_DIVE.md` | My bundle has the deploy ceilings, the 24-type test-forcing list and the API allocations; the other bundle has a strong governor-limits table. Merge them — **do not paste both**. |
| §3 Environments | my `05 §5`, `03 §1.9` | Nobody else appears to have covered the refresh→mask gate in depth. |
| §4 Branching | any bundle | All agree. Add my hotfix back-merge rule. |
| §5 CI/CD | my `04` (whole artifact) | Mine is the only one with **linted, runnable YAML** and flags verified against the CLI plugin source. |
| §6 DevOps tools | my `03` (whole artifact) | Mine is the only one with per-vendor click paths and an explicit stale-label list. |
| §7 Conflict clinic | my `05 §7` + the other bundles' conflict material | |
| §8 Packages | my `05 §13` | Add the file-count ceilings. |
| §9 Tests and validation | my `02 §5` | The five-level table and the 24-type list. |
| §10 Releases/rollback | my `05 §10-11` | |
| §11 Banking change control | my `05 §4` + `07 §7` | |
| §12 Design patterns | **link to Labs & Design**, add only the deployability column | Avoids a third copy. |
| §13 Certifications | my `06` | The Platform Administrator prerequisite and the "no Salesforce DevOps cert" correction are unique to mine. |

---

## 4. Corrections to apply to the other four pages

Small, surgical, and independently verified — see `01-guide-crossreference.md` for full citations.

| Page | Change | Lines |
|---|---|---|
| `crash-course.md` | Heap 6/12 MB → **10/25 MB**; "doubles to 12 MB" → "rises to 25 MB and CPU to 60,000 ms" | `:345`, `:425`, `:434` |
| `crash-course.md` | `Setup > Monitor > Logs > Debug Logs` → `Setup > Debug Logs` | `:85` |
| `crash-course.md` | Batch Apex batch-size row → separate "trigger batch size 200; 2,000 for platform events and CDC" | `:488` |
| `labs-design.md` | `login.lockout` → `Setup > Lockout Policies` | `:300` |
| `labs-design.md` | `setup.locked` → mark read-only/internal; Deployment Status displays it, does not set it | `:299` |
| `labs-design.md` | Split the system-properties table into "admin-settable" vs "internal org properties" | `:294-301` |
| `labs-design.md` | Deployment Options: name the three CLI commands; explain why Ant is superseded | `:317-330` |
| `user-management-data.md` | Add: profiles do not merge; the integration user class; Full-sandbox masking | Profiles §, Users § |
| `navigation-breadcrumbs.md` | Expand Deployment Settings; add the masking/refresh rows | `:144-159` |
| `index.md` | Add the depth line to the DevOps card; link the crash course's limits section to the DevOps table | `:132` |

**Also required by this repo's convention:** every fix ships with an `updates/*.MD` note
describing what was broken, what changed, and how it was verified. The merge round must add one
file per changed page, or one file covering the batch.

---

## 5. Source bundles — what to pull

| Bundle | Where | Role in the merge |
|---|---|---|
| `forreviews/20261114-020300-salesforceagain-kilo/` | `main` | **Primary** for §2b, §5, §6, §9, §13 |
| `forreviews/2026-11-14T023507_salesforcemore-v2/` | `main` | **Primary** for the key-principles framing and the merge map |
| `forreviews/20261114-020852-salesforcemore/` | `main` | Strong limits deep dive and certification research |
| `forreviews/20261114-023241-salesforceagain-v2/` | `main` | Second independent read; use for cross-checking, not for text |
| `forreviews/2026-11-14T023312_salesforcemore-v3/` | `main` | Third bundle; cross-check |
| `forreviews/2026-11-14T0210Z-salesforceyetagain-v2/` + loose | `main` | Crash-course-oriented material — route to `crash-course.md` |
| `forreviews/salesforceagain-v4-2026-11-14-0230/` | `main` | Late bundle; cross-check |
| loose `2026-11-14_salesforceagain-v3_*.md` (4 files) | `main` | Topic deep dives — cross-check |
| `research/salesforcemore-v2-2026-11-14T021057Z/` | branch `research/salesforcemore-v2-2026-11-14T021057Z` | The split source of the salesforcemore-v2 entry |
| `research/salesforceagain-v2-20261114/` | branch `research/salesforceagain-v2-20261114` | Split source |
| `research/2026-11-14T020300Z-kilo-salesforceagain/` | branch `research/salesforceagain-2026-11-14T020300Z` | My split source |
| `research/…` | branch `salesforceagain-v3` | Split source |

**Do not merge from the loose consolidated `.md` files** — they are concatenations and will drag
in duplicated headings. Merge from the split files.

---

## 6. Definition of done

- [ ] Every JD line from requisition 276046 maps to at least one section of the DevOps page
- [ ] All five published pages are internally consistent on: heap figures, debug-log path, deployment vocabulary, test-level names, Deployment Settings path
- [ ] The eight corrections in `01-jd-crossreference.md` §3 are applied
- [ ] Every deep dive is inside a `<details>` block; the page's own TOC still works
- [ ] No vendor label is published that the vendor's current documentation does not use
- [ ] No CLI flag is published that does not exist in the pinned CLI version
- [ ] An `updates/*.MD` note exists for each changed page
- [ ] The index page card for the DevOps track describes what is now inside it
- [ ] The merge round records which bundle won each contested claim, and why
