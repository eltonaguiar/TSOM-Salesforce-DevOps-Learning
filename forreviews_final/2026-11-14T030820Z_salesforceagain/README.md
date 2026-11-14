# forreviews_final — cross-reference, feedback and merge plan

| Field | Value |
|---|---|
| Folder | `forreviews_final/2026-11-14T030820Z_salesforceagain/` |
| Worktree | `salesforceagain` · **Agent:** kilo |
| Review window | 2026-11-14 02:03 → 03:20 UTC |
| Repo | <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning> (branch `main`) |
| Reviews | All 7 `forreviews/` entries + 5 remote branches + the loose root files |
| Peer-review passes | 3 independent (each covering different bundles), all re-verified against primary sources |
| Target page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> |
| Target index | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/#available-guides-1> |

---

## What is in here

| File | Contents |
|---|---|
| `01-guide-crossreference.md` | Every one of the **five** published Salesforce guide pages, mapped against my bundle, with the **exact file and line** of every correction needed |
| `02-bundle-crossreference.md` | Cross-reference of every bundle, branch and entry — who is authoritative for which topic, 17 contested claims with rulings, and what each bundle should fix or drop |
| `03-defect-register.md` | A flat, actionable defect list: **51 defects** across 8 bundles, severity-ranked, plus **12 defects the review found in my own bundle**, all fixed |
| `04-merge-plan.md` | The target structure for the published page, which bundle wins each section, the surgical changes needed on the other four pages, and the definition of done |

---

## The five headline findings

### 1. The published crash course has the wrong heap limit in three places

`crash-course.md:345`, `:425`, `:434` say **6 MB sync / 12 MB async**. The current official figures
are **10 MB / 25 MB**, with async CPU at 60,000 ms. The page's own advice is "process large volumes
asynchronously" — a developer sizing a Queueable job against 12 MB will hit
`System.LimitException` in production. **This is the highest-traffic correction in the exercise**,
because five of the seven bundles inherited the 12 MB figure from that page.

### 2. One bundle's workflow would have published the private key

`20261114-023241-salesforceagain-v2` uploads **`server.key`** as a CI artifact
(`04-cicd-github-salesforce.md:423-431`) and validates against `preprod` then quick-deploys the
job id to `prod` (`:410-421`, `:466-472`). A validation is org-specific — the prod validation must
be created against prod — and the JWT private key must never be archived.

### 3. My own workflow had the same class of bug

My PR-validation YAML cached `~/.sfdx` and `~/.sf`, which hold the CLI's **auth state**. A
restored runner can present a stale credential, and a poisoned cache becomes a credential-injection
path. Fixed: cache `~/.npm` only. **Recorded in full in `03-defect-register.md` §4 (M1)** — a review
that only finds other people's errors is not a review.

### 4. Two independent bundles published invented rules

`salesforcemore` states "75% org-wide, **1% per class** minimum" and `salesforcemore-v3` states
"every trigger needs some coverage, **1%**". There is no 1% rule in Salesforce. The rule is **75%
per class and trigger individually**, computed individually and different from the overall figure.
Two bundles reached for the same plausible-sounding number because nobody checked the CLI's own
message text.

### 5. The `<details>` syntax is already decided, and getting it wrong breaks the page

`docs/salesforce/devops-engineer.md` uses **26** `<details markdown="1">` blocks and **zero**
plain `<details>`. The `markdown="1"` attribute is what makes kramdown process the Markdown inside
an HTML block. A new collapsible section written as plain `<details>` renders its headings, tables
and code as literal text. (The other 128 plain `<details>` blocks in the repo are one-line quiz
answers with no Markdown to process.)

---

## What this changes about the merge

1. **Merge from the split files, never from the loose consolidated `.md` files.** They are
   concatenations with duplicated headings.
2. **A bundle whose content is a copy of a published page is a reference copy, not research.**
   `20261114-020852-salesforcemore/source-capture/*.md` are the published pages verbatim; merging
   them back would be a self-merge.
3. **The authoritative split is narrow.** For the limits, the tool UI, the CI/CD pipeline, the
   certification landscape and the JD cross-reference, my bundle is the source. For the key
   principles, the release model, the RACI, the 28-entry glossary shape and the page→section
   inventory, the other bundles are.
4. **Publish behaviours, not labels.** The `Setup > Deploy > Deployment Settings` field labels
   could not be verified; the behaviours are what a runbook needs.
5. **Publish domain names, not exam percentages.** No bundle could retrieve current exam weights;
   the study-guide trails are client-rendered.

---

## The 12 defects the review found in my own bundle — all fixed and pushed

`sf org login jwt` shown with two flags that do not exist · `sf project run` listed as a command ·
the forced-local-test type list described as 26 types when the list has 24 · an over-broad "no
Salesforce DevOps certification exists" claim · the JD qualifications numbered Q1–Q17 when the
posting has 14 bullets · Deployment Settings labels asserted as fact · an incomplete Copado
enterprise product name · an imprecise OIDC position · missing sandbox refresh cadence and scratch
allocations · a missing certification credential · the `<details>` syntax unspecified · and the
`~/.sfdx` cache above.

Full detail with before/after in `03-defect-register.md` §4. **The merge round should read my
bundle as corrected, not as first published.**

---

## One thing every agent should take from this

**A label you cannot find in current vendor documentation is a finding, not a gap.** Three bundles
asserted Gearset navigation or job-type names the vendor does not use, and one added keyboard
shortcuts that do not exist. The two bundles that tagged every claim with a confidence marker
produced the fewest errors. A confidence tag on every UI label and every number is the cheapest
quality control available here.
