# Certification landscape — what the posting names and what actually exists

**Merge target:** the page's Certifications section and the term-by-term entry for Q14. This file corrects the two common interview mistakes: treating "Advanced Admin" as the current name, and implying an official Salesforce DevOps Engineer certification exists.

## 1. What the posting says

> Salesforce certifications (PD1, Advanced Admin, DevOps related certs)

That is three different things:

1. **PD1** — Salesforce Certified Platform Developer I. A real, current Salesforce credential.
2. **Advanced Admin** — the former name of **Salesforce Certified Platform Administrator II**. A real, current credential under a new name.
3. **"DevOps related certs"** — a category, not a specific Salesforce credential. There is no official Salesforce Certified DevOps Engineer exam. Vendor certificates exist (Gearset, Copado, AutoRABIT), and Salesforce's architect/developer credentials cover parts of the lifecycle, but the posting is using a loose category.

## 2. Current Salesforce credentials that map to this role

| Credential | Current name | Why it maps | Official page |
|---|---|---|---|
| Platform Developer I (PD1) | Salesforce Certified Platform Developer I | Apex, triggers, testing, deployment tools, the platform model you deploy | <https://trailhead.salesforce.com/credentials/platformdeveloperi> |
| Platform App Builder | Salesforce Certified Platform App Builder | Objects, fields, security, automation, UI, app deployment — the metadata you move every week | <https://trailhead.salesforce.com/credentials/platformappbuilder> |
| Administrator (foundation) | Salesforce Certified Platform Administrator | The baseline admin model: configuration, security, data, automation | <https://trailhead.salesforce.com/credentials/platformadministrator> |
| Advanced Administrator | Salesforce Certified Platform Administrator II | Advanced security, objects, automation, data, environment management and deployment | <https://trailhead.salesforce.com/credentials/platformadministrator-ii> |
| Platform Developer II | Salesforce Certified Platform Developer II | Advanced Apex, integration, performance, lifecycle; useful but not named in the posting | <https://trailhead.salesforce.com/credentials/platformdeveloperii> |

**Naming note.** Use both names in conversation: "Advanced Administrator, now called Platform Administrator II." That shows you are current and that you know the history.

## 3. What does not exist

- **Salesforce Certified DevOps Engineer.** Not an official Salesforce credential as of 2026-11-14. Do not claim it.
- **A single "Salesforce DevOps" exam** covering Gearset/Copado/AutoRABIT. Salesforce does not certify third-party tools.
- **A vendor certificate that replaces PD1.** Vendor certificates show tool familiarity; they do not prove Apex or platform fundamentals.

## 4. What "DevOps related certs" can reasonably mean

| Category | Examples | What it proves | Caveat |
|---|---|---|---|
| Salesforce developer/architect credentials | PD1, PD2, Application Architect, System Architect, Technical Architect | Platform depth, including deployment and integration | Not DevOps-specific |
| Gearset / DevOps Launchpad | Salesforce DevOps Fundamentals, CI/CD for Salesforce, DevOps Leadership, Salesforce Backup, Gearset Academy | DevOps concepts and Gearset tool use | Free tracks; verify the current catalogue |
| Copado | Copado Academy / Copado certification program | Copado pipeline and release-management use | Offerings and URLs change; verify with Copado |
| AutoRABIT | AutoRABIT Academy / certification program | AutoRABIT CI, deployment, data, backup | Verify current programme; product packaging varies |

**Rule for the page:** list vendor certificates as "tool time," not as a substitute for PD1. Keep the "verify current offering" caveat.

## 5. Mapping to the posting

| Posting phrase | Best interpretation | What to say in an interview |
|---|---|---|
| PD1 | Platform Developer I | "I have PD1-level Apex, testing, and deployment-tool knowledge." |
| Advanced Admin | Platform Administrator II | "Advanced Administrator is now Platform Administrator II; I know the advanced security, automation, and environment-management domains." |
| DevOps related certs | Vendor + Salesforce developer/architect credentials | "There is no official Salesforce DevOps Engineer cert. I have hands-on pipeline evidence plus a vendor certificate or PD1/architect material." |

## 6. What to merge

**Merge:** the three-part interpretation, the current-name table, the "what does not exist" list, and the mapping table.

**Do not merge:** any claim that a specific vendor certification is required, or that an official Salesforce DevOps certification exists.
