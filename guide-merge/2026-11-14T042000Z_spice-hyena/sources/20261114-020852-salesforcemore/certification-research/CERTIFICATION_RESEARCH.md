# Certification Research — Salesforce Certifications Mentioned in Scotiabank Req 276046

**Worktree/session:** salesforcemore  
**Date-time stamp:** 20261114-020852  
**Source:** https://trailhead.salesforce.com/credentials/platformdeveloperi, /credentials/platformadministrator-ii, /credentials/platformappbuilder  
**Job posting certifications:** Platform Developer I (PD1), Advanced Admin (renamed Platform Administrator II), “DevOps related certs”

---

## 1. Salesforce Certified Platform Developer I (PD1)

**Source page:** https://trailhead.salesforce.com/credentials/platformdeveloperi  
**Exam guide (detailed curriculum):** https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201 *(JS-rendered; about-text captured below)*

### About the Exam (captured)
> Certified Platform Developers understand how to develop and deploy custom business logic and custom interfaces using the programmatic capabilities of the Lightning Platform. They can also extend the Lightning Platform using Apex and Visualforce.

### Recommended preparation (captured from page)
- Trailmix: “Prepare for Your Salesforce Platform Developer Certification” (Trailhead)
- Trail: “Study for the Salesforce Platform Developer Certification” — Platform Developer I Certification Study Guide (Trailhead)

### Related certifications
- Salesforce Certified Agentforce Specialist
- Salesforce Certified B2C Commerce Developer
- Salesforce Certified Platform App Builder
- Salesforce Certified Platform Developer II (PDII)

### Certification study & prepare links (captured)
- Prepare for Your Salesforce Platform Developer Certification (Trailmix)
- Study for the Salesforce Platform Developer Certification (Trail)

### DevOps-relevance notes for PD1
PD1 covers Apex, triggers, test classes, code coverage, governor limits, SOQL/DML, Visualforce basics — all directly relevant to the deployment-conflict and testing sections of the DevOps Engineer role. PD1 is the named certification in the posting and is the foundational cert for any Salesforce release engineer.

---

## 2. Salesforce Certified Platform App Builder

**Source page:** https://trailhead.salesforce.com/credentials/platformappbuilder  
**Exam guide (detailed curriculum):** https://trailheadacademy.salesforce.com/certificate/exam-app-builder---Plat-Admn-202 *(JS-rendered; about-text captured below)*

### About the Exam (captured)
> Certified Platform App Builders have the skills and knowledge to design, build, and deploy custom applications using the declarative customization capabilities of the Salesforce Platform.

### Recommended preparation (captured from page)
- Trail: “Prepare for Your Salesforce Platform App Builder Certification” (Trailhead)

### Related certifications
- Salesforce Certified Agentforce Specialist
- Salesforce Certified Platform Administrator
- Salesforce Certified Platform Administrator II

### DevOps-relevance notes for Platform App Builder
App Builder covers declarative customization: objects, fields, record types, page layouts, validation rules, Flows, security (profiles/permission sets/FLS), and app deployment basics. Maps directly to the “metadata you move every week” portion of the DevOps Engineer role (objects, Flow, security).

---

## 3. Salesforce Certified Platform Administrator II (formerly Advanced Admin)

**Source page:** https://trailhead.salesforce.com/credentials/platformadministrator-ii  
**Exam guide (detailed curriculum):** https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301 *(JS-rendered; about-text captured below)*

### About the Exam (captured)
> Certified Platform Administrator II holders are seasoned Salesforce Administrators who can harness the power of advanced features and functionality to solve a variety of business problems.

### Prerequisite (captured)
- Salesforce Certified Platform Administrator (the credential the posting calls “Advanced Admin”)

### Recommended preparation (captured from page)
- Trailmix: “Prepare for Your Salesforce Platform Administrator II Certification” (Trailhead)

### Related certifications
- Salesforce Certified CPQ Administrator
- Salesforce Certified Platform App Builder

### DevOps-relevance notes for Platform Administrator II
This is the renamed “Advanced Admin” referenced in the posting. It covers security, change management, environments/sandboxes, deployment, and org configuration — the core of banking change control and release management. Overlaps heavily with the DevOps training track sections on environments, sandbox strategy, change control, and audit.

---

## 4. “DevOps Related Certs”

The posting lists “DevOps related certs” as desired. There is **no official Salesforce “DevOps Engineer” certification** as of this capture. Vendor certifications exist:
- Copado certification
- Gearset certification
- AutoRABIT certification

These show tool-specific time but **do not replace PD1** per the training page guidance.

---

## Study Order Recommended for This Role

1. Crash course + PD1 material (Apex, tests, platform model you deploy)
2. This repo’s labs (hands-on: object + Flow, trigger + test, LWC, REST callout)
3. Platform Administrator II topics overlapping releases (security, change, environments)

---

## Exam Guide URLs (for merge agent to populate detailed curricula)

| Certification | Exam Guide URL |
|--------------|----------------|
| Platform Developer I | https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201 |
| Platform Administrator II | https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301 |
| Platform App Builder | https://trailheadacademy.salesforce.com/certificate/exam-app-builder---Plat-Admn-202 |

> The exam guide pages are JavaScript-rendered and returned empty via webfetch. A follow-up agent should visit these URLs in a browser or via the Trailhead Academy API to extract skill weights (e.g., “Developer Fundamentals 22%”, “Apex 26%”, etc.) and merge them here.
