# Metadata dependencies and deployment constraints

**Merge target:** section 13.4 and 13.5 of the downstream page, plus section 2 (failure table) and section 7 (conflict clinic). This is the research backing the posting's "metadata dependencies and deployment constraints" requirement.

## 1. The mental model

The Metadata API resolves dependencies **inside the payload**. It does not invent a parent that is missing from both the payload and the target. If a child references a parent the target does not have, the deploy fails with an error such as `invalid cross reference id`, `entity not found`, or "no such column."

A deploy is therefore a graph problem, not a file-copy problem.

## 2. Dependency graph

| Child component | Depends on | Typical error if parent is missing |
|---|---|---|
| Custom field | Custom or standard object | `no such column` / "field does not exist" |
| Validation rule | The fields it references | `no such column` |
| Record type | Object, business process, picklist values | `invalid cross reference id` |
| Page layout | Object, fields, related lists, record types | `invalid cross reference id` |
| Layout assignment | Profile or permission set + record type | Deploy succeeds; users see the wrong page |
| Permission set | Objects, fields, Apex classes, Flows, tabs, custom permissions | `entity not found` / missing component |
| Apex class | Other classes, custom objects/fields, metadata types | Compile failure in the target |
| Trigger | Handler class, object | Compile failure / `entity not found` |
| Flow | Objects, fields, Apex classes, subflows, custom metadata | Flow deploys but fails at runtime |
| LWC | Static resources, Apex controllers, custom labels | Component fails to load |
| FlexiPage (Lightning page) | Components, objects, fields | Page deploys but is not the active page |
| Custom metadata type | Records and references | `entity not found` |
| Named credential | External credential, auth provider, certificate | Callout fails at runtime |
| Connected app | Certificate, OAuth scopes | Login/auth fails |
| Unlocked/managed package | Its dependency versions | Install fails on a missing dependency |
| Sharing rule | Object, roles, groups | Rule deploys but does not grant the expected access |
| Queue / routing | Object, users, roles | Records route to the wrong place |

## 3. The rules that prevent most failures

1. **Deploy parent and child in the same payload when both are new.** Object + field + record type + layout + permission set is one reviewable unit. Do not deploy the object on Monday and the permission set "later."
2. **`package.xml` is a list, not a promise of order.** The API orders by metadata type internally, but an absent dependency is still absent.
3. **A dry-run against the target is the only honest dependency test.** A green deploy to Dev says nothing about UAT.
4. **Read the component name in the error and search the repo for the reference.** Add the missing parent; do not retry the same payload.
5. **Vendor dependency analysis is a suggestion, not an approval.** Gearset's problem analysis and Copado's dependency view can surface the missing component; a human reviews what was added.
6. **Do not use "ignore conflicts" in production.** It hides a real divergence between Git and the org.

## 4. A manifest that ships the whole record-type story

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Package xmlns="http://soap.sforce.com/2006/04/metadata">
  <types>
    <members>Invoice__c</members>
    <name>CustomObject</name>
  </types>
  <types>
    <members>Invoice__c.Status__c</members>
    <name>CustomField</name>
  </types>
  <types>
    <members>Invoice__c.Invoice_Layout</members>
    <name>Layout</name>
  </types>
  <types>
    <members>CB_Invoice_User</members>
    <name>PermissionSet</name>
  </types>
  <version>60.0</version>
</Package>
```

Use your project's API version, not the one in the example. The point is the shape: parent, child, assignment, and access in one reviewable unit.

## 5. Deployment constraints

These are the things a deploy cannot fix by including another component.

| Constraint | What it means | What you do instead |
|---|---|---|
| Feature not enabled in target | The metadata is valid but the target cannot accept or use it | Enable and license the feature first; re-validate |
| Secret is not metadata | Named credential passwords, private keys, and some connected-app values are not retrieved | Re-enter per org, use external credentials, or a secret manager; never commit them |
| Certificate private key is not exported | You can deploy the public cert, not the private key | Import the private key per org; test JWT auth |
| Managed package component is read-only | You cannot edit its Apex or metadata in Git | Configure around it, extend it, or upgrade the package |
| Profile is a monolith | Two stories editing the same profile conflict; a bad merge changes access | Ship permission sets; decompose profiles with a tool; require a second reviewer |
| Flow XML does not merge | Two developers on one Flow lose work | One owner per Flow per release; split into subflows |
| Destructive changes are separate | Deleting metadata is not "it was absent from the folder" | Use `destructiveChanges.xml`; accept that records on a deleted object are gone |
| Tests and 75% coverage | Production rejects Apex without passing tests and coverage | Run `RunLocalTests` or named tests; fix the tests, do not lower the bar |
| API version mismatch | The target may not support the source API version | Align `sourceApiVersion`; validate before the window |
| Record type assignment | The record type file is not the assignment | Deploy layout assignment and visibility in the same payload |
| Lightning page activation | A FlexiPage can deploy and still not be the active page | Activate it for the app/record type in the target |
| Named credentials / remote sites / certs | Endpoints and trust are per org | Configure per sandbox; include it in the pre-flight checklist |
| Data is not metadata | Records, attachments, and customer data do not ride in a metadata deploy | Use a data migration/seed process; mask and ticket it |
| Change Sets only work between related orgs | No Git diff, no CLI, no rollback | Use the CLI or a vendor pipeline with Git in front |
| Sandbox refresh overwrites | A refresh replaces metadata and data | Re-deploy from Git and re-run masking after refresh |
| Deploy user permissions | The integration user needs API access and deploy permissions | Use a dedicated user with a least-privilege deploy permission set |
| Concurrent deploys | Two deploys to one org can conflict or queue unpredictably; only one deployment runs at a time, and queued deployments are not guaranteed to run in submission order | Serialize per org with a concurrency group or deployment lock; submit in order one at a time |
| Hard-coded ids | The id in Dev is not the id in UAT | Use custom metadata, custom settings, or a query by developer name |
| `NoTestRun` in production | Rejected when the payload contains Apex | Use `RunSpecifiedTests` or `RunLocalTests` |
| "Ignore conflicts" | Hides a real divergence between Git and the org | Do not use it in production; fix the source of truth |

## 6. Destructive changes

A delete is a separate manifest:

```bash
sf project deploy start \
  --manifest manifest/package.xml \
  --post-destructive-changes manifest/destructiveChanges.xml \
  --target-org qa
```

Use pre-destructive changes only when the delete must happen before the add (for example, a rename that would collide). A delete in production is not undone by Git. Rollback of a delete means recreating the metadata, and any records that lived on a deleted object are gone.

## 7. Test levels — five, not four

The Metadata API `TestLevel` enum has five values. The older four-level answer is incomplete.

| Level | What it runs | When to use |
|---|---|---|
| `NoTestRun` | No tests | Development environments only; rejected in production when the payload contains Apex |
| `RunSpecifiedTests` | Only the tests you name | Fast, targeted validation; each deployed class/trigger must be covered to 75% by those tests |
| `RunRelevantTests` (Beta) | Only tests relevant to the deployment payload, identified from the payload and its dependencies | API version 66.0+; Apex-heavy deployments where you want test time to scale with the payload; annotate test classes for fine-grained control |
| `RunLocalTests` | All tests in the org except managed/unlocked package tests | The default for production deployments that include Apex; slower but honest |
| `RunAllTestsInOrg` | All tests, including managed-package tests | Rarely; very slow and usually not necessary for a release |

Source: [Metadata API `deploy()`](https://developer.salesforce.com/docs/platform/api-metadata/references/file-based-calls/meta-deploy.html) and the [Salesforce CLI deploy messages](https://github.com/salesforcecli/plugin-deploy-retrieve/blob/main/messages/deploy.metadata.md), accessed 2026-11-14.

**Interview line.** "There are five test levels. `RunRelevantTests` is the Beta level that runs tests relevant to the payload on API 66.0+. I still use `RunLocalTests` when I need the broadest honest gate before production."

## 8. Troubleshooting method

```text
1. Save the full error and the deploy id.
2. Identify the component and the missing reference.
3. Search the repo for the reference; is the parent in the payload?
4. Add the parent to the same payload, or deploy the parent first.
5. Re-run the dry-run against the same target.
6. If a test failed, read the stack trace; do not change the test level to hide it.
7. If coverage failed, find the uncovered lines.
8. If it is a managed package, stop; upgrade or configure around it.
9. Only then change code.
```

## 9. Error-to-fix quick table

| Error | First check | Fix |
|---|---|---|
| `no such column` / field does not exist | Is the field in the payload? Is it in the target? | Add the field or deploy the object+field first |
| `invalid cross reference id` | Record type, layout, or business process parent | Add the parent to the same payload |
| `entity not found` | Apex/Flow dependency or missing metadata type | Deploy the dependency or remove the reference |
| Test failure only in UAT/Prod | Test uses org data, a profile, a record type, or a setting that exists only in Dev | Make the test create its own data; use the target's test level |
| Coverage below 75% | Untested branches, managed package exclusion | Add meaningful tests; do not lower the bar |
| `CANNOT_MODIFY_MANAGED_OBJECT` | You tried to change a managed component | Configure around it or upgrade the package |
| Deploy succeeds but Flow is old | New version is not active | Activate the version or deploy as active |
| Record type deploys but users cannot create | Missing business process, picklist value, layout assignment, or visibility | Deploy all four together |
| Layout deploys but page is wrong | Layout not assigned; Lightning page not activated | Deploy the assignment and activate the page |
| Callout works in Dev, fails in UAT | Missing named credential secret, external credential, certificate, remote site, or endpoint | Configure per org |
| `REQUEST_LIMIT_EXCEEDED` | API usage, async queue, or concurrency | Check Setup → Company Information → API Usage; reduce/serialize/off-peak |

## 10. What to merge

**Merge:** the dependency graph, the six rules, the record-type manifest, the constraints table, the destructive-change warning, the troubleshooting method, and the error-to-fix table.

**Compress:** the full graph if the page is already long; keep the rows that match the posting (profiles, permission sets, record types, layouts, Flows, Apex).

**Do not merge:** any claim that a specific vendor's dependency analysis is authoritative. It is a suggestion.
