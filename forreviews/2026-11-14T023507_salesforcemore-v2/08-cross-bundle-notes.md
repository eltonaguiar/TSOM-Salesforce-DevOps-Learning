# Cross-bundle notes — sibling research and reconciliation

**For the merge agent.** This bundle is one of at least two research drops for the same Scotiabank requisition. This file records the overlap, the corrections, and which bundle to prefer where.

## 1. Sibling bundle

| Field | Value |
|---|---|
| Sibling folder | `research/2026-11-14T020300Z-kilo-salesforceagain/` |
| Worktree | `salesforceagain` |
| Started | 2026-11-14T02:03:00Z |
| Status at write time | README and `00-plan.md` present; detailed artifacts in flight |
| Relationship | Independent research; same job, same downstream page |

The sibling README's headline findings triggered a verification pass in this bundle. The items below were checked against primary sources on 2026-11-14.

## 2. Verified corrections applied to this bundle

| # | Claim in the sibling README | Verification | Action in this bundle |
|---|---|---|---|
| 1 | Metadata API deploy ceiling is ~39 MB compressed / ~600 MB uncompressed, 10,000 files for unlocked/2GP, 35,000 for AppExchange-reviewed 1GP | Confirmed on the [Metadata API `deploy()` reference](https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html) | Replaced the earlier "10,000 components / 400 MB" figure in `02-limits-constraints/other-limits-and-system-settings.md` |
| 2 | Only one deployment runs at a time per org; queued deployments are not necessarily executed in submission order | Confirmed on the same `deploy()` reference | Added to `02-limits-constraints/other-limits-and-system-settings.md`, `dependencies-and-constraints.md`, `inspection-and-drills.md`, and `04-cicd/github-actions-salesforce.md` |
| 3 | There are five test levels, including `RunRelevantTests` (Beta), not four | Confirmed in the [Salesforce CLI deploy messages](https://github.com/salesforcecli/plugin-deploy-retrieve/blob/main/messages/deploy.metadata.md) and the `source-deploy-retrieve` types; requires API 66.0+ | Added the five-level table to `02-limits-constraints/dependencies-and-constraints.md`; updated the term entry, drills, and CI trade-offs |
| 4 | Gearset's current UI is grouped into My connections, Metadata deployments, Continuous delivery, Backup & archiving, Sandbox seeding & compliance, Problem analyzers, Observability, Settings | Confirmed by the [Gearset docs collections](https://docs.gearset.com/en/) and the article lists in those collections | Rewrote `03-devops-tools/gearset-click-paths.md` around the current categories; kept older labels in parentheses |
| 5 | Gearset backup is a separately licensed data + metadata backup product; Gearset does not perform or schedule the Salesforce sandbox refresh | Confirmed by the Backup & archiving collection (data backup/restore, restoring metadata) and the Sandbox seeding collection (seeding/masking around a refresh) | Added the correction to `gearset-click-paths.md`; removed any implication that Gearset refreshes the sandbox |
| 6 | Copado's current branding includes Copado CI/CD, Copado Essentials, Agentia, Robotic Testing, AI Platform; "Copado Fundamentals" and a Copado "DevOps Center" tier are not current names | Confirmed by the [Copado platform page](https://www.copado.com/platform-overview) | Updated `03-devops-tools/copado-autorabit-devopscenter.md` and `tool-landscape.md` |
| 7 | AutoRABIT's current products are ARM (CI/CD), Vault (backup/restore), CodeScan (static analysis), Guard (security posture); "Test Repository" and standalone "Data Masking" are not current product names | Confirmed by the [AutoRABIT products page](https://www.autorabit.com/products/) | Updated `03-devops-tools/copado-autorabit-devopscenter.md` and `tool-landscape.md` |
| 8 | Advanced Admin is now Platform Administrator II, with Platform Administrator as a prerequisite | Confirmed on the [Platform Administrator II credential page](https://trailhead.salesforce.com/credentials/platformadministrator-ii) | Already in this bundle; the prerequisite is now explicit in `05-certifications/` |

## 3. Where this bundle is the better source

| Area | Why |
|---|---|
| Apex governor limits | Full per-transaction table plus org-wide/24-hour limits, with the official source and bulkification examples |
| System settings / org properties | A dedicated table of feature enablement, SSO, named credentials, certificates, email deliverability, sharing, and what deploys vs what does not |
| Metadata dependencies | A parent/child graph, deploy-order rules, a record-type manifest, and an error-to-fix table |
| GitHub Actions pipeline | A runnable five-job YAML, JWT auth, environment-scoped secrets, required reviewers, and a "why" table |
| Certifications | PD1, Platform App Builder, Platform Administrator, Platform Administrator II domain tables; vendor certificates; a 10-week study plan |
| Term-by-term entries | Every posting term with definition, why, example, failure mode, interview line |
| Sibling-page mapping | `07-merge/merge-map.md` maps the bundle to the crash course, breadcrumbs, labs, and user/data pages |

## 4. Where the sibling bundle may be the better source

| Area | Why |
|---|---|
| Vendor UI click-paths and plan gates | The sibling README says it ran dedicated vendor-documentation agents and cross-read the Salesforce CLI plugin source. If its `03-devops-tools-ui.md` is primary-source verified, prefer it over this bundle's category-level tables. |
| Exact Gearset/Copado/AutoRABIT feature packaging | The sibling explicitly tracks plan gates and corrections (for example, which Gearset features are separately licensed). Prefer its detail where it cites current vendor docs. |
| Metadata API deploy limits | We now agree on the numbers; prefer whichever file has the most direct citation. Both point to the `deploy()` reference. |
| "Fifth test level" and deployment queue order | We now agree; use the table in this bundle or the sibling's equivalent. |

## 5. Merge recommendation

1. **Use the sibling bundle for vendor UI detail** if its artifacts are complete and primary-source cited. Use this bundle for the limits/constraints spine, the CI/CD YAML, the certification curricula, and the term-by-term structure.
2. **Reconcile disagreements with a primary source, not with a vote.** Record the resolution in the merge notes.
3. **Do not merge both vendor-UI sections verbatim.** The page will contradict itself on menu labels. Pick one current label set and keep the "verify in your tenant" caveat.
4. **Keep the corrections.** The five test levels, the 39/600 MB deploy ceiling, the one-deployment-at-a-time queue, and "Gearset does not refresh the sandbox" are all worth publishing because they correct common interview answers.
5. **Do not publish a certification percentage** unless the current official exam guide has been fetched and cited. Domain names and study-guide links are enough.

## 6. Open items

- The sibling bundle's detailed files were not present when this note was written. Re-read them before merge; update this file if a new disagreement appears.
- The exact Gearset enterprise plan gates and Copado/AutoRABIT edition packaging should be confirmed against the bank's contract, not a public pricing page.
- Salesforce release notes can change the deploy limits and test levels. Re-check the `deploy()` reference on the merge date.
