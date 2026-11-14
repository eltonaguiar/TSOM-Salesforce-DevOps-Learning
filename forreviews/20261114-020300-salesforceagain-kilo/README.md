# Research bundle — Salesforce DevOps Engineer (Scotiabank req. 276046)

| Field | Value |
|---|---|
| Bundle | `2026-11-14T020300Z-kilo-salesforceagain` |
| Worktree | `salesforceagain` |
| Agent | kilo |
| Location on `main` | `forreviews/20261114-020300-salesforceagain-kilo/` (this folder) |
| Consolidated single-file copy | `forreviews/2026-11-14T020300_salesforceagain-kilo.md` |
| Branch | `research/salesforceagain-2026-11-14T020300Z` (pushed to `origin`) |
| Sibling bundle | `2026-11-14T021057Z_salesforcemore-v2` on branch `research/salesforcemore-v2-2026-11-14T021057Z` |
| Research start | 2026-11-14T02:03:00Z |
| Job | DevOps Engineer (Salesforce), Scotiabank, Toronto — Requisition 276046 |
| Job URL | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| Downstream page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> |
| Downstream repo | <https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM> |
| Status | Complete — all 10 artifacts written and cross-checked against primary sources |
| Contains secrets / customer data | No |

## Objective

Produce merge-ready, primary-source-verified research that (a) cross-references every line of the
job description against the existing `devops-engineer` training page, (b) goes one level deeper
than that page on every term, configuration and setting, (c) gives a practical, click-path-level
tour of the three named DevOps tools, (d) specifies a production-grade GitHub Actions + Salesforce
pipeline, and (e) deep-dives Salesforce limits, metadata dependencies, deployment constraints and
system properties — the exact line the posting calls *"Understanding of Salesforce limits,
metadata dependencies, and deployment constraints"*.

## Method

1. Pulled the live job posting and the live published training page.
2. Read the current `devops-engineer.md` source in the ServiceNow_Learning worktree
   (`/home/eaguiar2015/wt-sf-devops`) to establish the baseline.
3. Harvested primary sources through a text-extraction proxy where the vendor site is
   client-rendered (`help.salesforce.com` is JS-only and cannot be scraped directly; the
   `developer.salesforce.com` and vendor documentation hosts work).
4. Cross-read the Salesforce CLI plugin source on GitHub so every flag, option and test-level
   description in this bundle is the actual implementation string, not recalled from memory.
5. Ran three parallel vendor-documentation research agents (Gearset; Copado + AutoRABIT;
   GitHub Actions + Salesforce CLI), each instructed to return only what its source documents and
   to flag anything unverified.
6. Cross-checked every limit number against the official Salesforce Apex Developer Guide and
   Metadata API Developer Guide.

## Headline findings

| # | Finding | Why it matters |
|---|---|---|
| 1 | Metadata API deploy ceiling is **≈39 MB compressed / ≈600 MB uncompressed**, with **10,000 files** for unlocked/2GP packages and **35,000** for AppExchange-reviewed 1GP. | The existing page never states a payload ceiling. A release that crosses it fails for a reason no error message explains. |
| 2 | **Only one deployment runs at a time per org.** Queued deployments are *not* executed in submission order. | The classic bank-release failure: three teams all queued "at 9am", and prod got the wrong one first. |
| 3 | The metadata type list that forces a full local test run is **explicit** (ApexClass, Flow, PermissionSet, Profile, CustomField, CustomObject, RecordType, …). A package of only Reports/Dashboards runs **zero** tests. | Lets the release engineer pick the test level deliberately instead of by habit. |
| 4 | `RunRelevantTests` (Beta) is a **fifth** test level, not four. It is the only one that scales test time to payload size. | The existing page says "four stages" and lists four test levels — out of date. |
| 5 | Gearset's current UI uses a **grouped left sidebar** (`My connections`, `Metadata deployments`, `Continuous delivery`, `Backup & archiving`, `Sandbox seeding`, `Settings`). `Work Rules`, `Plan & Deploy`, `Deploy only changed components`, `Invalidate cache` are **not current labels**. | The existing page lists Gearset/Copado/AutoRABIT as a single row of names. Anyone asked "where do I click for backup?" would have guessed. |
| 6 | Gearset **backups are data + metadata backups with a separately licensed product**, and Gearset does **not** perform or schedule the Salesforce sandbox refresh itself. | Directly corrects a likely interview answer of "Gearset refreshes the sandbox". |
| 7 | Copado's "Fundamentals" and "DevOps Center" tiers and "Copado Data Masking" **do not exist** in current documentation. Current branding is **Copado Essentials / Essentials Plus** (standalone SaaS) and **Agentia Pipeline / Agentia Pipeline Pro** (enterprise). | The posting names "Copado" generically; the name you say in the interview should be current. |
| 8 | AutoRABIT has **no** "Test Repository" product and no standalone "Data Masking" product. Data masking lives in **AutoRABIT Vault**; CI/CD is **AutoRABIT ARM**. | Same reason. |
| 9 | "Advanced Admin" is now **Salesforce Certified Platform Administrator II**, and it has a **hard prerequisite**: Salesforce Certified Platform Administrator. | Affects exam sequencing and the claim on a résumé. |
| 10 | There is **no Salesforce-branded "DevOps Engineer" certification.** "DevOps related certs" means vendor credentials: Gearset Academy Certification, Copado Certified, AutoRABIT Academy ARM tracks. | The existing page already hints at this; this bundle gives the exact current names and what each covers. |
| 11 | Gearset's deployment-user requirement is **`Modify All Data`** (or narrowly `Modify Metadata Through Metadata API Functions` with per-type coverage), **`API Enabled`**, and **`Customize Application`** for Flow/LWC/custom-metadata types. | The concrete answer to "what does the integration user need?". |

## Bundle map

| File | Contents |
|---|---|
| `00-plan.md` | Plan, JD → artifact matrix, source policy, confidence rubric. |
| `01-jd-crossreference.md` | Every JD bullet → current page section → coverage verdict → what this bundle adds. |
| `02-limits-and-constraints.md` | Governor limits, platform/org limits, Metadata API deploy limits, metadata dependencies, deployment constraints. |
| `03-devops-tools-ui.md` | Gearset / Copado / AutoRABIT click-path-level tour with plan gates and corrections. |
| `04-github-actions-salesforce-cicd.md` | Production GitHub Actions pipeline, auth, quick-deploy pattern, YAML. Flags verified against the CLI plugin source. |
| `05-jd-term-deep-dive.md` | Term-by-term deep dive: every JD phrase → settings, variations, failure modes. |
| `06-certifications-curriculum.md` | PD1, Platform Administrator II, vendor DevOps certs, curricula, study order. |
| `07-system-properties-setup-paths.md` | Org settings that change deploy/limit behaviour, with Setup paths. |
| `08-cross-bundle-delta.md` | How this bundle relates to sibling bundles; where this one is authoritative. |
| `sources.md` | All sources with access date and verification status. |

## Known corrections to the existing page

| Existing page says | Correction | Evidence |
|---|---|---|
| Four deployment test levels | Five — `RunRelevantTests` (Beta) exists | Salesforce CLI plugin messages + Metadata API guide |
| "Deployment Settings: Allow inbound deployments" only | The Deployment Settings surface also gates CLI deploys and IP-restricted deploys | `07-system-properties-setup-paths.md` |
| Gearset/Copado/AutoRABIT as one generic table row | Three different products with different object models, different plan gates, and several stale names in common use | `03-devops-tools-ui.md` |
| "Salesforce renamed Advanced Admin to Platform Administrator II" | Correct, but the page omits the **Platform Administrator prerequisite** | Salesforce credential page |
| Async heap "6x higher" in the crash course | Async heap is **25 MB** (not 12 MB); async CPU is **60,000 ms** | Apex Developer Guide, governor limits |

## How the merge round should use this bundle

1. Start from `01-jd-crossreference.md` — it is the map from posting to page section.
2. Lift `02`, `05`, `06`, `07` as **collapsible (`<details>`) deep-dive blocks** appended to the
   corresponding existing sections of `devops-engineer.md`.
3. Use `03` to replace the single-line "DevOps tools" table with per-vendor subsections.
4. Use `04` as the new section (or a companion page) for GitHub Actions.
5. Use `08-cross-bundle-delta.md` to resolve conflicts with the sibling bundle
   `2026-11-14T021057Z_salesforcemore-v2`.
