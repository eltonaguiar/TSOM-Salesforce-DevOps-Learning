# 03 — Fidelity corrections (highest-value file)

Format: **Location → claim → why it is wrong/imprecise → fix**. Confidence stated. "Page" = live guide page; "bundle" = our research.

## C1 — Deactivated users CAN be reactivated (HIGH, high severity)
- **Location:** user-management-data page "User States" table; mirrored in flat `02` §User states.
- **Claim:** "Deactivated — cannot log in; license freed up (**can't be reactivated, must recreate**)".
- **Reality:** a deactivated user keeps the record and **can be reactivated** (Setup > Users > filter "All Users" > Reactivate). **Freeze** = block login, retain licence, unfreeze later. **Deactivate** = free the licence, keep the record, reactivate when needed. Only a hard-deleted user record needs recreation.
- **Fix:** replace the row with the 4-state table in `04` (paste-ready D).

## C2 — The "System Properties" table names keys that do not exist (HIGH)
- **Location:** labs-design "System Properties & OOB Features"; flat `02` §System properties.
- **Claim:** `org.wideSharing.default`, `setup.locked`, `apex.pageLimit`, `session.timeout`, `login.lockout`.
- **Reality:** none are Salesforce system-property keys. The real controls live in Sharing Settings (OWD), Deploy > Deployment Settings, Session Settings, Profiles > Login Hours/IP Ranges, and Metadata API types `SessionSettings`, `SecuritySettings`, `OrganizationSettings`.
- **Fix:** rename the section "Platform settings that behave like properties", give the real Setup path per row, and add: "Salesforce has no user-facing 'system properties' registry." B3's definition of the phrase is already correct — reuse it.

## C3 — Quick-deploy window has a number (HIGH; verify in org)
- **Location:** devops-engineer §9; flat `02` DevOps.
- **Claim:** "inside Salesforce's quick-deploy window" (no duration).
- **Fix:** "A validated deployment can be quick-deployed for **up to 10 days** after validation, and only if the payload has not changed."

## C4 — Coverage is three different rules (HIGH)
- **Claim:** "75% coverage is the production gate."
- **Fix:** state all of it:
  - `RunAllTestsInOrg` / `RunLocalTests`: **org-wide** Apex coverage ≥ 75%.
  - `RunSpecifiedTests`: the named tests must cover **each class and trigger in the deployment** at ≥ 75%.
  - Any **trigger at 0% coverage** fails the deploy.
  - Managed-package code is excluded from the count but still affects the org total.

## C5 — Sandbox refresh cadence (HIGH)
- **Location:** devops-engineer §3.
- **Claim:** "Refresh cadence is license-limited. Full is the slowest."
- **Fix:** add documented intervals (edition/contract dependent): Developer **1/day**, Developer Pro **1/day**, Partial Copy **every 5 days**, Full **every 29 days**. Also: cannot refresh from another sandbox; refresh replaces content; refresh time ≠ deploy time.

## C6 — Lab 4 teaches the wrong auth pattern (HIGH)
- **Location:** labs-design Lab 4.
- **Claim:** Named Credential with blank username/password and "Generate Authorization Header" unchecked for a public API.
- **Fix:** use **Authentication: Anonymous** (or a Remote Site Setting) for an unauthenticated endpoint. Blank Basic auth is a confusing half-state that can still emit an `Authorization` header. The `@future(callout=true)` part is correct.

## C7 — Custom-field ceiling (MEDIUM)
- **Claim:** "Limit custom fields per object (< 500)."
- **Fix:** 500 is a **design guideline**; the platform cap is ~**800 custom fields per object** (edition dependent). Say which is which.

## C8 — FLS ≠ sharing, and neither is automatic in Apex (HIGH)
- **Location:** user-management-data FLS; crash-course security design.
- **Claim:** "Set FLS at the Profile level, not page layout" (true but incomplete).
- **Fix:** permission sets are the modern carrier for FLS; `with sharing` enforces **record** sharing only and does **not** enforce CRUD/FLS. Use `WITH SECURITY_ENFORCED`, `stripInaccessible`, or explicit `Schema` checks.

## C9 — Setup path drift (HIGH for a breadcrumb reference)
- **Claim:** "Setup > Apex Jobs", "Setup > Scheduled Jobs".
- **Fix:** current releases consolidate these under **Setup > Background Jobs**. Sandboxes commonly appear as **Setup > Environments > Sandboxes**. Process Builder and Workflow Rules are retired — stop presenting them as usable. Add a "path drift by release" note (table in `04`).

## C10 — MFA / SSO missing (HIGH for banking)
- **Fix:** add that Salesforce enforces **MFA for all interactive logins** (since Feb 2022); **My Domain** is a prerequisite for SSO; integration users are API-only and exempt from interactive MFA but must use secure flows (connected app + JWT bearer) with a least-privilege permission set.

## C11 — Permission set licences vs permission sets (MEDIUM)
- **Fix:** feature access can come from **Permission Set Licenses**; a permission set cannot exceed the user's licence. Permission Set **Groups** bundle PSs and support **muting permission sets** to subtract access.

## C12 — Duplicate management is incomplete (MEDIUM)
- **Fix:** add matching rules (standard vs custom), duplicate rules per module (active/inactive), actions **Alert / Block / Report**, **Duplicate Jobs** for existing data, and that API callers can pass a duplicate-rule header to allow saves (verify header name in current docs).

## C13 — Licence descriptions (LOW)
- **Fix:** "Salesforce Platform — limited standard CRM" → "no standard CRM objects by default; custom apps only; standard objects only where the licence permits." Chatter Free cannot be upgraded in place.

## C14 — Rollback must name data restore (MEDIUM)
- **Location:** devops-engineer §10 rollback table.
- **Fix:** add a row: data changed by a post-deploy script/delete → Git cannot restore rows; use **Salesforce Backup & Restore** (or the bank's backup vendor) on a ticketed path; confirm the restore point (RPO) before the window.

## Cross-bundle contradictions to resolve

| Topic | Conflict | Resolution |
|---|---|---|
| Trigger coverage | B3 says `RunSpecifiedTests` needs 75% per class/trigger; page implies org-wide | Both true at different test levels — use C4 wording |
| Profile merging | crash-course says profiles "do not merge"; devops page allows thin delta + decomposition | Scope it: profiles merge badly **by hand**; decomposition tooling exists |
| "System properties" | B3 defines it correctly; labs page invents keys | Use B3's definition plus the C2 fix |
