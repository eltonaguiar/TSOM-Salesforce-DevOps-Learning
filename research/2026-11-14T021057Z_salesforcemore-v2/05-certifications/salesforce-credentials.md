# Salesforce credential curricula

**Merge target:** the Certifications section of the downstream page. This is the research behind the study order and the "what does the exam actually cover?" answer.

**Caveat.** Salesforce updates exam guides with each release. The domain names below are the stable structure; the weights and the exact topic list change. Fetch the current official exam guide PDF before you publish a percentage. Do not study from exam dumps.

## 1. Salesforce Certified Platform Developer I (PD1)

**Official page:** <https://trailhead.salesforce.com/credentials/platformdeveloperi>
**Study trail:** <https://trailhead.salesforce.com/content/learn/trails/platform-developer-i-certification-study-guide>

### 1.1 What the credential is for

The PD1 is the developer foundation: Apex, triggers, SOQL/SOSL, testing, the UI layer, and the debug/deployment tools. It is the credential the posting names explicitly.

### 1.2 Curriculum domains

| Domain | What it covers | Why a release engineer cares |
|---|---|---|
| Salesforce Fundamentals | Platform architecture, multi-tenancy, the data model, the MVC pattern, the development lifecycle | Explains why governor limits exist and why metadata is compiled against the target |
| Data Modeling and Management | Objects, fields, relationships, schema design, SOQL/SOSL, DML | The metadata you deploy; the queries that hit limits |
| Process Automation and Logic | Apex classes, triggers, interfaces, asynchronous Apex, exception handling, order of execution | The bulkification and dependency risks you review |
| User Interface | Lightning components, Visualforce, Lightning Web Components, page layouts | The UI metadata that deploys and the activation that does not |
| Testing | Test classes, assertions, test data, coverage, `Test.startTest()` | The production gate and the reason a green Dev test is not enough |
| Debug and Deployment Tools | Debug logs, checkpoints, the Developer Console, the CLI, change sets, Metadata API | The daily tools of this role |

### 1.3 Study emphasis for this role

- Trigger order of execution and recursion.
- Bulkification at 200 and 10,000 records.
- Writing tests that create their own data.
- `sf` CLI retrieve/deploy/test.
- Reading a deploy error and mapping it to a missing dependency.

### 1.4 Exam logistics (verify current)

- Register through Trailhead Academy / Salesforce Credentialing.
- Typical format: about 60 questions, about 105 minutes, multiple choice and multiple select.
- Passing score varies by exam; use the current exam guide.
- Plan for maintenance modules each release cycle.

## 2. Salesforce Certified Platform App Builder

**Official page:** <https://trailhead.salesforce.com/credentials/platformappbuilder>
**Study trail:** <https://trailhead.salesforce.com/content/learn/trails/prepare-for-your-salesforce-platform-app-builder-certification>

### 2.1 What the credential is for

Declarative application design: objects, fields, security, automation, UI, and app deployment. It is the best certificate for the metadata a DevOps engineer moves every week.

### 2.2 Curriculum domains

| Domain | What it covers | Why a release engineer cares |
|---|---|---|
| Salesforce Fundamentals | Platform capabilities, the app model, the declarative vs programmatic boundary | Explains what can be built without code and what must be deployed |
| Data Modeling and Management | Objects, fields, relationships, schema, data quality | The parent/child dependencies that break deploys |
| Security | Profiles, permission sets, OWD, role hierarchy, sharing, field-level security | The access diff you must review before production |
| Business Logic and Process Automation | Validation rules, Flow, approval processes, formula fields | The automation that does not merge and the Flow activation trap |
| User Interface | Lightning apps, pages, layouts, record types, Dynamic Forms | The layout/assignment/page-activation distinction |
| App Deployment | Change sets, packages, the deployment lifecycle | The transition from declarative build to release engineering |

### 2.3 Study emphasis for this role

- Permission sets vs profiles.
- Record types, page layouts, and Lightning page activation.
- Flow before-save vs after-save.
- Deployment options and their limits.

## 3. Salesforce Certified Platform Administrator

**Official page:** <https://trailhead.salesforce.com/credentials/platformadministrator>

### 3.1 What the credential is for

The baseline administrator credential: configuration, security, data, automation, and the standard applications. Platform Administrator II requires it (per the credential page).

### 3.2 Curriculum domains

| Domain | What it covers |
|---|---|
| Configuration and Setup | Org settings, company information, UI settings, app configuration |
| Object Manager and Lightning App Builder | Objects, fields, page layouts, Lightning pages, record types |
| Sales and Marketing Applications | Leads, opportunities, campaigns, products, price books |
| Service and Support Applications | Cases, queues, entitlements, service contracts, knowledge |
| Productivity and Collaboration | Activities, Chatter, groups, files |
| Data and Analytics Management | Import/export, data quality, reports, dashboards |
| Automation | Validation rules, Flow, approval processes, escalation rules |
| Security and Access | Profiles, permission sets, roles, OWD, sharing rules, login policies |

### 3.3 Study emphasis for this role

- Security and access (the permission diff).
- Automation (the Flow/validation-rule conflicts).
- Data management (the data-vs-metadata boundary).
- Configuration and setup (the org properties that do not deploy).

## 4. Salesforce Certified Platform Administrator II (formerly Advanced Administrator)

**Official page:** <https://trailhead.salesforce.com/credentials/platformadministrator-ii>
**Prerequisite:** Salesforce Certified Platform Administrator.

### 4.1 What the credential is for

Advanced administration: complex security, objects and fields, automation, data management, analytics, and environment management/deployment. It is the closest Salesforce credential to release engineering.

### 4.2 Curriculum domains

| Domain | What it covers | Why a release engineer cares |
|---|---|---|
| Security and Access | Advanced sharing, restriction rules, permission set groups, login policies, session settings | The access changes that a deploy can widen |
| Objects and Fields | Complex schema, relationships, field-level security, record types | The dependency graph |
| Automation | Advanced Flow, approvals, escalation, order of execution | The automation that does not merge and the bulk failures |
| Data Management | Data import/export, duplicate management, data quality, large data volumes | The data-vs-metadata boundary and masking |
| Analytics | Reports, dashboards, reporting snapshots | Usually out of scope for releases, but part of the admin model |
| Environment Management and Deployment | Sandboxes, change sets, packages, deployment tools, release management | The posting's core |
| Sales and Marketing Applications | Advanced sales configuration | Domain context |
| Service and Support Applications | Advanced service configuration | Domain context |
| Productivity and Collaboration | Advanced collaboration features | Domain context |

### 4.3 Study emphasis for this role

- Environment management and deployment (the direct overlap).
- Advanced security (the permission diff).
- Advanced automation (the conflict clinic).
- Sandboxes and data management (refresh and masking).

## 5. Platform Developer II (optional, not named)

**Official page:** <https://trailhead.salesforce.com/credentials/platformdeveloperii>

PD2 goes deeper into Apex, integration, performance, and the development lifecycle. It is not required by the posting, but it is the natural next step for a developer-heavy DevOps engineer. Mention it as optional.

## 6. What the exams do not cover

- Gearset, Copado, or AutoRABIT UI.
- A specific bank's change-management process.
- GitHub Actions or Azure DevOps YAML.
- Data masking product operations.

Those come from hands-on labs and vendor training, not the Salesforce exams. The page should say so.

## 7. What to merge

**Merge:** the domain tables, the "study emphasis" bullets, and the "what the exams do not cover" note.

**Do not merge:** exact question counts, time limits, or passing scores without the current official exam guide. Use "typically" and link the official page.
