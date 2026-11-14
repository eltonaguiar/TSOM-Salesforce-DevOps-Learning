# 02 — Cross-reference of every bundle, branch and entry

**Scope:** everything in <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning> at
2026-11-14 03:00 UTC — `main`, all branches, every `forreviews/` entry, and the loose files at the
`forreviews/` root.

**Method.** Each bundle was extracted locally and reviewed against primary sources (Metadata API
`deploy()` reference, `apex-gov-limits.html`, the Salesforce CLI plugin sources, and the vendor
documentation). Three independent peer-review passes were run, each covering a different set of
bundles, with the reviewers instructed to cite file:line and to say "cannot verify" rather than
guess.

---

## 1. Inventory

### 1.1 Remote branches

| Branch | Tip | Contents |
|---|---|---|
| `main` | `fd25fb8` | `forreviews/` (13 entries) + `forreviews_final/` (this review) |
| `research/salesforceagain-2026-11-14T020300Z` | `5b5eee2` | My split source: `research/2026-11-14T020300Z-kilo-salesforceagain/` (12 files) |
| `research/salesforcemore-v2-2026-11-14T021057Z` | `0d0f3d4` | The split source of the salesforcemore-v2 entry |
| `research/salesforceagain-v2-20261114` | — | The split source of the salesforceagain-v2 entry |
| `salesforceagain-v3` | — | The split source of the salesforceagain-v3 loose deep dives |

### 1.2 `forreviews/` entries

| Entry | Files | Approx. words | Agent/worktree |
|---|---|---|---|
| `20261114-020300-salesforceagain-kilo/` | 13 | 36,900 | **mine** (`salesforceagain`) |
| `2026-11-14T023507_salesforcemore-v2/` + loose consolidated | 25 | 29,100 + 29,900 | `salesforcemore-v2` |
| `20261114-020852-salesforcemore/` | 12 | 17,350 | `salesforcemore` |
| `20261114-023241-salesforceagain-v2/` + loose consolidated | 11 | — | `salesforceagain-v2` |
| `2026-11-14T023312_salesforcemore-v3/` | 8 | 6,600 | `salesforcemore-v3` |
| `2026-11-14T0210Z-salesforceyetagain-v2/` + 3 loose files | 7 | — | `salesforceyetagain-v2` |
| `salesforceagain-v4-2026-11-14-0230/` | 3 | — | `salesforceagain-v4` |
| `2026-11-14_salesforceagain-v3_*.md` (4 loose) | 4 | — | `salesforceagain-v3` |
| `2026-11-14T021036_salesforceyetagain-v3.md` (1 loose) | 1 | — | `salesforceyetagain-v3` |

**Roughly 75 files from six other agents, plus mine.**

---

## 2. Who is authoritative for what

This is the table the merge round actually needs.

| Topic | Authority | Runner-up | Why |
|---|---|---|---|
| **Metadata API deploy ceilings** (≈39 MB compressed / ≈600 MB uncompressed / 10,000 unlocked-2GP / 35,000 AppExchange-reviewed 1GP) | **mine** | `salesforcemore-v2` (identical, independently derived) | Only my bundle and salesforcemore-v2 carry it. `salesforcemore-v3` has **≈400 MB**, which is wrong by an order of magnitude. `salesforcemore` has none |
| **The 24 metadata types that force a full local test run** | **mine, alone** | — | Nobody else has it. `salesforcemore-v2` has the five test levels but not the trigger types |
| **Five test levels incl. `RunRelevantTests`** | mine + `salesforcemore-v2` | — | `salesforcemore` and `salesforcemore-v3` list **four** |
| **One deploy at a time + queue is NOT FIFO** | mine + `salesforcemore-v2` | — | The others state "one at a time" at most; the FIFO point is what makes it a release-control problem |
| **Governor limits (per-txn and per-org)** | **mine + `salesforcemore-v2`** (agree exactly) | `salesforcemore` (wrong heap) | `salesforcemore` and `salesforcemore-v3` both repeat the published page's wrong **12 MB** async heap |
| **Apex code size + 7,500 code units per deployment** | **mine, alone** | — | `salesforcemore` states a wrong "3 MB per class"; the others are silent |
| **`sf project deploy validate` + 10-day window + new deploy id** | **mine** | — | `salesforcemore-v2` harvests the id from `--dry-run` and never mentions `validate` |
| **CLI flags that do not exist** | **mine** | `salesforcemore-v3` (partly) | A wrong flag fails at the argument parser; this is a table worth having |
| **Runnable GitHub Actions YAML** | **mine** | `salesforcemore-v2` (has four mechanical defects) | Mine is actionlint-clean and flag-verified against CLI 2.158.7 |
| **Gearset / Copado / AutoRABIT click paths + stale-label list** | **mine** | `salesforcemore-v3` (tags its guesses `[UI: likely]`) | Both other bundles use a stale top-nav model (`Dashboard → Compare & Deploy`, `CI/CD` top nav) |
| **Vendor product taxonomy** (Copado Essentials / Copado CI/CD / Agentia umbrella; ARM / Vault / CodeScan / Guard) | **mine** | `salesforcemore-v3` (ARM + Vault only) | Mine is article-cited and includes the negatives |
| **Certifications — names, prerequisites, curricula** | mine + `salesforcemore-v2` | `salesforcemore-v3` (adds the DLA Architect credential, adopted) | Mine has the Platform Administrator prerequisite Trailhead-cited |
| **Key principles / release model / runbook tables** | **`salesforcemore-v2`** | `salesforcemore` (8 principles) | The 12-principle spine with anti-patterns and the release-model tables are theirs; my `00-plan.md` §4 is a compact fallback |
| **Term glossary in a fixed 5-part shape** | **`salesforcemore-v2`** (28 entries) | `salesforceagain-v2` (RACI) | Adopt their shape; take the RACI |
| **RACI** | **`salesforceagain-v2`** (`05:353-368`) | — | Nobody else has it |
| **Page → section inventory for all five guides** | **`salesforcemore`** (`merge-against-pages/MAPPING_MATRIX.md`) | `salesforcemore-v2` (`merge-map.md` §8) | Mine covers only the DevOps page |
| **Sibling-page (crash course etc.) material** | `salesforcemore` (verbatim captures only) | `salesforceyetagain-v2` (planning + crash-course work) | See §4 |

---

## 3. Contested claims and how to settle them

| # | Claim | Position A | Position B | **Call** |
|---|---|---|---|---|
| 1 | Compressed payload cap | mine + salesforcemore-v2: **≈39 MB** | salesforcemore-v3: **≈400 MB** | **A.** 400 MB is wrong by ~10×. B's own "10,000 files" row is right, which makes its byte cap more dangerous, not less |
| 2 | Async heap | mine + salesforcemore-v2: **25 MB** | salesforcemore, salesforcemore-v3: **12 MB** | **A.** Both wrong values were inherited from the published crash course. This is the highest-traffic correction in the whole exercise |
| 3 | Test levels | mine + salesforcemore-v2: **five** | salesforcemore, salesforcemore-v3: **four** | **A** |
| 4 | Coverage rule | mine: **75% per class/trigger individually** | salesforcemore: "75% org-wide, 1% per class minimum"; salesforcemore-v3: "1% trigger rule" | **A.** There is no "1% per class" rule in Salesforce. Both wrong claims are invented |
| 5 | Apex code size | mine: **6 MB per org (10 MB scratch), 1 M chars per class, 7,500 code units per deployment** | salesforcemore: "3 MB per class/trigger, 6 MB total in some contexts", "1 million per org" | **A.** "3 MB per class" does not exist; "1 million" is per class/trigger, not per org |
| 6 | Deploy queue | mine + salesforcemore-v2: one at a time **and not FIFO** | others: one at a time, no FIFO statement | **A** |
| 7 | `sf org login jwt` flags | mine + salesforcemore-v2 + salesforcemore-v3: `--jwt-key-file`, no `--client-secret` | — | **Consensus.** Correct |
| 8 | `sf project deploy report` flag | salesforcemore: `--deploy-id` | mine + salesforcemore-v3: `--job-id` | **B.** Verified against `plugin-deploy-retrieve/src/commands/project/deploy/report.ts` |
| 9 | CLI package to install | salesforcemore: `npm i -g sfdx-cli` | mine + salesforcemore-v3: `npm i -g @salesforce/cli` | **B.** `sfdx-cli` is the deprecated predecessor |
| 10 | Copado enterprise name | mine (before this review): "Agentia Pipeline / Pro" as the enterprise product | salesforcemore-v2: "Copado CI/CD … Agentia as the AI layer" | **Both, at different levels — now resolved in my bundle.** `copado.com/platform-overview` shows **Copado CI/CD** (enterprise), **Agentia** (unified umbrella, whose docs publications are *Agentia Pipeline* / *Agentia Pipeline Pro*), and **Copado Essentials** (standalone SaaS) |
| 11 | AutoRABIT masking location | mine: in **Vault**, with the exact path | salesforcemore-v2: "may sit in Vault… verify" | **A**, keep the hedge as a footnote only |
| 12 | Validation path | mine: `sf project deploy validate` → job id → `sf project deploy quick` | salesforcemore-v2: `--dry-run`, harvest id | **A.** The CLI's own doc says the job id comes from `validate` and is valid 10 days |
| 13 | `RunRelevantTests` API gate | salesforcemore-v2: "API version 66.0+" (asserted 4×) | mine: no version claim | **Mine.** The version gate could not be confirmed against the CLI messages or the Beta doc — drop it or cite the Beta doc |
| 14 | Admin II rename | mine + salesforcemore-v2: fact | salesforcemore-v3: `vendor-claim` | **Mine** (Trailhead-cited). Keep the hedge only for exam *weights* |
| 15 | Admin II prerequisite | mine + salesforcemore-v2: Platform Administrator is a hard prereq | salesforcemore: self-contradictory; salesforcemore-v3: absent | **Mine** |
| 16 | JD numbering | mine (now fixed): R1–R14, Q1–Q14 with Q8a–Q8d | salesforcemore-v2: R1–R12 / Q1–Q14 | **Mine after correction.** See §5 |
| 17 | Gearset navigation | mine: 6 groups from article navigation | salesforcemore-v2: 9 groups from the docs collection index | **Publish neither as *the* UI.** Publish task→screen; see §4 |

---

## 4. The one structural disagreement — and how to settle it

**Gearset navigation grouping.** My bundle lists six left-sidebar groups from the individual
articles. `salesforcemore-v2` lists nine, including *Problem analyzers*, *Observability* and
*Automated testing*, taken from the docs collection index. Neither is false; they are different
resolutions of the same doc set.

**Resolution:** do not publish a sidebar diagram at all. Publish a **task → screen** table
(`Compare and deploy`, `Deployment history`, `CI jobs`, `Pipelines`, `Data backup jobs`,
`Configure in-place masking`, …), and add one line noting that the left navigation is grouped and
that group names vary by rollout and licence tier. A task-to-screen table survives a UI change; a
screenshot does not.

The same rule applies to the Copado and AutoRABIT sections: publish the object model and the task
paths, and put every literal label behind a "labels vary by release — confirm in your tenant"
caveat.

---

## 5. Corrections I made to my own bundle as a result of this review

Recording these because the merge round needs to know the current state, not the state at first
push.

| # | Change | File | Why |
|---|---|---|---|
| 1 | **Removed the `~/.sfdx` and `~/.sf` cache from the PR-validation workflow** and replaced it with a `~/.npm`-only cache | `04` | Those directories hold the CLI's **auth state** — org aliases and refresh tokens. A restored runner can present a stale credential; a poisoned cache becomes a credential-injection path. Caught by my own CI research agent |
| 2 | Rewrote the runner-hygiene bullet to say the same thing | `05` | It previously recommended caching `~/.sfdx`/`~/.sf` |
| 3 | **Removed `sf project run`** from the CLI table — the command does not exist | `05` | Peer review found it; verified against the CLI command inventory |
| 4 | Added a **"commands and flags that do not exist"** table (19 entries) covering `sf project deploy quick deploy`, `--deploy-id`, `--jwt-key`, `--client-secret`, `--target-url`, `--wait-timeout`, `--code-coverage`, `--skip-lint`, `--warning-email`, `--test-name`, `sf project run`, `sf apex run query`, `sf package promote`, `sf code analyzer`, `sf lightning-inspect`, `sfdx-cli` | `04` | These fail at the argument parser, which is a confusing way to learn a mistake |
| 5 | Sharpened the **OIDC** position: Salesforce Token Exchange is a custom-handler external-IdP mechanism with **no official GitHub Actions recipe** — it is not a first-class CLI flow | `04` | Peer review |
| 6 | **Renumbered the JD qualification labels** from Q1–Q17 to the posting's actual **Q1–Q14**, with the posting's eighth bullet split into **Q8a–Q8d** | `01`, `00-plan` | The posting has 14 qualification bullets, not 17. My earlier draft over-counted by splitting one bullet into four and numbering the rest sequentially |
| 7 | Flagged the **`Setup > Deploy > Deployment Settings` labels as unverified** and added `SF_ORG_METADATA_REST_DEPLOY` / `org-metadata-rest-deploy` as the currently documented surface | `07` | Peer review could not confirm the labels; only "Enable Salesforce CLI Deploys" appears in an older guide |
| 8 | Added the **sandbox refresh cadence** (Developer 1 day, Partial Copy 5 days, Full 29 days) and **scratch org allocations** (Developer/trial 6/3, Enterprise 80/40, Unlimited 200/100) | `02` §7, `07` §3 | Peer review; verified against the Salesforce DX developer guide |
| 9 | Added the **Salesforce Certified Development Lifecycle and Deployment Architect** credential — the single most on-point Salesforce credential for this posting | `06` | Contributed by a peer review; it was the one credential my bundle was missing |
| 10 | **Resolved the Copado enterprise naming**: Copado Essentials (standalone) + **Copado CI/CD** (enterprise) + **Agentia** (unified umbrella, publications *Agentia Pipeline* / *Agentia Pipeline Pro*) | `03` | Two peer reviews disagreed; resolved against `copado.com/platform-overview` |
| 11 | Added the **`--details markdown="1">` convention** note to the merge plan | `04-merge-plan` | The DevOps page already uses 26 `markdown="1"` blocks and zero plain ones. Plain `<details>` in kramdown renders the Markdown inside as literal text |
| 12 | Added 5 new sources and a `copado.com/platform-overview` citation | `sources.md` | — |

---

## 6. Gaps that remain open across every bundle

| Gap | Covered by |
|---|---|
| The 24 metadata types that force a full local test run | **mine only** |
| The 7,500 code-unit per-deployment ceiling and the 6 MB org Apex ceiling | **mine only** |
| `sf project deploy validate` semantics, the 10-day window, the new deployment id | **mine only** |
| Deployment Status page mechanics (two live charts, 30-day history, cancellation) | **mine only** |
| `checkOnly` cannot validate a Master-Detail ↔ Lookup field-type change | **mine only** |
| The Master-Detail Recycle Bin destruction rule | **mine only** |
| Retention/expiry numbers (Copado 30-day token TTL, AutoRABIT 3-day approval auto-reject, 30/90-day report retention, 96-hour quick-deploy window, Gearset 7-year retention) | **mine only** |
| A runnable, lint-clean CI pipeline | **mine only** |
| Exam curriculum **weights** | **nobody** — the Trailhead study-guide trails are client-rendered. Publish domain names, not percentages |
| The published crash course's wrong heap figures flagged for correction | **mine only** (this review) |

---

## 7. What each bundle should have done differently

Aimed at the other agents, but written so the merge round can act on it directly.

### 7.1 `2026-11-14T023507_salesforcemore-v2` — the best-sourced bundle, with three YAML defects

**Take as-is:** `01/principles.md` (12-principle spine with anti-patterns), `01/release-model.md`
(runbook template, rollback table, control-gate checklist), `02/governor-limits.md`,
`02/other-limits-and-system-settings.md` §3 and §5, `02/dependencies-and-constraints.md` §2, §7
and §9, `04/auth-secrets-environments.md`, `06/term-entries.md` (28 entries, fixed 5-part shape),
`06/term-index.md` (coverage checklist), `07/merge-map.md` §3 and §8, `00-source-log/job-description.md`
R/Q numbering.

**Fix before merge:**
- `02/inspection-and-drills.md:9, :10, :25` and `02/other-limits-and-system-settings.md:21` list
  **`sf org list limits`**, which **does not exist**. The correct command is **`sf limits api
  display`**, and it shows **API request limits only — not storage**. Delete the "Storage" row's CLI
  cell.
- Drop the **"API version 66.0+"** gate on `RunRelevantTests` (`dependencies-and-constraints.md:117`,
  `term-entries.md:130`, `inspection-and-drills.md:72`, `github-actions-salesforce.md:243`,
  `08-cross-bundle-notes.md:23`). It could not be confirmed against the CLI messages or the Beta
  doc. Name `@IsTest(critical=true)` / `@IsTest(testFor='…')` instead.
- **Do not paste the reference YAML** (`04/github-actions-salesforce.md`). Four defects:
  1. `inputs.target` is bound only on `workflow_dispatch` (`:26-34`), so on `pull_request`/`push`
     `inputs.target || 'qa'` silently resolves to `'qa'` at `:40`, `:104`, `:162`, `:201`. The
     table at `:10` claims the workflow targets QA/UAT/Pre-Prod/Prod on a push — it never does.
  2. `sf project deploy quick` is run against `inputs.target` ∈ {qa, uat, preprod, prod}
     (`:187-192`), but the CLI's own doc says **"Don't use this command on sandboxes; the command is
     intended to be used on production orgs."** Three of four targets are wrong.
  3. `sfdx-git-delta` uses the **deprecated** `--output` / `--source` flags (`:76-81`, `:133-138`,
     `other-ci-platforms.md:52-53`, `:94-95`); v6 renamed them `--output-dir` / `--source-dir`.
  4. The tagging job needs `fetch-depth: 0` or it has no tags to push.
- `04/other-ci-platforms.md:90` writes the JWT key into the job **working directory**
  (`printf '%s' "$SF_JWT_KEY" > server.key`). Use `$RUNNER_TEMP` as the GitHub version does at
  `:66`.
- `03/copado-autorabit-devopscenter.md:11` and `03/tool-landscape.md:32` describe the enterprise
  product as "Copado CI/CD" with "Agentia as the AI layer"; the *docs publication* names are
  *Agentia Pipeline* / *Agentia Pipeline Pro*. Both levels are real — keep both, as now corrected
  in my bundle.
- `03/copado-autorabit-devopscenter.md:46` hedges AutoRABIT masking as "may sit in Vault or a
  related module — verify the edition". It **is** Vault; use the exact path.

**Skip:** `07/content-gaps.md` and `08/cross-bundle-notes.md` — merge instructions, not page content.

### 7.2 `20261114-020852-salesforcemore` — the best narrative, the weakest precision

**Take as-is:** `merge-against-pages/MAPPING_MATRIX.md` (the page→section inventory for all five
guides — the only artifact that maps the non-DevOps pages), `salesforce-principles/KEY_PRINCIPLES.md`,
`SALESFORCE_DEVOPS_DEEP_DIVE.md` §2, §4–§13, §23–§26 (conflict clinic, environment table, hotfix
rules, audit pack, labs, interview drills).

**Fix before merge:**
- `SALESFORCE_LIMITS_DEEP_DIVE.md:22` and `KEY_PRINCIPLES.md:60` give async heap as **12 MB** —
  the published page's error. **25 MB.**
- `SALESFORCE_LIMITS_DEEP_DIVE.md:75` says "Apex code size | 3 MB per class/trigger (6 MB total in
  some contexts)". There is no 3 MB per class. `:76` says "Apex characters | 1 million per org" —
  it is **per class / per trigger**. `:78` "Custom objects | Varies by edition (e.g., 2,000
  Enterprise)" — unverifiable, and the long-standing limit is **100 custom objects per org** for
  most editions. All three contradict the bundle's own `source-capture/crash-course.md:231`.
- `SALESFORCE_DEVOPS_DEEP_DIVE.md:275` and `KEY_PRINCIPLES.md:113` list **four** test levels.
- `SALESFORCE_LIMITS_DEEP_DIVE.md:84` and `KEY_PRINCIPLES.md:103` state "75% org-wide … 1% per class
  minimum". There is no 1% rule.
- `SALESFORCE_DEVOPS_DEEP_DIVE.md:599` installs `sfdx-cli` — deprecated predecessor.
- `SALESFORCE_DEVOPS_DEEP_DIVE.md:451-499` uses a **stale Gearset top-nav model**
  (`Dashboard → Compare & Deploy`, `Org Browser`, `CI/CD` top nav). Re-cut against the verified
  task→screen table before publishing.
- `CERTIFICATION_RESEARCH.md:67` is self-contradictory: it calls Platform Administrator "the
  credential the posting calls 'Advanced Admin'", while `:58` correctly identifies "Advanced Admin"
  as Platform Administrator **II**.
- `source-capture/README.md:12` and `:20` say a `devops-engineer.md` capture exists in
  `source-capture/`. **It does not** — there are 12 files and no such capture. Either add it or fix
  the index.

**Skip:** `source-capture/*.md` — these are **verbatim copies of the published pages** (headers
`Agent: opencode | Date: 2026-11-10`). Merging them back into the site is a self-merge. Keep them
only as a local reference copy. They are, however, the reason this bundle inherited the 12 MB heap
error.

### 7.3 `2026-11-14T023312_salesforcemore-v3` — the best methodology, two wrong numbers

**Take as-is:** the **`[Verify]` / `vendor-claim` confidence vocabulary** (`sources.md:24`) — adopt
it for the whole merge; `02-devops-tools-walkthroughs.md:139-183` (the CLI block: `validate`,
`quick --job-id`, `report --job-id`, `sfdx-git-delta` `sgt`, `@salesforce/cli` vs `sfdx`);
`04-limits-dependencies-constraints.md:80`, `:88-97` (the Master-Detail two-step worked example),
`:81` (`UNABLE_TO_LOCK_ROW`), `:143-151` (rollback reality);
`05-jd-term-deep-dives.md:37-38` (OSFI B-10/B-13), `:49-50` (`SandboxPostCopy`), `:90` (flow trigger
order 1–2000); `03-github-cicd-salesforce.md:183-198` (anti-patterns, auth/secret rotation).

**Fix before merge:**
- `04-limits-dependencies-constraints.md:66` gives the compressed payload cap as **≈400 MB**. It is
  **≈39 MB**. The same table's "10,000 files" (`:65`) is right, which is what makes the wrong byte
  cap dangerous.
- `04-limits-dependencies-constraints.md:19` gives async heap as **12 MB**. It is **25 MB**.
- `04-limits-dependencies-constraints.md:69` — "Every trigger needs some coverage [Verify the 1%
  trigger rule]". There is no 1% rule; it is **75% per class/trigger individually**.
- `04-limits-dependencies-constraints.md:70` lists **four** test levels.

**Re-cut before publishing:** the Gearset / Copado / AutoRABIT click-paths in
`02-devops-tools-walkthroughs.md:21-134` are tagged `[UI: likely]` / `[UI: verify]`, which honours
the bundle's own policy — but several positive labels are still wrong for Gearset. Use the task
→ screen table from my bundle instead and keep this bundle's `[UI: …]` tagging as the convention.

**Add from mine:** the 24-type forced-test list, the 7,500 code-unit ceiling, `deploy validate`
semantics, the Deployment Status mechanics, the `checkOnly` Master-Detail restriction, the
Master-Detail Recycle Bin rule, the retention/expiry numbers, and the current Gearset job-type
labels.

### 7.4 `20261114-023241-salesforceagain-v2` — strong middle ground, with a production-deploy defect

**Take as-is:** `02-metadata-dependencies-and-deployment-constraints.md` (the best
dependency/failure catalogue in the review — error→cause→fix at `:109-157`, the
profile/permission-set model at `:161-210`); `05-jd-term-by-term.md:353-368` (the **RACI**, which
nobody else has); `06-certifications-and-curriculum.md:121-144` (the official deployment-lifecycle
Architect credential, adopted into my bundle); the JWT auth flags at `04:63-69`.

**Fix before merge:** heap 12 MB (D27), four test levels (D28), "10,000 components" (D29), the
**validate-against-preprod-then-quick-deploy-to-prod** production defect (D30), and the
**`server.key` artifact upload** (D31). The last one is the worst kind of defect in this exercise:
it publishes the private key.

**Skip:** the loose consolidated copy `2026-11-14T023241_salesforceagain-v2.md` (24,547 words) —
it is a concatenation of the ten split files with no unique research.

### 7.5 `salesforceagain-v4-2026-11-14-0230` — skip wholesale

`comprehensive-devops-research.md` contains a wrong heap figure (D17), a callouts limit of **1**
instead of 100 (D18), a 10 MB package cap instead of ≈39 MB (D19), an invalid CLI flag (D20), an
unverifiable exam-weight table (D36), an unverifiable `.gearset/pipeline.yml` schema (D37), an
unsubstantiated "Banking/Finance Pack" (D38), and a false certification claim (D21). It has no
source list. Nothing from it should be merged without a full rewrite.

### 7.6 The loose `salesforceagain-v3` deep dives — mostly unusable, one good idea

| File | Verdict |
|---|---|
| `..._devops-gearset-ui-deep-dive.md` | **Skip** — stale nav (D39) and invented keyboard shortcuts (D40) |
| `..._devops-github-cicd-pipeline.md` | **Skip** — uses interactive `sf org login web` in CI (D25); unverifiable third-party action (D41) |
| `..._devops-governor-limits-deep-dive.md` | **Skip** — wrong org Apex ceiling (D22), wrong coverage rule (D23), non-existent command (D26) |
| `..._devops-metadata-dependencies-deep-dive.md` | **Take the dependency graph only.** Discard the "no automatic ordering — order package.xml yourself" model (D24) and the unverifiable circular-reference rule (D42) |

### 7.7 `salesforceyetagain-v2` — route to the crash course as corrections, not as a new page

`2026-11-14T0210Z-salesforceyetagain-v2-02_crash-course.md` (7,329 words) is a large derivative of
the **already-published** crash course (it credits the opencode page as its source at `:5`), plus
labs, user/data and DevOps material. It omits the live page's ELI5 introduction, the Official
Learning Resources section and the Quick Start Checklist.

**Route it to `crash-course.md` as corrections**, not as a replacement. The only substantive
findings are D32 (the certification claim), D33 (`sf org login web -d`) and D34 (the pseudo
system-properties table). The 9-principle planning file is useful but duplicates my `00-plan.md` §4.

`2026-11-14T021036_salesforceyetagain-v3.md` is an explicit placeholder with zero research content —
either fill it or drop it (D48).

### 7.8 The general rules

- **Do not merge from the loose consolidated `.md` files.** They are concatenations with duplicated
  headings. Merge from the split files.
- **A bundle whose content is a copy of a published page is a reference copy, not research.** Mark
  it as such so the merge round does not paste a page back into itself.
- **Every numeric claim needs a source tag.** The two bundles that used one produced the fewest
  errors; the ones that did not produced most of the S1 defects above.
