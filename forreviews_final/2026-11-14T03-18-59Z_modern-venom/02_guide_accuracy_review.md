# 02 — Salesforce guide accuracy review

Scope: the five Salesforce guide sources on the learning repo `main` branch, read in full, plus the existing
research artifacts that paraphrase them. Each finding cites a primary source. Severity is about learner /
interviewer impact, not about how hard the fix is.

## What is correct (checked, not assumed)

Before the findings, the load-bearing facts were verified and hold:

- **Governor limits** — 100 SOQL sync, 10,000 DML rows, 6 MB / 12 MB heap, 100 callouts, 10,000 ms /
  60,000 ms CPU, 75% production coverage gate. All correct in `crash-course.md` and `devops-engineer.md`.
- **"Advanced Admin" → Platform Administrator II** — correct rename; matches the independent sibling
  research bundle.
- **Setup breadcrumb paths** — the paths in `navigation-breadcrumbs.md` and the inline paths in
  `devops-engineer.md` / `labs-design.md` are accurate (Object Manager, Users, Profiles, Permission Sets,
  Roles, Sharing Settings, Flows, Apex, Deploy, Sandboxes, Data, Named Credentials, etc.).
- **Sandbox types** — Developer / Developer Pro / Partial Copy / Full, with the right use for each.
- **Conflict clinic** — the six conflict classes (profiles, permission sets, record types, page layouts,
  flows, Apex dependencies) and their causes match how Salesforce metadata actually merges.
- **`sf project deploy start --dry-run`**, `--manifest`, `--post-destructive-changes`, `--pre-destructive-changes`,
  `--test-level`, `sf apex run test`, `sf package version create`, `sf package install` — all valid current
  `sf` v2 commands.

## Findings

### F-01 · HIGH · `labs-design.md` Lab 2 — `Crypto.getRandomInteger().abs()` does not compile

**Location:** `labs-design.md`, Lab 2, step 1 (the trigger code).
**Claim in guide:**
```apex
p.Project_Code__c = 'PRJ-' + String.valueOf(Crypto.getRandomInteger().abs());
```
**Evidence:** the Apex `Long` class reference lists exactly three methods — `format()`, `intValue()`,
`valueOf(String)`. There is no `abs()`. `Crypto.getRandomInteger()` returns `Long`.
**Impact:** Lab 2 fails at compile time. A learner following the guide cannot complete the lab, and the
error message ("Invalid method") sends them looking in the wrong place.
**Fix:** `Math.abs(Crypto.getRandomInteger())` — Apex `Math.abs` has a `Long` overload.

### F-02 · HIGH · `labs-design.md` Lab 3 — `sf project generate component` is not a command

**Location:** `labs-design.md`, Lab 3, step 2.
**Claim in guide:**
```bash
sf project generate component -n projectCard -l lwc
```
**Evidence:** the `sf` CLI command reference lists `sf project generate` with exactly one subcommand,
`manifest`. The Lightning component generator lives in `@salesforce/plugin-templates` as
`sf template generate lightning component`.
**Impact:** Lab 3 step 2 fails with "command not found"; the learner is blocked before writing any LWC.
**Fix:**
```bash
sf template generate lightning component --name projectCard --output-dir force-app/main/default/lwc
```

### F-03 · MEDIUM · `labs-design.md` — the "Important System Properties" table is fabricated

**Location:** `labs-design.md`, "System Properties & OOB Features", the five-row table.
**Claim in guide:** `org.wideSharing.default`, `setup.locked`, `apex.pageLimit`, `session.timeout`,
`login.lockout`.
**Evidence:** `setup.locked`, `apex.pageLimit`, `session.timeout`, and `login.lockout` return no results and
are not part of the Salesforce organization-settings model. Only `org.wideSharing.default` is real.
**Impact:** a learner who goes looking for these properties finds nothing; an interviewer who asks "what
does `setup.locked` do?" has caught an invented fact.
**Fix:** replace the table with the real controls — `org.wideSharing.default` / `org.wideSharing.read` /
`org.wideSharing.readWrite`, Session Settings (session timeout, identity verification, login IP ranges),
Password Policies, and Login Hours. Remove the four invented names.

### F-04 · MEDIUM · `labs-design.md` Lab 3 — `sf org login web -d -a my-dev-org` uses an unverified flag

**Location:** `labs-design.md`, Lab 3, step 1.
**Claim in guide:** `sf org login web -d -a my-dev-org`
**Evidence:** the `-d` short flag could not be confirmed from the `plugin-org` source during this review;
the same guide elsewhere correctly warns "confirm flags with `--help`".
**Impact:** possible unknown-flag error at the first step of the lab.
**Fix:** `sf org login web --alias my-dev-org` and set the default org explicitly with the documented flag
from `sf org login web --help`.

### F-05 · MEDIUM · `labs-design.md` Lab 4 contradicts `crash-course.md` on Remote Site Settings

**Location:** `labs-design.md`, Lab 4, step 2 ("Create Remote Site Setting (fallback if Named Credential
doesn't work)").
**Contrast:** `crash-course.md` states "If you use Named Credentials, you don't need Remote Site Settings."
**Evidence:** Named Credentials are the supported way to avoid Remote Site Settings for a callout; a Remote
Site Setting is only needed for a direct endpoint callout.
**Impact:** the "fallback" framing teaches the wrong mental model and sends learners to configure a second
thing the platform does not require.
**Fix:** state that the Named Credential removes the Remote Site Setting requirement, and that a Remote Site
Setting is only needed if the Apex uses a direct endpoint instead of `callout:<namedCredential>`.

### F-06 · MEDIUM · existing `certifications.md` lists credentials that do not exist

**Location:** `forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/certifications.md`, certification table.
**Claim in artifact:** "Salesforce Apex Developer / LWC Developer" and "ServiceNow Certified Salesforce Admin".
**Evidence:** Salesforce does not issue an "Apex Developer" or "LWC Developer" credential, and there is no
"ServiceNow Certified Salesforce Admin". The real credentials are Platform Developer I / II, JavaScript
Developer I (LWC), Platform App Builder, Platform Administrator II, and the vendor (Copado / Gearset /
AutoRABIT) certificates.
**Impact:** the research note is wrong on its own topic and would mislead the job applicant it was written for.
**Fix:** see `03_work_update/corrections_to_existing_notes.md`.

### F-07 · LOW · `crash-course.md` — "Bulk API | REST/CSV"

Bulk API 1.0 is SOAP/CSV; Bulk API 2.0 is REST/JSON. The table collapses them. Minor, but the guide is
otherwise precise about protocols.

### F-08 · LOW · `crash-course.md` — "Scheduled jobs | 100 concurrent"

The limit is 100 scheduled Apex jobs per org, not "concurrent". Wording only.

### F-09 · LOW · `crash-course.md` — Trailhead trail IDs should be re-verified

The trail links (`sfx_admin_beginner`, `sfx_dev_beginner`, `data_management`, `apex_integration_services`,
`lightning_web_components_basics`, `force_com_security`) were not re-checked against
`trailhead.salesforce.com` in this pass. Trail IDs are renamed periodically; verify each before publishing.

### F-10 · LOW · `devops-engineer.md` — does not mention `sf project deploy validate`

The guide uses `sf project deploy start --dry-run` (valid). The purpose-built `sf project deploy validate`
command is absent. Per the sibling research bundle, `validate` requires Apex tests and is explicitly not for
sandboxes — worth a sentence so the learner does not reach for it on a sandbox.

## Summary

| Severity | Count | Items |
|----------|-------|-------|
| HIGH | 2 | F-01 (Apex compile error), F-02 (nonexistent CLI command) |
| MEDIUM | 4 | F-03 (fabricated properties), F-04 (unverified flag), F-05 (Remote Site contradiction), F-06 (fake certs) |
| LOW | 4 | F-07, F-08, F-09, F-10 |

The two HIGH findings both sit in `labs-design.md` and both block a hands-on lab outright. That guide is the
one to fix first; `03_work_update/labs_design.md` carries the corrected text.
