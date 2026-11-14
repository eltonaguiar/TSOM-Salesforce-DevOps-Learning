# Research bundles

Each research bundle is a self-contained, timestamped research drop produced by one agent (or one
agent worktree) against a single objective. Bundles are **inputs to a later merge round**, not
published curriculum.

## Folder naming

```
research/<UTC-timestamp>-<worktree-name>/
```

- `<UTC-timestamp>` — `YYYY-MM-DDTHHMMSSZ`, the moment the research started (not the commit time).
- `<worktree-name>` — the agent worktree / session name. This is the uniqueness key. Two agents
  working the same repo at the same minute must not collide, so the worktree name is mandatory.

Examples:

| Folder | Agent / worktree | Started (UTC) |
|---|---|---|
| `2026-11-14T020300Z-kilo-salesforceagain` | kilo / `salesforceagain` | 2026-11-14 02:03 |
| `2026-11-14T021057Z_salesforcemore-v2` | kilo / `salesforcemore-v2` | 2026-11-14 02:10 |

## Standard bundle layout

| File / directory | Purpose |
|---|---|
| `README.md` | Bundle manifest: objective, scope, method, headline findings, known gaps. |
| `00-plan.md` | The plan the work was executed against: JD → research-item matrix, method, source policy. |
| `01-*.md` … `07-*.md` | Numbered research artifacts. The number is the canonical cross-bundle sort key. |
| `sources.md` | Every URL used, with access date and a verification status (`verified` / `vendor-claim` / `unverified`). |

## Rules for contributors

1. **Do not edit another bundle.** Bundles are append-only per agent. The merge round owns consolidation.
2. **Every factual claim carries a source.** If a UI label could not be verified, say so explicitly
   rather than guessing — a wrong button name is worse than a gap.
3. **Record premise corrections.** When current vendor documentation contradicts a widely repeated
   claim (product names, tier names, button labels), the correction goes in the artifact itself
   and in the "known corrections" table of the bundle README.
4. **Mark confidence.** Use `verified` (primary source confirms it), `vendor-claim` (vendor states it,
   not independently confirmed), `unverified` (could not confirm — say what would confirm it).
5. **No secrets, no customer data.** Never paste tokens, certificates, sandbox URLs, or customer rows.

## Merge round

The merge agent takes the bundles and produces the publishable page(s) under
`https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/`,
using the existing Salesforce guide pages as the surrounding structure:

- Salesforce Crash Course
- Navigation & Breadcrumbs
- Labs & Design
- User Management & Data
- DevOps & Release Engineering

Cross-bundle overlap is expected and fine. When two bundles disagree, prefer the one with a
primary-source citation and record the resolution in the merge notes.
