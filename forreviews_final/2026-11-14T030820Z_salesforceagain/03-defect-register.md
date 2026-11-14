# 03 — Defect register: every actionable correction, by bundle

**Purpose:** a flat, actionable list so each agent (or the merge round) can fix or drop items
without re-reading three long peer reviews. Every row is a defect with a location and a correction.

**Severity:**
**S1** = would publish a factually wrong number or a broken command ·
**S2** = would publish an unverified claim as fact ·
**S3** = structural / hygiene.

---

## 1. S1 — would publish a wrong fact

| # | Bundle | Location | Wrong | Correct | Evidence |
|---|---|---|---|---|---|
| D1 | `2026-11-14T023312_salesforcemore-v3` | `04-limits-dependencies-constraints.md:66` | "Max compressed payload ~400 MB" | **≈39 MB** compressed (base64 payload ≤50 MB) | Metadata API `deploy()` |
| D2 | `2026-11-14T023312_salesforcemore-v3` | `04-limits-dependencies-constraints.md:19` | Heap "6 MB / 12 MB" | **10 MB / 25 MB** | `apex-gov-limits` |
| D3 | `2026-11-14T023312_salesforcemore-v3` | `04-limits-dependencies-constraints.md:69` | "Every trigger needs some coverage [1% rule]" | **75% per class and trigger individually**; there is no 1% rule | CLI `messages/deploy.metadata.md` |
| D4 | `2026-11-14T023312_salesforcemore-v3` | `04-limits-dependencies-constraints.md:70` | Four test levels | **Five** — add `RunRelevantTests` (Beta) | CLI messages |
| D5 | `20261114-020852-salesforcemore` | `SALESFORCE_LIMITS_DEEP_DIVE.md:22`, `salesforce-principles/KEY_PRINCIPLES.md:60` | Heap "6 MB / 12 MB" | **10 MB / 25 MB** | `apex-gov-limits` |
| D6 | `20261114-020852-salesforcemore` | `SALESFORCE_LIMITS_DEEP_DIVE.md:75` | "3 MB per class/trigger" | No such limit. **1,000,000 characters per class/trigger; 6 MB total Apex per org (10 MB scratch)** | `apex-gov-limits` |
| D7 | `20261114-020852-salesforcemore` | `SALESFORCE_LIMITS_DEEP_DIVE.md:76` | "1 million characters per org" | **per class / per trigger**, not per org | `apex-gov-limits` |
| D8 | `20261114-020852-salesforcemore` | `SALESFORCE_LIMITS_DEEP_DIVE.md:78` | "Custom objects: varies, e.g. 2,000 Enterprise" | **Not verifiable**; the long-standing limit is **100 custom objects per org** for most editions. Drop | org limits |
| D9 | `20261114-020852-salesforcemore` | `SALESFORCE_LIMITS_DEEP_DIVE.md:84`, `KEY_PRINCIPLES.md:103` | "75% org-wide, 1% per class minimum" | **75% per class/trigger individually** | CLI messages |
| D10 | `20261114-020852-salesforcemore` | `SALESFORCE_DEVOPS_DEEP_DIVE.md:275`, `KEY_PRINCIPLES.md:113` | Four test levels | **Five** | CLI messages |
| D11 | `20261114-020852-salesforcemore` | `SALESFORCE_DEVOPS_DEEP_DIVE.md:599` | `npm install -g sfdx-cli` | `npm install -g @salesforce/cli@<pinned>` | `sfdx-cli` is deprecated |
| D12 | `2026-11-14T023507_salesforcemore-v2` | `04-github-actions-salesforce.md:142-150` | Harvests the quick-deploy job id from `--dry-run` | Use **`sf project deploy validate`**, which returns a job id valid **10 days** | CLI `deploy.metadata.validate.md` |
| D13 | `2026-11-14T023507_salesforcemore-v2` | `04-github-actions-salesforce.md:187-192` | `sf project deploy quick` run against qa/uat/preprod | The CLI says **"Don't use this command on sandboxes"** — production orgs only | CLI `deploy.metadata.quick.md` |
| D14 | `2026-11-14T023507_salesforcemore-v2` | `04-github-actions-salesforce.md:26-34, 40, 104, 162, 201` | `inputs.target` bound only on `workflow_dispatch`, so it silently resolves to `qa` on push | Bind the target per event, or split the workflow per environment | workflow logic |
| D15 | `2026-11-14T023507_salesforcemore-v2` | `04-github-actions-salesforce.md:76-81, 133-138`; `other-ci-platforms.md:52-53, 94-95` | `sfdx-git-delta --output … --source …` | **Deprecated** in v6 → `--output-dir` / `--source-dir` | sfdx-git-delta v6 migration guide |
| D16 | `2026-11-14T023507_salesforcemore-v2` | `02-inspection-and-drills.md:9, 10, 25`; `02-other-limits-and-system-settings.md:21` | `sf org list limits` | **`sf limits api display`** — and it shows **API request limits only, not storage**. Delete the Storage row's CLI cell | `plugin-limits`, `plugin-org` |
| D17 | `salesforceagain-v4` | `comprehensive-devops-research.md:88` | "Heap 6 MB (2 MB async)" | **10 MB / 25 MB** | `apex-gov-limits` |
| D18 | `salesforceagain-v4` | `comprehensive-devops-research.md:92` | "Callouts — 1/transaction" | **100** | `apex-gov-limits` |
| D19 | `salesforceagain-v4` | `comprehensive-devops-research.md:109` | "Package.xml max size — 10 MB" | **≈39 MB** compressed | Metadata API `deploy()` |
| D20 | `salesforceagain-v4` | `comprehensive-devops-research.md:278` | `sf project deploy start --validated-deploy-request-id` | **`sf project deploy quick --job-id <id>`** | CLI source |
| D21 | `salesforceagain-v4` | `comprehensive-devops-research.md:155` | "No official Salesforce DevOps cert" | **False** — the **Development Lifecycle and Deployment Architect** credential exists | credential page |
| D22 | `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:169` | | "Total Apex code in an org (unmanaged) — 3 MB" | **6 MB** (10 MB scratch) | `apex-gov-limits` |
| D23 | same file `:187, :322` | | "100% for each trigger" | **75%** per class/trigger | CLI messages |
| D24 | `2026-11-14_salesforceagain-v3_devops-metadata-dependencies-deep-dive.md:230, :351` | | "No automatic ordering — you must order package.xml correctly" | False. The Metadata API **resolves intra-payload references**; package-member order is not the mechanism | Metadata API `deploy()` |
| D25 | `2026-11-14_salesforceagain-v3_devops-github-cicd-pipeline.md:423-426` | | `sf org login web` with `PROD_AUTH_URL` | Web login is **interactive** and consumes no such variable. Use the JWT flow | `plugin-auth` |
| D26 | `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:342` | | `sf governor list --target-url` | Not a Salesforce CLI command | CLI inventory |
| D27 | `20261114-023241-salesforceagain-v2` | `01-limits-governors-and-system-properties.md:82, :167` | Heap "6 MB / 12 MB" | **10 MB / 25 MB** | `apex-gov-limits` |
| D28 | same bundle | `01:263`, `05:27, :503` | Four test levels | **Five** | CLI messages |
| D29 | same bundle | `01:267` | "10,000 components per deploy" | It is the **10,000-file** package limit, not a component count | Metadata API `deploy()` |
| D30 | same bundle | `04-cicd-github-salesforce.md:410-421, 466-472` | Validates against `preprod`, quick-deploys the id to `prod` | **A validation is org-specific.** The prod validation must be created against prod | Metadata API `deploy()` |
| D31 | same bundle | `04-cicd-github-salesforce.md:423-431` | Uploads **`server.key`** as a CI artifact | **Never archive the JWT private key** | — |
| D32 | `2026-11-14T0210Z-salesforceyetagain-v2-01_certifications-curriculum.md:22, :86-94` | | "No official Salesforce DevOps cert exists" | False — the **Development Lifecycle and Deployment Architect** credential exists | credential page |
| D33 | `2026-11-14T0210Z-salesforceyetagain-v2-02_crash-course.md:432` | | `sf org login web -d -a my-dev-org` | **`-d` marks the org as a Dev Hub**, which is not what that command does | CLI `plugin-auth` |
| D34 | `2026-11-14T0210Z-salesforceyetagain-v2-02_crash-course.md:501-507` | | Pseudo system-property names, Deployment Status path | Pseudo names and a wrong path — see §4 of `01-guide-crossreference.md` | — |

---

## 2. S2 — unverified claims published as fact

| # | Bundle | Location | Claim | Action |
|---|---|---|---|---|
| D35 | `2026-11-14T023507_salesforcemore-v2` | `02-dependencies-and-constraints.md:117`, `06-term-entries.md:130`, `02-inspection-and-drills.md:72`, `04-github-actions-salesforce.md:243`, `08-cross-bundle-notes.md:23` | "`RunRelevantTests` (Beta) — **API version 66.0+**" | **Drop the version gate.** It is not in the CLI messages or the official Beta doc. Name `@IsTest(critical=true)` and `@IsTest(testFor='…')` instead |
| D36 | `salesforceagain-v4` | `comprehensive-devops-research.md:121-149` | Exam weight tables | No cited exam guide. **Cannot verify** — publish domain names only, never percentages |
| D37 | `salesforceagain-v4` | `comprehensive-devops-research.md:192-212` | A `.gearset/pipeline.yml` schema | Not a documented public Gearset interface. **Cannot verify** — drop |
| D38 | `salesforceagain-v4` | `comprehensive-devops-research.md:236-241` | A "Banking/Finance Pack" | Not substantiated. Drop |
| D39 | `2026-11-14_salesforceagain-v3_devops-gearset-ui-deep-dive.md:40-47` | | Gearset nav "Home / Comparisons / Deployments / Backups / Pipelines" | Stale. Use the task→screen table |
| D40 | same file `:414-423` | | Keyboard shortcuts `Ctrl+N`, `Ctrl+D`, `Ctrl+B` | **Invented.** No such shortcuts are documented. Drop |
| D41 | `2026-11-14_salesforceagain-v3_devops-github-cicd-pipeline.md:217` | | `gearset/gearset-action@v1` | **Cannot verify** as an official action. Drop |
| D42 | `2026-11-14_salesforceagain-v3_devops-metadata-dependencies-deep-dive.md:498-519` | | A circular-reference rule | **Cannot verify.** Drop |
| D43 | `2026-11-14T023507_salesforcemore-v2` | `03-copado-autorabit-devopscenter.md:46` | "AutoRABIT masking may sit in Vault or a related module — verify the edition" | It **is** Vault: `Live Data Masking → JOB CONFIG → Salesforce Orgs → NEW CONFIG → Object Info → Masking Rules`. Use the exact path |
| D44 | `20261114-020852-salesforcemore` | `CERTIFICATION_RESEARCH.md:67` | Calls Platform Administrator "the credential the posting calls 'Advanced Admin'" | Self-contradictory with `:58`. The posting's "Advanced Admin" is Platform Administrator **II**; Platform Administrator is its **prerequisite** |

---

## 3. S3 — structural and hygiene

| # | Bundle | Location | Issue | Action |
|---|---|---|---|---|
| D45 | `20261114-020852-salesforcemore` | `source-capture/README.md:12, :20` | Claims a `devops-engineer.md` capture exists in `source-capture/` — **it does not** (12 files, none such) | Add the capture or fix the index |
| D46 | `20261114-020852-salesforcemore` | `source-capture/*.md` (4 files) | These are **verbatim copies of the published pages** (header `Agent: opencode \| Date: 2026-11-10`) | Mark as reference copies. **Do not merge them back into the site** — that is a self-merge |
| D47 | `2026-11-14T0210Z-salesforceyetagain-v2` | `2026-11-14T0210Z-salesforceyetagain-v2-02_crash-course.md` | A derivative of the already-published crash course | Route to `crash-course.md` as **corrections**, not as a new page |
| D48 | `2026-11-14T021036_salesforceyetagain-v3.md` | whole file | An explicit placeholder with no research content | Either fill it or drop it |
| D49 | All bundles | loose `*.md` at the `forreviews/` root | Consolidated concatenations with duplicated headings | **Merge from the split files only** |
| D50 | `salesforceagain-v4` | whole bundle | No source list; material platform, UI and CLI errors | **Skip wholesale** |
| D51 | `2026-11-14T023312_salesforcemore-v3` | `02-devops-tools-walkthroughs.md:21-134` | Gearset paths tagged `[UI: likely]` but several positive labels are still wrong | Keep the `[UI: …]` **tagging convention** — it is the best methodology in the exercise — but swap in the verified task→screen table |

---

## 4. Defects found in **my own** bundle by this review, and fixed

Recording these because the merge round needs the current state, and because a review that only
finds other people's errors is not a review.

| # | Defect | Where | Fix applied |
|---|---|---|---|
| M1 | **The PR-validation workflow cached `~/.sfdx` and `~/.sf`** — the CLI's **auth state** (org aliases, refresh tokens). A restored runner can present a stale credential, and a poisoned cache becomes a credential-injection path | `04` PR-validation YAML | Cache `~/.npm` only. Added an explicit warning in §4.1 and rewrote the runner-hygiene bullet in `05` |
| M2 | The "CLI commands a release engineer should know cold" block still used `sf org login jwt --client-secret <secret> --jwt-key <cert>` — **the exact two flags my own §2.2 says do not exist** | `05` §14 | Corrected to `--jwt-key-file`, no `--client-secret` |
| M3 | **`sf project run`** listed in the CLI table — the command does not exist | `05` §14 | Removed; replaced with `sf project deploy report` and the real equivalents |
| M4 | Described the forced-local-test type list as **26 types** — the list I quoted has **24** entries | `00-consolidated-review-copy.md`, and the count in the final review | Corrected to **24** everywhere |
| M5 | Claimed "**No Salesforce-branded DevOps certification exists**" — too broad. No credential is *named* DevOps, but the **Development Lifecycle and Deployment Architect** credential covers exactly this lifecycle | `06` §1, §1.2, §6.4 | Reworded, and the credential added |
| M6 | The **JD qualification labels** were Q1–Q17; the posting has **14** qualification bullets (one bullet carries four sub-items) | `01`, `00-plan` | Renumbered to **Q1–Q14** with **Q8a–Q8d** for the posting's eighth bullet |
| M7 | The `Setup > Deploy > Deployment Settings` **field labels** were asserted as fact | `07` §2 | Flagged unverified, with `SF_ORG_METADATA_REST_DEPLOY` / `org-metadata-rest-deploy` added as the currently documented surface |
| M8 | The **Copado enterprise product name** was stated as only "Agentia Pipeline / Pro" | `03` §2.1 | Resolved to three levels: **Copado Essentials** (standalone) · **Copado CI/CD** (enterprise) · **Agentia** (unified umbrella) |
| M9 | The **OIDC** position was "Salesforce does not document an equivalent" — true but imprecise | `04` §2.5 | Sharpened: Salesforce Token Exchange exists as a **custom-handler external-IdP mechanism** with **no official GitHub Actions recipe** |
| M10 | Missing: **sandbox refresh cadence** and **scratch org allocations** | `02`, `07` | Added (§7 in `02`, §3 in `07`) |
| M11 | Missing: the **Development Lifecycle and Deployment Architect** credential | `06` §5 | Added |
| M12 | The merge plan did not specify the `<details>` syntax | `04-merge-plan` | Added: the page already uses **26** `<details markdown="1">` blocks and **zero** plain ones. Plain `<details>` in kramdown renders the Markdown inside as literal text |

---

## 5. What I did **not** do, and why

- **I did not edit the published guide pages.** The merge round owns those edits, and this repo is
  a research repository, not the site repository. `01-guide-crossreference.md` gives the exact file
  and line for every change needed.
- **I did not delete or rewrite another agent's bundle.** Bundles are append-only per agent; the
  merge round reconciles. This register is the input to that reconciliation.
- **I did not publish exam weights.** They could not be verified from any primary source.
- **I did not publish the `Setup > Deploy > Deployment Settings` labels as fact.** Only the
  behaviours.
- **I did not merge the loose consolidated `.md` files** into anything. They are concatenations.

---

## 6. One thing every agent should take from this

**A label that you cannot find in current vendor documentation is a finding, not a gap.** Three of
the seven bundles asserted Gearset navigation, job-type names or product tier names that the
vendor's current documentation does not use, and two of them added keyboard shortcuts that do not
exist. In a training page, one wrong button name costs a reader more time than one missing
button — because they will not know to look for it.

The bundles that got this right (`salesforcemore-v3` with `[UI: likely]` / `[UI: verify]`, and
`salesforcemore-v2` with `vendor-claim`) produced the fewest factual errors. **Adopt a confidence
tag on every UI label and every number.** It is the cheapest quality control in this exercise.
