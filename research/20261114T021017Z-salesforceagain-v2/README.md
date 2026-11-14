# Salesforce DevOps Research — Run Manifest

| Field | Value |
|---|---|
| **Agent / worktree** | `salesforceagain-v2` (Kilo) |
| **Created (UTC)** | 2026-11-14T02:10:17Z |
| **Folder** | `research/20261114T021017Z-salesforceagain-v2/` |
| **Target role** | DevOps Engineer (Salesforce), Scotiabank, Requisition 276046, Commercial Banking Engineering, Toronto |
| **Primary source JD** | <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> |
| **Merge target** | <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> and sibling Salesforce guides (crash course, breadcrumbs, labs, user & data) |
| **Status** | Round 1 — research complete, ready for merge round |
| **Confidence** | High on platform mechanics and limits; medium on vendor UI button paths (they change by edition/release — verify in-tenant) |

## What this folder is

This is a **self-contained round-1 research drop**. It is written so a later agent can merge it into the published training site without re-doing discovery. Every file states what it covers, what it assumes, and where it should land.

It deliberately **does not duplicate** the existing crash course. The published crash course already covers objects/fields, security basics, Flow vs Apex, and a first pass at governor limits. This drop goes **deeper**: exact limit values, per-transaction vs per-org vs per-24h, system properties, metadata dependency graphs, deployment constraints, tool UI walkthroughs, and a production-grade GitHub Actions pipeline.

## Files and merge destinations

| File | What it is | Merge destination on the docs site |
|---|---|---|
| `PLAN.md` | Structured approach, Salesforce key principles, research method, quality bar | New "Editorial standard / how this track is built" note, or `docs/salesforce/devops-engineer/#appendix-plan` |
| `01-limits-governors-and-system-properties.md` | Deep dive: governor limits, platform/org limits, API limits, system properties, how to measure | Extend `#2-metadata-that-breaks-releases` and crash-course governor-limit section; add a new "Limits & system properties" child page |
| `02-metadata-dependencies-and-deployment-constraints.md` | Dependency graphs, ordering, destructive changes, Metadata API constraints, failure catalogue | Extend `#2-metadata-that-breaks-releases` + `#7-conflict-clinic` |
| `03-devops-tools-ui-walkthroughs.md` | Gearset, Copado, AutoRABIT, DevOps Center: where to click for compare/deploy/backup/rollback | Expand `#6-devops-tools` into per-tool subsections |
| `04-cicd-github-salesforce.md` | End-to-end GitHub Actions pipeline, auth, delta deploys, gates, promotion, rollback | Expand `#5-cicd` with a full worked pipeline |
| `05-jd-term-by-term.md` | Every JD line and skill parsed into term → definition → config/settings/variations → what you do in the role | New "JD decoder" page linked from the track index |
| `06-certifications-and-curriculum.md` | PD1, Platform Administrator II (ex-Advanced Admin), Development Lifecycle & Deployment Architect, vendor certs; curricula + study order | Expand `#certifications` |
| `sources.md` | Every URL used, with what it was used for and access caveats | Provenance appendix |

## Reading order for the merge agent

1. `PLAN.md` — understand the principles and the intended structure.
2. `05-jd-term-by-term.md` — the spine; it maps 1:1 to the requisition.
3. `01`, `02`, `04` — the technical core (limits, dependencies, pipeline).
4. `03` — tool-specific UI evidence.
5. `06` — credential mapping.
6. `sources.md` — verify any claim that looks time-sensitive.

## Hard constraints respected

- **No invented numbers.** Limits are the canonical Salesforce values; anything edition-dependent or release-dependent is flagged.
- **No fabricated UI screenshots.** UI paths are described as "typical layout; verify in your tenant."
- **No secrets.** No org IDs, tokens, customer data, or real endpoints.
- **Regulated-environment lens.** Every recommendation is framed for a bank: audit trail, segregation of duties, change ticket, rollback evidence.

## Known gaps for round 2

- Vendor pricing and exact edition feature-gating (Gearset/Copado/AutoRABIT) — commercial, changes often.
- Exact certification domain weights — must be confirmed from the current official exam guide PDF (Salesforce gates its docs behind auth/bot checks; see `sources.md`).
- Screenshots/diagrams — text-only in this round; a diagram pass would help `02` and `04`.
- Real org-verified `sf` CLI flags — flags move between CLI majors; run `--help` before publishing command blocks.
