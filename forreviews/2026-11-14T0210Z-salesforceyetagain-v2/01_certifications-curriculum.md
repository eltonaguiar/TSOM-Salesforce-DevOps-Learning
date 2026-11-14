# Salesforce Certifications — Curriculum Research

**Worktree:** salesforceyetagain-v2  
**Date:** 2026-11-14T02:10Z  
**Source track:** Salesforce DevOps Engineer — Release Engineering Training (Scotiabank requisition 276046)  
**Official cert pages:**
- Platform Developer I: https://trailhead.salesforce.com/credentials/platformdeveloperi
- Platform App Builder: https://trailhead.salesforce.com/credentials/platformappbuilder
- Platform Administrator II (formerly Advanced Admin): https://trailhead.salesforce.com/credentials/platformadministrator-ii

---

## Certifications named in the track

The DevOps Engineer posting names **Platform Developer I**, **Advanced Admin**, and "DevOps related certs."

| Credential named in track | Current official name | Maps to DevOps role |
|---|---|---|
| Platform Developer I | Salesforce Certified Platform Developer I | Apex, tests, platform model you deploy |
| Advanced Admin | Salesforce Certified Platform Administrator II (renamed from Advanced Admin) | Security, change, environments — topics overlapping releases |
| (not named, but relevant) | Salesforce Certified Platform App Builder | Metadata you move every week: objects, Flow, security |
| "DevOps related certs" | No official Salesforce "DevOps Engineer" cert exists | Copado, Gearset, AutoRABIT vendor certs show tool time; do not replace PD1 |

---

## 1. Platform Developer I

**About:** Certified Platform Developers understand how to develop and deploy custom business logic and custom interfaces using the programmatic capabilities of the Lightning Platform. They extend the platform using Apex and Visualforce.

**Exam guide:** https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201  
**Study guide trail:** https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide  
**Trailmix:** Prepare for Your Salesforce Platform Developer I credential

**Curriculum (relevant to this DevOps track):**
- Apex programming (classes, triggers, governor limits)
- SOQL / SOSL queries
- DML and transaction control
- Test classes and code coverage (75% production gate)
- Debug logs and troubleshooting
- Visualforce pages and controllers
- Deployment basics (Change Sets, CLI)
- Bulkification and bulk patterns

**Why it matters for DevOps:** PD1 is the baseline the posting expects. You cannot sign off on an Apex story without understanding triggers, tests, governor limits, and the 75% coverage gate that production enforces.

---

## 2. Platform App Builder

**About:** Certified Platform App Builders have the skills and knowledge to design, build, and deploy custom applications using the declarative customization capabilities of the Salesforce Platform.

**Exam guide:** https://trailheadacademy.salesforce.com/certificate/exam-app-builder---Plat-Admn-202  
**Study trail:** https://trailhead.salesforce.com/content/learn/trails/prepare-for-your-salesforce-platform-app-builder-certification

**Curriculum (relevant to this DevOps track):**
- Data model: objects, fields, relationships (lookup / master-detail), record types
- Automation: Flow (replacing Workflow Rules / Process Builder)
- Security: profiles, permission sets, roles, org-wide defaults, field-level security
- App deployment: Change Sets, sandbox strategy, package basics
- UI: page layouts, Lightning App Builder, Lightning Web Components awareness

**Why it matters for DevOps:** This is the metadata you move every week — objects, Flow, security. Release engineers must evaluate whether a change is declarative (App Builder domain) or programmatic (PD1 domain), because that determines testing, deployment path, and conflict risk.

---

## 3. Platform Administrator II (formerly Advanced Admin)

**About:** Seasoned Salesforce Administrators who can harness advanced features and functionality to solve business problems. Has Platform Administrator as a prerequisite.

**Exam guide:** https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301  
**Trailmix:** Prepare for Your Salesforce Advanced Administrator credential  
**Note:** The track says "Salesforce renamed this credential to Platform Administrator II. Study the current exam guide and use both names in conversation."

**Curriculum (relevant to this DevOps track):**
- Security and access (profiles, permission sets, roles, sharing)
- Data management (import/export, validation rules, duplicate management)
- Automation troubleshooting (Flow)
- UI customization and page layouts
- Reports and dashboards
- Change management and environments (overlaps releases)

**Why it matters for DevOps:** Platform Administrator II topics that overlap releases — security, change, environments — are the ones the DevOps Engineer role needs. Study order per the track: crash course and PD1 material first, then this page's labs, then Platform Administrator II topics overlapping releases.

---

## 4. "DevOps related certs" — no official Salesforce DevOps cert

**There is no official Salesforce "DevOps Engineer" certification to list as if it existed.** The track is explicit:

- Copado, Gearset, and AutoRABIT offer their own certificates
- Those show tool time
- They do **not** replace PD1

**Positioning:** Treat vendor DevOps certs as supplementary evidence of tool familiarity (Gearset/Copado/AutoRABIT compare-and-deploy pipelines). The core credentials remain PD1 + Platform App Builder + Platform Administrator II.

---

## Recommended study order (per the track)

1. Crash course (objects, security, Flow, Apex, governor limits)
2. PD1 material (Apex, tests, platform model)
3. DevOps track labs (Lab A–E: retrieve/dry-run, profile conflict, failing validation, runbook, sandbox+mask checklist)
4. Platform Administrator II topics overlapping releases (security, change, environments)

---

## Verification note

Exam weights and domain breakdowns were not captured from the credential pages (JavaScript-rendered). Before finalizing a study plan, pull the official exam guide PDFs linked above and map each domain to the 12 DevOps training items in `00_planning-salesforce-principles.md`.