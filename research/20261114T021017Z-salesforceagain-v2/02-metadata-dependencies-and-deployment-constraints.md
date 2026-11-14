# 02 — Metadata Dependencies & Deployment Constraints

> **Scope:** "Understanding of Salesforce limits, metadata dependencies, and deployment constraints" + "Resolve deployment conflicts" + "Troubleshoot deployment failures and dependency issues."
> **Companion:** `01-limits-governors-and-system-properties.md` covers numeric limits. This file covers **ordering, reference graphs, and the failure catalogue**.

---

## 1. The one-sentence model

A Salesforce deploy is a **set of instructions applied to an existing schema**. The Metadata API checks every reference in your payload against (a) the payload and (b) what already exists in the target. A missing reference fails the deploy; a present reference with missing *assignment* succeeds but leaves the feature broken. Release engineering is therefore **dependency management plus post-deploy verification**.

---

## 2. The dependency graph you must be able to draw

<details>
<summary><strong>2.1 Object-level dependency chain (left must exist before right)</strong></summary>

```text
Custom Object
  └─ Fields (including formula/logic that reference other fields)
       ├─ Validation Rules (reference fields)
       ├─ Record Types (select picklist values / business processes)
       │    └─ Business Processes (Sales/Support/Lead/...)
       ├─ Page Layouts (reference fields + record types)
       │    └─ Layout Assignments (per profile / record type)
       ├─ Compact Layouts
       ├─ Field-Level Security (profile / permission set)
       ├─ List Views (reference fields + filters)
       └─ Search Layouts

Lightning Record Page (FlexiPage)
  └─ Activation / assignment (app + record type + profile)
       └─ depends on fields, components, Apex/LWC bundles

Custom Tab
  └─ Custom App (tab membership)
       └─ Profile / Permission Set (app + tab visibility)

Apex Class
  ├─ referenced Apex Classes / interfaces
  ├─ referenced custom objects/fields/SObjectType
  ├─ Custom Metadata Types / Custom Settings
  └─ Test Class (must be in payload or already present)

Flow
  ├─ referenced objects/fields
  ├─ referenced Apex (invocable)
  ├─ subflows
  ├─ custom metadata/settings
  └─ Flow Definition (active version pointer)

Permission Set
  ├─ objects/fields (must exist)
  ├─ Apex classes (must exist)
  ├─ Flows (must exist)
  └─ Custom permissions / tabs / apps

Profile
  └─ everything a permission set does, plus layout assignments + login IP ranges
```

**Interview move:** draw this on a whiteboard. It immediately explains most "invalid cross reference id" errors.
</details>

<details>
<summary><strong>2.2 The deploy order that avoids most failures</strong></summary>

A safe default order for a mixed payload:

1. **Objects** (custom objects, custom metadata types, custom settings)
2. **Fields** (including formula/roll-up, but watch references)
3. **Picklist values / global value sets / business processes**
4. **Record types**
5. **Validation rules**
6. **Layouts** (page, compact, search) and **Lightning pages (FlexiPages)**
7. **Apex classes** (dependency order), **LWC bundles**, **Aura bundles**
8. **Flows** (and subflows)
9. **Custom tabs, apps**
10. **Permission sets / permission set groups**
11. **Profiles** (thin deltas only)
12. **Layout assignments / FlexiPage activation / app assignments**
13. **Sharing rules / OWD** (after objects/fields; expect recalculation)
14. **Custom metadata records / custom settings data**
15. **Named credentials / external credentials / remote sites** (or verify they exist)
16. **Reports / dashboards / folders**

> The Metadata API does not guarantee your order within a single deploy, but it does resolve many intra-payload dependencies. When it can't, split into **phased deploys** in this order. Tools (Gearset/Copado/AutoRABIT) implement a version of this ordering for you — know what they do so you can debug when they get it wrong.

</details>

<details>
<summary><strong>2.3 Renames are not renames</strong></summary>

Salesforce metadata generally does **not** support an in-place rename in a deploy. A "rename" is:

1. Create the new component (new API name).
2. Migrate references (formulas, layouts, Apex, Flows, reports).
3. Deploy the new component + references.
4. Deploy a **destructive change** to remove the old component (pre- or post-destructive).
5. Migrate data if it was a field (data migration is **not** metadata).

**Consequence:** a rename is a multi-step, multi-deploy change with a data component. Never let a developer "just rename it in the sandbox and deploy."

</details>

---

## 3. The failure catalogue (error string → cause → first check)

<details>
<summary><strong>3.1 Compile / reference errors</strong></summary>

| Error you see | Usual cause | First check |
|---|---|---|
| `Invalid cross reference id` | Record type / layout / business process assignment points at something missing | Deploy the parent (object, record type, layout) in the same payload |
| `no such column` / `field does not exist` | Flow/layout/formula/Apex references a field not in payload and not in target | Add the field to the payload |
| `entity not found` | Apex references an sObject not deployed | Add the object |
| `Variable does not exist` / `Method does not exist` | Apex dependency class/method missing | Deploy the dependency or remove the reference |
| `Duplicate value found` | Unique field / duplicate rule conflict on deploy of data | Deploy metadata without data; handle data separately |
| `Cannot modify managed object` | You edited a managed-package component | Configure around it or upgrade the package |
| `Insufficient access rights on cross-reference id` | Deploying user lacks access to a referenced record (e.g., record type) | Use an integration user with Modify All Data / appropriate perms |
| `The package is not valid` / `Unknown user permission` | Profile/permset contains a permission not available in target (edition/feature) | Remove or feature-gate the permission |
| `Apex compile failure` | Missing dependency or API version mismatch | Add dependency; check `sourceApiVersion` |
</details>

<details>
<summary><strong>3.2 Test failures that look like deploy failures</strong></summary>

| Symptom | Cause | Fix |
|---|---|---|
| Passes in Dev, fails in QA/UAT | Test reads existing org data (`LIMIT 1`) or relies on a record type/profile present only in Dev | Tests create their own data; no org-data assumptions |
| `Too many SOQL queries: 101` inside a test | Handler not bulkified; test inserts 200 records | Bulkify; query once |
| `UNABLE_TO_LOCK_ROW` in tests | Parallel DML on same rows; or `SeeAllData` | Avoid `SeeAllData`; isolate data |
| Coverage below 75% | New Apex not covered | Add tests; coverage is org-wide but new code must be covered by the tests you run |
| `Test execution time exceeded` | Slow tests, callouts in tests | Mock callouts (`HttpCalloutMock`), reduce data |
| Managed package test failures | `RunAllTestsInOrg` runs package tests | Use `RunLocalTests` for release validation |

> **Rule:** production rejects the deploy if tests fail, even if the metadata is valid. Test design is part of release engineering.
</details>

<details>
<summary><strong>3.3 "Green deploy, broken feature" (not an error — a constraint)</strong></summary>

| Symptom after a green deploy | Missing piece | Where to fix |
|---|---|---|
| Users can't create a new record type | Record type not assigned to profile/permission set; or no page layout assignment | Setup > Object > Record Types / Page Layouts; Permission Sets |
| Users see an old layout | Layout assignment not deployed; or Lightning page not activated | Setup > Object > Page Layouts; Lightning App Builder activation |
| Flow change has no effect | New Flow version deployed as **Draft**, not Active | Setup > Flows > version → Activate |
| Permission set has no effect | Not assigned to users | Setup > Permission Sets > Manage Assignments |
| Custom metadata record missing | Data not deployed (metadata type ≠ records) | Deploy custom metadata records; or data tool |
| Callout 401 | Named/External Credential principal not configured in target | Setup > Named Credentials / External Credentials |
| Validation rule not firing | Rule inactive, or field-level security hides the field | Setup > Object > Validation Rules; FLS |
| Record page shows old components | FlexiPage not activated for app/record type | Lightning App Builder > Activation |

**Release checklist:** for every deployed component, name the **assignment/activation** step. If you cannot, you have not finished the change.
</details>

---

## 4. Profiles and permission sets (the #1 conflict source)

<details>
<summary><strong>4.1 Why profiles conflict</strong></summary>

A profile XML is a grab-bag: user permissions, object permissions, field permissions, layout assignments, record-type visibility, tab visibility, app visibility, login hours, login IP ranges, and more. Two branches editing the same profile produce a conflict in a file that is thousands of lines long and not human-reviewable at a glance. A bad merge can **grant or revoke access nobody reviewed**.

**What the role expects you to say:** *"We stop putting story access in profiles. We ship a permission set per feature/persona and deploy that. Profiles are only touched for profile-only settings, with a second reviewer reading the permission diff."*
</details>

<details>
<summary><strong>4.2 The permission-set strategy</strong></summary>

| Pattern | Use |
|---|---|
| One permission set per **feature** | Small, reviewable, deployable with the story |
| One permission set per **persona/job function** | Bundled into a **permission set group** |
| Permission set **group** | Assigns a job function's set of sets; avoids a new monolith |
| Muting permission set | Temporarily revoke within a group |
| Profile | Only for profile-only settings (layout assignment historically, login hours/IP, default app) |

**Anti-pattern:** one giant `CB_Admin` permission set that every story edits → you recreated the profile merge problem.
</details>

<details>
<summary><strong>4.3 Deploying profiles safely when you must</strong></summary>

- Deploy a **thin delta**, not the whole profile, where the tool supports profile decomposition (Gearset does; Copado/AutoRABIT have equivalents).
- **Diff the permission changes** and have a second person read them.
- Never hand-merge a 10,000-line profile XML.
- Watch for **org-specific values** in profiles (user licence–specific permissions) that should not travel.
- Deploy profiles **after** objects/fields/classes/flows they reference.
- Expect **timeouts** on large profiles; split or use a tool with profile-aware deploys.
</details>

<details>
<summary><strong>4.4 Permission set vs profile — the comparison table</strong></summary>

| Aspect | Profile | Permission Set |
|---|---|---|
| Required per user | Exactly one | Zero or more |
| Can grant access | Yes | Yes (additive only) |
| Can deny/remove access | Yes (relative to baseline) | No (use muting sets in a group) |
| Merge-friendliness | Poor (huge, noisy) | Better if small |
| Deploy size/time | Large | Smaller |
| Typical role in a modern org | Baseline only | Feature/persona access |
| Record-level sharing | No (roles/OWD/rules do that) | No |
| Layout/app/tab assignment | Yes (historically) | Yes for many settings |

**Security model reminder:** record access = OWD + role hierarchy + sharing rules + manual sharing + teams + territory (if enabled) + Apex sharing. Profiles/permsets control **object and field** access, not row access.
</details>

---

## 5. Record types, page layouts, and Lightning pages

<details>
<summary><strong>5.1 The minimum viable record-type payload</strong></summary>

Deploy in one payload (or in this order):

1. Object + fields used by the record type's picklists/business process.
2. Business process (e.g., Support Process, Sales Process) and picklist values.
3. **Record Type** itself.
4. **Page Layout** for that record type.
5. **Page Layout Assignment** (profile + record type).
6. **Permission Set / Profile** granting record-type visibility.
7. **Lightning Record Page** (if used) + **activation** for app/record type.
8. **Compact Layout** assignment (if used).

Miss 5 or 6 → "deploy succeeded, users can't use it."
Miss 7 → "Lightning users see the classic layout."
</details>

<details>
<summary><strong>5.2 Classic layout vs Lightning record page (FlexiPage)</strong></summary>

- **Page Layout** = classic layout; still used for some components and for Classic, and for layout assignment.
- **FlexiPage / Lightning Record Page** = the Lightning Experience page built in Lightning App Builder. It must be **activated** for specific apps/record types/profiles.
- Testers say "the page is wrong" when the **FlexiPage was never activated**, not when the layout failed.

**Check:** Setup > Lightning App Builder > open page > Activation, or Object Manager > [Object] > Lightning Record Pages.
</details>

<details>
<summary><strong>5.3 Record type visibility vs layout assignment (two different things)</strong></summary>

- **Record type visibility** (profile/permset): can the user *see/select* this record type?
- **Page layout assignment** (profile + record type): which layout renders for that user/record type?

Both are needed. A user can see the type but get the wrong layout, or get the right layout but not see the type.
</details>

---

## 6. Flows and Apex dependencies

<details>
<summary><strong>6.1 Flow-specific constraints</strong></summary>

- **XML does not merge.** Two developers editing the same flow lose one side.
- **Version semantics:** a flow has versions; only one is **Active**. A deploy can create a new version that is Draft. Verify activation.
- **Flow Definition** points to the active version; deploying the flow and the definition matters.
- **Subflows** must be deployed with (or before) the parent.
- **Invocable Apex** referenced by a flow must exist.
- **Custom metadata/settings** referenced must exist or the flow faults at runtime.
- **Before-save vs after-save:** before-save flows are faster and avoid extra DML; after-save flows can update other records. A flow built as after-save that should be before-save will time out under volume.

**Mitigation:** one owner per flow per release, or split into subflows.
</details>

<details>
<summary><strong>6.2 Apex dependency ordering</strong></summary>

- Deploy a class with every class/interface it references (or ensure they exist in target).
- Deploy the **test class** in the same payload (or it must already exist and be valid).
- Inner classes, enums, and `SObjectType` references are dependencies too.
- Trigger + handler + service + selector + test is the usual bundle.
- API version must be compatible with the target.

**Failure signature:** `Method does not exist` or `Variable does not exist` at compile time in the target → missing member, not a syntax error in your file.
</details>

<details>
<summary><strong>6.3 Order of execution (why before/after matters to the release)</strong></summary>

A simplified order:

1. Loads the original record.
2. System validation (required fields, field format).
3. **Before-save Flows / before triggers** (can modify the same record without a second DML).
4. Custom validation rules.
5. Duplicate rules.
6. **After-save Flows / after triggers** (can modify other records; changes cause another save cycle).
7. Assignment rules, auto-response, workflow rules.
8. Escalation rules.
9. Roll-up summaries recalculate.
10. Sharing recalculation.
11. Commit.

**Release-engineering angle:** a before-trigger cannot see a roll-up that recalculates later. A change that "worked in Dev" can fail under volume if it creates recursive save cycles.
</details>

---

## 7. Destructive changes (deletes)

<details>
<summary><strong>7.1 How deletes actually work</strong></summary>

- A component **not present** in your payload is **not** deleted. Deletion requires explicit **destructive changes** metadata (`destructiveChanges.xml` / `destructiveChangesPre.xml` + `package.xml`).
- **Pre-destructive** deletes before the deploy (use when a rename would collide).
- **Post-destructive** deletes after the deploy (the common case).
- Deletes are **not** undone by a Git revert. Rollback means recreating metadata; **records on a deleted custom object are gone**.
- Deleting a field deletes its data (after the recycle bin / if not restored).
- Deleting a custom object can cascade to children (master-detail).

**Rule:** a destructive change is a separate, reviewed, ticketed deploy with a data backup plan. Never bundle a delete into a "normal" release without calling it out.
</details>

<details>
<summary><strong>7.2 Delete checklist</strong></summary>

- [ ] Confirm nothing references the component (Apex, Flow, layout, report, integration, validation rule).
- [ ] Confirm data can be lost (or is backed up).
- [ ] Confirm the delete is post- or pre-destructive, and why.
- [ ] Confirm the change ticket names the data impact.
- [ ] Confirm rollback plan is "recreate metadata + restore data," not "git revert."
- [ ] Deploy and verify the component is actually gone.
- [ ] Remove references from Git so the next full retrieve does not resurrect it.
</details>

---

## 8. Dependency analysis tooling

<details>
<summary><strong>8.1 What tools do for you (and what they miss)</strong></summary>

| Tool | Dependency help | Limitation |
|---|---|---|
| **Salesforce CLI** | `sf project deploy start` resolves many intra-payload deps; error messages name the missing component | No visual graph; you must read errors |
| **Gearset** | Dependency analysis, "missing dependency" suggestions, Flow Navigator, profile decomposition | Can still miss runtime/assignment deps |
| **Copado** | Deployment dependency tracking, commit/back-promotion | Depends on metadata being committed correctly |
| **AutoRABIT ARM** | Compare + dependency resolution, pre/post destructive | Same class of tool |
| **DevOps Center** | Git + work items + promotion; surfaces conflicts | GitHub-first; unsupported metadata types |
| **SFDX plugins** (e.g., dependency/community plugins) | Generate a dependency tree | Plugin quality varies; verify output |

**What none of them fix:** assignment/activation (layout assignment, record type visibility, FlexiPage activation, permission set assignment). That is your post-deploy checklist.
</details>

<details>
<summary><strong>8.2 A practical pre-deploy dependency audit</strong></summary>

1. List every component in the payload (`sf project deploy preview` / tool diff).
2. For each, list its references (object, fields, classes, flows, metadata types, credentials).
3. Confirm each reference is **in the payload or already in the target**.
4. Confirm each component's **assignment/activation** step is in the runbook.
5. Confirm **destructive changes** are explicit and reviewed.
6. Confirm **test class coverage** for any Apex.
7. Confirm **API version** compatibility.
8. Confirm **permission diff** reviewed by a second person.
</details>

---

## 9. Deployment constraints by strategy

<details>
<summary><strong>9.1 Change sets</strong></summary>

**Constraints**

- Only between related orgs (sandbox ↔ production, or same-hub sandboxes).
- Component selection is manual; easy to miss dependencies.
- No reviewable diff; no branch; no tag; no rollback.
- Profile XML you cannot merge.
- Inbound change set must be validated and deployed; size limits apply.

**Verdict for this role:** explain it, then retire it. Use CLI or a Metadata-API tool with Git in front.
</details>

<details>
<summary><strong>9.2 Unpackaged metadata from Git (the default for a large bank org)</strong></summary>

**Constraints**

- The whole repo can become one unreviewable tree.
- Deploy order is on you (or your tool).
- Delete tracking needs destructive manifests.
- No versioning/upgrade semantics.

**Verdict:** still the right default for a large existing org; add packages at real boundaries later.
</details>

<details>
<summary><strong>9.3 Unlocked packages</strong></summary>

**Constraints**

- Requires a Dev Hub.
- Versioned; upgradeable; dependency list.
- Org-dependent unlocked packages are easier to adopt but cannot install elsewhere without the same unpackaged deps.
- Not a silver bullet for "package the entire org."

**Verdict:** use at **real module boundaries** (a credit-application module, not "all of Sales Cloud").
</details>

<details>
<summary><strong>9.4 Managed packages</strong></summary>

**Constraints**

- You upgrade them; you do not edit their metadata.
- `CANNOT_MODIFY_MANAGED_OBJECT` if you try.
- Package upgrades can change behaviour; test before production.
- Namespace prefix changes names.

**Verdict:** treat upgrades as releases with their own validation and rollback (previous version install, if supported).
</details>

---

## 10. Interview drills

1. **Draw the dependency chain for a new record type.** Object → fields → business process/picklists → record type → layout → layout assignment → record type visibility → (FlexiPage + activation) → permission set.
2. **Why did the record type deploy "succeed" but users can't use it?** Missing record type visibility on profile/permset and/or layout assignment.
3. **Why do profiles conflict?** They are huge, noisy, and contain access; two edits collide and a bad merge changes permissions.
4. **How do you delete a field safely?** Explicit destructive change, second review, data backup, verify references gone, ticket, recreate-to-rollback plan.
5. **How do you deploy Apex with dependencies?** Class + dependencies + test in one payload; read compile errors as missing-member, not syntax.
6. **What do tools not fix?** Assignments/activation and post-deploy verification.
7. **What is the order of execution and why does it matter?** Before-save vs after-save; roll-ups recalc later; recursion risk under volume.
8. **How do you handle a rename?** New component + migrate references + destructive delete + data migration; it is multi-deploy.
9. **How do you prove a deploy is safe?** Validation against prod-like org, named tests, dependency audit, permission diff review, assignment checklist, rollback tag.
10. **What breaks first at scale?** Missing dependencies and unassigned metadata, then runtime limits (see `01`).

---

**Next:** `03-devops-tools-ui-walkthroughs.md` — where these actions live in Gearset, Copado, AutoRABIT, and DevOps Center.
