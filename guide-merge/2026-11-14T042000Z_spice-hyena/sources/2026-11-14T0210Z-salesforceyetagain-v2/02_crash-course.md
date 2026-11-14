# Salesforce Crash Course

**Worktree:** salesforceyetagain-v2  
**Date:** 2026-11-14T02:10Z  
**Source:** Salesforce Technical Training — ELI5 Crash Course (agent: opencode, 2026-11-10)  
**Related pages:**
- Navigation & Breadcrumbs: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/navigation-breadcrumbs/
- Labs & Design: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/
- User Management & Data: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/user-management-data/
- DevOps & Release Engineering: https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/devops-engineer/

Prerequisite per the DevOps track: do this crash course first if Apex, Flow, profiles, and permission sets are still fuzzy.

---

## Navigation & Breadcrumbs

Salesforce uses **Setup** for administration and **App Launcher** for end users.

### App Launcher & Home

| Task | Path |
|---|---|
| Home dashboard | Home |
| All apps | App Launcher (9-dot grid, top-left) |
| Switch apps | App Launcher > [App Name] |
| User profile & settings | Click avatar (top-right) > Settings |
| Switch to Setup | Click avatar > Setup |

### Setup navigation tree

Gear menu (⚙️) > **Setup** opens the left-hand navigation panel.

| Task | Path |
|---|---|
| Users | Setup > Users > Users |
| Profiles | Setup > Profiles |
| Permission Sets | Setup > Permission Sets |
| Roles | Setup > Roles |
| Permission Set Groups | Setup > Permission Set Groups |
| Sharing Settings | Setup > Sharing Settings |
| Field-Level Security | Setup > Object Manager > [Object] > Fields & Relationships > [Field] > Set Field-Level Security |

### Object & Field Configuration

| Task | Path |
|---|---|
| Object Manager home | Setup > Object Manager |
| View/edit an object | Setup > Object Manager > [Object Name] |
| Create custom object | Setup > Object Manager > Create > Custom Object |
| Fields & Relationships | Setup > Object Manager > [Object] > Fields & Relationships |
| Create custom field | Setup > Object Manager > [Object] > Fields & Relationships > New |
| Page Layouts | Setup > Object Manager > [Object] > Page Layouts |
| Record Types | Setup > Object Manager > [Object] > Record Types |
| Validation Rules | Setup > Object Manager > [Object] > Validation Rules |

### Security & Access

| Task | Path |
|---|---|
| Profiles | Setup > Profiles > [Profile Name] |
| Permission Sets | Setup > Permission Sets > [Permission Set Name] |
| Roles | Setup > Roles > Roles |
| Sharing Settings (OWD) | Setup > Sharing Settings |
| Field-Level Security | Setup > Object Manager > [Object] > Fields & Relationships > [Field] > Set Field-Level Security |
| Connected Apps (OAuth) | Setup > App Manager > Connected Apps |
| Named Credentials | Setup > Named Credentials |

### Automation

| Task | Path |
|---|---|
| Flow Builder home | Setup > Flows |
| Create new flow | Setup > Flows > New Flow |
| Approval Processes | Setup > Approval Processes |
| Email Templates | Setup > Email Templates |
| Outbound Messages | Setup > Outbound Messages |

### Development (Code)

| Task | Path |
|---|---|
| Apex Classes | Setup > Apex Classes |
| Triggers | Setup > Apex Triggers |
| Visualforce Pages | Setup > Visualforce Pages |
| Lightning Components (LWC/Aura) | Setup > Lightning Components |
| Anonymous Apex | Developer Console > Debug > Open Execute Anonymous Window |
| Developer Console | Gear menu (⚙️) > Developer Console |
| Salesforce CLI | Command line: `sf` (formerly `sfdx`) |

### Integration

| Task | Path |
|---|---|
| Remote Site Settings | Setup > Remote Site Settings |
| Named Credentials | Setup > Named Credentials |
| External Credentials | Setup > External Credentials |
| Connected Apps | Setup > App Manager > Connected Apps |
| External Data Sources | Setup > External Data Sources |
| Platform Events | Setup > Platform Events |

### Deployment & DevOps

| Task | Path |
|---|---|
| Sandboxes | Setup > Sandboxes |
| Change Sets | Setup > Deploy > Change Sets |
| Deployment Status | Setup > Deploy > Deployment Status |
| Sandbox Templates | Setup > Sandboxes > Sandbox Templates |
| Apex Test Execution | Setup > Apex Test Execution |
| DevOps Center (if enabled) | Setup, search "DevOps Center" |
| Salesforce CLI | `sf project deploy start`, `sf project retrieve start` |

### Monitoring & Troubleshooting

| Task | Path |
|---|---|
| Debug Logs | Setup > Debug Logs |
| Trace Flags | Setup > Trace Flags |
| Apex Jobs | Setup > Apex Jobs |
| Optimizer | Setup > Optimizer |
| System Status | https://status.salesforce.com |

### Data Management

| Task | Path |
|---|---|
| Data Import Wizard | Setup > Data > Data Import Wizard |
| Data Loader | Download from Setup > Data > Data Loader |
| Export | Setup > Data > Export |
| Duplicate Rules | Setup > Duplicate Rules |

---

## Quick-reference Setup paths (every admin/dev task)

**Objects:** Setup > Object Manager > [Object] > Fields & Relationships > New  
**Security:** Setup > Profiles / Setup > Permission Sets / Setup > Sharing Settings  
**Automation:** Setup > Flows > New Flow  
**Code:** Setup > Apex Classes / Setup > Apex Triggers / Setup > Lightning Components  
**Integration:** Setup > Named Credentials / Setup > Remote Site Settings / Setup > App Manager > Connected Apps  
**Deployment:** Setup > Sandboxes / Setup > Deploy > Change Sets / `sf project deploy start`  
**Monitoring:** Setup > Debug Logs / Setup > Optimizer / Setup > Apex Test Execution  
**Data:** Setup > Data > Data Import Wizard / Setup > Data > Data Loader / Setup > Duplicate Rules  

Common "where is it" answers:
- Create a custom field: Setup > Object Manager > [Object] > Fields & Relationships > New
- Write Apex code: Setup > Apex Classes > New (or Developer Console)
- Make a field required: field definition > Required, or a Validation Rule
- See debug logs: Setup > Debug Logs
- Set up API access: Setup > Remote Site Settings or Setup > Named Credentials
- Add a user: Setup > Users > New User
- Build automation without code: Setup > Flows > New Flow

---

## Objects, records, fields

Salesforce organizes data in three layers:

| Layer | What it is | Real-world example |
|---|---|---|
| Object | A type of thing you track (table) | Account, Contact, Opportunity, Case |
| Record | One specific instance (row) | "Acme Corp" (an Account record) |
| Field | One piece of data (column) | Phone number, Industry, Annual Revenue |

**Standard vs Custom Objects**
- Standard Objects: come with Salesforce (Account, Contact, Lead, Opportunity, Case, User)
- Custom Objects: built for business needs (e.g., "Property Listing," "Course Enrollment")

---

## Users, profiles, roles & security

### Users

A User is a person who logs into Salesforce. Each user needs:
- A username (email format, unique across all Salesforce orgs)
- A profile
- A role (optional, for sharing)
- A license (determines what they can do)

### Profiles

A Profile controls what a user can see and do:
- Object permissions (read, create, edit, delete)
- Field permissions
- Page layouts
- Apps and tabs visible
- Login hours and IP ranges

**Best practice:** Don't give everyone "System Administrator." Use the least permissive profile that lets them do their job.

### Permission Sets

Permission Sets grant additional access on top of a profile. Use them instead of creating a new profile for every small exception. Permission Set Groups bundle multiple permission sets for a job function.

### Roles

Roles control record-level sharing (who can see which records). Roles form a hierarchy — people higher up can see records owned by people below them.

| Concept | Controls |
|---|---|
| Profiles | What you can do (object/field level) |
| Permission Sets | Extra access beyond profile |
| Roles | Which records you can see (org-wide sharing + hierarchy) |
| Org-Wide Defaults | Baseline record visibility (Private, Public Read Only, Public Read/Write) |

### License types

| License Type | What it's for |
|---|---|
| Salesforce | Full CRM access (sales, service, custom apps) |
| Salesforce Platform | Custom apps, no standard CRM objects |
| Chatter Free | Collaboration only |
| External Identity | Customers/partners logging in via Experience Cloud |

---

## Data integrity & relationships

### Relationship types

| Relationship | What it means | Example |
|---|---|---|
| Lookup | Loose association; child can exist without parent | Case → Account |
| Master-Detail | Tight association; child cannot exist without parent; deleting parent deletes child | Opportunity → Opportunity Line Item |
| Hierarchical | Self-lookup on User (manager) | User → Manager |

### Roll-Up Summary Fields

Only available on Master-Detail relationships. Automatically calculate values from child records on the parent: SUM, COUNT, MIN, MAX.

### Data integrity best practices

- Required fields prevent missing critical data
- Unique fields prevent duplicate records (e.g., email)
- Validation rules block bad data at save time
- Dependent picklists ensure valid combinations (Country → State)
- Record types give different page layouts and picklist values by business process

---

## Automation: Flow vs Apex vs Visualforce vs LWC

### Flow (modern standard)

Flow is Salesforce's no-code/low-code automation tool. It replaces Workflow Rules and Process Builder (both retiring).

| Flow Type | When it runs | Use case |
|---|---|---|
| Screen Flow | User clicks a button | Guided data entry, wizard forms |
| Record-Triggered Flow | Record created/updated | Auto-update fields, create related records |
| Scheduled-Triggered Flow | On a schedule | Nightly data cleanup, batch emails |
| Platform Event Flow | Event received | React to external system events |

### When to code vs. when to Flow

| Use Flow | Use Apex |
|---|---|
| Field updates, record creation | Complex logic with loops and collections |
| Simple email alerts | Callouts to external APIs |
| UI screens for data entry | Bulk processing of 10,000+ records |
| | Approval processes |
| | Custom calculations beyond formula fields |

### Code: Apex, Visualforce, LWC

**Apex** — Salesforce's proprietary server-side language (similar to Java). Concepts: Class, Trigger, SOQL, DML, Governor Limits.

**Visualforce** — older UI framework (HTML-like tags with Apex controllers). Still used for custom PDF rendering (quotes, invoices) and precise layout control.

**LWC** — modern UI framework (JavaScript + HTML). Standard for custom UI in Lightning Experience. Files: `component.js`, `component.html`, `component.js-meta.xml`.

| Technology | Best for |
|---|---|
| Flow | Simple automation, no-code preferred |
| Apex | Complex logic, bulk data, API callouts, triggers |
| Visualforce | PDF generation, legacy pages, precise layout |
| LWC | Custom UI, Lightning Experience pages |

---

## Integration: APIs & external systems

| Integration Type | Protocol | Use case |
|---|---|---|
| REST API | REST/JSON | Modern web/mobile integrations, real-time data |
| SOAP API | SOAP/XML | Legacy enterprise systems |
| Bulk API | REST/CSV | Loading millions of records |
| Streaming API | CometD/Pub-Sub | Real-time notifications when data changes |
| Outbound Message | SOAP | Send data to external system when record changes |
| Named Credentials | — | Securely store endpoint URLs and auth (no hardcoded passwords) |

### Named Credentials (best practice)

Instead of hardcoding a URL and password in Apex, use `callout:MyExternalAPI/data`. Named Credentials handle auth and bypass the Remote Site Settings requirement.

### Remote Site Settings

Before Salesforce can call an external API, add the external URL to Setup > Remote Site Settings. Not needed if using Named Credentials.

---

## Troubleshooting & performance

### Common issues & where to look

| Symptom | Where to check |
|---|---|
| Apex code not running as expected | Setup > Debug Logs (set trace flags on users) |
| Flow errors | Setup > Flow > [Flow] > Debug / Fault paths |
| Record not saving (validation rule) | Setup > Object Manager > [Object] > Validation Rules |
| User can't see a field | Setup > Profiles > [Profile] > Field-Level Security |
| Slow page load | Setup > Optimizer > Page Load Performance |
| API callout failing | Setup > Remote Site Settings / Named Credentials |
| Governor limit exceeded | Debug Logs show which limit was hit |

### Governor limits (Salesforce's "speed limits")

Salesforce runs on multi-tenant architecture. Governor limits guarantee fair resource usage.

| Limit | Default | What it means |
|---|---|---|
| SOQL queries | 100 per transaction | Don't query in a loop |
| DML rows | 10,000 per transaction | Bulkify your code |
| Heap size | 6 MB sync / 12 MB async | Don't load too much into memory |
| Callouts | 100 per transaction | Batch external API calls |
| CPU time | 10,000 ms sync / 60,000 ms async | Avoid inefficient loops |

**Bulkification example:** collect IDs first, query once, then process in memory — never query inside a `for` loop.

**Debug Logs:** Setup > Debug Logs > New > select user > set expiration and log level (Finest) > perform action > download and read.

---

## Design considerations

### Before you build

| Question | Why it matters |
|---|---|
| Can Flow do this instead of code? | Flows are easier to maintain; code requires test classes |
| Will this scale to 1M+ records? | Governor limits apply; bulkify everything |
| Who needs to see this data? | Roles, OWD, sharing rules affect design |
| What happens if the external system is down? | Error handling, retry logic, fallback behavior |
| Is this data sensitive? | Field-level security, encryption |
| Will users adopt this? | Keep UI simple, use Lightning Design System |

### Security design

- Least privilege: profiles get minimum access; Permission Sets add extras
- `with sharing` / `without sharing` keywords on Apex
- CRUD/FLS checks before DML
- SOQL injection: use bind variables, never string concatenation
- Named Credentials: never hardcode passwords or tokens

### Performance design

- Bulkify triggers (handle Trigger.new as a collection)
- Avoid SOQL in loops
- Use selective queries (filter on indexed fields)
- Asynchronous processing (@future, Queueable, Batch Apex) for long-running tasks

---

## Out-of-the-box features to know

| Feature | What it does | Where |
|---|---|---|
| Record Types | Different page layouts, picklists, business processes per object | Setup > Object Manager > [Object] > Record Types |
| Formula Fields | Read-only calculated fields (no code) | Setup > Object Manager > [Object] > Fields > Formula |
| Roll-Up Summary | Aggregate child records on parent (Master-Detail only) | Setup > Object Manager > [Parent] > Fields |
| Validation Rules | Block invalid data at save | Setup > Object Manager > [Object] > Validation Rules |
| Approval Processes | Multi-step record approval with email | Setup > Approval Processes |
| Sandboxes | Isolated copies for dev/test | Setup > Sandboxes |
| Change Sets | Move configuration between orgs | Setup > Deploy > Change Sets |
| Salesforce CLI | Command-line dev tool | developer.salesforce.com/tools/sfdxcli |
| Optimizer | Health check, recommends improvements | Setup > Optimizer |
| Platform Cache | Cache frequently accessed data in memory | Setup > Platform Cache |

---

## Labs & Design

### Lab 1 — Build a Custom Object & Flow

**Goal:** Create a custom object, add fields, automate with Flow.

1. Setup > Object Manager > Create > Custom Object. Label: "Project", Plural: "Projects", Object Name: `Project__c`. Check Allow Reports, Allow Activities, Track Field History. Save.
2. Setup > Object Manager > Project__c > Fields & Relationships > New. Add fields: Project Code (Text, Required), Status (Picklist: Planning, In Progress, On Hold, Completed), Target Completion Date (Date).
3. Setup > Flows > New Flow > Record-Triggered Flow. Object: Project__c, Trigger: "A record is created". Add Assignment: set Status = "Planning" if null. Add Update Records to update the triggering record. Save as "Auto-set Project Status", Activate.
4. Test: App Launcher > Projects > New. Create a project without Status. Verify Status auto-fills to "Planning."

**Learned:** Object creation, field types, Flow automation without code.

### Lab 2 — Write Your First Apex Trigger

**Goal:** Write an Apex trigger with a test class (≥75% coverage required to deploy).

1. Setup > Apex Triggers > New. Name: `ProjectTrigger`. Object: Project__c. Events: before insert, before update.
   ```
   trigger ProjectTrigger on Project__c (before insert, before update) {
       for (Project__c p : Trigger.new) {
           if (String.isBlank(p.Project_Code__c)) {
               p.Project_Code__c = 'PRJ-' + String.valueOf(Crypto.getRandomInteger().abs());
           }
       }
   }
   ```
2. Setup > Apex Classes > New. Name: `ProjectTriggerTest`.
   ```
   @isTest
   private class ProjectTriggerTest {
       @isTest static void testProjectCodeGeneration() {
           Project__c p = new Project__c(Name='Test Project');
           insert p;
           p = [SELECT Project_Code__c FROM Project__c WHERE Id = :p.Id];
           System.assertNotEquals(null, p.Project_Code__c);
           System.assert(p.Project_Code__c.startsWith('PRJ-'));
       }
   }
   ```
3. Setup > Apex Test Execution. Select ProjectTriggerTest, Run. Verify 100% coverage.

**Learned:** Triggers, test classes, code coverage requirement, SOQL query.

### Lab 3 — Build a Lightning Web Component

**Goal:** Create an LWC that displays project information.

1. `sf org login web -d -a my-dev-org`
2. `sf project generate component -n projectCard -l lwc`
3. Edit `projectCard.js`:
   ```
   import { LightningElement, api } from 'lwc';
   export default class ProjectCard extends LightningElement {
       @api projectName;
       @api projectStatus;
   }
   ```
4. Edit `projectCard.html`:
   ```
   <template>
       <lightning-card title={projectName} icon-name="standard:project">
           <div class="slds-m-around_medium">
               <p><strong>Status:</strong> {projectStatus}</p>
           </div>
       </lightning-card>
   </template>
   ```
5. Edit `projectCard.js-meta.xml` (apiVersion 60.0, isExposed true, target lightning__RecordPage).
6. `sf project deploy start`
7. Setup > Object Manager > Project__c > Page Layouts > [Layout] > Lightning Record Page > Edit Page > drag projectCard onto page > Save and activate.

**Learned:** LWC structure, Salesforce CLI deployment, Lightning App Builder.

### Lab 4 — Make a REST API Callout

**Goal:** Call an external REST API from Apex using Named Credentials.

1. Setup > Named Credentials > New. Label: "JSON Placeholder API", Name: `JSON_Placeholder_API`, URL: `https://jsonplaceholder.typicode.com`, Identity: Named Principal, Auth: Password Authentication.
2. (Fallback) Setup > Remote Site Settings > New. Name: "JSON Placeholder", URL: `https://jsonplaceholder.typicode.com`, Active.
3. Setup > Apex Classes > New. Name: `ExternalApiCaller`.
   ```
   public class ExternalApiCaller {
       @future(callout=true)
       public static void fetchPosts() {
           Http http = new Http();
           HttpRequest req = new HttpRequest();
           req.setEndpoint('callout:JSON_Placeholder_API/posts/1');
           req.setMethod('GET');
           HttpResponse res = http.send(req);
           if (res.getStatusCode() == 200) {
               System.debug('Response: ' + res.getBody());
           } else {
               System.debug('Error: ' + res.getStatusCode());
           }
       }
   }
   ```
4. Developer Console > Debug > Open Execute Anonymous Window. Run `ExternalApiCaller.fetchPosts();`. Check Debug Logs.

**Learned:** Named Credentials, callouts, @future asynchronous methods, HttpRequest/HttpResponse.

### Design patterns

| Pattern | When to use |
|---|---|
| Bulkification | Always — triggers handle multiple records at once |
| Trigger Framework | Multiple triggers on same object; one trigger per object, delegate to handler classes |
| Selector Layer | Reusing SOQL queries |
| Domain Layer | Business logic per object |
| Service Layer | Cross-object logic |
| Async Processing | Long-running operations (@future, Queueable, Batch Apex) |

### Security design

- Least privilege; `with sharing`; CRUD/FLS checks; SOQL injection prevention via bind variables; Named Credentials for endpoints/auth

### System properties & OOB features

| Property | Where | What it controls |
|---|---|---|
| org.wideSharing.default | Setup > Sharing Settings | Org-wide default record visibility |
| setup.locked | Setup > Deploy > Deployment Status | Whether metadata changes are allowed |
| session.timeout | Setup > Session Settings | Idle session expiration |

---

## User Management & Data

### Users: creation & lifecycle

**Path:** Setup > Users > New User

| Field | What it does |
|---|---|
| First Name / Last Name | Display name |
| Email | Login ID and notification address |
| Username | Unique across all Salesforce orgs (email format) |
| User License | Determines feature access |
| Profile | Base permissions (objects, fields, apps) |
| Role | Record-level sharing position in hierarchy |
| Alias | Short identifier shown in lists |
| Time Zone / Locale | Date/time formatting and business hours |

### User states

| State | Description |
|---|---|
| Active | Can log in and use Salesforce |
| Inactive (Frozen) | Cannot log in; keeps history and records |
| Deactivated | Cannot log in; license freed up |

**Best practice:** Freeze users instead of deactivating when they leave temporarily. Deactivate only when you need the license back and won't need the user again.

### Profiles & permission sets

Profiles are the base permission set (one per user). Permission Sets grant additional access without changing the profile. Permission Set Groups bundle multiple permission sets.

### Roles & record sharing

**Org-Wide Defaults (OWD)** set baseline record visibility. Sharing can only expand access, never restrict below OWD.

| Setting | Meaning |
|---|---|
| Private | Only owner and above in role hierarchy can see |
| Public Read Only | Everyone can see, only owner can edit |
| Public Read/Write | Everyone can see and edit |
| Controlled by Parent | Child visibility follows parent (Master-Detail only) |

**Path:** Setup > Sharing Settings

Role hierarchy: users higher up can see records owned by users below them.

Sharing Rules extend access beyond OWD and role hierarchy: Criteria-Based, Owner-Based, Territory-Based.

### Data import & export

**Data Import Wizard** (Setup > Data > Data Import Wizard): best for <50,000 records, standard objects. Steps: select object/operation, upload CSV, map columns, match records, review and import.

**Data Loader** (Setup > Data > Data Loader): best for 50,000 to 5 million records. Operations: Insert, Update, Upsert, Delete, Hard Delete, Export.

**Export** (Setup > Data > Export / Export All): Export includes active records; Export All includes deleted (recycle bin). Output: ZIP with CSV per object.

### Data integrity & quality

**Validation Rules** (Setup > Object Manager > [Object] > Validation Rules): prevent bad data from being saved.

Example: Opportunity Amount must be positive when Stage is "Closed Won"
```
AND(
    ISPICKVAL(StageName, 'Closed Won'),
    Amount <= 0
)
```

**Required fields:** field-level Required (always), Validation Rule (conditional), Page Layout Required (layout only, bypassable via API).

**Dependent Picklists:** control picklist values based on another field (Country → State).

**Record Types:** different page layouts, picklist values, business processes per object.

### Field-Level Security & Encryption

**FLS** (Setup > Object Manager > [Object] > Fields & Relationships > [Field] > Set Field-Level Security): Visible / Read Only / Hidden. Best practice: set FLS at Profile level, not page layout (layouts can be bypassed via API/reports; FLS cannot).

**Shield Platform Encryption:** encrypts sensitive data at rest (Deterministic vs Probabilistic). Requires Shield license. Consider for PII (SSN, credit card, health data).

### Duplicate Management

**Matching Rules** (Setup > Duplicate Management > Matching Rules): define what makes two records "the same."  
**Duplicate Rules** (Setup > Duplicate Management > Duplicate Rules): Alert / Block / Report when a duplicate is detected.

### Data design best practices

**Object design:** use standard objects when possible; extend task/event for activity-like objects; Master-Detail for tight parent-child; Lookup for loose associations; limit custom fields per object (< 500); junction objects for many-to-many.

**Field design:** picklists instead of free text for categories; checkboxes for boolean states; set defaults; external IDs for integration keys; index frequently queried fields.

**Relationship design:** Master-Detail when child can't exist without parent; Lookup when independent; avoid lookup loops; junction objects for many-to-many.

### Troubleshooting data & access issues

| Symptom | Likely cause |
|---|---|
| User can't see a record | OWD too restrictive, user not in role hierarchy |
| User can't see a field | FLS = Hidden for their profile |
| User can't edit a field | FLS = Read Only, or field required but not on layout |
| Record won't save | Validation rule failure |
| Duplicate records created | No duplicate rule, or rule set to Alert only |

"Why can't I see this?" checklist: 1) user Active? 2) Profile Read access to object? 3) Profile Read access to field? 4) Role positioned correctly? 5) Sharing Rule granting access? 6) OWD too restrictive? 7) record owned by someone visible through hierarchy?

---

## DevOps & Release Engineering

The DevOps Engineer (Salesforce) role at Scotiabank (requisition 276046) owns "make Salesforce releases fast, safe, and auditable." Developers build the furniture; the release engineer owns the loading dock, the truck, the checklist, and the proof.

### Training items (work in order)

| # | Training item | Done when |
|---|---|---|
| 1 | Source of truth — metadata lifecycle in Git; Salesforce DX | Retrieve one metadata type, commit it, dry-run deploy to a second org |
| 2 | Metadata that breaks releases — limits, dependencies, constraints | Name the dependency a failed deploy is missing without opening the org |
| 3 | Environments and sandboxes — Dev/QA/UAT/Pre-Prod/Prod; create/refresh; masking | Draw the path; say which sandbox type each stage uses; why a Full copy is masked |
| 4 | Branching — feature, release, hotfix | Say where a hotfix is cut from and which branches it merges back into |
| 5 | CI/CD — GitHub Actions, Azure DevOps, GitLab | Describe the same four stages in any of those tools |
| 6 | DevOps tools — Gearset, Copado, AutoRABIT, or CLI | Say what the CLI does that the vendor UI does not replace |
| 7 | Conflict clinic — profiles, permission sets, record types, layouts, Flows, Apex | Have a fix for each, not just the symptom |
| 8 | Packages — unlocked / managed | Say when unpackaged source is still the right deploy |
| 9 | Tests and validation — automated testing | Explain dry-run vs quick deploy vs a real prod deploy |
| 10 | Releases, hotfixes, rollback — runbook template (Lab D) | Fill the runbook template from memory |
| 11 | Banking change control — audit, security, compliance | List the artifacts an auditor asks for after a prod deploy |
| 12 | Design patterns you coach — DevOps-friendly design | Reject a story that edits Admin.profile for one field |

### 1. Source of truth

Production is not the source of truth. Git is. The org is a target you deploy to.

A Salesforce DX project is a folder of metadata XML plus `sfdx-project.json`. The modern CLI is `sf` (older `sfdx` still appears; same product family).

Practice on two free Developer Edition orgs, aliased `dev` and `qa`:
```
sf org login web --alias dev --instance-url https://login.salesforce.com
sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev
sf project deploy start --dry-run --target-org qa
```

**What to commit:** custom objects, fields, validation rules, Flows, Apex, LWC, permission sets, custom metadata, named credentials metadata (not the secret), a manifest (package.xml) or package directory the pipeline always deploys.

**What not to commit:** profiles as the place business access lives; `.sfdx/`, org auth files, consumer secrets, JWT private keys; retrieved junk you did not mean to ship.

Destructive deletes are a separate file, not a side effect of "it was not in the folder":
```
sf project deploy start --manifest manifest/package.xml --post-destructive-changes manifest/destructiveChanges.xml --target-org qa
```

Trailhead: Org Development Model, Salesforce DX Development Model, App Development with Salesforce DX, Quick Start: Salesforce DX, package.xml, Git and GitHub basics.

### 2. Metadata that breaks releases

Deploys compile the payload against the target org via the Metadata API. Missing references = failed deploy.

| Failure | Usual cause | Check first |
|---|---|---|
| no such column / field does not exist | Flow, layout, formula, or Apex references a field not in payload and not in target | Add the field, or deploy to the org that already has it |
| invalid cross reference id | Record type, layout, or business process assignment points at something missing | Deploy the parent (object, record type, layout) in the same payload |
| entity not found / Apex dependency | Class A uses class B, B not deployed | Deploy the dependency, or stop referencing it |
| Test failure only in prod/UAT | Test uses a profile, record type, or custom setting that exists in Dev and not target | Make the test create its own data; do not rely on org data |
| Flow version deployed but users see old one | New version is not active | Activate the version, or deploy the flow as Active |
| Coverage below 75% | Production gate | See tests section |
| CANNOT_MODIFY_MANAGED_OBJECT | Tried to change a managed-package component | Configure around it, or upgrade the package |

Governor limits matter: a deploy can succeed and the feature can still fall over in prod because the code is not bulkified. Ask: "what happens when this runs on 200 records?"

### 3. Environments and sandboxes

| Stage | What it's for | Usual sandbox | Who promotes into it |
|---|---|---|---|
| Dev | Build and unit test | Developer / Developer Pro | Developer, via Git |
| QA | Automated validation, integration | Developer Pro or Partial Copy | Pipeline, on merge |
| UAT | Business testers | Partial Copy, or masked Full | Release engineer, from release branch |
| Pre-Prod | Dress rehearsal against prod-like metadata and volume | Full or recent Partial, refreshed close to window | Release engineer |
| Prod | Customers | Production | Release engineer, after approval, inside the window |

Scratch orgs are not sandboxes. Use scratch orgs for package builds; sandboxes for the Dev→Prod path. UAT is not a scratch org in a bank.

Sandbox types: Developer (metadata only, isolated build), Developer Pro (more room, QA when no rows needed), Partial Copy (metadata + template sample, UAT when testers need some rows), Full (metadata + all data, pre-prod/performance).

Full copies contain customer data. Refresh is done when masking has run and access is limited. Salesforce Data Mask is the product to know. Refresh cadence is license-limited; Full is slowest.

Setup paths: List and refresh sandboxes (Setup > Sandboxes); Sandbox template (Setup > Sandboxes > Sandbox Templates); Allow inbound deploys (Setup > Deploy > Deployment Settings); See what is running (Setup > Deploy > Deployment Status); DevOps Center (Setup, search "DevOps Center"); Data Mask (App Launcher > Data Mask).

### 4. Branching

```
main                         ← matches production
  hotfix/<ticket>            ← cut from main only
  release/2026-11-27         ← cut from main when the release freezes
    feature/<ticket>-name    ← short-lived, merged into the release branch
```

Rules:
- A hotfix is cut from `main` (main is what production runs). Merges back to `main` and into any open release branch.
- A feature branch lives days, not weeks. Salesforce XML (Flows, profiles) does not merge.
- The release branch is what QA and UAT deploy. Developers do not deploy their feature branch into UAT.
- Tag production after a successful deploy: `release-2026-11-27`. That tag is the rollback target.
- Commit messages carry the change-ticket id. That is the audit trail.

### 5. CI/CD

Same pipeline in GitHub Actions, Azure DevOps, or GitLab. Only the YAML header changes.

| Stage | Trigger | What it runs | Target |
|---|---|---|---|
| Validate | Pull request | `sf project deploy start --dry-run` + story's Apex tests | CI sandbox refreshed/reset on schedule |
| Integrate | Merge to release branch | Real deploy | QA |
| Stage | Release manager | Validation-only deploy | Pre-Prod, then Prod |
| Release | Change window, after approval | Quick deploy of validated prod job, or fresh deploy if validation expired | Prod |

Authentication in CI is JWT or a stored auth URL in the CI secret store. Never `sf org login web` on a runner, never a password in the repo. The connected app, integration user, and permission set on that user are part of the design. The integration user can deploy; it cannot be a shared human admin login.

Minimum commands:
```
sf project deploy start --dry-run --test-level RunSpecifiedTests --tests CommercialBankingReleaseTest --target-org ci
sf apex run test --test-level RunLocalTests --code-coverage --result-format human --wait 30 --target-org qa
```

`--test-level` values: `NoTestRun`, `RunSpecifiedTests`, `RunLocalTests`, `RunAllTestsInOrg`. Production will not accept `NoTestRun` when the payload contains Apex.

### 6. DevOps tools

| Tool | What it is | Expected to know |
|---|---|---|
| Salesforce CLI (`sf`) | Deploy/retrieve/test/package engine | Run a dry-run and read the failure. Every other tool is a UI over this or the Metadata API |
| DevOps Center | Salesforce product: work items, Git, promotion | Native option when the bank does not want another vendor. Still not a reason to skip Git discipline |
| Gearset | Compare and deploy, CI, backups | Compare orgs, spot forgotten metadata, gate on tests |
| Copado | User stories, pipelines, compliance packs | Pipeline and promotion path |
| AutoRABIT | CI/CD and data tooling | Same answer as Gearset/Copado: promotion path, back-promotion, where secrets live |
| Change Sets | Setup UI between related orgs | Why they fail at this job's scale: no reviewable diff, no hotfix branch, profile XML you cannot merge, no rollback tag |

### 7. Conflict clinic

**Profiles:** `Admin.profile-meta.xml` is a dump of user permissions, object permissions, field permissions, layout assignments, record-type visibility. Two stories editing it will conflict; a bad merge can grant or remove access you did not review. Fix: ship a permission set (or permission set group) per persona or per feature. Leave the profile alone unless the story truly changes a profile-only setting.

**Permission sets:** smaller, but still a conflict if every story edits one giant `CB_Admin` permission set. Split by feature or persona. Permission Set Groups bundle them.

**Record types:** deploy the record type, the layout, and the permission set that grants visibility in one payload. Do not deploy the record type Monday and the permission set "later."

**Page layouts:** the layout file is not the assignment (assignment lives on profile and record type). Don't confuse classic page layout with Lightning record page (FlexiPage).

**Flows:** Flow XML does not merge. One owner per flow while in a release, or split into subflows. Know whether your deploy leaves the new version Draft or Active. Fast mitigation: activate the previous version in Setup > Flows, then redeploy the last good tag.

**Apex and dependencies:** deploy the class and its test in the same payload. Tests create their own data. A trigger with no coverage blocks production.

### 8. Packages

| Kind | Who it's for | DevOps note |
|---|---|---|
| Unlocked package | Your own team, modular internal apps | Versioned, upgradeable, has a dependency list. Best fit when a boundary is real |
| Org-dependent unlocked package | A module depending on unpackaged metadata in that org | Faster to adopt, harder to install elsewhere |
| Managed package (1GP or 2GP) | An ISV, or a hard IP boundary | You upgrade it. You do not edit its Apex in Git |

Unpackaged metadata deployed from Git is still the right default for a large existing commercial-banking org. Do not propose "package the entire org" as the first move.

You need a Dev Hub to create second-generation packages and scratch orgs (Setup > Dev Hub). Unlocked packages do not require a namespace. Managed packages usually have one.

Typical commands:
```
sf package version create --package CB_Credit --installation-key-bypass --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30
```
Promote that version before production. Do not install a beta package version into prod.

### 9. Tests and validation

| Action | Changes the org? | Why run it |
|---|---|---|
| Validation / dry-run | No | Prove the payload compiles and tests pass against that org |
| Quick deploy | Yes | Promote a validation that already succeeded, inside the quick-deploy window |
| Real deploy | Yes | First deploy, or the validation expired, or the payload changed |

Production rules:
- A payload with Apex must run tests
- Salesforce requires 75% coverage as the production gate
- `RunSpecifiedTests` means you name the tests, and the Apex you deploy has to be covered by those tests
- `RunLocalTests` runs local tests and skips managed-package tests. It is the honest gate before a release, and slow — that's why you validate before the window, then quick-deploy inside it
- A green Dev sandbox is not evidence. The validation that counts is against the org you are about to change

### 10. Releases, hotfixes, rollback

| Speed | When | Branch | Deploy bar |
|---|---|---|---|
| Scheduled | The release calendar | `release/<date>` | Full validation, UAT sign-off, change ticket, window |
| Hotfix | Prod defect, next release is too late | `hotfix/<ticket>` from `main` | Same validation, smaller payload, still a ticket |
| Emergency | Active customer or regulatory harm | `hotfix/<ticket>` from `main` | Short path that is already written |

Emergency is a shorter approval chain, not a skipped pipeline.

**Runbook template (fill for every prod promotion — Lab D):**
```
Change ticket:
Release tag:
Payload (package directory or manifest):
Source branch / commit:
Validation org / deploy id / time:
Tests run and coverage:
Prod deploy id / time:
Approver (not the author):
Sandbox or feature flags to flip after deploy:
Rollback tag:
Rollback owner:
How we will know it worked (one query, one screen, one test):
```

**Rollback:** Metadata does not roll back by itself. Rollback is a forward deploy of the last known-good tag, or a package install of the previous version. If you do not have a tag from the last good prod deploy, you do not have a rollback.

### 11. Banking change control

Keep these every time:
- Change ticket id in the commit and the pull request
- Diff a second person read (not the author)
- Validation deploy id and prod deploy id
- Test run id and coverage number
- Named approver, different from the person who wrote the change
- Release tag
- For a Full sandbox refresh: refresh time, mask-complete confirmation, who is allowed to log in

Segregation of duties: the developer who wrote the Apex does not approve their own production deploy. The pipeline should make that structural, not cultural. The integration user deploys; a human approves — different identities.

Do not put production customer data in a slide, a debug log pasted into a ticket, or an unmasked sandbox. Debug logs can contain field values; turn them off when diagnosis is done.

### 12. Design patterns you have to coach

| Pattern | Why release engineering cares |
|---|---|
| Permission sets over profile edits | Profiles do not merge. Permission sets do, if kept small |
| One flow owner per release; subflows for parallel work | Flow XML does not merge |
| Tests create their own data | Empty sandboxes and prod-like sandboxes behave the same |
| No hardcoded ids | The id in Dev is not the id in UAT. Use custom metadata or a query |
| Named Credentials for callouts | Endpoints differ per sandbox. Secrets never go in Git |
| Custom metadata / custom settings for toggles | Ship a feature dark and turn it on after deploy, without another deploy |
| Bulkified Apex | A deploy can be green and still fail the first real batch |
| No environment-specific branches | `if (org.IsSandbox)` is a last resort. Config belongs in the target |

---

## Labs (DevOps track)

**Lab A — Retrieve, review, dry-run:** two Developer Edition orgs aliased `dev` and `qa`; create permission set `CB_Release_Reader` in `dev`; retrieve only that permission set; read the XML; dry-run deploy to `qa`; real deploy; change the permission set in `qa` Setup directly; retrieve; see the diff. Done when the only path into `qa` is Git and you can explain the diff in one sentence.

**Lab B — Profile conflict, on purpose:** two branches each add a different field permission to the same profile XML; merge; watch it conflict; throw that approach away; recreate both permissions as two permission sets; merge those; write three sentences on why the profile conflicted, what a bad merge would have granted, what you will tell a developer who asks to edit `Admin` profile for one field.

**Lab C — Failing validation:** write an Apex class that references a second class you do not deploy; dry-run; save the error; add the missing class; dry-run again; add a test that queries `Account` without inserting one; run in an empty org; fix the test to insert the row. Done when you can map an error string to "missing dependency" vs "test depends on org data" without guessing.

**Lab D — Runbook:** fill the runbook template for Lab A as if `qa` were production. Include a rollback tag even though the exercise is fake.

**Lab E — Sandbox and mask checklist:** write the checklist you would attach to a refresh ticket (sandbox name/type/why, next eligible refresh, template name, fields to mask, who confirms mask complete, who is allowed to log in before confirmation, which integration endpoints must point at non-prod).

---

## Interview drills

1. Where is the source of truth? Git. Production is a deploy target. If Setup and Git disagree, that is an incident, not a workflow.
2. Walk a change to prod: feature branch → pull request → dry-run with tests → merge to release branch → QA deploy → UAT → prod validation before the window → approval → quick deploy or fresh deploy → tag → ticket updated with both deploy ids.
3. Hotfix during an open release? Cut from `main`, not the release branch. Merge back to `main` and to the open release branch.
4. Why did this profile deploy fail or scare you? Profiles are a grab bag of access. Two stories conflict. A bad merge changes access you did not mean to ship. Prefer permission sets.
5. Flow deploy succeeded but users see the old screen? The new version is probably not the active version. Check before redeploying.
6. Validate vs quick deploy? Validate does not change the org. Quick deploy applies a validation that already passed, inside the platform window, so the change window stays short.
7. Unlocked vs managed? Unlocked is yours, versioned, for internal modules. Managed is something you upgrade and do not edit. Packaging the entire existing bank org on day one is not a plan.
8. What do you hand an auditor? Ticket, diff, approver who is not the author, validation id, prod deploy id, test run, tag, and for any Full sandbox, mask-complete evidence.

---

## Quiz

1. Name the five environments in the posting and the sandbox type for UAT if testers need sample data but not a full customer copy.
2. A hotfix is cut from which branch, and which branches does it merge back into?
3. Why is a 75% coverage result in a Developer sandbox not enough to call production safe?
4. A deploy of a new record type succeeds, and users cannot create that type. What two assignments are probably missing?
5. What is the difference between a dry-run and a quick deploy?
6. Why do you refuse a story whose only access change is an edit to `Admin.profile`?
7. What does a Git revert not undo after a production deploy?
8. Which sandbox type requires a mask confirmation before broad login, and why?

Answers are in the sections above. If you cannot answer, do the matching lab again.