# 06 — Certifications named in the posting, and their curricula

> JD line covered: **"Salesforce certifications (PD1, Advanced Admin, DevOps related certs)"** (Q17).
>
> Credential names and prerequisites read from the official Salesforce credential pages on
> **2026-11-14**. Vendor certification details read from each vendor's own training/academy
> pages.

---

## 1. What the posting is actually asking for

| Posting phrase | Current credential | Prerequisite | Notes |
|---|---|---|---|
| **PD1** | **Salesforce Certified Platform Developer** (exam `Plat-Dev-201`) | — | The posting's "PD1". Trailhead calls it "Platform Developer"; the exam id retains `Plat-Dev-201` |
| **Advanced Admin** | **Salesforce Certified Platform Administrator II** (exam `Plat-Admn-301`) | **Salesforce Certified Platform Administrator** — this is a hard prerequisite, not a recommendation | Salesforce renamed "Advanced Administrator" to "Platform Administrator II". The existing training page says the rename but omits the prerequisite |
| **DevOps related certs** | **No Salesforce-branded DevOps certification exists.** These are vendor credentials | Per vendor | Say the vendor names explicitly; do not imply a Salesforce DevOps cert exists |
| *(implied but unnamed)* | **Salesforce Certified Platform App Builder** | — | Directly relevant: declarative metadata is what a release engineer deploys most often. The existing page mentions it as a study option |

### 1.1 The naming trap

The posting was written before the renames. In an interview:

- Say "**Platform Administrator II**" (and note it is the credential formerly called Advanced
  Administrator) — not "Advanced Admin".
- Say "**Salesforce Certified Platform Developer**" — not "Developer I" without the "Platform".
- Do **not** say "Salesforce DevOps Engineer certification". It does not exist.

### 1.2 The prerequisite changes your sequencing

| If you have | You are eligible for | You still need for this role |
|---|---|---|
| Nothing | Platform Administrator → Platform Administrator II → Platform Developer | Vendor DevOps cert, and the hands-on release engineering evidence |
| Platform App Builder | Platform Administrator → Administrator II; Platform Developer | Same |
| Platform Developer only | Platform Administrator → Administrator II (separate track) | Same |
| Administrator II only | Platform Developer (no prerequisite) | Same |

**Practical sequencing for this posting:** Platform App Builder (fastest, covers the declarative
metadata you deploy daily) → Platform Administrator (needed for Administrator II) → Platform
Administrator II → Platform Developer (PD1). Vendor DevOps certification in parallel or after.

---

## 2. Salesforce Certified Platform Developer (PD1) — curriculum

**Purpose:** "Certified Platform Developers understand how to develop and deploy custom business
logic and custom interfaces using the programmatic capabilities of the Lightning Platform."

**How it maps to the JD:** PD1 covers the *content* a release engineer deploys. It does **not** cover
Git, CI/CD, environments, releases, rollback, or audit. Those come from the vendor certs and from
the job itself. A PD1-only candidate is strong on Apex and weak on releases.

**Curriculum (official study-guide trail modules):**

| Domain | What it covers | Release-engineering relevance |
|---|---|---|
| **Apex Basics** | Variables, operators, classes, triggers, unit tests, execution order, debugging | You review this code every day. Test discipline = deployment gate discipline |
| **Apex and the Salesforce Platform** | Apex in the platform: objects, SOQL/SOSL, DML, collections, governor limits, sObjects | The limits are your capacity model (`02 §2`) |
| **Apex Testing** | Test classes, `testMethod`, `SeeAllData`, setup/teardown, coverage, running tests | **Directly maps to the deployment test level and the 75% per-class rule** |
| **Object Manager** | Objects, fields, validation rules, record types, page layouts, compact layouts | The metadata you deploy most often; the record-type/layout dependency chain |
| **Security** | Profiles, permission sets, permission set groups, OWD, roles, sharing, field-level security | The conflict clinic (`05 §7.1`, `05 §7.2`) |
| **Data Model and Management** | Data modelling, relationships, validation/duplicate rules, import/export | Data masking and data design (`05 §6`) |
| **Workflow and Process Automation** | Workflow, Flow, Process Builder, approval processes | The Flow version trap and the before/after-save distinction |
| **Debug and Deployment** | Debug logs, trace flags, deployment options, the deployment process, change sets | **The most directly relevant module for this role** |
| **Platform Cache** | Session, org and platform cache | Performance in Pre-Prod; cache invalidation after a deploy |

**Study order for this posting:** Debug and Deployment → Apex Testing → Security → Object Manager →
Apex and the Salesforce Platform → the rest. Do not start at Apex Basics if you already write Apex.

**Exam mechanics:** 60 questions, 60 minutes, 65% pass mark, no negative marking, **retake
attempts are limited** — confirm the current attempt allowance on the exam page before booking.

---

## 3. Salesforce Certified Platform Administrator II — curriculum

**Purpose:** "seasoned Salesforce Administrators who can harness the power of advanced features and
functionality."

**Prerequisite:** Salesforce Certified Platform Administrator.

**Curriculum domains (official study-guide trail modules):**

| Domain | Release-engineering relevance |
|---|---|
| **Configuration and Setup** | Org settings: deployment settings, session/password/lockout policies, system properties (`07`) |
| **Object Manager and Data Management** | The metadata surface you deploy and retrieve |
| **Security and Access** | Permission sets/groups, sharing, the deploy identity's permissions (`07 §4`) |
| **Setup and Maintenance** | Sandboxes, refresh, templates, releases, change management (`07 §3`) |
| **Service and Support** | Case handling and support; escalation paths |
| **Productivity / App Builder depth** | Flow, approval processes, the automation you deploy |

**Why it matters for this role:** the release engineer is the person who *configures the org so
that releases are safe*. Administrator II is the exam for that configuration vocabulary. In an
interview, "I set the deployment IP allowlist, I govern the integration user's permissions, I own
the sandbox refresh and masking checklist" is an Administrator II answer.

---

## 4. Salesforce Certified Platform App Builder — curriculum

**Purpose:** "design, build, and deploy custom applications using the declarative customization
capabilities of the Salesforce Platform."

| Domain | Relevance |
|---|---|
| **Object and Field Design** | Custom objects, fields, validation rules |
| **Security** | Profiles, permission sets, sharing — the declarative half of the conflict clinic |
| **Flow** | Before/after-save flows, record-triggered flows, the version trap |
| **Page Layouts and UI** | Layouts, Lightning record pages, the record-type → layout assignment chain |
| **App Design and Customisation** | Apps, tabs, Lightning pages, sharing |
| **Data and Analytics** | Reports, dashboards, data import/export |
| **Packaging and Deployment** | Unlocked packages, deployment options, change sets — **directly on the JD** |

**This is the fastest high-value credential for a release engineer**, because most of what a
release engineer reviews, retrieves and deploys is declarative metadata, and the exam already
contains a packaging-and-deployment domain.

---

## 5. Other credentials worth naming in an interview

| Credential | Why it is worth mentioning |
|---|---|
| **Salesforce Certified Architect — Associate / Professional** | Systems design: environments, integration, identity. Speaks directly to "DevOps friendly design patterns" and platform boundaries (the unlocked-package decision) |
| **Salesforce Certified Identity and Access Management Designer** | The deploy identity, connected apps, certificate-based auth, secret management — the exact controls a regulated bank will probe |
| **Salesforce Certified Marketing / Sales Cloud / Service Cloud Consultant** | Domain credibility in Commercial Banking (Sales Cloud is the likely core) |

---

## 6. "DevOps related certs" — the vendor credentials

### 6.1 Gearset Academy Certification

| Attribute | Detail |
|---|---|
| Provider | Gearset, delivered through **DevOps Launchpad** |
| Audience | Admins, developers, architects and release managers |
| Coverage | The full Salesforce DevOps lifecycle: **deployments, automation, backup**, plus version control, CI/CD, release management, sandbox seeding, CPQ and Salesforce backup strategies |
| Format | Guided modules with practical work in the app; a practical certification |
| Link | <https://devopslaunchpad.com/courses/gearset-academy-certification/> |
| Fit for this JD | **Strongest** match: the JD explicitly names Gearset first, and the certification's scope (compare, deploy, pipeline, backup, masking) is the JD's scope |

### 6.2 Copado Certified

| Attribute | Detail |
|---|---|
| Provider | Copado |
| Entry point | Copado Success certification guides (<https://success.copado.com/s/certification-guides>) and credential validation (<https://success.copado.com/s/validate-credentials>) |
| Scope | Pipelines, user stories, promotions, deployments, compliance, Copado Robotic Testing |
| Caution | The enterprise product naming changed (**Agentia Pipeline / Agentia Pipeline Pro**). A certification earned years ago may refer to `Copado Deployer` or the Metadata Pipelines product. Check the current certification catalogue rather than naming a tier from memory |
| Fit for this JD | Strong for the governance half: compliance rules, quality gates, promotion and back-promotion |

### 6.3 AutoRABIT Academy

| Attribute | Detail |
|---|---|
| Provider | AutoRABIT |
| Entry point | <https://academy.autorabit.com/> — publishes an **ARM Core Track**, ARM Professional/Admin certification tracks, and a **Tier One ARM Certification Exam** |
| Scope | ARM (CI/CD, pipelines, approvals, release labels), Vault (backup, data masking), CodeScan (SAST) |
| Caution | Confirm which UI generation the curriculum targets — **ARM classic vs ARM New UI** have different screens and different feature flags |
| Fit for this JD | Strong for the data half: masking and backup are a named JD responsibility, and AutoRABIT is deepest there |

### 6.4 How to answer "do you have a DevOps certification?"

> "There is no Salesforce-branded DevOps certification. On the Salesforce side I hold Platform
> Developer and Platform Administrator II, because the content I release is Apex, Flow, security and
> deployment settings. On the tooling side I hold the vendor credential — [Gearset Academy / Copado
> Certified / AutoRABIT ARM] — because that is where the pipeline, compliance and masking product
> knowledge lives. What I would not do is list a tool cert and imply it covers release engineering;
> the runbooks, the rollback model and the audit pack are what I actually bring."

---

## 7. Which credentials matter for which interview question

| Interview question | Credential that helps most | Why |
|---|---|---|
| "Explain the deployment test level and coverage rules" | PD1 (Apex Testing) + Debug and Deployment module | It is literally the exam content |
| "How do you resolve a profile conflict?" | PD1 (Security) + App Builder (Security) | Profiles, permission sets, permission set groups |
| "What org settings govern deployment?" | Administrator II (Setup and Maintenance, Configuration and Setup) | Deployment settings, session policies, sandboxes |
| "How do you design package boundaries?" | App Builder (Packaging and Deployment) + Architect Associate | Unlocked packages, dependency boundaries |
| "How do you authenticate a pipeline?" | Identity and Access Management Designer | Connected apps, certificates, secrets, scopes |
| "Which tool would you pick for masking and backup?" | AutoRABIT ARM/Vault cert | It is the product knowledge |
| "How do you prove a release was controlled?" | Administrator II + the vendor compliance features | Compliance rules, quality gates, evidence |

---

## 8. Certification-maintenance reality

Salesforce credentials require **maintenance** to stay active — a periodic exam or a set of
Trailhead units. Two practical consequences:

1. **A certification you let lapse is a claim you should not make.** Check the maintenance status
   on the Salesforce credential verification page before putting it on a résumé.
2. **The material changes.** The Deployment Settings and DevOps Center surfaces change. If the
   certification is recent but the org is old, or vice versa, trust the org.

---

## 9. Unverified / open items

| Item | Status | How to confirm |
|---|---|---|
| Exact current exam-question count, duration, pass mark and retake allowance for PD1 / Administrator II | Not re-verified on the exam page (the exam pages are behind the Trailhead Academy app) | The exam page linked from each credential page: <https://trailheadacademy.salesforce.com/certificate/exam-platform-dev1---Plat-Dev-201> and `.../exam-platform-admin2---Plat-Admn-301` |
| Exact per-domain weightings for the PD1 and Administrator II exam outlines | The Trailhead study-guide trails render client-side; the weights were not retrievable as text | Open the study-guide trail in a browser: <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide> and `.../platform-administrator-certification-study-guide` |
| Current Copado certification catalogue names | The certification-guide index is behind a Salesforce Knowledge render | <https://success.copado.com/s/certification-guides> |
| Current AutoRABIT ARM certification track names | The academy site is a dynamic storefront | <https://academy.autorabit.com/> |
| Whether a "Salesforce Certified Release Manager" credential exists | **Not found** in the credential catalogue; no evidence of such a credential | <https://trailhead.salesforce.com/credentials> |
