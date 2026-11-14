# TSOM-Salesforce-DevOps-Learning

Learning resources and training items for the **Salesforce DevOps Engineer** role (Scotiabank requisition 276046, Commercial Banking Engineering, Toronto) and the broader Salesforce track published at:

- <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/>
- Sibling guides: crash course, navigation breadcrumbs, labs & design, user management & data.

This repo is the **research and drafting layer**. The published site is the **presentation layer**. Research lands here first; a merge round organises it into the site.

---

## Repository layout

```
TSOM-Salesforce-DevOps-Learning/
├── README.md                 ← this file (index)
├── CONTRIBUTING.md           ← folder + naming convention for all agents
└── research/
    └── <UTC timestamp>-<worktree>/
        ├── README.md         ← run manifest + handoff
        ├── PLAN.md           ← structured approach + Salesforce key principles
        ├── 01-…              ← deep dives
        ├── …
        └── sources.md        ← provenance + access caveats
```

## Research runs

| Run folder | Worktree | Focus | Status |
|---|---|---|---|
| [`research/20261114T021017Z-salesforceagain-v2/`](research/20261114T021017Z-salesforceagain-v2/) | `salesforceagain-v2` | Limits & governor limits, system properties, metadata dependencies & deployment constraints, DevOps tool UI walkthroughs, GitHub Actions CI/CD, JD term-by-term decoder, certification curriculum | Round 1 complete — ready to merge |

> New runs go in a **new** timestamped folder. Never overwrite another agent's run.

## What each run must contain

At minimum:

1. `README.md` — manifest, scope, confidence, merge destinations, known gaps.
2. `PLAN.md` — the structured approach and the principles it follows.
3. The research content, numbered for reading order.
4. `sources.md` — every URL, what it supported, and whether it was blocked.

See `CONTRIBUTING.md` for the full convention.

## Merge process (round 2)

1. Read the run's `README.md` and `PLAN.md`.
2. Merge into the published `devops-engineer` page **under existing anchors** (`#6-devops-tools`, `#2-metadata-that-breaks-releases`, etc.); do not renumber.
3. Split sections into child pages where the main page becomes too long.
4. Verify time-sensitive claims (limits, CLI flags, vendor UI labels) against current official docs before publishing.
5. Add diagrams for the dependency graph and the pipeline.
6. Keep the regulated-banking lens.

## Ground rules

- **No secrets, customer data, org IDs, or tokens.**
- **No invented numbers.** Flag edition/version-dependent values as "verify".
- **No duplicated crash-course material** — cross-link instead.
- **Commit only your own files.** Use a branch + PR; do not push others' work.
