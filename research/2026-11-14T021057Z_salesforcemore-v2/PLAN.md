# PLAN — structured research approach

## 1. Objective

Produce a merge-ready research package for the Salesforce DevOps Engineer (Scotiabank requisition 276046) training page, with emphasis on:

1. Salesforce key principles and the release-engineering model they justify.
2. Governor limits, other platform/org limits, system settings and org properties, metadata dependencies, and deployment constraints.
3. Practical, technical use of each DevOps tool, including Gearset UI click-paths for compare/deploy, backup, CI, pipelines, monitoring, and audit.
4. A GitHub Actions + Salesforce CI/CD pipeline and the reasons behind each design choice.
5. Research on the certifications named in the posting (PD1, Advanced Admin / Platform Administrator II, and "DevOps related certs") and their curricula.
6. A term-by-term deep dive for every line in the posting.

## 2. Method

### 2.1 Source hierarchy

1. **Official Salesforce documentation** — Metadata API, Apex limits, sandbox docs, deployment docs, credential pages.
2. **Official vendor documentation** — Gearset docs, Copado docs, AutoRABIT docs, Salesforce DevOps Center help.
3. **Reputable secondary sources** — Trailhead study guides, vendor academies, well-known DevOps write-ups. Used only when the first two are inaccessible, and labelled as secondary.
4. **Job posting** — treated as the scope contract. Every bullet is mapped to a research file.

### 2.2 Work sequence

1. Capture the posting and split it into atomic requirements.
2. Map each requirement to a page section and a research file.
3. Research the "why" first (principles), then the "what" (limits, dependencies, constraints), then the "how" (tools, pipeline, click-paths).
4. Write each unit with: definition, why the role cares, concrete example, failure mode, interview line.
5. Mark every fact that can change with a verify-at-time-of-use note.
6. Produce the merge map so a second agent can integrate without guessing.

### 2.3 Quality bar

- No invented UI paths presented as universal.
- No certification percentages without the current official exam guide.
- No secrets, customer data, or org auth files.
- Every claim that matters to an interview has a concrete example or command.
- Every table has a "what to do" column, not just a definition.

## 3. Salesforce key principles used as the spine

These are the principles the downstream page should keep repeating. They explain why the release model looks the way it does.

| Principle | What it means for release engineering | Where it appears |
|---|---|---|
| **Git is the source of truth** | The org is a deploy target. Setup edits that are not in Git are drift. | `01-salesforce-key-principles/`, `06-term-deep-dives/` |
| **A deploy is a compile against the target** | The Metadata API resolves dependencies in the payload and enforces the target's tests and limits. | `02-limits-constraints/dependencies.md` |
| **Promote one artifact** | Build/validate once, promote the same commit or package version through environments. | `04-cicd/`, `06-term-deep-dives/` |
| **Least privilege and segregation of duties** | The integration user deploys; a human approves; the author does not approve their own change. | `04-cicd/auth-secrets-environments.md`, `06-term-deep-dives/` |
| **Environment parity, not environment branches** | Configure the target; do not fork the codebase per environment. | `01-salesforce-key-principles/` |
| **Test against the org you will change** | A green Dev test is not evidence for UAT or Prod. | `02-limits-constraints/`, `04-cicd/` |
| **Bulkify by default** | A deploy can be green and the feature can fail at 200 or 10,000 records. | `02-limits-constraints/governor-limits.md` |
| **Make metadata modular** | Permission sets, packages, subflows, and custom metadata reduce conflicts. | `01-salesforce-key-principles/`, `06-term-deep-dives/` |
| **Design for reversibility** | A tag, a previous package version, and a Flow-version mitigation are part of the design. | `06-term-deep-dives/` |
| **Mask before you share** | A Full sandbox is a customer-data copy until masking completes. | `06-term-deep-dives/`, `02-limits-constraints/system-settings.md` |
| **Evidence is part of the deploy** | Ticket, diff, approval, deploy ids, test results, tag, mask confirmation. | `06-term-deep-dives/`, `04-cicd/` |
| **Observability after deploy** | A deploy is not done until the smoke test, the API usage check, and the business check pass. | `04-cicd/`, `02-limits-constraints/inspection-and-drills.md` |

## 4. Research questions

### Limits and constraints

- Which Apex governor limits are per transaction, which are per org, and which are per 24 hours?
- What is the difference between a governor limit and an org allocation?
- Which "system properties" (feature enablement, settings, secrets, certificates, SSO, email deliverability) are not normal metadata?
- Which metadata dependencies cause the common deploy errors, and what is the deploy order?
- Which constraints cannot be solved by a deploy at all (data, secrets, managed packages, feature switches)?

### Tools

- What does each vendor layer add over the Metadata API and the `sf` CLI?
- Where in Gearset do you compare, deploy, validate, run CI, build a pipeline, back up, restore, monitor drift, and read the audit history?
- What are the equivalent paths in Copado, AutoRABIT, and DevOps Center?
- When is a Change Set still acceptable, and why is it not the answer at this scale?

### CI/CD

- What are the minimum jobs in a Salesforce pipeline, and what does each one prove?
- How does JWT authentication work, and where do the secrets live?
- Why is a quick deploy not the same as a validation?
- How do GitHub Environments, required reviewers, branch protection, and environment-scoped secrets implement segregation of duties?
- What changes when the same pipeline runs in Azure DevOps or GitLab?

### Certifications

- Which credentials does the posting actually name, and what are their current official names?
- What does each exam cover, and which domains overlap release engineering?
- Is there an official Salesforce DevOps certification? (No.)
- Which vendor certificates are worth listing, and what do they prove?
- What is a realistic study order for this role?

## 5. Deliverables

| File | Purpose |
|---|---|
| `00-source-log/SOURCES.md` | Source URLs, access date, confidence |
| `00-source-log/job-description.md` | Posting captured and split into requirements |
| `01-salesforce-key-principles/principles.md` | The principles spine |
| `01-salesforce-key-principles/release-model.md` | Environments, branching, promotion, control gates |
| `02-limits-constraints/governor-limits.md` | Apex governor limits and bulkification |
| `02-limits-constraints/other-limits-and-system-settings.md` | Org/platform limits and system properties |
| `02-limits-constraints/dependencies-and-constraints.md` | Metadata dependencies and deployment constraints |
| `02-limits-constraints/inspection-and-drills.md` | UI/CLI inspection and interview drills |
| `03-devops-tools/tool-landscape.md` | Tool comparison and selection |
| `03-devops-tools/gearset-click-paths.md` | Gearset practical click-paths |
| `03-devops-tools/copado-autorabit-devopscenter.md` | The other tools and Change Sets |
| `04-cicd/github-actions-salesforce.md` | Pipeline stages, YAML, why |
| `04-cicd/auth-secrets-environments.md` | JWT, secrets, environments, approvals |
| `04-cicd/other-ci-platforms.md` | Azure DevOps and GitLab mapping |
| `05-certifications/certification-landscape.md` | What the posting names and what exists |
| `05-certifications/salesforce-credentials.md` | PD1, App Builder, Admin, Admin II curricula |
| `05-certifications/vendor-and-study-plan.md` | Vendor certs and study plan |
| `06-term-deep-dives/term-index.md` | Every posting term mapped to a file |
| `06-term-deep-dives/term-entries.md` | Term-by-term deep dives |
| `07-merge/merge-map.md` | File → page section mapping |
| `07-merge/content-gaps.md` | What the current page lacks and what to change |
| `08-cross-bundle-notes.md` | Reconciliation with the sibling `salesforceagain` bundle and verified corrections |

## 6. Open questions for the merge agent

1. Does the downstream page want full click-paths, or a compact table plus a caveat? The research provides both a table and detail so the merge agent can choose.
2. Should the certification section keep exact exam weights? Recommendation: no, unless the current official exam guide PDF is fetched and cited. Use domains and study-guide links.
3. Should the GitHub Actions YAML be inline on the page or linked? Recommendation: inline in a collapsible block, with a short "why" table outside it.
4. Should the page mention Scotiabank by name in the body? Recommendation: only in the header and the JD matrix. The body should describe a regulated-bank pattern, not an internal procedure.
5. Should vendor click-paths be labelled with a "last verified" date? Recommendation: yes, with the research date and a "labels drift" warning.

## 7. Acceptance criteria

- Every posting bullet has a mapped research unit.
- Every limits table has a source and a verify note.
- Every tool has a practical example and a failure mode.
- The pipeline has a runnable YAML and a "why" explanation.
- The certification research distinguishes official Salesforce credentials from vendor certificates.
- The merge map is sufficient for a second agent to integrate without re-reading the whole bundle.
- No secrets, customer data, or invented bank policy.
