# Salesforce DevOps Engineer - Complete Research Documentation

## Source Materials
- **Primary**: Scotiabank Job Requisition 276046 (DevOps Engineer - Salesforce)
- **Reference**: ServiceNow Learning Module - Salesforce DevOps Engineer Track
- **Tools**: Gearset, Copado, AutoRABIT, Salesforce CLI (`sf`)

---

## Section 1: Salesforce Crash Course Fundamentals

### 1.1 Objects, Records, Fields
| Concept | Description | DevOps Relevance |
|---------|-------------|------------------|
| **Standard Objects** | Account, Contact, Opportunity, Lead, Case | Cannot delete, only extend |
| **Custom Objects** | Created by org, API name ends in `__c` | Deployed via metadata API |
| **Custom Fields** | Data types: Text, Number, Picklist, Formula, Lookup, Master-Detail | Field-level security via profiles/perm sets |
| **Record Types** | Different business processes, picklist values, page layouts per type | Require layout + visibility assignment |

### 1.2 Navigation Breadcrumbs (Key Setup Paths)
| Task | Setup Path |
|------|------------|
| **Create/Edit Objects** | Setup → Object Manager → [Object] → Fields & Relationships |
| **Profiles** | Setup → Users → Profiles |
| **Permission Sets** | Setup → Users → Permission Sets |
| **Roles** | Setup → Users → Roles |
| **Sandboxes** | Setup → Sandboxes |
| **Deployments** | Setup → Deploy → Deployment Status |
| **Change Sets** | Setup → Deploy → Outbound Change Sets |
| **DevOps Center** | App Launcher → DevOps Center |
| **Data Mask** | App Launcher → Data Mask (after package install) |
| **Named Credentials** | Setup → Security → Named Credentials |
| **Connected Apps** | Setup → Apps → App Manager |

### 1.3 Users, Profiles, Roles, Licenses
| Component | Purpose | DevOps Consideration |
|-----------|---------|---------------------|
| **Profile** | Baseline permissions (object, field, layout, app) | **Don't edit for features** - use permission sets |
| **Permission Set** | Additive permissions | Small, mergeable, versionable |
| **Permission Set Group** | Bundle perm sets for job functions | Reduces monolith permissions |
| **Role** | Record-level access hierarchy | Independent of profiles |
| **License** | Feature access (Sales Cloud, Service Cloud, Platform) | Limits sandbox types |

### 1.4 Data Integrity
| Feature | Purpose | Deploy Concern |
|---------|---------|----------------|
| **Validation Rules** | Prevent bad data entry | Must test in target org |
| **Duplicate Rules** | Identify/block duplicates | Matching rules must exist in target |
| **Field-Level Security** | Control field visibility | Deployed with profiles/perm sets |

### 1.5 Automation Comparison
| Tool | Use Case | DevOps Impact |
|------|----------|---------------|
| **Flow (Record-Triggered)** | Complex logic, before/after save | XML doesn't merge; single owner per release |
| **Flow (Screen)** | Guided user input | Version management critical |
| **Apex Trigger** | Complex logic, bulk operations | Must be bulkified; 75% coverage required |
| **Process Builder** | Legacy; being retired | Migrate to Flow |
| **Workflow Rules** | Legacy; simple field updates | Migrate to Flow |

### 1.6 Integration Patterns
| Pattern | When to Use | DevOps Concern |
|---------|-------------|----------------|
| **Named Credentials** | External callouts | Endpoints per environment; secrets never in Git |
| **External Services** | Declarative API integration | Schema changes require re-import |
| **Platform Events** | Async pub/sub | Require subscriber in target org |
| **Change Data Capture** | Real-time data sync | Entity subscription must exist |

---

## Section 2: Salesforce Key Principles & Best Practices

### 2.1 Source of Truth Principle
> **Production is not the source of truth. Git is.** The org is a target you deploy to.

```bash
# Correct workflow
sf project retrieve start --metadata PermissionSet:CB_Release_Reader --target-org dev
git add force-app/main/default/permissionsets/CB_Release_Reader.permissionset-meta.xml
git commit -m "feat: add CB_Release_Reader permission set [TKT-1234]"
sf project deploy start --dry-run --target-org qa
```

### 2.2 Governor Limits (Critical for DevOps)

| Limit Category | Limit | Practical Impact |
|----------------|-------|------------------|
| **Apex CPU Time** | 10,000 ms/transaction | Poorly bulkified code fails at volume |
| **Heap Size** | 6 MB (2 MB async) | Large SOQL queries overflow |
| **SOQL Queries** | 100/transaction (200 async) | N+1 problem in triggers |
| **DML Statements** | 150/transaction | Single-record DML in loops fails |
| **DML Rows** | 10,000/transaction | Bulk operations must chunk |
| **Callouts** | 1/transaction | Batch or async for multiple |
| **API Requests** | 15,000/24hr | CI pipelines consume quota |

### 2.3 Metadata Dependencies That Break Deploys

| Dependency | Failure | Prevention |
|------------|---------|------------|
| Field referenced by Flow/Apex | `no such column` | Deploy field first |
| Record type + layout + visibility | Users can't create records | Deploy all three together |
| Apex class dependency missing | `entity not found` | Deploy dependent classes in same payload |
| Managed package modification | `CANNOT_MODIFY_MANAGED_OBJECT` | Configure around, don't fork |
| Flow version not active | Users see old version | Activate after deploy |

### 2.4 Deployment Constraints

| Constraint | Value | Workaround |
|------------|-------|------------|
| **Package.xml max size** | 10 MB | Use multiple manifests |
| **Deploy timeout** | ~30-60 min | Validate first, quick deploy in window |
| **Test coverage (prod)** | 75% org-wide | RunLocalTests before window |
| **Destructive changes** | Separate file | `destructiveChanges.xml` pre/post |
| **Profile merge** | XML doesn't merge cleanly | Use permission sets instead |

---

## Section 3: Certification Curriculum Deep Dive

### 3.1 Platform Developer I (PD1) - Required per Job Description

**Exam Outline (per Trailhead):**

| Domain | Weight | Key Topics |
|--------|--------|------------|
| **Salesforce Fundamentals** | 10% | Multi-tenant, MVC, data model, governor limits |
| **Data Modeling & Management** | 12% | Objects, fields, relationships, schema builder |
| **Logic & Process Automation** | 46% | **Apex triggers, classes, SOQL, SOSL, governor limits, testing, batch, future, queueable** |
| **User Interface** | 10% | LWC basics, Visualforce (legacy), Lightning App Builder |
| **Testing** | 12% | Test classes, test data factory, `@testSetup`, coverage requirements |
| **Debug & Deploy** | 10% | Debug logs, CLI, change sets, packages |

**Study Resources:**
- Trailhead: [Apex Basics](https://trailhead.salesforce.com/content/learn/trails/apex_basics)
- Trailhead: [Apex Testing](https://trailhead.salesforce.com/content/learn/modules/apex_testing)
- Exam Guide: [Platform Developer I](https://trailhead.salesforce.com/credentials/platformdeveloperi)

### 3.2 Advanced Admin (Platform Administrator II) - Required per Job Description

**Exam Outline:**

| Domain | Weight | Key Topics |
|--------|--------|------------|
| **Security & Access** | 20% | Profiles, perm sets, FLS, OWD, sharing rules, roles |
| **Data Management** | 10% | Import/export, Data Loader, duplicate mgmt |
| **Automation** | 30% | **Flow (record-triggered, screen, autolaunched), Process Builder migration** |
| **Analytics & Reports** | 10% | Report types, dashboards, bucket fields |
| **Change Management** | 15% | **Sandboxes, change sets, packages, DevOps Center** |
| **Mobile & Lightning** | 10% | App Builder, dynamic forms/actions |
| **Admin Settings** | 5% | Company info, fiscal year, languages |

**Study Resources:**
- Trailhead: [Admin Advanced](https://trailhead.salesforce.com/content/learn/trails/admin_advanced)
- Exam Guide: [Platform Administrator II](https://trailhead.salesforce.com/credentials/platformadministrator-ii)

### 3.3 DevOps-Related Certifications (No Official Salesforce DevOps Cert)

| Vendor | Certification | Value |
|--------|---------------|-------|
| **Gearset** | Gearset Certified | Tool-specific proficiency |
| **Copado** | Copado Certified (Admin/Developer/Architect) | Platform-specific, enterprise recognized |
| **AutoRABIT** | AutoRABIT Certified | Tool-specific |
| **Salesforce** | DevOps Center Trailhead | Native tool familiarity |

---

## Section 4: DevOps Tools - Practical Usage Guide

### 4.1 Gearset (Most Common in Banking)

#### Compare & Deploy
**UI Path**: Dashboard → "Select source and target orgs" → Compare

**Practical Steps**:
1. Login to Gearset → Connect Dev and QA orgs
2. Click "Compare" → Select metadata types (Apex, Flows, Perm Sets, etc.)
3. Review "New", "Changed", "Deleted" tabs
4. Click any item → "Show depends on" to see missing dependencies
5. Select items → "Validate" → Choose test level (RunLocalTests)
6. If validation passes → "Deploy"

#### Backup
**UI Path**: Dashboard → "Backup" tab → Select org → Configure schedule

**Practical Steps**:
1. Enable backup for target org
2. Schedule daily/weekly
3. Retention: 90 days typical for banking
4. Restore: Select point-in-time → "Restore to org" (creates deploy)

#### CI/CD Pipeline
**UI Path**: Pipelines → "Create pipeline" → Connect GitHub repo

```yaml
# Gearset generates this in repo
# .gearset/pipeline.yml
stages:
  - name: "Validate"
    environment: "ci-sandbox"
    testLevel: "RunSpecifiedTests"
  - name: "QA Deploy"
    environment: "qa"
    testLevel: "RunLocalTests"
  - name: "UAT Deploy"
    environment: "uat"
    testLevel: "RunLocalTests"
    requiresApproval: true
  - name: "Prod Deploy"
    environment: "prod"
    testLevel: "RunLocalTests"
    requiresApproval: true
    deployMethod: "quickDeploy"
```

### 4.2 Copado (Enterprise Scale)

#### Pipeline Creation
**UI Path**: Copado App → Pipelines → New Pipeline

**Practical Steps**:
1. Define stages: Dev → QA → UAT → Pre-Prod → Prod
2. Create promotion paths between each
3. Configure quality gates (tests, approvals)
4. Add compliance pack for audit trail

#### Hotfix/Back-Promotion
**UI Path**: Hotfixes → New Hotfix → Select source (Prod) → Target (Dev)

**Practical Steps**:
1. Create hotfix record from Prod deployment
2. Auto-creates branch in Git
3. Fix applied in hotfix branch
4. Promote back through pipeline
5. Merge to main + release branches

#### Compliance & Audit
**UI Path**: Compliance → Compliance Packs → Banking/Finance Pack

**Practical Steps**:
1. Enable "Banking Compliance Pack"
2. Configures: Required approvals, test evidence, rollback docs
3. Auto-generates audit report per deployment

### 4.3 AutoRABIT

#### Conflict Analyzer
**UI Path**: Deployment Planning → Conflict Analysis

**Practical Steps**:
1. Select source (Git) and target (Sandbox)
2. Run "Analyze Conflicts"
3. Review: Profile conflicts, Record type conflicts, Flow conflicts
4. Auto-suggests permission set splits

#### Backup Manager
**UI Path**: Backup Manager → Schedule Backup

**Practical Steps**:
1. Full metadata backup daily
2. Data backup for key objects (Account, Opportunity, Case)
3. Point-in-time recovery UI

### 4.4 Salesforce CLI (`sf`) - Foundation for All

```bash
# 1. Authenticate (JWT for CI)
sf org login jwt --client-id <consumer_key> --jwt-key-file server.key --username integration@bank.com --alias ci-org

# 2. Retrieve specific metadata
sf project retrieve start --metadata "PermissionSet:CB_Release_Reader,ApexClass:CreditCheck" --target-org dev

# 3. Dry-run deploy (VALIDATE ONLY)
sf project deploy start --manifest manifest/package.xml --target-org qa --dry-run

# 4. Real deploy with tests
sf project deploy start --manifest manifest/package.xml --target-org prod --test-level RunLocalTests --wait 60

# 5. Quick deploy (after successful validation)
sf project deploy start --validated-deploy-request-id 0Afxx0000000000 --target-org prod

# 6. Run specific tests
sf apex run test --test-level RunSpecifiedTests --tests "CreditCheckTest,AccountTriggerTest" --target-org qa --code-coverage --wait 30

# 7. Package version create
sf package version create --package "CB_Credit_Module" --code-coverage --installation-key-bypass --wait 30

# 8. Install package
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30 --publish-wait 60
```

---

## Section 5: CI/CD Pipeline Best Practices (GitHub Actions)

### 5.1 Complete Pipeline Example

```yaml
# .github/workflows/salesforce-ci-cd.yml
name: Salesforce CI/CD Pipeline

on:
  pull_request:
    branches: [main, release/**]
  push:
    branches: [release/**]

env:
  SF_DEV_HUB_AUTH_URL: ${{ secrets.SF_DEV_HUB_AUTH_URL }}
  SF_QA_AUTH_URL: ${{ secrets.SF_QA_AUTH_URL }}
  SF_UAT_AUTH_URL: ${{ secrets.SF_UAT_AUTH_URL }}
  SF_PROD_AUTH_URL: ${{ secrets.SF_PROD_AUTH_URL }}

jobs:
  validate:
    name: Validate (PR Check)
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Salesforce CLI
        uses: salesforce/github-actions/setup-sfdx@v1
        with:
          sfdx-version: latest
      
      - name: Authenticate to CI Sandbox
        run: |
          echo "${SF_DEV_HUB_AUTH_URL}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias ci-sandbox
      
      - name: Dry-run Deploy
        run: |
          sf project deploy start \
            --manifest manifest/package.xml \
            --target-org ci-sandbox \
            --test-level RunSpecifiedTests \
            --tests "CommercialBankingReleaseTest" \
            --dry-run
      
      - name: Run Apex Tests
        run: |
          sf apex run test \
            --test-level RunLocalTests \
            --code-coverage \
            --result-format tap \
            --target-org ci-sandbox \
            --wait 60

  deploy-qa:
    name: Deploy to QA
    needs: validate
    if: github.event_name == 'push' && startsWith(github.ref, 'refs/heads/release/')
    runs-on: ubuntu-latest
    environment: qa
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Salesforce CLI
        uses: salesforce/github-actions/setup-sfdx@v1
      
      - name: Deploy to QA
        run: |
          echo "${SF_QA_AUTH_URL}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias qa
          sf project deploy start \
            --manifest manifest/package.xml \
            --target-org qa \
            --test-level RunLocalTests \
            --wait 60

  deploy-uat:
    name: Deploy to UAT
    needs: deploy-qa
    runs-on: ubuntu-latest
    environment: uat
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Salesforce CLI
        uses: salesforce/github-actions/setup-sfdx@v1
      
      - name: Deploy to UAT
        run: |
          echo "${SF_UAT_AUTH_URL}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias uat
          sf project deploy start \
            --manifest manifest/package.xml \
            --target-org uat \
            --test-level RunLocalTests \
            --wait 60

  deploy-prod:
    name: Deploy to Production
    needs: deploy-uat
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Salesforce CLI
        uses: salesforce/github-actions/setup-sfdx@v1
      
      - name: Deploy to Production
        run: |
          echo "${SF_PROD_AUTH_URL}" > auth.txt
          sf org login sfdx-url --sfdx-url-file auth.txt --alias prod
          sf project deploy start \
            --manifest manifest/package.xml \
            --target-org prod \
            --test-level RunLocalTests \
            --wait 60
      
      - name: Tag Release
        run: |
          TAG="release-$(date +%Y-%m-%d)-${GITHUB_SHA::7}"
          git tag -a "$TAG" -m "Production deploy $GITHUB_SHA"
          git push origin "$TAG"
```

### 5.2 Pipeline Stages Mapped to Job Requirements

| Job Requirement | Pipeline Stage | Implementation |
|-----------------|----------------|----------------|
| "Design, implement, maintain CI/CD pipelines" | All stages | GitHub Actions + SF CLI |
| "Manage multi-environment release strategies" | QA → UAT → Pre-Prod → Prod | Environment-specific auth |
| "Coordinate scheduled releases" | Release branches | `release/YYYY-MM-DD` branches |
| "Hotfixes and emergency deployments" | Hotfix branch | `hotfix/TKT-123` from `main` |
| "Audit, security, compliance standards" | Approval gates | GitHub Environments + required reviewers |
| "Document release processes, runbooks" | Post-deploy step | Auto-generated deploy summary |

---

## Section 6: Conflict Clinic - Practical Resolutions

### 6.1 Profiles vs Permission Sets

**Problem**: Two developers edit `Admin.profile` → merge conflict → access changes unintended

**Resolution**:
```xml
<!-- BAD: Editing profile directly -->
<!-- Admin.profile-meta.xml - 10,000 lines, unmergeable -->

<!-- GOOD: Create focused permission sets -->
<!-- CB_Credit_Read.permissionset-meta.xml -->
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>CB Credit Read Access</label>
    <objectPermissions>
        <allowRead>true</allowRead>
        <object>Credit_Application__c</object>
    </objectPermissions>
    <fieldPermissions>
        <field>Credit_Application__c.SSN__c</field>
        <readable>true</readable>
    </fieldPermissions>
</PermissionSet>
```

**UI Path to Create**: Setup → Permission Sets → New → Add object/field permissions

### 6.2 Record Types Deployment

**Problem**: Deploy succeeds but users can't create record type

**Missing Components** (deploy together):
```xml
<!-- package.xml must include ALL THREE -->
<types>
    <members>Account.CB_Corporate</members>
    <name>RecordType</name>
</types>
<types>
    <members>Account-CB_Corporate_Layout</members>
    <name>Layout</name>
</types>
<types>
    <members>CB_Credit_Analyst</members>
    <name>PermissionSet</name>
</types>
```

**UI Path to Verify**: Setup → Object Manager → Account → Record Types → Verify Page Layout Assignment + Profile Visibility

### 6.3 Flow Version Activation

**Problem**: New Flow version deployed but users see old version

**Resolution**:
1. After deploy, go to Setup → Flows
2. Find flow → Click version number
3. Click "Activate" on new version
4. Or deploy with `--activate-flow` (tool-dependent)

**UI Path**: Setup → Process Automation → Flows → [Flow Name] → Versions → Activate

### 6.4 Apex Dependency Missing

**Problem**: `ClassA references ClassB but ClassB not in payload`

**Resolution**:
```bash
# 1. Retrieve all dependencies
sf project retrieve start --metadata "ApexClass:ClassA,ApexClass:ClassB" --target-org dev

# 2. Verify both in Git
git status force-app/main/default/classes/

# 3. Deploy together
sf project deploy start --manifest manifest/package.xml --target-org qa
```

---

## Section 7: Banking/Regulated Environment Requirements

### 7.1 Change Control Artifacts (Every Production Deploy)

| Artifact | Source | Stored Where |
|----------|--------|--------------|
| Change Ticket ID | Jira/ServiceNow | Commit message, PR description |
| Second-person Diff Review | GitHub PR | PR approval (not author) |
| Validation Deploy ID | CI/CD logs | Pipeline artifact |
| Production Deploy ID | Deployment Status | Deployment record in Prod |
| Test Run ID + Coverage | Test execution | CI logs + TestResult in org |
| Named Approver | Change ticket | PR approval + deployment approval |
| Release Tag | Git tag | `release-YYYY-MM-DD-sha` |
| Sandbox Mask Confirmation | Data Mask logs | Change ticket attachment |

### 7.2 Sandbox Strategy for Banking

| Stage | Sandbox Type | Refresh Cadence | Masking Required |
|-------|--------------|-----------------|------------------|
| Dev | Developer/Scratch | On demand | No |
| QA | Developer Pro | Weekly | No (synthetic data) |
| UAT | Partial Copy | Per release | **Yes** (template data) |
| Pre-Prod | Full Copy | Per release | **Yes** (full mask) |
| Prod | Production | N/A | N/A |

**Data Mask Checklist** (Pre-Prod/Full):
- [ ] Identify PII fields: Email, Phone, SSN, DOB, Account Numbers
- [ ] Run Salesforce Data Mask or vendor script
- [ ] Verify mask complete: Sample 10 records per object
- [ ] Restrict access: Only ticket-assigned users until confirmation
- [ ] Update integrations: Point endpoints to non-prod URLs
- [ ] Document in change ticket: Mask completion timestamp, verifier

### 7.3 Segregation of Duties (Technical Enforcement)

```yaml
# GitHub Branch Protection Rules (Enforced)
main:
  required_reviews: 2
  required_reviewers: [platform-team, security-team]
  dismiss_stale_reviews: true
  require_code_owner_reviews: true

release/*:
  required_reviews: 1
  required_reviewers: [release-engineers]

# Deployment Identity Separation
# Developer: Human, writes code, creates PR
# Integration User: Service account, deploys via CI (no UI login)
# Approver: Human, different from developer, clicks "Approve" in GitHub/Change ticket
```

---

## Section 8: Design Patterns for DevOps-Friendly Salesforce

### 8.1 Permission Sets Over Profile Edits
```apex
// Developer asks: "Add field access to Admin profile"
// DevOps Engineer says: "Create permission set instead"
// Result: Mergeable, versionable, auditable
```

### 8.2 One Flow Owner Per Release
```markdown
# Release 2026-11-27
## Flow Ownership
- Credit_Application_Flow: @dev-jane (feature TKT-1001)
- Account_Onboarding_Flow: @dev-bob (feature TKT-1002)
- No other edits to these flows this release
```

### 8.3 Tests Create Their Own Data
```apex
@isTest
static void testCreditCheck() {
    // BAD: Relies on existing data
    // Account a = [SELECT Id FROM Account LIMIT 1];
    
    // GOOD: Creates own data
    Account a = new Account(Name='Test Bank', Type='Corporate');
    insert a;
    
    Credit_Application__c app = new Credit_Application__c(
        Account__c = a.Id,
        Amount__c = 100000
    );
    insert app;
    
    Test.startTest();
    CreditCheckService.run(app.Id);
    Test.stopTest();
    
    // Assertions
}
```

### 8.4 No Hardcoded IDs
```apex
// BAD: Hardcoded ID (different per org)
Id recordTypeId = '012xxx000000000AAA';

// GOOD: Query by name
Id recordTypeId = [SELECT Id FROM RecordType 
    WHERE SObjectType='Account' AND DeveloperName='CB_Corporate' 
    LIMIT 1].Id;

// BETTER: Custom Metadata (deployable, configurable)
CB_Config__mdt config = [SELECT Corporate_Record_Type__c 
    FROM CB_Config__mdt WHERE MasterLabel='Default' LIMIT 1];
Id recordTypeId = config.Corporate_Record_Type__c;
```

### 8.5 Named Credentials for Callouts
```apex
// BAD: Hardcoded endpoint + secret in code
HttpRequest req = new HttpRequest();
req.setEndpoint('https://api.bank.com/v1/credit');
req.setHeader('Authorization', 'Bearer hardcoded_secret');

// GOOD: Named Credential (configured per org)
HttpRequest req = new HttpRequest();
req.setEndpoint('callout:Bank_Credit_API/v1/credit');
// Auth handled by Named Credential automatically
```

### 8.6 Custom Metadata for Feature Flags
```apex
// Deploy feature dark, enable after deploy
CB_Feature_Flag__mdt flag = [SELECT Is_Enabled__c 
    FROM CB_Feature_Flag__mdt WHERE DeveloperName='New_Credit_Engine' LIMIT 1];

if (flag.Is_Enabled__c) {
    NewCreditEngine.run();
} else {
    LegacyCreditEngine.run();
}
```

### 8.7 Bulkified Apex (The 200-Record Test)
```apex
// BAD: Single record processing
trigger AccountTrigger on Account (before insert) {
    for (Account a : Trigger.new) {
        // SOQL inside loop = 200 queries = LIMIT EXCEEDED
        Contact c = [SELECT Id FROM Contact WHERE Email = :a.Email LIMIT 1];
    }
}

// GOOD: Bulkified
trigger AccountTrigger on Account (before insert) {
    // 1. Collect all emails
    Set<String> emails = new Set<String>();
    for (Account a : Trigger.new) {
        emails.add(a.Email);
    }
    
    // 2. Single query
    Map<String, Contact> emailToContact = new Map<String, Contact>();
    for (Contact c : [SELECT Id, Email FROM Contact WHERE Email IN :emails]) {
        emailToContact.put(c.Email, c);
    }
    
    // 3. Process in memory
    for (Account a : Trigger.new) {
        Contact c = emailToContact.get(a.Email);
        // logic here
    }
}
```

---

## Section 9: Rollback Procedures

### 9.1 Rollback Decision Tree

```
PRODUCTION ISSUE DETECTED
         |
         v
    SEVERITY?
    /      \
  MINOR   MAJOR
    |        |
    v        v
Deactivate  STOP BLEEDING
Flow/       (Deactivate automation,
Process     disable triggers if safe)
    |        |
    v        v
Redeploy    VALIDATE PREVIOUS TAG
Last Good   (sf project deploy start --dry-run
Tag         --target-org prod)
    |        |
    v        v
Verify      DEPLOY PREVIOUS TAG
Fix         (sf project deploy start
             --target-org prod)
    |        |
    +--------+
         |
         v
   INCIDENT REVIEW
```

### 9.2 What Git Revert Does NOT Undo
| Scenario | Git Revert Effect | Actual Fix Required |
|----------|-------------------|---------------------|
| Destructive delete ran | Metadata recreated | **Data gone** - restore from backup |
| Post-deploy data script ran | Code reverted | **Rows unchanged** - need reverse script |
| Flow version activated | XML reverted | **Activate previous version** in Setup |
| Package upgraded | Package XML reverted | **Downgrade package** (if beta) or reinstall previous |

---

## Section 10: Interview Drills (From ServiceNow Guide)

| Question | Expected Answer |
|----------|-----------------|
| "Where is the source of truth?" | **Git**. Production is a deploy target. If Setup and Git disagree, that's an incident. |
| "Walk a change to prod." | Feature branch → PR → Dry-run with tests → Merge to release branch → QA deploy → UAT → Prod validation before window → Approval → Quick deploy → Tag → Ticket updated with both deploy IDs. |
| "Hotfix during open release?" | Cut from `main`, not release branch. Merge back to `main` AND open release branch. |
| "Why did this profile deploy fail?" | Profiles are grab bags of access. Two stories conflict. Bad merge changes unintended access. Prefer permission sets. |
| "Flow deploy succeeded but users see old screen." | New version likely not active. Check Setup → Flows → Activate new version. |
| "Validate vs quick deploy?" | Validate doesn't change org. Quick deploy applies a passed validation inside platform window, keeping change window short. |
| "Unlocked vs managed package?" | Unlocked = yours, versioned, internal modules. Managed = upgrade only, don't edit. Packaging entire org day one = not a plan. |
| "What do you hand an auditor?" | Ticket, diff, approver ≠ author, validation ID, prod deploy ID, test run, tag, Full sandbox mask evidence. |

---

## Appendix: Key Commands Reference

### Salesforce CLI (`sf`)
```bash
# Authentication
sf org login web --alias dev
sf org login jwt --client-id xxx --jwt-key-file key.pem --username user@bank.com --alias ci

# Metadata
sf project retrieve start --metadata "PermissionSet:Name,ApexClass:Name" --target-org dev
sf project deploy start --manifest manifest/package.xml --target-org qa --dry-run
sf project deploy start --manifest manifest/package.xml --target-org prod --test-level RunLocalTests

# Tests
sf apex run test --test-level RunLocalTests --code-coverage --wait 60 --target-org qa
sf apex run test --test-level RunSpecifiedTests --tests "TestClass1,TestClass2" --target-org prod

# Packages
sf package version create --package "MyPackage" --code-coverage --wait 30
sf package install --package 04tXXXXXXXXXXXX --target-org uat --wait 30

# Org Info
sf org display --target-org prod
sf org list
```

### Git Operations
```bash
# Release branch
git checkout main
git pull
git checkout -b release/2026-11-27
git push -u origin release/2026-11-27

# Hotfix
git checkout main
git pull
git checkout -b hotfix/TKT-1234
# fix...
git commit -am "fix: hotfix for TKT-1234"
git push -u origin hotfix/TKT-1234
# PR to main + release branch

# Tag production deploy
git tag -a "release-2026-11-27-abc123" -m "Prod deploy abc123"
git push origin release-2026-11-27-abc123
```

---

*Documentation generated 2026-11-14 for TSOM-Salesforce-DevOps-Learning repository*
*Mapped to Scotiabank Requisition 276046 and ServiceNow DevOps Engineer Track*