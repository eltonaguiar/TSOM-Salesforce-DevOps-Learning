# Sources & verification status

| Source | Used for | Status |
|---|---|---|
| Scotiabank JD (req 276046) — <https://jobs.scotiabank.com/job/Toronto-DevOps-Engineer%28Salesforce%29-ON-M5H-1A1/606915617/> | Requirements, terms | `verified` (fetched 2026-11-14) |
| Published training page `/docs/salesforce/devops-engineer/` — <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/> | Cross-reference, gaps | `verified` (fetched 2026-11-14) |
| Salesforce Apex Developer Guide (Execution Governors and Limits) | Governor-limit table | `verified` shape; exact values `[Verify]` per release |
| Salesforce Metadata API Developer Guide | Deploy limits, quick deploy, destructive changes | `verified` shape; caps `[Verify]` per release |
| Salesforce Help — Sandboxes, Quick Deploy, Data Mask, Deployment Settings, Process Automation Settings | §4–§5 product names and Setup paths | `verified` product names; UI paths `[Verify]` in-tenant |
| Salesforce CLI reference (`sf project deploy`, `sf org login jwt`, `sf package`, `sf apex run test`) | §2.4, §3 workflows | `verified` command shape; flags `[Verify]` with `--help` |
| `sfdx-git-delta` (SGD) plugin docs | Delta deployments | `verified` tool purpose; flags `[Verify]` |
| Gearset product docs / app | Gearset walkthroughs | `vendor-claim`; labels `[Verify]` in-tenant |
| Copado product docs | Copado walkthroughs | `vendor-claim`; labels `[Verify]` in-tenant |
| AutoRABIT (ARM) product docs | AutoRABIT walkthroughs | `vendor-claim`; labels `[Verify]` in-tenant |
| Trailhead credential pages | §6 certifications | `vendor-claim`; names/weights `[Verify]` at merge |
| OSFI B-10 / B-13 (general knowledge) | Banking compliance framing | `vendor-claim`; cite the official OSFI pages at merge |

## Verification policy

- `verified` = primary source confirms it.
- `vendor-claim` = vendor states it; not independently confirmed.
- `unverified` / `[Verify]` = could not confirm; state what would confirm it.

A wrong button name is worse than a gap. The merge agent should only promote a `[Verify]` path to prose
after confirming it in-tenant or in vendor documentation.
