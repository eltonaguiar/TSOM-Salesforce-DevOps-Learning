# Research bundle — Salesforce DevOps Engineer (Scotiabank 276046)

| Field | Value |
|---|---|
| Bundle | `2026-11-14T021057Z_salesforcemore-v2` |
| Worktree | `salesforcemore-v2` |
| Agent | kilo |
| Research date | 2026-11-14 |
| Job | DevOps Engineer (Salesforce), Scotiabank, Toronto, Requisition 276046 |
| Job URL | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| Downstream page | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> |
| Status | Research complete for merge round 2; no secrets or customer data included |

> **Review tracking:** consolidated single-file copy: [`../2026-11-14T023507_salesforcemore-v2.md`](../2026-11-14T023507_salesforcemore-v2.md). Canonical split bundle and PR: <https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning/pull/2>.

## What this bundle is

This is a structured research package, not the final page. It is designed so a second agent can merge the material into the existing DevOps training page without re-researching it.

The research is split into small files so the merge agent can accept, reject, or rewrite each unit independently. Every file starts with a "merge target" line naming the section of the downstream page it belongs to.

## How to read the bundle

| Folder | What it contains | Merge disposition |
|---|---|---|
| `00-source-log/` | Job description, source URLs, access date, confidence notes | Reference only; do not paste wholesale into the page |
| `01-salesforce-key-principles/` | The platform principles that justify the release model | Merge as framing / "why" material |
| `02-limits-constraints/` | Governor limits, org/platform limits, system settings, metadata dependencies, deployment constraints, inspection and drills | Merge into section 13 of the page; highest priority |
| `03-devops-tools/` | Tool landscape; Gearset, Copado, AutoRABIT, DevOps Center click-paths; Change Sets vs CLI | Merge into sections 6 and 6.1 |
| `04-cicd/` | GitHub Actions + Salesforce pipeline, JWT auth, environments, secrets, Azure/GitLab equivalents | Merge into sections 5 and 5.1 |
| `05-certifications/` | Certification landscape, Salesforce credential curricula, vendor certificates, study plan | Merge into the Certifications section and section 14 |
| `06-term-deep-dives/` | Term index and term entries for every posting line | Merge into section 14 |
| `07-merge/` | Merge map and content-gap recommendations | Instructions for the merge agent, not page content |
| `08-cross-bundle-notes.md` | Reconciliation with the sibling `2026-11-14T020300Z-kilo-salesforceagain` bundle and verified corrections | Read before merging; do not paste into the page |

## What is safe to merge as-is

- The limits tables, dependency tables, constraints tables, and the CLI/UI inspection table in `02-limits-constraints/`.
- The GitHub Actions workflow and the "why this shape" notes in `04-cicd/`.
- The tool click-path tables in `03-devops-tools/`, with the caveat that vendor labels drift.
- The certification landscape and study plan, with the "verify current exam guide" note intact.

## What needs a human decision before merge

- **Vendor click-paths.** Gearset, Copado, AutoRABIT, and DevOps Center change menu labels between editions. Keep the "verify in your tenant" caveat. Never present a click-path as guaranteed for every edition.
- **Exact limits.** The Apex governor table is taken from the current Salesforce limits page; platform limits and metadata payload ceilings change. Keep the "verify current release" note.
- **Certification exam weights.** Do not publish percentages from memory. Use the topic domains and official study-guide links; let the merge agent add current weights only from the official exam guide PDF.
- **Bank-specific process.** The Scotiabank change-control specifics are not public. The research describes a defensible regulated-environment pattern, not Scotiabank's internal procedure.

## What must not be merged

- Any credential, org auth file, JWT key, consumer secret, or customer data. None is included.
- Any claim that a vendor UI path is universal across editions.
- Any claim that a Salesforce "DevOps Engineer" certification officially exists. It does not; the page must say so.
- Any invented Scotiabank policy, approver name, tool licence, or environment name.

## Confidence summary

| Area | Confidence | Why |
|---|---|---|
| Apex governor limits | High | Official Salesforce limits page, checked 2026-11-14 |
| Metadata dependency behaviour | High | Documented Metadata API behaviour and repeated field experience |
| Deployment constraints | High | Documented platform behaviour |
| GitHub Actions + Salesforce pattern | High on mechanics; medium on bank-specific approval flow | Mechanics are standard; the approval flow is a design choice |
| Gearset click-paths | Medium | Public docs and UI conventions; labels vary by edition |
| Copado / AutoRABIT / DevOps Center click-paths | Medium | Category-level accuracy; edition-specific labels must be verified |
| Certification curricula | Medium | Official credential pages and study-guide titles; current exam weights need the official exam guide |
| Scotiabank internal process | Low / not public | Not asserted; the bundle describes a regulated-environment pattern |

## Next action

Give this folder to the merge agent with `07-merge/merge-map.md`. The merge agent should update the downstream page, keep the collapsible `<details>` structure, and preserve the "verify at time of use" caveats.
