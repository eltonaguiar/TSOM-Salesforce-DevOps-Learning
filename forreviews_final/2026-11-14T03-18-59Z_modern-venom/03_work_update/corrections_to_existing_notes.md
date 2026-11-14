# Corrections to existing research notes

These are factual fixes to artifacts already published under
`forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/` on `main`. They are listed here rather than applied
in place so the concurrent agent working the same review does not collide.

## 1. `certifications.md` — credentials that do not exist

The certification table lists two credentials Salesforce does not issue:

| In the artifact | Reality |
|-----------------|---------|
| "Salesforce Apex Developer" | Not a credential. The code credentials are **Platform Developer I** and **Platform Developer II**. |
| "LWC Developer" | Not a credential. The LWC credential is **JavaScript Developer I**. |
| "ServiceNow Certified Salesforce Admin" | Does not exist. ServiceNow does not certify Salesforce administrators. |

### Corrected table

| Level | Credential | Focus |
|-------|------------|-------|
| Entry | Salesforce Administrator | Core CRM ops, security, sandboxes, change sets |
| Entry | Platform App Builder | Declarative app development, objects, Flow, security |
| Intermediate | **Platform Developer I** | Apex, tests, triggers, the platform model you deploy |
| Intermediate | **JavaScript Developer I** | LWC and Lightning platform UI |
| Advanced | **Platform Developer II** | Advanced Apex, integration, performance |
| Advanced | **Platform Administrator II** | The renamed "Advanced Admin" — security, change, environments |
| Specialist | Service Cloud / Sales Cloud Consultant | Product-specific consulting |
| Vendor | Copado / Gearset / AutoRABIT certificates | Tool time only; do not replace PD1 |

There is **no official Salesforce "DevOps Engineer" certification**. The posting's "DevOps related certs"
means the vendor certificates plus PD1.

## 2. `crash_course.md` — gaps against its own source

The note is a faithful paraphrase but omits four sections the source guide treats as load-bearing. Add them:

1. **Integration types table** — REST, SOAP, Bulk (1.0 SOAP/CSV vs 2.0 REST/JSON), Streaming (CometD/Pub-Sub),
   Outbound Message, Named Credentials, External Credentials. The note mentions REST/SOAP only.
2. **Named Credentials vs Remote Site Settings** — the note should state that a Named Credential removes the
   Remote Site Setting requirement for a callout.
3. **"Other limits to know"** — Apex code size (1M characters), mass email daily limit, scheduled Apex jobs
   (100 per org), Batch Apex default 200 / max 2,000, Flow interview limits. The note stops at the five big
   ones.
4. **Official learning resources** — the Trailhead trail links, developer docs, and YouTube channels. The note
   references Trailhead generically but carries no links.

## 3. `key_principles.md` — one wording fix

Principle 4 lists the five governor limits correctly. One addition worth making: the principle says "SOQL
queries: 100 per transaction (sync)" but does not mention that asynchronous transactions get **200** SOQL
queries. Learners frequently overcorrect by assuming 100 everywhere.

## 4. `research_index.md` — status update

Once the four notes in this bundle are folded in, update the index:

| Document | Old status | New status |
|----------|-----------|------------|
| `devops_release_engineering.md` | ⏳ Pending | ✅ Complete |
| `navigation_breadcrumbs.md` | ⏳ Pending | ✅ Complete |
| `labs_design.md` | ⏳ Pending | ✅ Complete (with corrections) |
| `user_management_data.md` | ⏳ Pending | ✅ Complete |

Also update the "Research Status Tracker" table and the Phase 2 / Phase 3 progress blocks, which still show
the DevOps specialization as untouched.
