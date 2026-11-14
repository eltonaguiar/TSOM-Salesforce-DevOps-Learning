# Content gaps and recommendations

**For the merge agent.** This is the audit of the current downstream page against the research. It explains what to change, not just what to add.

## 1. What the current page does well

- The role ownership table is clear and senior.
- Sections 1–12 cover the mechanics: source of truth, metadata failures, environments, branching, CI stages, tools, conflicts, packages, tests, releases, banking control, design patterns.
- The conflict clinic is strong on profiles, permission sets, record types, layouts, Flows, and Apex.
- The runbook template, rollback table, and audit-pack list are directly useful.
- The quiz and interview drills are good.

## 2. Gaps against the user's request

| Gap | Current state | What to add | Priority |
|---|---|---|---|
| Governor limits | The page only points to the crash course | A full per-transaction table, the org-wide limits, bulkification examples, `Limits` snippet, drills | P0 |
| Other limits | Not covered | API usage, metadata payload, storage, concurrency, email, Flow, custom-object caps | P0 |
| System settings / "system properties" | Not covered | Feature enablement, settings metadata, SSO, named credentials, certificates, email deliverability, sharing | P0 |
| Metadata dependencies | A failure table, no graph | Parent/child graph, deploy-order rules, record-type manifest, error-to-fix table | P0 |
| Deployment constraints | Scattered | A single constraints table with workarounds | P0 |
| Gearset UI | Category-level only | Compare/deploy, CI, pipelines, backup, data, monitoring, audit click-paths | P0 |
| Copado/AutoRABIT/DevOps Center | Category-level only | Task tables with caveats | P1 |
| GitHub Actions pipeline | Stage table only | Runnable YAML, five-job model, JWT auth, environment approvals, "why" table | P0 |
| Certifications | A short mapping table | Current names, curricula, vendor certs, study plan, "no official DevOps cert" | P1 |
| Term-by-term depth | Not present | A collapsible entry for every posting term | P0 |
| JD cross-reference | Training table, not a full matrix | A line-by-line matrix for responsibilities and requirements | P1 |

## 3. Specific edits

### 3.1 Header

- Update "Confidence" because the page now includes vendor click-paths. Suggested: "high on platform mechanics; vendor UI labels drift, so click-paths carry a verify-in-your-tenant caveat."
- Add a "Last expanded" date and a one-line summary of the new sections.

### 3.2 Contents

Add:

- JD coverage matrix
- 5.1 GitHub Actions pipeline, end to end
- 6.1 Tool click-paths
- 13. Limits, system settings, dependencies, and deployment constraints
- 14. JD term-by-term deep dive

### 3.3 Training items

Add rows 13 and 14:

| # | Item | JD line | Done when |
|---|---|---|---|
| 13 | Limits and constraints | Limits, dependencies, constraints | You can name the limit family, the setting, and the missing dependency for a failed deploy |
| 14 | Term deep dive | Every posting line | You can answer any term in 60 seconds |

### 3.4 Section 2

- Keep the failure table.
- Add the dependency graph and the error-to-fix table from `02-limits-constraints/dependencies-and-constraints.md`.
- Add a "deployment failure decision tree" or the troubleshooting method.

### 3.5 Section 3

- Keep the sandbox table.
- Add the refresh-completion checklist: masking, integration cut-over, SSO, access.
- Add the system-settings pre-flight checklist from `02-limits-constraints/other-limits-and-system-settings.md`.

### 3.6 Section 5

- Keep the stage table.
- Add 5.1 with the five-job model, the YAML, the JWT auth, the environment approvals, and the "what not to do" list.
- Add the Azure/GitLab concept mapping as a short subsection.

### 3.7 Section 6

- Keep the tool table.
- Add 6.1 with the Gearset task table, the Copado/DevOps Center tables, the Change Sets "why fail" list, and the CLI set.
- Add the selection matrix.

### 3.8 Section 7

- Keep the conflict clinic.
- Add the "why profiles conflict" permission-diff review step and the record-type four-part rule if not already clear.

### 3.9 Section 8

- Keep the package table.
- Add the package version/`04t` example and the "do not package the whole org" warning.

### 3.10 Section 9

- Keep the validate/quick deploy/real deploy table.
- Add the test levels and the `RunLocalTests` trade-off.
- Add the "tests create their own data" example.

### 3.11 Section 10

- Keep the three speeds and the runbook.
- Add the rollback table's "Git revert does not restore data" warning.
- Add the release tag as the rollback target.

### 3.12 Section 11

- Keep the audit-pack list.
- Add the segregation-of-duties table and the environment-approval mechanics.
- Add the "author is not the approver" rule.

### 3.13 Section 12

- Keep the design-pattern table.
- Add the "no environment branches" and "custom metadata toggles" examples.
- Add the "design so the deploy is boring" line.

### 3.14 New Section 13

Use `02-limits-constraints/` as the source. Keep the collapsible subsections:

1. Apex governor limits
2. Org-wide platform limits
3. System settings and org properties
4. Metadata dependencies
5. Deployment constraints
6. How to inspect limits
7. Limit-aware design and drills

### 3.15 New Section 14

Use `06-term-deep-dives/term-entries.md`. Convert each term to a `<details markdown="1">` block. Keep the five-part shape but compress entries already covered by section 13.

### 3.16 Certifications

- Correct the names: Platform Administrator and Platform Administrator II.
- State that there is no official Salesforce DevOps Engineer certification.
- Add the domain tables and study emphasis.
- Add the vendor certificate table with the caveat.
- Add the 10-week plan or a 6-step study order.

## 4. Technical rendering note

The repo uses Jekyll + kramdown. Raw HTML blocks do not parse markdown by default. Use:

```html
<details markdown="1">
<summary><strong>Title</strong></summary>

Markdown content.

</details>
```

Some existing pages in the repo use `<details>` without `markdown="1"`, and their inner tables render as raw pipes on the live site. Do not copy that pattern for the new devops sections.

## 5. What not to change

- Do not remove the existing labs, interview drills, quiz, or runbook template; they are good.
- Do not replace the banking change-control section with a generic DevOps essay.
- Do not add a vendor-specific procedure as if it were the bank's official process.
- Do not publish exact certification weights without the current official exam guide.
- Do not publish a real org id, consumer key, certificate, secret, or customer data.

## 6. Suggested merge order

1. Header + Contents.
2. JD coverage matrix.
3. Section 13 (limits/dependencies/constraints).
4. Section 14 (term deep dives).
5. Section 6.1 (tools) and Section 5.1 (pipeline).
6. Certifications.
7. Verify all `<details>` blocks and links.
8. Re-read the page as an interviewer: can every posting bullet be answered in one sentence?
