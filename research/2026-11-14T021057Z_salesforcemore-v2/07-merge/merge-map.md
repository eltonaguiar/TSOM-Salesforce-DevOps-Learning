# Merge map — research file → downstream page

**For the round-2 merge agent.** This file is instructions, not page content.

## 1. Target structure

The current page is `docs/salesforce/devops-engineer.md` in `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`. It has sections 1–12, Labs, Interview drills, Certifications, Quiz, and Related pages.

Recommended target structure:

```text
Header
Contents
What this role actually owns
Training items
JD coverage matrix                  ← new
1. Source of truth
2. Metadata that breaks releases
3. Environments and sandboxes
4. Branching
5. CI/CD
5.1 GitHub Actions pipeline         ← new
6. DevOps tools
6.1 Tool click-paths                ← new
7. Conflict clinic
8. Packages
9. Tests and validation
10. Releases, hotfixes, rollback
11. Banking change control
12. Design patterns
13. Limits, system settings, dependencies, constraints   ← new
14. JD term-by-term deep dive       ← new
Labs
Interview drills
Certifications
Quiz
Related pages
```

## 2. File-to-section map

| Research file | Page section | Action | Notes |
|---|---|---|---|
| `00-source-log/job-description.md` | Header + new JD coverage matrix | Insert matrix; update header | Keep the posting URL and requisition id. Do not paste the full JD. |
| `01-salesforce-key-principles/principles.md` | Intro, 11, 12, 14 | Weave in | Use the one-line interview answers, not the whole file |
| `01-salesforce-key-principles/release-model.md` | 3, 4, 10 | Expand | The page already has the shape; add the runbook/rollback detail and the environment gates |
| `02-limits-constraints/governor-limits.md` | New 13.1 | Insert | Keep the table and the bad/good Apex example; compress cursor rows |
| `02-limits-constraints/other-limits-and-system-settings.md` | New 13.2, 13.3 | Insert | Keep the system-settings table and the pre-flight checklist |
| `02-limits-constraints/dependencies-and-constraints.md` | New 13.4, 13.5; expand 2 and 7 | Insert | Keep the dependency graph, the record-type manifest, and the constraints table |
| `02-limits-constraints/inspection-and-drills.md` | New 13.6, 13.7 | Insert | Keep the inspection map, the command set with the `--help` note, and the drills |
| `03-devops-tools/tool-landscape.md` | 6 | Expand | Keep the layer cake and the selection matrix |
| `03-devops-tools/gearset-click-paths.md` | New 6.1 | Insert | Keep the task tables and the "verify in your tenant" caveat |
| `03-devops-tools/copado-autorabit-devopscenter.md` | New 6.1 | Insert/compress | Keep the Copado and DevOps Center tables; compress AutoRABIT |
| `04-cicd/github-actions-salesforce.md` | New 5.1 | Insert | Put the YAML in a collapsible block; keep the five-job table and the why table |
| `04-cicd/auth-secrets-environments.md` | 5.1, 11 | Insert | Keep the JWT flow, secrets table, environment approvals, and segregation-of-duties table |
| `04-cicd/other-ci-platforms.md` | 5 | Insert a short subsection | Keep the concept mapping and the invariants; no need for all three full pipelines |
| `05-certifications/certification-landscape.md` | Certifications, 14 | Replace/expand | Correct "Advanced Admin" to Platform Administrator II; state that no official DevOps cert exists |
| `05-certifications/salesforce-credentials.md` | Certifications | Expand | Keep the domain tables and study emphasis; do not publish unverified weights |
| `05-certifications/vendor-and-study-plan.md` | Certifications | Expand | Keep the vendor table with the caveat and the 10-week plan |
| `06-term-deep-dives/term-index.md` | 14 | Use as a checklist | Do not paste the index; it is for coverage |
| `06-term-deep-dives/term-entries.md` | 14 | Convert to collapsibles | Keep the five-part shape; compress entries already covered by 13 |
| `07-merge/content-gaps.md` | — | Read before editing | Lists the specific changes and priorities |

## 3. Collapsible markup

The downstream page is Jekyll + kramdown. Raw HTML blocks do **not** parse markdown by default. Use:

```html
<details markdown="1">
<summary><strong>Term — one-line description</strong></summary>

Markdown here, including tables and code fences.

</details>
```

Do **not** copy the `<details>` style from some other pages in the repo that omit `markdown="1"`; their inner tables render as raw pipes. The devops page should render correctly.

Add a blank line after `<summary>` and before `</details>`.

## 4. Content changes by priority

### P0 — required for the user's request

1. Add **13. Limits, system settings, dependencies, and deployment constraints** with the governor-limit table, the system-settings table, the dependency graph, and the constraints table.
2. Add **14. JD term-by-term deep dive** with a collapsible entry for every posting term.
3. Add **6.1 Tool click-paths**, with Gearset compare/deploy, CI, pipelines, backup, monitoring, and audit paths.
4. Add **5.1 GitHub Actions pipeline** with the runnable YAML, the five-job table, and the "why" table.
5. Add the **JD coverage matrix** near the top.

### P1 — quality improvements

6. Update the header confidence line: button-paths are now included, with a verify caveat.
7. Update the Contents list for 5.1, 6.1, 13, 14.
8. Expand the Certifications section with the PD1/App Builder/Admin II curricula and the "no official DevOps cert" statement.
9. Add the pre-flight checklist for a target org.

### P2 — optional

10. Add the Azure DevOps / GitLab concept mapping.
11. Add the 10-week study plan.
12. Add the full error-to-fix table if section 2 becomes too long.

## 5. Facts that must keep a caveat

- Apex governor numbers: "verify current release".
- Metadata payload ceiling (10,000 / 400 MB): "commonly cited; verify current Metadata API limits page".
- Gearset/Copado/AutoRABIT/DevOps Center UI labels: "verify in your tenant; labels drift".
- Certification exam weights: do not publish without the current official exam guide.
- Scotiabank process: describe a regulated-environment pattern, not an internal procedure.

## 6. What not to merge

- Secrets, org auth files, JWT keys, consumer secrets, customer data.
- Any claim that a vendor UI path is universal.
- Any claim that a Salesforce DevOps Engineer certification officially exists.
- Any invented bank policy, approver, environment name, or licence.
- The full job description verbatim; use the coverage matrix.

## 7. Acceptance check for the merge

- [ ] Every posting bullet appears in the coverage matrix.
- [ ] Section 13 covers governor limits, org/platform limits, system settings, dependencies, and constraints.
- [ ] Section 14 has an entry for every term in the index.
- [ ] Section 6.1 has Gearset compare/deploy, CI, pipelines, backup, monitoring, and audit.
- [ ] Section 5.1 has a runnable YAML and a why table.
- [ ] All `<details>` blocks use `markdown="1"`.
- [ ] All changeable facts carry a caveat.
- [ ] No secrets or customer data.

## 8. Sibling-page opportunities

The research also feeds the other Salesforce guides in the same repo, not just the DevOps page.

| Research file | Sibling page | Suggested addition |
|---|---|---|
| `02-limits-constraints/governor-limits.md` | Salesforce Crash Course (`docs/salesforce/crash-course.md`) | A compact governor-limits table and the 200/10,000-record review questions; link to the DevOps page for the full deep dive |
| `02-limits-constraints/dependencies-and-constraints.md` | Crash Course; Labs & Design (`docs/salesforce/labs-design.md`) | A "missing dependency" lab and an error-to-fix table |
| `03-devops-tools/gearset-click-paths.md` | Navigation & Breadcrumbs (`docs/salesforce/navigation-breadcrumbs.md`) | A "Deployment & DevOps" row set: Setup → Deploy → Deployment Status, Setup → Sandboxes, Setup → DevOps Center, plus vendor-tool paths |
| `04-cicd/auth-secrets-environments.md` | Labs & Design | A lab: create a JWT auth flow, store a key in a CI secret, validate a deploy, never commit the key |
| `05-certifications/salesforce-credentials.md` | Learning Paths page (general docs) | A study order and the current credential names (Platform Administrator II, not "Advanced Admin") |
| `06-term-deep-dives/term-entries.md` | Crash Course; Interview Prep | Short definitions and the "interview line" for Apex, Flow, permission sets, record types, layouts, security |
| `02-limits-constraints/other-limits-and-system-settings.md` | User Management & Data (`docs/salesforce/user-management-data.md`) | A pre-flight checklist for permissions, SSO, named credentials, and email deliverability in a sandbox |
| `01-salesforce-key-principles/principles.md` | DevOps page; Crash Course | The principles spine as a shared intro; reuse the one-line answers |

**Rule for sibling pages:** add a short section and link to the DevOps page for the full treatment. Do not duplicate the full limits/dependency tables across four pages; the repo will drift.

