# 08 — Cross-bundle delta and reconciliation

**For the merge round.** This bundle is one of two independent research drops for Scotiabank
requisition 276046. This file records the overlap, who is authoritative where, and what to do
about the one genuine divergence.

| Field | Value |
|---|---|
| This bundle | `research/2026-11-14T020300Z-kilo-salesforceagain/` |
| Worktree | `salesforceagain` |
| Sibling bundle | `research/2026-11-14T021057Z_salesforcemore-v2/` |
| Sibling worktree | `salesforcemore-v2` |
| Both started | 2026-11-14 (UTC) |
| Downstream target | `docs/salesforce/devops-engineer.md` in the ServiceNow_Learning repo |

The sibling bundle already wrote a reconciliation file against this bundle's early README
(`08-cross-bundle-notes.md` in that bundle). **We agree on all eight headline corrections** — the
deploy ceilings, the one-deploy-at-a-time/non-FIFO queue, the five test levels, the Gearset UI
shape and backup product, the Copado and AutoRABIT product renames, and the Platform
Administrator II prerequisite. No reconciliation conflict remains on those.

---

## 1. Where this bundle is the better source

| # | Content only this bundle has | Why it wins | Where to lift it |
|---|---|---|---|
| 1 | **The complete list of metadata types that force all local tests to run** — `ApexClass`, `ApexComponent`, `ApexPage`, `ApexTrigger`, `ArticleType`, `BaseSharingRule`, `CriteriaBasedSharingRule`, `CustomField`, `CustomObject`, `DataCategoryGroup`, `Flow`, `InstalledPackage`, `NamedFilter`, `OwnerSharingRule`, `PermissionSet`, `Profile`, `Queue`, `RecordType`, `RemoteSiteSetting`, `Role`, `SharingReason`, `Territory`, `Validation Rules`, `Workflow` — plus the worked examples (1 `CustomField` forces a full run; 100 Reports + 40 Dashboards does not) | It is the single most actionable fact in the posting's test-and-validation area, and it is quoted verbatim from the Metadata API Developer Guide. The sibling bundle has the five test levels but not the type list | `02-limits-and-constraints.md` §5.1 |
| 2 | **CLI flags verified against the plugin source, not the docs** — `sf org login jwt` uses `--jwt-key-file` and has **no `--client-secret`**; `sf org login jwt` has aliases `force:auth:jwt:grant` / `auth:jwt:grant` (deprecated) | Several widely copied runbooks show `--jwt-key` and `--client-secret`; neither exists in the current implementation. Publishing the wrong flag is a broken pipeline for the reader | `04-github-actions-salesforce-cicd.md` §2.2 |
| 3 | **`sf project deploy validate` semantics** — it **requires** Apex tests (`NoTestRun` is not an option); it **does not support source tracking**; the CLI explicitly says **"Don't use this command on sandboxes"** and directs you to `sf project deploy start --dry-run --test-level RunLocalTests` for sandbox validation | This is the validate/quick-deploy pattern the posting implies, and the sandbox/prod split is a common source of broken pipelines | `04` §4.4 |
| 4 | **`sf project deploy quick` semantics** — the validation job id is **valid for 10 days**; `--use-most-recent` only considers validations from the **past 3 days or less**; it skips Apex tests; it does not support source tracking; it is not intended for sandboxes | These are the exact rules that decide whether a quick deploy is legitimate | `04` §4.4 |
| 5 | **`sf apex run test` flag set** — `--output-dir`, `--class-names`, `--suite-names`, `--result-format` with values `human` / `tap` / `junit` / `json`, `--detailed-coverage`, `--synchronous`, `--poll-interval`, `--wait` | Needed to wire a real JUnit/coverage artefact into a CI pipeline | `04` §4.1 |
| 6 | **`checkOnly` cannot validate a Master-Detail ↔ Lookup field-type change**; a deploy that adds a Master-Detail field soft-deletes all detail records in the Recycle Bin and **permanently deletes them during the deploy**; a Lookup→Master-Detail conversion requires detail records to reference a master or be soft-deleted, and a successful deploy **permanently empties the Recycle Bin** | A destructive, non-recoverable data behaviour that belongs on a release-engineering page, and which a Git revert cannot undo | `02` §4.2 and §4.3 |
| 7 | **Deployment Status page mechanics** — two live charts (components processed; Apex tests run, with the currently running test named), cancellation semantics including `Finalizing Deploy` on API 65.0+, and a **30-day** deployment history window | Directly supports the audit-evidence discussion: Salesforce's own view is only 30 days, so a 7-year retention policy requires exporting CI artefacts | `02` §3.2, `07` §2 |
| 8 | **The negative-result lists** — 16 numbered "not a current documented label" findings for Gearset, Copado and AutoRABIT (`Work Rules`, `Plan & Deploy`, `Deploy only changed components`, `Invalidate cache`, `Last deployed`/`Unmanaged` as compare tabs, `Pipeline Job`/`Deployment Job`, `Reset sandbox`, Copado `Fundamentals`/`DevOps Center`/`Data Masking`, Copado Work Item types and "Blocked" status, AutoRABIT `Test Repository`, AutoRABIT `Max Batch Size`, ARM "Stages/Steps/Components" vocabulary, and more) | The most valuable training artefact in the bundle, because it stops the page from teaching wrong labels and stops the reader from asserting them in an interview. The sibling bundle has the corrections but not the exhaustive negative list | `03` §0 and §5 |
| 9 | **Specific retention/expiry numbers that are release blockers** — Copado credentials expire after **30 days** of inactivity (Salesforce refresh-token TTL) with no proactive warning; AutoRABIT pending approvals **auto-reject after 3 days** and **self-approval is impossible even for an admin**; AutoRABIT CI build reports are unavailable after **30 days** and SCA source after **90 days**; AutoRABIT Quick Deploy uses components validated in the last **96 hours**; Gearset record data is retained **7 years** with metadata retained indefinitely; AutoRABIT masking rollback data is retained **7 days** | These are the numbers a release engineer must put in a runbook | `03` §2.8, §2.9, §3.4, §3.5, §3.6, §1.8 |
| 10 | **Copado's per-commit/promotion file ceilings** — 8,000 files for a Copado-created commit or promotion, 10,000 for manual-step or Git-repository deployments; and **only a Copado Admin** may add user stories to a promotion targeting production | A concrete gate a release engineer can be asked about | `03` §2.4 |
| 11 | **The 7,500 class-and-trigger code units per Apex deployment ceiling**, alongside the 6 MB org-wide Apex code ceiling and the 10 MB scratch ceiling | The per-deployment ceiling is the one that bites large orgs and is absent from most training material | `02` §2.4 |
| 12 | **AutoRABIT masking precedence** — local masking rules take precedence over global rules; `Config Details` can disable workflows, validation rules, triggers and flows during masking | Operationally important when a masking run fails on an automation | `03` §3.5 |
| 13 | **A full org-settings catalogue mapped to JD lines** — `Setup > Deploy > Deployment Settings` (inbound deploy gate, CLI deploy gate, deployment IP allowlist, 30-day history), sandbox templates as a privacy control, debug logs as a **data-leak surface** in a bank, the "deployed but nothing happened" post-deploy checklist, and a settings-matrix by JD term | The sibling bundle covers system settings more briefly; this bundle indexes them against the posting so nothing is orphaned | `07` |

---

## 2. Where the sibling bundle is the better source

| # | Content in the sibling bundle | Why it wins | Where to lift it |
|---|---|---|---|
| 1 | `01-salesforce-key-principles/principles.md` and `release-model.md` | The user explicitly asked for "planning best on Salesforce key principles". The sibling bundle has this as a standalone, well-argued artifact; this bundle only has the principle table inside `00-plan.md` §4 | Use the sibling's principles as the framing layer; this bundle's `00-plan.md` §4 is a compact fallback |
| 2 | Folder-per-topic organisation with an explicit **"Merge target"** line on every file | This bundle is flat-file. The "Merge target" annotation tells the merge round exactly which downstream section each artefact feeds, which removes guesswork | Adopt the annotation convention in the merged page |
| 3 | `07-merge/merge-map.md` and `content-gaps.md` | The sibling bundle already produced a merge map and a gap list. Do not duplicate that work | Use theirs as the merge plan; this bundle's `01-jd-crossreference.md` is the supporting evidence |
| 4 | `02-limits-constraints/inspection-and-drills.md` | A practical "where do I look" companion (UI paths + CLI/code) plus interview drills. This bundle has the limits but fewer inspection drills | Merge both; the sibling's drills are the more usable form for a student |
| 5 | `03-devops-tools/gearset-click-paths.md` lists a **more granular Gearset navigation grouping** (adding *Problem analyzers*, *Observability*, *Automated testing*, *Sandbox seeding & compliance*, *Settings / Team management*) | See the divergence below | Use theirs as the navigation list; use this bundle's article-level citations |
| 6 | `05-certifications/certification-landscape.md` and `vendor-and-study-plan.md` | The sibling bundle separates the landscape from the curriculum and adds a study plan; this bundle combines them | Use theirs for the study plan; this bundle adds the **prerequisite chain** and the exam-domain mapping |
| 7 | `06-term-deep-dives/term-index.md` and `term-entries.md` | A one-entry-per-term format with interview lines. This bundle's `05` covers the same ground with more configuration depth per term | Use the sibling's index format, this bundle's depth |

---

## 3. The one genuine divergence — Gearset navigation grouping

| Bundle | Navigation groups |
|---|---|
| This bundle (`03` §1.1) | `My connections` · `Metadata deployments` · `Continuous delivery` · `Backup & archiving` · `Sandbox seeding` · `Data deployments` · `Settings` |
| Sibling bundle | `My connections` · `Metadata deployments` · `Continuous delivery` · `Backup & archiving` · `Sandbox seeding & compliance` · `Problem analyzers` · `Observability` · `Automated testing` · `Settings / Team management` |

**Neither is wrong; they are different resolutions of the same doc set.** The sibling's list comes
from the Gearset **documentation collections index**; this bundle's list comes from the individual
articles' navigation and the screens those articles describe (there is a separate `Data history`
screen under data deployments, which the sibling's grouping folds elsewhere).

**Resolution for the merged page:** do not publish a single rigid sidebar as *the* Gearset UI.
Publish the **task → screen** mapping (which both bundles agree on and which is what a learner
needs), and note that the left sidebar is grouped and that group names vary by rollout and licence
tier. A task-to-screen table is stable; a screenshot of a sidebar is not.

---

## 4. Suggested merge order

1. **Framing** — sibling `01-salesforce-key-principles/*` (principles + release model).
2. **Structure** — sibling `07-merge/merge-map.md` (which section takes what).
3. **Depth, in page order** — this bundle's `01` (JD cross-reference) drives the order; then
   `02` (limits) → `03` (tools) → `04` (CI/CD) → `05` (terms) → `06` (certs) → `07` (settings).
4. **Sibling extras** — `inspection-and-drills.md` after the limits section;
   `certification-landscape.md` + `vendor-and-study-plan.md` after the certifications section;
   `term-index.md` alongside `05`.
5. **Formatting** — wrap every deep dive in `<details><summary>…</summary>…</details>` and keep
   the existing page's section numbering intact so existing links still resolve.
6. **Corrections** — apply the correction table in this bundle's `01` §3 and the sibling's
   `08-cross-bundle-notes.md` §2 together; they do not conflict.

---

## 5. Conflicts requiring a human decision

| # | Question | Why it needs a decision |
|---|---|---|
| 1 | Does the published page get a **companion page** (`devops-engineer-deep`) or do all of this get folded into `devops-engineer.md` as collapsible blocks? | The merged content is several times the current page length. The user asked for "deeper documentation into collapsible sections", which suggests folding in — but a companion page keeps the original scannable and is easier to maintain |
| 2 | Should the **sub-agent research** be published, or distilled into prose? | The negative-result lists (`03` §5) are valuable but read like an audit. Publishing them under a `<details>` "Naming traps and stale labels" heading preserves their value without cluttering the page |
| 3 | Is the **exam-domain weighting** table published at all? | Neither bundle could retrieve the current weights (the Trailhead study-guide trails are client-rendered). Publishing unverified weights would be a mistake. **Recommendation: publish the domain names, not the percentages**, and link the study guide |
| 4 | Do the **Copado prices** stay in? | Vendor pricing changes; it is not needed for the posting. **Recommendation: drop the prices, keep the edition-feature matrix** |
| 5 | Should the Gearset **navigation grouping** be published as a sidebar diagram? | See §3. **Recommendation: no diagram; publish the task → screen table instead** |
