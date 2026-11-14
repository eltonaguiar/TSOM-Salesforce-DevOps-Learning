# Dedupe manifest — sources → merged pages

**Input:** 85 markdown files from `forreviews/` (7 bundle folders + 11 loose files) on `main`.
**Output:** 5 merged Salesforce pages.
**Method:** every claim in the bundles was checked against a primary source before it was allowed into a
merged page. Claims that disagreed with the primary source were rejected, not merged.

---

## 1. Why dedupe was needed

The 85 files are not 85 pieces of research. Topic overlap, measured by keyword across all 85:

| Topic | Files mentioning it |
|---|---|
| Certifications | 63 |
| Gearset / Copado / AutoRABIT | 65 |
| Sandbox / masking | 52 |
| Governor limits | 50 |
| Quick deploy | 44 |
| Test levels | 26 |
| Heap `6/12 MB` | 13 |
| `400 MB` payload | 4 |
| "1%" coverage rule | 3 |

Only **3 pairs are byte-identical**:

| Duplicate | Kept |
|---|---|
| `2026-11-14T0210Z-salesforceyetagain-v2-README.md` ≡ `README.md` | the folder copy |
| `2026-11-14T0210Z-salesforceyetagain-v2-01_certifications-curriculum.md` ≡ `01_certifications-curriculum.md` | the folder copy |
| `2026-11-14T0210Z-salesforceyetagain-v2-02_crash-course.md` ≡ `02_crash-course.md` | the folder copy |

The rest is **semantic** duplication: the same research performed independently 2–4 times, with the errors
copied along with the findings. Five bundles publish the same wrong heap figure because they all read the
same upstream page.

That is why a per-defect merge would not have worked. Fixing 51 defects individually leaves the wrong numbers
in whichever copy nobody touched. The merge had to go **upstream**: fix the page the bundles were copying.

---

## 2. What went into the merged pages

### From the bundles — verified before merging

| Item | Value merged | Verified against |
|---|---|---|
| Metadata API payload ceilings | ~39 MB compressed, ~600 MB uncompressed, 10,000 files (unlocked/2GP), 35,000 (1GP AppExchange) | `meta-deploy.html` — "Maximum compressed .zip folder size … Approximately 39 MB" |
| Base64 mechanics | 50 MB zip ceiling, ~22% overhead → ~39 MB pre-encoding | same page |
| Five test levels | `NoTestRun`, `RunSpecifiedTests`, `RunRelevantTests`, `RunLocalTests`, `RunAllTestsInOrg` | CLI reference |
| Three coverage rules | org-wide 75% + triggers need *some* coverage; OR per-item 75% with `RunSpecifiedTests` | `meta_rest_deploy_recentvalidation.htm` |
| Quick deploy window | **10 days** from validation | `project deploy validate` reference — "valid for 10 days" |
| `--use-most-recent` limit | **3 days** | `project deploy quick` reference |
| `validate` is production-only | "Don't use this command on sandboxes" | CLI reference |
| Destructive changes | `pre-` / `post-destructive-changes` semantics | CLI reference |
| Deployment queue not FIFO | one at a time, not FIFO | Metadata API behaviour |
| Intra-payload reference resolution | parent + child in one payload; order is not the mechanism | Metadata API `deploy()` |

### Rejected — bundles were wrong

| Bundle claim | Reality | Disposition |
|---|---|---|
| Heap 6 MB sync / 12 MB async | **10 MB / 25 MB**. 6/12 is the *callout request/response size* limit, a different row | Rejected. Page now states both, labelled |
| Heap "doubles" async | 10→25 MB is 2.5×; CPU 10,000→60,000 ms is 6× | Rejected |
| "1% per class / per trigger" coverage | No such rule. Org-wide 75% + triggers need *some* coverage; or per-item 75% under `RunSpecifiedTests` | Rejected |
| Payload ceiling 400 MB | ~39 MB compressed | Rejected. 10× error |
| Payload "10 MB" (one bundle) | ~39 MB compressed | Rejected |
| `npm install -g sfdx-cli` | Deprecated; use `@salesforce/cli@<pinned>` | Rejected |
| `sf org list limits` | Not a command; `sf limits api display`, and it does not report storage | Rejected |
| `--validated-deploy-request-id` | Not a flag; `sf project deploy quick --job-id` | Rejected |
| Exam weight percentages | No cited exam guide | Not merged — unverifiable |

### Defects fixed in the pages themselves

These were in the *published* pages, not the bundles. Five, all confirmed by reading the page source:

| Page:line | Defect | Fix |
|---|---|---|
| `user-management-data.md:51` | "Deactivated … can't be reactivated, must recreate" | Deactivated users **can** be reactivated |
| `labs-design.md:294-300` | Five invented "system properties" (`org.wideSharing.default`, `setup.locked`, `apex.pageLimit`, `session.timeout`, `login.lockout`) | Replaced with real Setup **settings**, and an explanation that Salesforce has no general-purpose property store |
| `labs-design.md` Lab 4 | "Authentication: Password Authentication" with blank username/password | Correct protocol is **No Authentication** / Anonymous; blank password auth fails at callout |
| `navigation-breadcrumbs.md:169-170` | `Setup > Apex Jobs` / `Setup > Scheduled Jobs` | Consolidated into `Setup > Background Jobs` |
| `navigation-breadcrumbs.md:104-105` | Process Builder / Workflow Rules as live Setup paths | Marked **retired**; Flow is the replacement |
| `crash-course.md:345,426,435` | Heap 6/12 MB (see above) | 10/25 MB + callout row added |
| `crash-course.md:484` | "75%+" with no qualification | Points at the three-rule explanation |

---

## 3. What was deliberately not merged

| Item | Why not |
|---|---|
| Gearset / Copado / AutoRABIT click paths | The published guide says these stay at category level. Three bundles give conflicting paths, and nobody has clicked them. Publishing one set would be guessing |
| Exam weight percentages | No bundle cites an exam guide. Invented weights are the exact error the review was meant to catch |
| `RunRelevantTests` API version gate (claimed 66.0+) | Not in the CLI messages or the official Beta doc. Described without a version number |
| Metadata API ordering "fix" (some bundles say you must order package.xml) | False — the API resolves intra-payload references. Rejected |
| A "Salesforce DevOps Engineer" certification | Does not exist. The guide's own Certifications section says so, and the merged page keeps that |

---

## 4. File disposition

| Path | Disposition |
|---|---|
| `sources/2026-11-14T0210Z-salesforceyetagain-v2/*` | **Canonical** for certifications and crash-course content. Its 3 loose twins deleted |
| `sources/20261114-020300-salesforceagain-kilo/*` | **Canonical** for structure: JD cross-reference matrix, source log, self-delta. Correct on every contested number |
| `sources/2026-11-14T023507_salesforcemore-v2/*` | **Canonical** for limits: only bundle that documents its own corrections (`08-cross-bundle-notes.md`) |
| `sources/20261114-020852-salesforcemore/*` | Rejected on 3 counts (heap, 1% rule, deprecated CLI). Kept for the record |
| `sources/2026-11-14T023241_salesforceagain-v2/*` | Correct instinct (flags its own uncertainty with `[Verify]`), wrong numbers. Kept for the record |
| `sources/2026-11-14T023312_salesforcemore-v3/*` | Best epistemic hygiene — flags the 400 MB and 1% figures as unverified. Kept |
| `sources/salesforceagain-v4-2026-11-14-0230/*` | Worst numeric accuracy (2 MB async, 10 MB payload, bad CLI flag). Kept for the record |

Every source file is preserved verbatim under `sources/` so the merge is auditable. Nothing was edited in
place; the merged pages are separate files in `merged/`.

---

## 5. How to apply the merged pages

```bash
# from the guide repo root
cp merged/crash-course.md            docs/salesforce/crash-course.md
cp merged/devops-engineer.md         docs/salesforce/devops-engineer.md
cp merged/labs-design.md             docs/salesforce/labs-design.md
cp merged/navigation-breadcrumbs.md  docs/salesforce/navigation-breadcrumbs.md
cp merged/user-management-data.md    docs/salesforce/user-management-data.md
```

Line deltas versus the live pages:

| Page | Before | After | Delta |
|---|---|---|---|
| `crash-course.md` | 629 | 630 | +1 |
| `devops-engineer.md` | 554 | 670 | **+116** |
| `labs-design.md` | 353 | 366 | +13 |
| `navigation-breadcrumbs.md` | 207 | 209 | +2 |
| `user-management-data.md` | 374 | 374 | 0 |

`devops-engineer.md` carries almost all the new material, which is correct: the crash course is a beginner
page and the release-engineering depth belongs on the DevOps track.