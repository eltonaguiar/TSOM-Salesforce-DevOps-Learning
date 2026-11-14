# 06 — Salesforce Certifications & Curriculum Research

> **Scope:** the JD line "Salesforce certifications (PD1, Advanced Admin, DevOps related certs)" plus the round-2 requirement to research the **curriculum** behind each.
> **Important:** exact exam domain weights change with each release. This file describes the **domains and study path**, and tells you where to confirm the current weightings. Do not memorise percentages from a blog.

---

## 1. What the JD actually names

| JD phrase | Current Salesforce credential | Notes |
|---|---|---|
| **PD1** | **Salesforce Certified Platform Developer I** | Exam code `Plat-Dev-201` |
| **Advanced Admin** | **Salesforce Certified Platform Administrator II** | Formerly "Advanced Administrator"; exam code `Plat-Admn-301`. Prerequisite: Platform Administrator |
| **DevOps related certs** | **Salesforce Certified Platform Development Lifecycle and Deployment Architect** | Exam code `Plat-Arch-202`; this is the closest official "DevOps" credential |

There is **no** official certification literally called "Salesforce DevOps Engineer." When an interviewer says "DevOps cert," they usually mean the **Development Lifecycle and Deployment Architect**, or a **vendor** certification (Copado/Gearset/AutoRABIT). Say this precisely — it signals you know the credential landscape.

> Credential names were modernised: "Salesforce Certified Administrator" → **Salesforce Certified Platform Administrator**; "Advanced Administrator" → **Platform Administrator II**; "Development Lifecycle and Deployment Architect" → **Platform Development Lifecycle and Deployment Architect**. Use both names in conversation.

---

## 2. Credential map

<details>
<summary><strong>2.1 At a glance</strong></summary>

| Credential | Level | Prerequisite | Best for | Maps to JD |
|---|---|---|---|---|
| Platform Administrator | Foundational admin | None | Admin baseline | Indirect |
| Platform Administrator II | Advanced admin | Platform Administrator | Senior admin / release admin | "Advanced Admin" |
| Platform App Builder | Declarative builder | None (Admin recommended) | Designing objects, Flow, security | Strong adjacent |
| Platform Developer I (PD1) | Developer | None | Apex, tests, deploy | "PD1" |
| Platform Developer II (PDII) | Advanced developer | PD1 | Complex Apex, integrations, advanced | Optional depth |
| Platform Development Lifecycle & Deployment Architect | Architect | Recommended: PD1/Admin + experience | Release architecture, environments, governance | "DevOps related" |
| Application Architect / System Architect | Architect track | Multiple prerequisites | Broader architecture | Career ceiling |

</details>

---

## 3. Platform Developer I (PD1)

<details>
<summary><strong>3.1 What it proves</strong></summary>

You can build and deploy custom business logic and interfaces on the Lightning Platform: Apex, SOQL/SOSL, DML, triggers, testing, and the deployment model. It is the **developer baseline** the JD asks for under "Salesforce Platform Developer experience."

**Official page:** <https://trailhead.salesforce.com/credentials/platformdeveloperi>
**New experience / exam registration:** <https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201>
**Study trail:** "Study for the Salesforce Platform Developer Certification"
**Prep trailmix:** "Prepare for Your Salesforce Platform Developer Certification"
</details>

<details>
<summary><strong>3.2 Domain areas (study these; verify current weights in the exam guide)</strong></summary>

- **Salesforce fundamentals** — platform architecture, MVC, multi-tenancy, metadata.
- **Data modeling and management** — objects, relationships, schema builder, SOQL/SOSL, DML.
- **Process automation and logic** — Flow, Apex, triggers, order of execution.
- **User interface** — Lightning components (LWC/Aura basics), Visualforce (legacy), Lightning pages.
- **Testing, debugging, and deployment** — test classes, coverage, debug logs, Metadata API, change sets, CLI, packages.
- **Performance** — governor limits, bulkification, async Apex, query selectivity.
- **Integration** — REST/SOAP callouts, Named Credentials, remote sites, Platform Events.

**How it maps to this role:** the "Testing, debugging, and deployment" and "Performance" domains are exactly the release-engineering skills in `01` and `02`. The role does not require you to be the best Apex author, but PD1 fluency lets you **review** Apex for bulkification and dependency risks.
</details>

<details>
<summary><strong>3.3 PD1 study sequence (practical)</strong></summary>

1. **Developer Beginner** trail (objects, Apex basics, SOQL, DML).
2. **Apex Basics & Database** module + **Apex Triggers** module.
3. **Apex Testing** module — write a test class, assert bulk behaviour.
4. **Asynchronous Apex** module — future, Queueable, Batch, Scheduled.
5. **Search Solution Basics** (SOSL) and **SOQL** deep dive.
6. **Lightning Web Components Basics** trail.
7. **Metadata API / deployment** modules + `sf` CLI hands-on.
8. Build the four labs in the published **Labs & Design** page.
9. Take practice exams; review every wrong answer against the official guide.

**Evidence you can show an interviewer:** a repo with an Apex trigger + handler + test class, a delta deploy workflow, and a debug log showing you diagnosed a limit.
</details>

---

## 4. Platform Administrator II (the JD's "Advanced Admin")

<details>
<summary><strong>4.1 What it proves</strong></summary>

Advanced declarative administration: complex security, data management, automation at scale, and environment/change management. It is the **admin-side counterpart** to PD1.

**Official page:** <https://trailhead.salesforce.com/credentials/platformadministrator-ii>
**Exam registration:** <https://trailheadacademy.salesforce.com/certificate/exam-platform-admin2---Plat-Admn-301>
**Prerequisite:** <https://trailhead.salesforce.com/credentials/platformadministrator>
**Prep trailmix:** "Prepare for Your Salesforce Platform Administrator II Certification"
</details>

<details>
<summary><strong>4.2 Domain areas</strong></summary>

- **Security and access** — profiles, permission sets, permission set groups, OWD, role hierarchy, sharing rules, territory, login policies.
- **Object and data model** — objects, fields, relationships, record types, schema design.
- **Process automation** — Flow, approvals, order of execution, fault handling.
- **Data management** — import/export, duplicate management, data quality, validation rules.
- **Analytics / reporting** — reports, dashboards, report types (lighter weight).
- **Environment and change management** — sandboxes, change sets, deployment, DevOps Center.
- **Audit and compliance** — field history, setup audit trail, access reviews.

**How it maps to this role:** the security model and environment-management domains are directly relevant to `02` (profiles/permsets, record types/layouts, security model) and `05` B10/B11.
</details>

<details>
<summary><strong>4.3 Why "Advanced Admin" matters for a DevOps engineer</strong></summary>

Most release conflicts in a bank are **admin metadata**: profiles, permission sets, record types, layouts, sharing. An engineer who only knows Apex will misdiagnose them. Admin II gives you the vocabulary to resolve conflicts and to coach admins toward deployable patterns.
</details>

---

## 5. Platform Development Lifecycle and Deployment Architect (the "DevOps cert")

<details>
<summary><strong>5.1 What it proves</strong></summary>

You can assess environments and requirements and design a **development lifecycle, release, and deployment architecture**: environment strategy, source control, CI/CD, testing, governance, and change management.

**Official page:** <https://trailhead.salesforce.com/credentials/developmentlifecycledeploymentarchitect>
**Exam registration:** <https://trailheadacademy.salesforce.com/certificate/exam-dev-lifecycle---Plat-Arch-202>
**Study trailmix:** "Architect Journey: Development Lifecycle and Deployment"
</details>

<details>
<summary><strong>5.2 Domain areas</strong></summary>

- **Development lifecycle** — org development vs package development vs hybrid; environment strategy; sandbox types.
- **Source control and branching** — Git models, branching strategy, release branching, hotfix.
- **Deployment** — Metadata API, change sets, CLI, packages, tools (Gearset/Copado/AutoRABIT/DevOps Center), destructive changes.
- **Testing** — unit/integration/UAT, test levels, coverage, test data, automation.
- **Environment management** — refresh, seeding, masking, parity, scratch orgs, Dev Hub.
- **Governance** — approvals, segregation of duties, audit, compliance, change management.
- **Architecture and metrics** — release architecture, DORA-style metrics, scaling teams.

**How it maps to this role:** this is essentially the JD. If you can only pursue one "DevOps" credential, pursue this one after PD1/Admin foundations.
</details>

<details>
<summary><strong>5.3 Study path</strong></summary>

1. Complete the **Architect Journey: Development Lifecycle and Deployment** trailmix.
2. Study the three lifecycle models (org-dependent, package-based, hybrid) and when each fits.
3. Build a small end-to-end pipeline (this repo's `04` is a starter).
4. Practise designing an environment ladder for a regulated org (five stages, mask, SoD).
5. Read the **Architect** credential overview: <https://trailhead.salesforce.com/credentials/architectoverview>
6. Review governance/audit case studies (banking analogies are fine).
</details>

---

## 6. Adjacent credentials worth knowing

<details>
<summary><strong>6.1 Platform App Builder</strong></summary>

Declarative app design: objects, relationships, Flow, security, UI. It fills gaps between Admin and Developer and is often the easiest "next" credential for an admin-heavy team.

<https://trailhead.salesforce.com/credentials/platformappbuilder>
</details>

<details>
<summary><strong>6.2 Platform Developer II (PDII)</strong></summary>

Advanced Apex, integration, performance, and lifecycle. Useful if you want to be the person who can fix the Apex, not just deploy it. Requires PD1.

<https://trailhead.salesforce.com/credentials/platformdeveloperii>
</details>

<details>
<summary><strong>6.3 Salesforce Certified Platform Administrator (foundation)</strong></summary>

The prerequisite for Admin II and the vocabulary baseline for everything else.

<https://trailhead.salesforce.com/credentials/platformadministrator>
</details>

---

## 7. Vendor certifications (Copado, Gearset, AutoRABIT)

<details>
<summary><strong>7.1 What they are worth</strong></summary>

Vendor credentials show **tool time**, not platform fundamentals. In an interview they are a plus when the bank already owns the tool; they do not replace PD1 or the Deployment Architect credential.

| Vendor | Credential area | What it signals |
|---|---|---|
| **Copado** | Copado certifications / Copado Fundamentals | Work items, pipelines, promotion, compliance |
| **Gearset** | Gearset DevOps certifications / training | Compare/deploy, pipelines, backup |
| **AutoRABIT** | AutoRABIT certifications | ARM deployments, CodeScan, Vault |

**Advice:** if the job posting names a tool the bank uses, a vendor badge is a cheap differentiator — but only after you can explain the Metadata API underneath it (see `03` §0).
</details>

<details>
<summary><strong>7.2 How to talk about vendor certs without over-claiming</strong></summary>

*"I've used Gearset/Copado/AutoRABIT at the UI level for compare, deploy, and promotion, and I understand they sit on the Metadata API. My platform fundamentals are PD1/Admin-level, so I can debug when the tool's dependency resolution misses something."*
</details>

---

## 8. Curriculum: 8-week plan for this role

<details>
<summary><strong>8.1 Week-by-week</strong></summary>

| Week | Focus | Modules / trails | Repo file |
|---|---|---|---|
| 1 | Platform fundamentals | Admin Beginner; Developer Beginner | crash course |
| 2 | Data model + security | Data Security; Profiles & Permission Sets; Sharing | `05` B10/B11 |
| 3 | Apex + triggers + tests | Apex Basics, Triggers, Apex Testing | `05` B8 |
| 4 | Limits + performance | Asynchronous Apex; governor limits; query selectivity | `01` |
| 5 | Metadata + deployment | Metadata API; `sf` CLI; package.xml; destructive changes | `02` |
| 6 | Git + CI/CD | Git basics; build the `04` pipeline in a dev org | `04` |
| 7 | Environments + governance | Sandboxes; Data Mask; release architecture; SoD | `05` A2/A4/A6 |
| 8 | Cert + mock interview | PD1 or Admin II practice exams; mock drills | `05` §Interview |

</details>

<details>
<summary><strong>8.2 Hands-on evidence to build (better than badges)</strong></summary>

- Two Developer Edition orgs, aliased `dev` and `qa`.
- A Git repo with `force-app`, `sfdx-project.json`, `.forceignore`.
- A permission set deployed via PR validation.
- An Apex trigger + handler + bulk test.
- A delta-deploy GitHub Actions workflow.
- A runbook filled for a fake production release.
- A one-page environment ladder diagram.

</details>

---

## 9. Exam logistics and maintenance (verify current terms)

<details>
<summary><strong>9.1 What to confirm before booking</strong></summary>

- **Exam guide PDF** for the current release — read the domain weights and objectives. Salesforce gates some docs behind login/bot checks; if a URL 403s, use the Trailhead Academy "See New Experience" link or the official exam guide linked from the credential page.
- **Prerequisites** (Admin II requires Platform Administrator).
- **Format** — proctored, multiple-choice/multi-select; some exams include scenario questions.
- **Maintenance** — Salesforce requires completing maintenance modules each release cycle to keep a credential active; check <https://trailhead.salesforce.com/credentials/verification>.
- **Cost and scheduling** — via Trailhead Academy; prices and delivery options vary by region.

**Do not** publish a hard domain-weight table from memory. Link the official guide and describe the domains.
</details>

---

## 10. Recommended study order for requisition 276046

```text
Platform Administrator (foundation)
   → Platform Developer I (PD1)        ← JD explicitly names
   → Platform Administrator II         ← JD's "Advanced Admin"
   → Platform Development Lifecycle
     and Deployment Architect          ← JD's "DevOps related cert"
   → (optional) Platform App Builder / PDII
   → (optional) vendor cert for the bank's tool
```

**Why this order:** the role is release engineering, so you need both sides — developer (deploy/compile/test) and admin (security/config conflicts). The Deployment Architect credential is the synthesis, and it is much easier once PD1 and Admin II vocabulary is in place.

---

## 11. How to present certifications in an interview

<details>
<summary><strong>11.1 The framing</strong></summary>

- Lead with the **credential that matches the JD** (PD1, Admin II, Deployment Architect).
- Say what each one **lets you do**, not just that you passed it.
- Be honest about vendor tools: "UI-level experience, understands the Metadata API underneath."
- Connect each credential to a **release outcome**: fewer failed deploys, safer permission changes, auditable promotions.

**Example:** *"PD1 gives me the Apex/testing/deployment vocabulary to review a change before it ships. Admin II gives me the security-model vocabulary to resolve profile and record-type conflicts. The Deployment Architect track is the one that maps directly to this role — environment strategy, CI/CD, governance."*
</details>

---

## 12. Sources for this file

- Platform Developer I: <https://trailhead.salesforce.com/credentials/platformdeveloperi>
- Platform Administrator II: <https://trailhead.salesforce.com/credentials/platformadministrator-ii>
- Platform Administrator: <https://trailhead.salesforce.com/credentials/platformadministrator>
- Platform App Builder: <https://trailhead.salesforce.com/credentials/platformappbuilder>
- Platform Developer II: <https://trailhead.salesforce.com/credentials/platformdeveloperii>
- Platform Development Lifecycle and Deployment Architect: <https://trailhead.salesforce.com/credentials/developmentlifecycledeploymentarchitect>
- Architect overview: <https://trailhead.salesforce.com/credentials/architectoverview>
- Certification verification/maintenance: <https://trailhead.salesforce.com/credentials/verification>

> Verified 2026-11-14: credential names and exam codes above. Domain weights intentionally not stated — confirm from the current official exam guide before publishing a table.
