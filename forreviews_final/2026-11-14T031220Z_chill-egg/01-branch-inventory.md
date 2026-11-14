# Branch and bundle inventory

Read at 2026-11-14T03:12Z. `origin/main` of `TSOM-Salesforce-DevOps-Learning` is `db39d1b` (86 tracked files). The local checkout of that repo is 7 commits behind `origin/main` on `forreviews-split/salesforcemore-v2-2026-11-14T023507Z`. This inventory uses `origin/main`, not the stale checkout.

`findtorontoevents_antigravity.ca` branches named `salesforceagain` and `salesforceyetagain` are the trading repo. They are not this review corpus. Ignore them.

## TSOM-Salesforce-DevOps-Learning

| Ref | Unique vs `origin/main` | Disposition |
|---|---|---|
| `origin/main` | Canonical. All review drops below live under `forreviews/`. | Read this. |
| `origin/research/salesforceagain-2026-11-14T020300Z` | `research/2026-11-14T020300Z-kilo-salesforceagain/` (11 files) plus `research/README.md` | Already copied to `forreviews/20261114-020300-salesforceagain-kilo/` by `db39d1b`. No unique research left to merge. |
| `origin/research/salesforceagain-v2-20261114` | `research/20261114T021017Z-salesforceagain-v2/` plus `CONTRIBUTING.md`. Open PR #1. | Diff against `forreviews/20261114-023241-salesforceagain-v2` is `INDEX.md` only (37 lines on main, absent on the branch). Do not merge as a second tree. |
| `origin/research/salesforcemore-v2-2026-11-14T021057Z` | `research/2026-11-14T021057Z_salesforcemore-v2/`. Open PR #2. | Diff against `forreviews/2026-11-14T023507_salesforcemore-v2` is a 2-line tracking note in `README.md`. Already on main. Do not merge as a second tree. |
| `origin/salesforceagain-v3` | 0 files that are not already on main. Main has 28 files this branch lacks. | Behind. Ignore. |
| Local `main` | `96e1614`, 12 commits behind `origin/main`. | Do not branch new review work from local `main`. |

## Bundles already on `origin/main`

| Path | What it is | Still the best source for |
|---|---|---|
| `forreviews/20261114-020852-salesforcemore/` | Early capture of the four guide pages plus limits and principles | Historical source capture only. Guides have moved. |
| `forreviews/2026-11-14T0210Z-salesforceyetagain-v2/` | Planning, certs, crash-course notes. Also duplicated as loose files beside the folder. | Nothing the later bundles do not cover. |
| `forreviews/2026-11-14T021036_salesforceyetagain-v3.md` | Placeholder. | Discard. |
| `forreviews/20261114-020300-salesforceagain-kilo/` | JD crosswalk, limits, tool UI, CI, certs, setup paths, cross-bundle delta | Vendor UI detail, if a click-path is needed and it cites a vendor doc. |
| `forreviews/20261114-023241-salesforceagain-v2/` | Same shape as the kilo bundle, later pass | Same. Prefer this over the kilo bundle when they disagree, then check the primary source. |
| `forreviews/2026-11-14T023507_salesforcemore-v2/` | Full split bundle: principles, limits, tools, CI, certs, terms, merge map, content-gaps | Limits spine, five test levels, deploy ceiling, Gearset/Copado/AutoRABIT name corrections. The `07-merge/content-gaps.md` file is partly stale. See alignment. |
| `forreviews/2026-11-14T023312_salesforcemore-v3/` | JD crossref, tool walkthroughs, CI, limits, terms, certs | Use where it marks a claim `[Verify]`. Do not treat unverified button names as page copy. |
| `forreviews/2026-11-14_salesforceagain-v3_devops-*.md` | Four flat deep dives (Gearset UI, GitHub CI, governor limits, metadata dependencies) | Secondary. Prefer the split bundles. |
| `forreviews/salesforceagain-v4-2026-11-14-0230/` | One long research file plus a plan | Stale on credential names. README still says “Advanced Admin” with no rename note. Do not prefer it over the live DevOps page. |
| Loose `forreviews/*.md` next to folders | Tracking copies of the folders | Not a second source. |

## ServiceNow learning repo

Live pages confirmed by fetch on 2026-11-14:

- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/navigation-breadcrumbs/
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/user-management-data/
- https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/

`origin/main` has all five files plus `updates/2026-11-13-salesforce-devops-training.md`. Line counts on `origin/main`: crash course 629, labs 353, user/data 374, breadcrumbs 207, devops 554.

| Ref | Salesforce track | Note |
|---|---|---|
| `origin/main` | All five guides | This is what the site serves. |
| `docs/salesforce-devops-deepdive` (worktree `~/wt-sf-devops`) | Same five files as main for `docs/salesforce` | Empty diff vs main on those paths. No pending guide delta. |
| `origin/direction-a-gaps-sam-guide-2026-11-13` | Crash course, labs, breadcrumbs, user/data. No `devops-engineer.md`. | Open SN PR #2. Branched before the DevOps track. A normal merge will not delete the DevOps page. A Pages build from this branch would omit it. Do not deploy Pages from it. |
| `origin/docs/sam-guide-gaps-2026-11-13` | Same omission | Same deploy hazard. |
| `origin/arlo/theme-and-tsom-labs-2026-11-05`, `origin/freebuff-guides-2026-11-05T2135Z`, `origin/hermes-success-pack-2026-11-06` | No `docs/salesforce/` | Historical. Not a review source. |

## Open PRs

| PR | Repo | Action |
|---|---|---|
| [#1](https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning/pull/1) | DevOps learning | Close or retarget. Content is already under `forreviews/20261114-023241-salesforceagain-v2/`. |
| [#2](https://github.com/eltonaguiar/TSOM-Salesforce-DevOps-Learning/pull/2) | DevOps learning | Close or retarget. Content is already under `forreviews/2026-11-14T023507_salesforcemore-v2/`. |
| SN #2 | ServiceNow learning | SAM guide gaps. Out of scope for this Salesforce review except the Pages-deploy hazard above. |
