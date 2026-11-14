# 01 — Cross-reference against the published Salesforce training guides

**Target:** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/#available-guides-1>
**Source of truth for the guides:** <https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM> (`docs/salesforce/*.md`)
**Checked:** 2026-11-14, against commit `768f0b3` of the guide repo and the live published pages.

The "Available guides" block on the index page exposes **five** Salesforce pages. Each one has a
different audience, and each one contains material that my research bundle either **extends**,
**corrects**, or **contradicts**. This file is the cross-reference; the corrections are the
priority.

---

## 1. Guide-by-guide cross-reference

| Guide | Page | Audience | What my bundle adds | What my bundle corrects |
|---|---|---|---|---|
| **Salesforce Crash Course** | `docs/salesforce/crash-course.md` (517 lines) | Complete beginners | Nothing — it is deliberately out of scope for a release-engineering track | **3 wrong heap figures** (`:345`, `:425`, `:434`); **1 deprecated Setup path** (`:85`); **1 conflated limit** (`:488`) |
| **Navigation & Breadcrumbs** | `docs/salesforce/navigation-breadcrumbs.md` (207 lines) | Admins + devs doing a task | My `07-system-properties-setup-paths.md` is the **deployment-side extension** of this page: it adds the *Deployment Settings* surface, the *deployment IP allowlist*, the *API Usage Notifications*, the *Debug Logs as a data-leak surface*, the *post-deploy "deployed but nothing happened" checklist*, and a settings-matrix indexed by JD line | Nothing broken, but **1 material gap**: no Deployment Settings detail beyond a single row, and no masking/refresh controls |
| **Labs & Design** | `docs/salesforce/labs-design.md` (~360 lines) | Learners doing 4 hands-on labs | My `05` and `02` supply the release-engineering version of its design patterns, and the "what happens at 200 records / 10,000 records" review questions | **2 wrong system-property rows** (`:299`, `:300`); the **Deployment Options** table (`:317`) is pre-merge-tool |
| **User Management & Data** | `docs/salesforce/user-management-data.md` (~380 lines) | Admins managing users and data | My `05 §7.1` turns its Profiles/Permission Sets/Permission Set Groups section into the **deploy-conflict** model; my `07 §4` adds the **deploy identity** as a distinct user class; my `05 §6.3` adds the masking obligation to the data-quality story | Nothing factually wrong; **one framing gap** — it never says profiles do not merge, which is the single most important fact for a release engineer reading that page |
| **DevOps & Release Engineering** | `docs/salesforce/devops-engineer.md` (554 lines) | The target of this whole effort | The entire bundle | **8 corrections** — see `01-jd-crossreference.md` §3 in my bundle |

---

## 2. Corrections needed in the crash course (exact lines)

These are the highest-confidence, highest-value findings in this review, because they are on a
**published beginner page** that the DevOps page links to as the prerequisite reading.

### 2.1 Heap size is wrong in three places

| Line | Current text | Correct text | Why |
|---|---|---|---|
| `crash-course.md:345` | `\| Heap size \| 6 MB (sync) / 12 MB (async) \|` | `\| Heap size \| 10 MB (sync) / 25 MB (async) \|` | Apex Developer Guide, *Execution Governors and Limits* |
| `crash-course.md:425` | `### 3. Heap Size — 6 MB Synchronous / 12 MB Asynchronous` | `### 3. Heap Size — 10 MB Synchronous / 25 MB Asynchronous` | same |
| `crash-course.md:434` | `Process large volumes asynchronously (Batch Apex, Queueable) where the heap limit doubles to 12 MB.` | `… where the heap limit rises to 25 MB and CPU to 60,000 ms.` | "doubles" is also wrong — 10 → 25 MB is 2.5×, not 2× |

**Why it matters beyond the number.** The page's own advice is "process large volumes
asynchronously". A developer who believes async heap is 12 MB will size a Queueable job against
12 MB and hit `System.LimitException` in production. This is precisely the class of error the
posting's "understanding of Salesforce limits" line is testing for.

**Authoritative source:** <https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html>
— heap 10 MB sync / **25 MB** async; CPU 10,000 ms sync / **60,000 ms** async; email services heap 50 MB.

### 2.2 A deprecated Setup path that contradicts the table it sits in

| Line | Current text | Correct text |
|---|---|---|
| `crash-course.md:85` | `\| System Log / Apex Logs \| Setup > Monitor > Logs > Debug Logs \|` | `Setup > Debug Logs` (System Log is retired; **Monitor** was deprecated years ago) |

The line directly above it (`:84`) already says `Setup > Debug Logs`. So the crash course
contradicts itself and contradicts `navigation-breadcrumbs.md:167` and `:202`, which both use
`Setup > Debug Logs`. Two of the three published references are already right — this is a
one-line fix that removes an inconsistency a reader will hit on their first debug-log task.

### 2.3 A conflated limit

| Line | Current text | Problem | Correct text |
|---|---|---|---|
| `crash-course.md:488` | `\| Batch Apex batch size \| 200 default \| Max 2,000 records per batch \|` | The "2,000" is the **trigger batch size for platform events and Change Data Capture**, not a Batch Apex setting. Batch Apex's own batch size is a `Database.QueryLocator`/scope size of 200. | `\| Batch Apex batch size \| 200 (Database.QueryLocator scope) \| Apex trigger batch size is 200, or 2,000 for platform events and Change Data Capture \|` |

**Release relevance:** a developer who reads "max 2,000 records per batch" will design a trigger
that assumes 2,000 records — and that trigger will process 200 at a time on ordinary records while
processing 2,000 at a time on platform events, which is a different bulkification story for each.

### 2.4 Items on the crash course worth *adding*, not fixing

| Add | Where | Why |
|---|---|---|
| The deploy-identity user class (integration user, certificate auth, dedicated permission set) | crash course §Users | The page teaches users and profiles but never mentions the one user a DevOps track depends on |
| `Setup > Deploy > Deployment Settings` | crash course §Navigation | A beginner reading "Deployment Options" in Labs & Design needs to know the org can refuse inbound deploys |
| Named Credentials → External Credentials distinction (secrets live outside Git) | crash course §Integration | The page has the right instinct; add the "the secret never goes in Git" rule |

---

## 3. Corrections needed in Labs & Design (exact lines)

### 3.1 The "Important System Properties" table is mostly internal flags presented as settings

`labs-design.md:294-301`:

| Line | Current row | Problem | Correct row |
|---|---|---|---|
| `:299` | `\| setup.locked \| Setup > Deploy > Deployment Status \| Whether metadata changes are allowed \|` | `setup.locked` is an internal org property. **Deployment Status *displays* lock state; it does not configure it.** Pointing a reader at a page to change a setting they cannot change there is the worst kind of wrong. | `\| setup.locked \| (internal — read-only) \| Whether the org is in metadata-locked mode; surfaced on Deployment Status, changed by Salesforce, not by an admin \|` |
| `:300` | `\| login.lockout \| Setup > Session Settings \| Failed login lockout policy \|` | Wrong page. Lockout is its own Setup section. | `\| login.lockout \| Setup > Lockout Policies \| Failed login lockout policy \|` |
| `:297` | `\| org.wideSharing.default \| Setup > Sharing Settings \|` | Correct. | keep |
| `:298` | `\| apex.pageLimit \| Internal \|` | Correctly marked internal. Keep as the model for the other rows. | keep |
| `:301` | `\| session.timeout \| Setup > Session Settings \|` | Correct. | keep |

**The pattern to teach instead:** a table split into **"admin-settable"** (Sharing Settings,
Session Settings, Lockout Policies) and **"internal org properties, read-only"** (`setup.locked`,
`apex.pageLimit`). Right now all five rows are presented as if they are the same kind of thing.

### 3.2 The "Deployment Options" table is pre-merge-tool

`labs-design.md:317-330` lists Change Sets, Salesforce CLI (SFDX), Metadata API, Ant Migration
Tool, DevOps Center, Gearset/Copado/AutoRABIT. Three gaps for a reader who will be interviewed on
this:

1. **The CLI has three deployment commands, not one.** `sf project deploy start` (deploy),
   `sf project deploy validate` (validation-only, returns a job id), `sf project deploy quick`
   (apply a validation without re-running tests). A reader who learns only `deploy start` will
   not know how to shorten a change window.
2. **"Ant Migration Tool" is described as "legacy XML-based deployment (being superseded by
   CLI)"** — accurate, but the page should say *why it is being superseded*: the CLI is
   source-format-first and works with source tracking and unlocked packages.
3. **The vendor row says "Same Metadata API underneath"** — correct and important. Add that the
   **deploy identity's permissions** are what differ in practice, and that no vendor tool removes
   the need for Git discipline.

### 3.3 The Labs page is the right place for the release-engineering design patterns

The page's "Design Considerations" (§252-289) is a strong checklist. Three additions from my
bundle, each with a *deployability* consequence rather than a style rule:

| Add | Consequence |
|---|---|
| Permission sets over profile edits | Profiles do not merge. A profile edit is a merge conflict and an unreviewed access change |
| No hardcoded IDs | Use Custom Metadata / Custom Settings; the id in Dev is not the id in UAT |
| Config toggles in Custom Metadata | Ship a feature dark and enable it after deploy — rollback without a redeploy |

These are already in my bundle's `05 §10`; the point here is that **the DevOps page should link
back to Labs & Design for the pattern catalogue** rather than restating it, so the two pages do
not drift.

---

## 4. Corrections needed in User Management & Data

Nothing in this page is factually wrong. Three **framing gaps** for a DevOps-track reader:

| Gap | Current | Add |
|---|---|---|
| Profiles and merging | "Profiles … Use Permission Sets for exceptions." Correct but silent on the release consequence. | One line: *Profiles do not merge. Two stories editing the same profile produce a conflict, and a bad merge changes access nobody reviewed. Ship access as permission sets.* |
| The deploy identity | Users are taught as people: create, deactivate, password, reset. | Add the **integration user** class: a named non-human user with `API Enabled` + `Modify Metadata Through Metadata API Functions` (per type) or `Modify All Data`, authenticated by certificate, whose permissions are reviewed like any other change. |
| Sandboxes and data | The page covers import/export and data quality, not sandbox data. | Add: a **Full** sandbox copy carries production data, so masking is a gate — restrict logins until mask-complete is confirmed. |

---

## 5. Corrections needed in the DevOps page (target)

My bundle's `01-jd-crossreference.md` §3 carries the full table. Summary of the eight:

| # | Correction | Where it lands |
|---|---|---|
| 1 | **Five** test levels, not four — add `RunRelevantTests` (Beta) | §9 Tests and validation |
| 2 | `sf project deploy validate` and `sf project deploy quick` are first-class commands; `--dry-run` is not the only validation mode | §5 CI/CD, §9 |
| 3 | The **24 metadata types** that force a full local test run | §9 (new) |
| 4 | Coverage is **per class and trigger individually**, each ≥75% | §9 |
| 5 | Deploy ceilings: ≈39 MB compressed / ≈600 MB uncompressed / 10,000 files (35,000 for AppExchange-reviewed 1GP); **one deploy at a time, queue not FIFO** | §2 (new) |
| 6 | Gearset / Copado / AutoRABIT current product and label names, plus the backup and masking reality | §6 (rewrite) |
| 7 | Platform Administrator II **requires** Platform Administrator; there is **no** Salesforce DevOps cert | Certifications |
| 8 | Activating an older Flow version is a **mitigation**, not a rollback | §10 |

---

## 6. Cross-page consistency issues (not a single page's fault)

| Issue | Pages | Recommendation |
|---|---|---|
| Debug log path | crash-course `:85` vs `:84`, `:323`, `:333`, `:496`; navigation-breadcrumbs `:167`, `:202` | Fix crash-course `:85` to `Setup > Debug Logs` |
| Governor limits table | crash-course `:339-349` and `:357-491` | Single source of truth; link the DevOps page's full table from the crash course rather than duplicating |
| Deployment vocabulary | labs-design `:317-330`; navigation-breadcrumbs `:144-159`; devops-engineer §1, §6 | Adopt one vocabulary: **retrieve → review → commit → validate → deploy → tag → roll back** |
| `Setup > Deploy > Deployment Settings` | navigation-breadcrumbs `:155` (one row); labs-design (absent); devops-engineer §3 (one mention) | Expand in the DevOps page; link from the other two |
| Test-level names | devops-engineer §5, §9 (four levels); crash-course `:488` ("Test methods must cover 75%+") | Use the five-level table everywhere |

---

## 7. What the "Available guides" index page still needs

The index block for the Salesforce track is accurate. Two additions:

1. **Add a line to the DevOps card** naming the *depth* now available: "…plus deploy ceilings and
   governor limits, the metadata types that force a full test run, vendor UI click-paths for
   Gearset/Copado/AutoRABIT, and a production GitHub Actions pipeline."
2. **Link the crash course's governor-limits section to the DevOps page's full table**, so a
   beginner who hits a limit has somewhere to go without the DevOps page having to stay ELI5.

---

## 8. Provenance of every correction in this file

| Correction | Source | Confidence |
|---|---|---|
| Heap 10 MB / 25 MB; CPU 10,000 / 60,000 ms; email heap 50 MB | Apex Developer Guide — *Execution Governors and Limits* | `verified` |
| Trigger batch size 200; 2,000 for platform events and CDC | same | `verified` |
| `Setup > Debug Logs` is the current path | `navigation-breadcrumbs.md:167` (this repo) + the crash course's own four other references | `verified` |
| `Setup > Lockout Policies` is a separate Setup section | Salesforce Setup structure; the repo's own `navigation-breadcrumbs.md` §Monitoring lists `Setup > Debug Logs` and `Setup > Trace Flags` but does not list lockout — see `07 §5` | `vendor-claim` — confirm in a live org before publishing |
| `setup.locked` is not admin-configurable | `Setup > Deploy > Deployment Status` displays deployment/lock state; no admin toggle is documented | `verified` as "not documented"; confirm the exact UI wording in a non-prod org |
| `sf project deploy validate` / `sf project deploy quick` exist as commands | Salesforce CLI plugin source `plugin-deploy-retrieve/src/commands/project/deploy/{validate,quick}.ts` | `verified` |
| Five test levels incl. `RunRelevantTests` (Beta) | CLI plugin `messages/deploy.metadata.md` + Metadata API guide | `verified` |
| Deploy ceilings; one deploy at a time; queue not FIFO | Metadata API Developer Guide — `deploy()` | `verified` |
