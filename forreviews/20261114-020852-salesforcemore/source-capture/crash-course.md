# Source Capture — Salesforce Crash Course
**Source URL:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/crash-course/
**Agent:** opencode | **Date:** 2026-11-10
**Platform:** Salesforce | **Audience:** Complete beginners
**Confidence:** high

## Contents
- What Is Salesforce?
- The Big Picture: Objects, Records, Fields
- Navigation: Where Things Live
- Users, Profiles, Roles & Security
- Data Integrity & Relationships
- Automation: Flow, Process Builder, Workflow
- Code: Apex, Visualforce, LWC
- Integration: APIs & External Systems
- Troubleshooting & Performance
- Governor Limits Deep Dive
- Design Considerations
- Out-of-the-Box Features to Know
- Official Salesforce Learning Resources
- Quick Start Checklist

## What Is Salesforce?
Salesforce is a cloud-based Customer Relationship Management (CRM) platform. Everything lives in one place so sales, service, and marketing teams all see the same customer data.
**ELI5 analogy:** A school where every student has one folder with grades, attendance, parent contact info, and teacher notes. Every teacher opens the same folder. Salesforce is that folder system for businesses and customers.

## The Big Picture: Objects, Records, Fields

| Layer | What It Is | Real-World Example |
|-------|-----------|-------------------|
| Object | A type of thing you track (table) | Account, Contact, Opportunity, Case |
| Record | One specific instance (row) | “Acme Corp” (an Account record) |
| Field | One piece of data (column) | Phone number, Industry, Annual Revenue |

### Standard vs Custom Objects
- **Standard Objects:** Account, Contact, Lead, Opportunity, Case, User
- **Custom Objects:** Built for business needs (e.g., “Property Listing,” “Course Enrollment”)

## Navigation: Where Things Live

| Task | Breadcrumb Path |
|------|-----------------|
| Home / Dashboard | Home tab |
| App Launcher | App Launcher (9-dot grid) > [App Name] |
| Object Manager | Setup > Object Manager > [Object Name] |
| Fields & Relationships | Setup > Object Manager > [Object] > Fields & Relationships |
| Page Layouts | Setup > Object Manager > [Object] > Page Layouts |
| Profiles | Setup > Profiles > [Profile Name] |
| Permission Sets | Setup > Permission Sets > [Permission Set Name] |
| Roles | Setup > Roles > Roles |
| Users | Setup > Users > Users |
| Flows | Setup > Flows |
| Apex Classes | Setup > Apex Classes |
| Visualforce Pages | Setup > Visualforce Pages |
| Lightning Components (LWC) | Setup > Lightning Components |
| Remote Site Settings | Setup > Remote Site Settings |
| Named Credentials | Setup > Named Credentials |
| Connected Apps | Setup > App Manager > Connected Apps |
| Debug Logs | Setup > Debug Logs |
| Optimizer | Setup > Optimizer |

## Users, Profiles, Roles & Security

### Users
A User needs: username (email format), a profile, a role (optional), a license.

| License Type | What It’s For |
|-------------|---------------|
| Salesforce | Full CRM access |
| Salesforce Platform | Custom apps, no standard CRM objects |
| Chatter Free | Collaboration only |
| External Identity | Customers/partners via Experience Cloud |

### Profiles
Controls what a user can see and do: object permissions, field permissions, page layouts, apps/tabs, login hours, IP ranges.
**Best practice:** Don’t give everyone System Administrator. Least permissive profile.

### Permission Sets
Grant additional access on top of a profile. Use instead of creating a new profile for every small exception.
**Example:** Sales user needs edit access to custom “Commission” object → assign “Commission Edit” Permission Set.

### Roles
Control record-level sharing. Roles form a hierarchy — higher roles see records owned by lower roles.

| Concept | Controls |
|---------|----------|
| Profiles | What you can do (object/field level) |
| Permission Sets | Extra access beyond profile |
| Roles | Which records you can see (org-wide sharing + hierarchy) |
| Org-Wide Defaults | Baseline record visibility (Private, Public Read Only, Public Read/Write) |

## Data Integrity & Relationships

| Relationship | What It Means | Example |
|-------------|---------------|---------|
| Lookup | Loose association; child can exist without parent | Case → Account |
| Master-Detail | Tight association; child cannot exist without parent; deleting parent deletes child | Opportunity → Opportunity Line Item |
| Hierarchical | Self-lookup on User (manager) | User → Manager |

### Roll-Up Summary Fields (Master-Detail only)
| Type | What It Does |
|------|--------------|
| SUM | Adds up a number field from all children |
| COUNT | Counts child records |
| MIN / MAX | Smallest/largest value among children |

### Data Integrity Best Practices
- Required fields — prevent missing critical data
- Unique fields — prevent duplicates (e.g., email)
- Validation rules — block bad data at save time
- Dependent picklists — valid combinations (Country → State)
- Record types — different page layouts and picklist values by business process

## Automation: Flow, Process Builder, Workflow

| Flow Type | When It Runs | Use Case |
|-----------|-------------|----------|
| Screen Flow | User clicks a button | Guided data entry, wizard forms |
| Record-Triggered Flow | Record created/updated | Auto-update fields, create related records |
| Scheduled-Triggered Flow | On a schedule | Nightly cleanup, batch emails |
| Platform Event Flow | Event received | React to external events |

Flow replaces Workflow Rules and Process Builder (both retiring).

### When to Code vs. Flow
| Use Flow | Use Apex |
|----------|----------|
| Field updates, record creation | Complex logic with loops and collections |
| Simple email alerts | Callouts to external APIs |
| UI screens for data entry | Bulk processing of 10,000+ records |
| | Approval processes |
| | Custom calculations beyond formula fields |

## Code: Apex, Visualforce, LWC

### Apex
Salesforce’s proprietary language (Java-like), server-side.

| Concept | What It Is | Example |
|---------|-----------|---------|
| Class | Container for methods/logic | `public class CaseHandler { ... }` |
| Trigger | Runs before/after record save | `trigger CaseTrigger on Case (before insert) { ... }` |
| SOQL | Salesforce Object Query Language | `SELECT Id, Name FROM Account WHERE Industry = 'Technology'` |
| DML | Data Manipulation Language | `insert newCase;` |
| Governor Limits | Runtime limits | 100 SOQL queries/transaction, 10,000 records per DML |

### Visualforce
Older UI framework (HTML-like tags with Apex controllers). Used for custom PDF rendering, precise layout control, legacy pages.

### Lightning Web Components (LWC)
Modern UI framework (JavaScript + HTML). Standard for custom UI in Lightning Experience.

| File | Purpose |
|------|---------|
| component.js | Logic (wire services, event handlers, Apex calls) |
| component.html | UI template (Lightning Design System) |
| component.js-meta.xml | Configuration (where component can be used) |

### When to Use Each
| Technology | Best For |
|------------|----------|
| Flow | Simple automation, no-code preferred |
| Apex | Complex logic, bulk data, API callouts, triggers |
| Visualforce | PDF generation, legacy pages, precise layout |
| LWC | Custom UI, Lightning pages, components |

## Integration: APIs & External Systems

| Integration Type | Protocol | Use Case |
|-----------------|----------|----------|
| REST API | REST/JSON | Modern web/mobile integrations, real-time data |
| SOAP API | SOAP/XML | Legacy enterprise systems |
| Bulk API | REST/CSV | Loading millions of records |
| Streaming API | CometD/Pub-Sub | Real-time notifications |
| Outbound Message | SOAP | Send data to external system on record change |
| Named Credentials | — | Securely store endpoint URLs and auth |
| Named Credentials + External Credentials | — | OAuth 2.0 for external auth |

### Named Credentials (Best Practice)
Instead of hardcoding URL/password in Apex:
```
// BAD
req.setEndpoint('https://api.example.com/data');
// GOOD
req.setEndpoint('callout:MyExternalAPI/data');
```
**Remote Site Settings** required before callouts (unless using Named Credentials).

## Troubleshooting & Performance

| Symptom | Where to Check |
|---------|----------------|
| Apex not running as expected | Setup > Debug Logs (trace flags on users) |
| Flow errors | Setup > Flow > [Flow] > Debug / Fault paths |
| Record not saving | Setup > Object Manager > [Object] > Validation Rules |
| User can’t see a field | Setup > Profiles > [Profile] > Field-Level Security |
| Slow page load | Setup > Optimizer > Page Load Performance |
| API callout failing | Setup > Remote Site Settings / Named Credentials |
| Governor limit exceeded | Debug Logs show which limit was hit |

### Debug Logs
1. Setup > Debug Logs > New
2. Select user to trace, set expiration and log level (Finest)
3. Perform action, download and read log

## Governor Limits Deep Dive

Salesforce is multi-tenant; limits guarantee fair resource usage. Exceeding a limit throws `LimitException`.

### 1. SOQL Queries — 100 per Transaction (Sync)
**Why:** Every query hits the database (most expensive resource). **Violation:** Querying inside a `for` loop.
**Fix:** Collect IDs first, query once, process in memory (bulkify). Use selective queries on indexed fields. Assume `Trigger.new` can have 200 records.

### 2. DML Rows — 10,000 per Transaction
**Why:** Writing records locks rows/writes to disk. **Violation:** `insert`/`update` inside a loop.
**Fix:** Collect records into a list, one DML call on the whole list.

### 3. Heap Size — 6 MB Sync / 12 MB Async
**Why:** Memory hogging starves other tenants. **Fix:** Query only needed fields, use LIMIT, process large volumes async, null out unused variables.

### 4. Callouts — 100 per Transaction
**Why:** Callouts are slow, tie up threads. **Violation:** Callout inside a loop.
**Fix:** Named Credentials, async callouts (`@future(callout=true)`, Queueable, Batch), batch external requests.

### 5. CPU Time — 10,000 ms Sync / 60,000 ms Async
**Why:** CPU shared across tenants. **Fix:** Avoid nested loops, use Maps for lookups, minimal trigger logic, delegate to helper classes.

### 6. Other Limits
| Limit | Default | Context |
|-------|---------|---------|
| Apex classes/triggers | 1 million characters | Code size |
| Test methods | 75%+ coverage | Deployment requires coverage |
| Email (single) | 5,000/day | Messaging.SingleEmailMessage |
| Email (mass) | 10/day | Messaging.MassEmailMessage |
| Scheduled jobs | 100 concurrent | @future, Queueable, Batch |
| Batch Apex batch size | 200 default | Max 2,000 records per batch |

### Monitoring Limits
**Debug Logs:** Setup > Debug Logs > New > Finest level > run operation > search `FATAL_ERROR` / `System.LimitException`.
**Apex Limits class:**
```
Integer queriesUsed = Limits.getQueries();
Integer queriesLimit = Limits.getLimitQueries();
```

## Design Considerations

| Question | Why It Matters | Where to Decide |
|----------|---------------|-----------------|
| Can Flow do this instead of code? | Flows easier to maintain, no test classes | Setup > Flows |
| Will this scale to 100K+ records? | Governor limits apply; bulkify | Apex design |
| Who needs to see/edit this data? | Profiles, roles, OWD, sharing, FLS | Setup > Security |
| Is this data sensitive? | FLS, encryption, Shield | Setup > Security |
| What if external API is down? | Error handling, retry, fallback | Apex exception handling |
| Will users adopt this? | UI simplicity, Lightning Design System | Lightning App Builder |
| How will this be deployed? | Change sets, CLI, CI/CD, sandbox strategy | Setup > Deploy |

### Code Design Patterns
| Pattern | When to Use | Example |
|---------|-------------|---------|
| Bulkification | Always — triggers handle multiple records | Process Trigger.new as a list |
| Trigger Framework | Multiple triggers on same object | One trigger per object, delegate to handlers |
| Selector Layer | Reusing SOQL queries | ProjectsSelector.getByStatus('Active') |
| Domain Layer | Business logic per object | ProjectsDomain.setDefaultStatus() |
| Service Layer | Cross-object logic | ProjectService.createProjectWithTasks() |
| Async Processing | Long-running operations | @future, Queueable, Batch Apex |

### Security Design
| Consideration | Implementation |
|--------------|----------------|
| Least privilege | Profiles = minimum; Permission Sets = extras |
| with sharing | Apex respects sharing by default; without sharing only when necessary |
| CRUD/FLS checks | Check Schema.isAccessible() before DML |
| SOQL injection | Use bind variables (:variable), never string concatenation |
| Named Credentials | Never hardcode passwords/tokens |
| Apex test data | Create test data in @isTest; use @testSetup |

## Out-of-the-Box Features to Know

| Feature | What It Does | Where |
|---------|-------------|-------|
| Record Types | Different page layouts, picklists, business processes per object | Setup > Object Manager > [Object] > Record Types |
| Formula Fields | Read-only calculated fields (no code) | Setup > Object Manager > [Object] > Fields > Formula |
| Roll-Up Summary | Aggregate child records on parent (Master-Detail only) | Setup > Object Manager > [Parent] > Fields |
| Validation Rules | Block invalid data at save | Setup > Object Manager > [Object] > Validation Rules |
| Approval Processes | Multi-step approval with email | Setup > Approval Processes |
| Sandboxes | Isolated copies for dev/test | Setup > Sandboxes |
| Change Sets | Move config between orgs | Setup > Deploy > Change Sets |
| Salesforce CLI | Command-line development | developer.salesforce.com/tools/sfdxcli |
| Developer Console | Built-in IDE | Gear menu > Developer Console |

## Official Salesforce Learning Resources

### Trailhead Trails
| Trail | What You’ll Learn | Link |
|-------|------------------|------|
| Admin Beginner | Objects, fields, users, security, automation | trailhead.salesforce.com/trails/sfx_admin_beginner |
| Developer Beginner | Apex, Visualforce, LWC basics | trailhead.salesforce.com/trails/sfx_dev_beginner |
| Data Management | Import, export, data quality, Dataloader | trailhead.salesforce.com/trails/data_management |
| Integration | APIs, Named Credentials, callouts | trailhead.salesforce.com/trails/apex_integration_services |
| Lightning Web Components | Build modern UI | trailhead.salesforce.com/trails/lightning_web_components_basics |
| Security | Profiles, roles, sharing, field-level security | trailhead.salesforce.com/trails/force_com_security |

### Official Documentation
| Resource | What It Covers | Link |
|----------|---------------|------|
| Salesforce Help | End-user and admin docs | help.salesforce.com |
| Salesforce Developer Docs | Apex, Visualforce, LWC, APIs | developer.salesforce.com/docs |
| Apex Developer Guide | Apex language, triggers, governor limits | developer.salesforce.com/docs/atlas.en-us.apexcode |
| LWC Developer Guide | Lightning Web Components | developer.salesforce.com/docs/component-library/lwc |
| Salesforce CLI | Command-line tool | developer.salesforce.com/tools/sfdxcli |

### Quick Start Checklist (First Week)
- Create free Salesforce Developer Org (developer.salesforce.com/signup)
- Complete Trailhead “Admin Beginner” trail
- Complete Trailhead “Developer Beginner” trail
- Create custom object with fields and relationships
- Build a Record-Triggered Flow
- Write simple Apex trigger and test class
- Build basic LWC component
- Set up Named Credentials and make a REST callout
- Review Debug Logs for a failed operation
- For DevOps/release role, continue with DevOps Engineer training track
