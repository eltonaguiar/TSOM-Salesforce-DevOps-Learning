# Merge-Against-Pages Mapping Matrix

**Worktree/session:** salesforcemore  
**Date-time stamp:** 20261114-020852  
**Purpose:** Shows where each research item maps onto each GitHub Pages variation page, so a later agent can merge and organize this work against the canonical pages.  
**Merge agent target pages:**
1. devops-engineer — https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/
2. crash-course — https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/
3. navigation-breadcrumbs — https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/navigation-breadcrumbs/
4. labs-design — https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/
5. user-management-data — https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/user-management-data/

## Research items (produced in this session)

| ID | Item | Folder | File |
|----|------|--------|------|
| R1 | Salesforce limits, metadata dependencies, deployment constraints deep dive | workspace root | SALESFORCE_LIMITS_DEEP_DIVE.md |
| R2 | Salesforce DevOps deep dive (JD cross-reference, Gearset UI, CI/CD, interview drills) | workspace root | SALESFORCE_DEVOPS_DEEP_DIVE.md |
| R3 | Salesforce key principles deep dive | salesforce-principles/ | KEY_PRINCIPLES.md |
| R4 | Certification research (PD1, App Builder, Admin II, DevOps certs) | certification-research/ | CERTIFICATION_RESEARCH.md |
| R5 | Plan (Salesforce key principles planning frame) | root of dated folder | PLAN.md |
| R6 | Source captures (crash-course, navigation-breadcrumbs, labs-design, user-management-data, GitHub repo README) | source-capture/ | *.md |

## Variation pages and their current sections

### Page 1 — devops-engineer (DevOps & Release Engineering)
Current sections: What this role actually owns; Training items; 1 Source of truth; 2 Metadata that breaks releases; 3 Environments and sandboxes; 4 Branching; 5 CI/CD; 6 DevOps tools; 7 Conflict clinic; 8 Packages; 9 Tests and validation; 10 Releases/hotfixes/rollback; 11 Banking change control; 12 Design patterns you coach; Labs; Interview drills; Certifications; Quiz.

### Page 2 — crash-course
Current sections: What Is Salesforce?; The Big Picture; Navigation; Users/Profiles/Roles/Security; Data Integrity & Relationships; Automation; Code (Apex/Visualforce/LWC); Integration; Troubleshooting & Performance; Governor Limits Deep Dive; Design Considerations; Out-of-the-Box Features; Official Learning Resources; Quick Start Checklist.

### Page 3 — navigation-breadcrumbs
Current sections: App Launcher & Home; Setup Navigation Tree; Object & Field Configuration; Security & Access; Automation; Development (Code); Integration; Deployment & DevOps; Monitoring & Troubleshooting; Data Management; Quick Reference.

### Page 4 — labs-design
Current sections: Pre-Existing Labs & Documentation; Lab 1 (custom object & Flow); Lab 2 (Apex trigger); Lab 3 (LWC); Lab 4 (REST callout); Design Considerations; System Properties & OOB Features; What to Think About Before You Build.

### Page 5 — user-management-data
Current sections: Users: Creation & Lifecycle; Profiles & Permission Sets; Roles & Record Sharing; Licenses & Permission Types; Data Import & Export; Data Integrity & Quality; Field-Level Security & Encryption; Duplicate Management; Data Design Best Practices; Troubleshooting Data & Access Issues.

## Mapping matrix: research item → page section → merge note

| Research | devops-engineer section | crash-course section | navigation-breadcrumbs section | labs-design section | user-management-data section | Merge note |
|----------|------------------------|----------------------|-------------------------------|---------------------|------------------------------|------------|
| R1 (limits/dependencies/constraints) | Section 2 “Metadata that breaks releases”; Section 9 “Tests and validation” | Governor Limits Deep Dive | Deployment & DevOps; Monitoring & Troubleshooting | Design Considerations (bulkification) | — | Expand Section 2 with governor limits table, dependency graph, error-string mapping, pre-deploy checklist |
| R2 (DevOps deep dive / Gearset UI / CI/CD) | All sections (this page is built from R2) | — | Deployment & DevOps | Deployment Options table | — | R2 is the superset of this page; merge agent should fold R2’s Gearset UI paths and CI/CD reference into devops-engineer Section 6 |
| R3 (key principles) | Section 12 “Design patterns you coach” | Design Considerations | Setup Navigation Tree (all) | The “Buy vs Build” / Maintenance Question | Profiles & Permission Sets; Roles & Record Sharing | Distribute principles across pages; principles doc is the planning frame |
| R4 (certifications) | Certifications section | Official Learning Resources | — | — | — | Add exam-guide URLs + skill-weight placeholders (exam guides JS-rendered, need browser fetch) |
| R5 (plan) | — | — | — | — | — | Planning artifact; not merged into pages |
| R6 (source captures) | — | crash-course.md | navigation-breadcrumbs.md | labs-design.md | user-management-data.md | Raw captures for merge agent reference |

## Recommended merge order (for the merge agent)

1. Start with `devops-engineer` — it’s the canonical page for the Scotiabank role. Fold R2 (Gearset UI paths, CI/CD reference, interview drills) and R1 (limits/dependencies/constraints deep dive) into it.
2. Expand `crash-course` Governor Limits Deep Dive with R1 content and link to R3 principles.
3. Update `navigation-breadcrumbs` Deployment & DevOps and Security & Access sections with R1/R3 cross-references.
4. Update `labs-design` Design Considerations and Deployment Options with R3 and R2 cross-references.
5. Update `user-management-data` with R3 security-layer mappings.
6. Add certification exam-guide URLs (R4) to `devops-engineer` Certifications section; note that detailed skill weights need a browser fetch of the JS-rendered exam guides.

## Files for merge agent to consume

- `/20261114-020852-salesforcemore/PLAN.md` — planning frame
- `/20261114-020852-salesforcemore/salesforce-principles/KEY_PRINCIPLES.md` — principles
- `/20261114-020852-salesforcemore/certification-research/CERTIFICATION_RESEARCH.md` — cert research
- `/20261114-020852-salesforcemore/source-capture/*.md` — raw page captures
- Workspace root: `SALESFORCE_LIMITS_DEEP_DIVE.md`, `SALESFORCE_DEVOPS_DEEP_DIVE.md` — the two deep dives
