# Other limits, system settings, and org properties

**Merge target:** section 13.2 and 13.3 of the downstream page. This file covers the limits that are not per-transaction, and the per-org switches that a metadata deploy does not carry.

## 1. The five limit families

| Family | Scope | Example | Where it shows up |
|---|---|---|---|
| Apex governor limits | One transaction | 100 SOQL, 150 DML, 10 MB heap | Runtime `System.LimitException`; see `governor-limits.md` |
| Org/platform allocations | Whole org, often per 24 hours | API requests, async Apex, storage, concurrent long-running transactions | Pipeline or integration gets 403 / `REQUEST_LIMIT_EXCEEDED` |
| Metadata/deploy ceilings | One deploy/retrieve | Component count, payload size, test runtime | Large release fails or times out |
| Feature/configuration caps | Whole org | Custom objects, fields, permission sets, flows, validation rules | A story cannot add the component it needs |
| System settings / org properties | Whole org | Feature enablement, SSO, named credentials, certificates, email deliverability | Deploy succeeds, feature/auth fails |

## 2. API request limits

**What they are.** Every REST, SOAP, Bulk, and Metadata API request consumes the org's daily API allocation. The allocation depends on edition, licence types, and user count. The integration user does not get a separate unlimited bucket.

**Why a release engineer cares.** A pipeline that retrieves the whole org, runs a full test suite, and polls a deploy every second can consume a meaningful slice of the day's API calls. If the pipeline shares a user with production integrations, a busy release day becomes an integration outage.

**How to inspect.** Setup → Company Information → API Usage shows the last 24 hours and the allocation. The CLI can show org limits with `sf org list limits` and `sf limits api display` (confirm the command in your CLI version).

**How to stay under it.**
- Use delta manifests (`sfdx-git-delta`) instead of full retrieves.
- Use `--wait` on deploy/test commands instead of a tight poll loop.
- Schedule nightly validation off-peak.
- Use a dedicated integration user for CI.
- Cache what does not change.
- Split very large test suites; do not run `RunAllTestsInOrg` on every commit.

## 3. Metadata and deploy ceilings

Salesforce caps what one deploy or retrieve can contain. The commonly cited ceiling is **10,000 components and a 400 MB payload**; re-check the current Metadata API limits page for your release before you quote it.

**Why it matters.** A full-org retrieve or deploy is the classic way to hit the ceiling. It is also the classic way to make a release unreviewable. Delta manifests, package directories, and split payloads are the design response.

**Related constraints:**
- Test runtime: a large `RunLocalTests` can take a long time. Validate before the window and quick-deploy inside it.
- Coverage: production requires 75% when the payload contains Apex.
- API version: the target must support the source API version.
- Destructive changes: they are a separate manifest, not a side effect of absence.

## 4. Storage and data limits

Setup → Company Information → Storage shows data and file storage. Sandboxes have their own storage; a Developer sandbox cannot hold production-scale data. Tests and data loads consume storage. A full copy of production data into a sandbox is a licence, cost, and privacy decision, not just a technical one.

## 5. Concurrency limits

- Long-running synchronous transactions over 5 seconds: 10–50 concurrent, based on licences.
- Batch Apex: 5 concurrent jobs, 1 concurrent `start`, 100 holding in the flex queue.
- Deployments are long-running operations. Two deploys to one org can queue or conflict; serialize per org with a CI concurrency group or a deployment lock.

## 6. Email and Flow limits

- `sendEmail` is limited to 10 calls per transaction; org-wide daily email limits apply.
- Sandboxes often block email. Do not use email as a test signal; stub it.
- Flow has its own interview, scheduled-run, and version-history limits. A Flow that queries per record is still a limit problem even if the limit is not an Apex governor.

## 7. Custom object, field, and permission-set caps

Editions allocate maximum custom objects, fields, tabs, apps, and permission sets. A story can be valid metadata and still be blocked by the org's allocation. Check the edition allocation and the current usage before you promise a field. Permission-set sprawl is a design problem, not a platform cap you can ignore.

## 8. "System properties" — the per-org switches

In this research, "system properties" means the per-org settings that behave like platform switches: feature enablement, org preferences, endpoints, certificates, and secrets. They are not business data, and many do not travel cleanly in a metadata deploy.

| Setting / property | Setup path | Deployable like metadata? | Release consequence |
|---|---|---|---|
| Feature enablement: Person Accounts, Multi-Currency, CPQ, Field Service, Shield, Revenue Cloud, Sites, Omni-Channel | Feature Settings / Company Information / product settings | Usually an org switch, not a file | Dependent metadata fails or does nothing until the feature is enabled and licensed in the target |
| Company Information: org id, locale, time zone, default currency | Company Information | Org-specific | Never copy production's org id or locale into a sandbox |
| System Settings | Settings → System Settings | Some `*Settings` metadata types | Org-wide behaviour; review the diff, do not deploy blind |
| Apex Settings | Apex Settings | `ApexSettings` where supported | Debug-log retention and other behaviour differ by environment |
| Session Settings | Session Settings | `SessionSettings` | Timeout/caching changes can log users out or weaken security |
| Password and login policies | Security → Password Policies; Login IP Ranges | Some deployable, some org-specific | Do not weaken production policy to make a CI runner work; allowlist the runner |
| Connected Apps / External Client Apps | App Manager | Metadata plus per-org consumer key, secret, certificate | The consumer key is per org; the JWT certificate must be uploaded per org |
| Named Credentials / External Credentials | Named Credentials | Endpoint metadata; the secret is not retrieved | The callout works in Dev and fails in UAT because the secret/principal is missing |
| Remote Site Settings | Remote Site Settings | `RemoteSiteSetting` | Often org-specific; a missing entry blocks a callout at runtime |
| Certificates and Keys | Certificate and Key Management | Public certificate only; private key is not exported | JWT auth and mutual TLS fail until the private key is imported per org |
| Email Deliverability | Email Deliverability | Org setting, not normal metadata | Sandboxes often block email; choose the test setting deliberately |
| SSO / SAML | Single Sign-On Settings | Metadata plus IdP certificate | Sandbox IdP differs; test login before inviting UAT users |
| Sites / Digital Experiences / Guest User | Sites / Digital Experiences | Metadata plus per-org configuration | Guest-user access is a security review item |
| Sharing Settings / OWD | Sharing Settings | Object `sharingModel` plus `SharingRules` metadata | A deploy can widen data access; prove it with a real low-privilege user |
| API version / feature compatibility | Apex Classes; Company Information; project config | Project setting, not a deploy file | Align `sourceApiVersion` with the target |

## 9. Pre-flight checklist for a target org

1. Is the feature licensed and enabled?
2. Are the settings metadata types compatible with the target?
3. Are the named credential secrets, external credentials, and certificates present?
4. Are endpoints pointed at non-production systems?
5. Is email deliverability set for the test (and not sending to customers)?
6. Has SSO been tested with a real sandbox user?
7. Does the integration/deploy user have the right permissions (API Enabled, the deploy permissions, Author Apex where needed)?
8. Is the target API version supported?

If you cannot answer these before the window, you have a configuration risk, not a code risk.

## 10. What to merge

**Merge:** the five-family table, the API-usage caution, the metadata ceiling with the verify note, the system-settings table, and the pre-flight checklist.

**Compress:** the storage/flow/custom-object sections into a short table unless the page needs every category.

**Do not merge:** any exact API allocation number, because it is edition/licence-specific. Point to Setup → Company Information → API Usage instead.
