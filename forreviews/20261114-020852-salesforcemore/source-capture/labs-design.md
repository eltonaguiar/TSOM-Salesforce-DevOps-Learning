# Source Capture — Salesforce Labs, Design Considerations & Documentation
**Source URL:** https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/salesforce/labs-design/
**Agent:** opencode | **Date:** 2026-11-10
**Platform:** Salesforce | **Purpose:** Pre-existing labs, design considerations, system properties, and out-of-box features
**Confidence:** high

## Contents
- Pre-Existing Labs & Documentation
- Lab 1: Build a Custom Object & Flow
- Lab 2: Write Your First Apex Trigger
- Lab 3: Build a Lightning Web Component
- Lab 4: Make a REST API Callout
- Design Considerations
- System Properties & OOB Features
- What to Think About Before You Build

## Pre-Existing Labs & Documentation

| Resource | What It Is | Link |
|----------|-----------|------|
| Trailhead | Free guided learning with hands-on challenges | trailhead.salesforce.com |
| Trailhead Projects | Step-by-step project-based labs | trailhead.salesforce.com/en/content/learn/projects |
| Developer Console | Built-in IDE for Apex, Visualforce, SOQL | Gear menu > Developer Console |
| Developer Workbook | Guided Apex and Visualforce tutorials | developer.salesforce.com/docs/atlas.en-us.workbook |
| LWC Recipes | Sample LWC components | developer.salesforce.com/docs/component-library/lwc |
| Apex Recipes | Sample Apex code patterns | developer.salesforce.com/docs/atlas.en-us.apexcode |
| Salesforce CLI | Command-line development tool | developer.salesforce.com/tools/sfdxcli |
| Workbench | Browser-based data inspector and query tool | workbench.developerforce.com |

## Lab 1: Build a Custom Object & Flow

**Goal:** Create a custom object, add fields, and automate field updates with Flow.

**Steps:**
1. Create custom object “Project” (Project__c): Setup > Object Manager > Create > Custom Object. Check “Allow Reports”, “Allow Activities”, “Track Field History”.
2. Add fields: Setup > Object Manager > Project__c > Fields & Relationships > New
   - Field 1: Text, “Project Code”, Required
   - Field 2: Picklist, “Status”, Values = Planning, In Progress, On Hold, Completed
   - Field 3: Date, “Target Completion Date”
3. Build Flow: Setup > Flows > New Flow > Record-Triggered Flow. Object Project__c, Trigger “A record is created”. Add Assignment (set Status = “Planning” if null). Add Update Records. Save as “Auto-set Project Status”, Activate.
4. Test: App Launcher > Projects > New. Create project without Status. Verify Status auto-fills to “Planning”.

**Learned:** Object creation, field types, Flow automation without code.

## Lab 2: Write Your First Apex Trigger

**Goal:** Write an Apex trigger updating a related field, with a test class (≥75% coverage required).

**Steps:**
1. Trigger `ProjectTrigger` on Project__c (before insert, before update):
```
trigger ProjectTrigger on Project__c (before insert, before update) {
    for (Project__c p : Trigger.new) {
        if (String.isBlank(p.Project_Code__c)) {
            p.Project_Code__c = 'PRJ-' + String.valueOf(Crypto.getRandomInteger().abs());
        }
    }
}
```
2. Test class `ProjectTriggerTest`:
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
3. Run tests: Setup > Apex Test Execution > select ProjectTriggerTest > Run. Verify 100% coverage.

**Learned:** Triggers, test classes, code coverage, SOQL query.

## Lab 3: Build a Lightning Web Component

**Goal:** Create an LWC displaying project information.

**Steps:**
1. Authorize Dev Org: `sf org login web -d -a my-dev-org`
2. Create LWC: `sf project generate component -n projectCard -l lwc`
3. Edit projectCard.js:
```
import { LightningElement, api } from 'lwc';
export default class ProjectCard extends LightningElement {
    @api projectName;
    @api projectStatus;
}
```
4. Edit projectCard.html:
```
<template>
    <lightning-card title={projectName} icon-name="standard:project">
        <div class="slds-m-around_medium">
            <p><strong>Status:</strong> {projectStatus}</p>
        </div>
    </lightning-card>
</template>
```
5. Edit projectCard.js-meta.xml (apiVersion 60.0, isExposed true, target lightning__RecordPage)
6. Deploy: `sf project deploy start`
7. Add to record page: Setup > Object Manager > Project__c > Page Layouts > [Layout] > Lightning Record Page > edit page > drag projectCard > save and activate.

**Learned:** LWC structure, Salesforce CLI deployment, Lightning App Builder.

## Lab 4: Make a REST API Callout

**Goal:** Call an external REST API from Apex using Named Credentials.

**Steps:**
1. Named Credential “JSON Placeholder API”: Setup > Named Credentials > New. URL https://jsonplaceholder.typicode.com. Identity Named Principal. Auth Password Authentication (blank for public API).
2. Remote Site Setting fallback: Setup > Remote Site Settings > New. URL https://jsonplaceholder.typicode.com. Active.
3. Apex class `ExternalApiCaller`:
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
4. Test from Anonymous Apex: `ExternalApiCaller.fetchPosts();` Check Debug Logs.

**Learned:** Named Credentials, callouts, @future async methods, HttpRequest/HttpResponse.

## Design Considerations

### Before You Build: The Checklist

| Question | Why It Matters | Where to Decide |
|----------|---------------|-----------------|
| Can Flow do this instead of code? | Flows easier to maintain, no test classes | Setup > Flows |
| Will this scale to 100K+ records? | Governor limits; bulkify everything | Apex design |
| Who needs to see/edit this data? | Profiles, roles, OWD, sharing, FLS | Setup > Security |
| Is this data sensitive? | FLS, encryption, Shield Platform Encryption | Setup > Security |
| What if external API is down? | Error handling, retry, fallback | Apex exception handling |
| Will users adopt this? | Page layout usability, Lightning Design System | Lightning App Builder |
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

## System Properties & Out-of-the-Box Features

### Important System Properties

| Property | Where | What It Controls |
|----------|-------|------------------|
| org.wideSharing.default | Setup > Sharing Settings | Org-wide default record visibility |
| setup.locked | Setup > Deploy > Deployment Status | Whether metadata changes are allowed |
| apex.pageLimit | Internal | Visualforce page size limits |
| session.timeout | Setup > Session Settings | How long before idle sessions expire |
| login.lockout | Setup > Session Settings | Failed login lockout policy |

### Out-of-the-Box Features

| Feature | What It Does | Where |
|---------|-------------|-------|
| Record Types | Different page layouts, picklists, business processes per object | Setup > Object Manager > [Object] > Record Types |
| Formula Fields | Read-only calculated fields (no code) | Setup > Object Manager > [Object] > Fields > Formula |
| Roll-Up Summary | Aggregate child records on parent (Master-Detail only) | Setup > Object Manager > [Parent] > Fields |
| Validation Rules | Block invalid data at save | Setup > Object Manager > [Object] > Validation Rules |
| Approval Processes | Multi-step record approval with email | Setup > Approval Processes |
| Sandboxes | Isolated copies for dev/test | Setup > Sandboxes |
| Change Sets | Move metadata between orgs | Setup > Deploy > Change Sets |
| Optimizer | Health check, recommends improvements | Setup > Optimizer |
| Platform Cache | Cache frequently accessed data in memory | Setup > Platform Cache |
| Apex Scheduler | Schedule Apex classes periodically | Setup > Apex Classes > [Batch Class] > Schedule |

### Deployment Options

| Option | Best For |
|--------|----------|
| Change Sets | Simple config moves between related orgs (sandbox → production) |
| Salesforce CLI (SFDX) | Source-driven development, CI/CD, version control |
| Metadata API | Programmatic deployment, custom tooling |
| Ant Migration Tool | Legacy XML-based deployment (superseded by CLI) |
| DevOps Center | Salesforce-native work items and Git promotion (if enabled) |
| Gearset / Copado / AutoRABIT | Vendor compare-and-deploy pipelines (enterprise orgs; same Metadata API underneath) |

## What to Think About Before You Build

### The “Buy vs Build” Decision
1. Is there an AppExchange app that does this? (Save time, costs money)
2. Can Flow do this? (Fastest to build, easiest to maintain)
3. Do you need Apex? (Only for complex logic, callouts, bulk operations)
4. Do you need LWC? (Only for custom UI beyond standard page layouts)

### The “Maintenance” Question

| Question | Good Answer |
|----------|-------------|
| Who maintains this after you leave? | Documented Flow or well-structured Apex with test classes |
| Can an admin modify it? | Flow/declarative = yes; Apex = no |
| Is it documented? | Comments in code, Flow descriptions, external wiki |
| Are there test classes? | Yes, ≥75% coverage (Salesforce requirement) |
| Can it be deployed to production? | Via Change Sets or CLI, tested in sandbox first |
