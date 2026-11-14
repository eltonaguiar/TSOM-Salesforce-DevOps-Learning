# JD term-by-term deep dive

Each term below appears in the Scotiabank requisition. The goal is a review-ready explanation plus the
release-engineering implication.

<details>
<summary><strong>1. Multi-environment release (Dev, QA, UAT, Pre-Prod, Prod)</strong></summary>

- **Dev** — Developer/Dev Pro sandbox per developer or pair. `System Administrator`. Commit to feature
  branches. No direct push to higher orgs.
- **QA** — Developer Pro or Partial Copy. Automated integration/regression on merge. Integration
  endpoints point at non-prod.
- **UAT** — Partial Copy or masked Full. Business testers validate stories with realistic data shapes.
- **Pre-Prod** — Full or fresh Partial, refreshed near the window. Release rehearsal against prod-like
  metadata and volume.
- **Prod** — Live. Only through an approved window, with segregation of duties and a tagged release.

**Implication:** each stage is a *different org*, so anything environment-specific (endpoints, secrets,
feature flags) must be configurable, not hardcoded.
</details>

<details>
<summary><strong>2. Scheduled releases, hotfixes, emergency deployments</strong></summary>

- **Scheduled** — release train; full validation, UAT sign-off, CAB approval, window.
- **Hotfix** — cut from `main` (what prod runs), validated, deployed small, merged back to `main`
  **and** any open release branch.
- **Emergency** — P1/customer/regulatory harm; a *pre-written* short path (one named approver +
  validation), never "whoever is online clicks Setup". Still documented afterward.

**Implication:** emergency is a shorter approval chain, not a skipped pipeline.
</details>

<details>
<summary><strong>3. Audit, security &amp; compliance (banking)</strong></summary>

- **OSFI** (Canada): B-10 third-party risk, B-13 technology/cyber risk — traceability of who changed code
  and environments.
- **SOX 404 / segregation of duties:** author ≠ approver ≠ deploy identity. Enforce in branch protection +
  environment approvals.
- **Audit pack per deploy:** change ticket, PR approval log, validation job id + test/coverage, prod
  deploy id + timestamp, release tag, and (for Full sandboxes) mask-complete evidence.
</details>

<details>
<summary><strong>4. Sandbox strategy (create, refresh, mask)</strong></summary>

- Refresh cadence: Developer/Dev Pro daily, Partial every 5 days, Full every 29 days.
- Use a **`SandboxPostCopy`** Apex class to rewrite emails to `.invalid`, repoint Named Credentials to
  non-prod, and disable production schedules on refresh.
- **Masking** before broad login: email, phone, government id (SIN/SSN), account/facility numbers, DOB,
  balances. Confirm mask complete; limit logins to the ticket until then.
</details>

<details>
<summary><strong>5. Conflict resolution (profiles, permission sets, record types, layouts, Flows)</strong></summary>

- **Profiles:** grab-bag XML of user/object/field permissions, layout + record-type visibility. Two
  stories editing one profile conflict; a bad merge changes access. Fix: put story access in **permission
  sets** (or groups); keep profiles for profile-only settings. Deploy thin profile deltas with
  decomposition if unavoidable.
- **Permission sets:** split by feature/persona; use **Permission Set Groups** to bundle without a new
  monolith.
- **Record types:** deploy with business process, picklist values, layout assignment, and visibility in
  **one payload**.
- **Page layouts:** layout ≠ assignment. Assignment lives on profile/record type; and classic layout ≠
  Lightning record page (FlexiPage) — check activation per app.
- **Flows:** XML does not merge. One owner per flow per release, or split into subflows. Know whether
  deploy leaves the version Draft or Active. Mitigation for a bad active version: activate the previous
  version, then redeploy the last good tag.
- **Apex:** deploy class + test together; tests create their own data; a missing dependency fails at
  compile in the target.
</details>

<details>
<summary><strong>6. Apex &amp; triggers (patterns)</strong></summary>

- **One trigger per object** dispatching to a handler class.
- **Bulkify**: handle 200-record lists; no SOQL/DML in loops.
- **Frameworks** (fflib / trigger-handler) for re-entrancy control and bypass during data loads.
- **Async** (`Queueable`/`Batchable`) for heavy work, respecting async limits and chaining.
</details>

<details>
<summary><strong>7. Flows — before-save vs after-save</strong></summary>

- **Before-save (Fast Field Updates):** same-record field updates; no extra DML; fastest; use it for
  same-record logic.
- **After-save (Actions &amp; Related Records):** related records, notifications, async; fires after commit.
- **Trigger order** integer (1–2000) sequences multiple record-triggered flows on the same object.
- A before-save job built as after-save times out at volume — a design-review red flag.
</details>

<details>
<summary><strong>8. Packages — unlocked vs managed</strong></summary>

- **Unlocked (2GP):** versioned internal modules; dependency trees; install like an app; promote before
  prod.
- **Org-dependent unlocked:** references org metadata; faster adoption, not portable — say the limitation
  out loud.
- **Managed (1GP/2GP):** third-party/IP boundary; you **upgrade**, never edit its Apex in Git.
- **Default for a large bank org:** unpackaged metadata from Git, modularized over time into unlocked
  packages. Do not propose "package the entire org" first.
</details>

<details>
<summary><strong>9. Salesforce DX &amp; CLI</strong></summary>

- **Source format** decomposes big XML (e.g. one object with hundreds of fields) into per-field files —
  kills most git merge conflicts.
- **Scratch orgs** = disposable, source-driven, Dev Hub-based; good for isolated package CI.
  **Sandboxes** = persistent prod copies; required for a bank org with managed packages/SSO/licenses.
</details>

<details>
<summary><strong>10. Automated testing &amp; validation</strong></summary>

- **Validate/dry-run** — no org change; proves compilation + tests against *that* org.
- **Quick deploy** — applies a passed validation inside the 10-day window; invalidated by any later change.
- **Real deploy** — first deploy, expired validation, or changed payload.
- Production with Apex requires tests; 75% org-wide coverage; `RunLocalTests` is the honest release gate.
</details>

<details>
<summary><strong>11. DevOps-friendly design patterns to coach</strong></summary>

| Pattern | Why release engineering cares |
|---|---|
| Permission sets over profile edits | Profiles do not merge; small permission sets do |
| One flow owner per release, subflows for parallel work | Flow XML does not merge |
| Tests create their own data | Empty and prod-like sandboxes behave the same |
| No hardcoded ids | The id in Dev is not the id in UAT — use custom metadata or a query |
| Named Credentials for callouts | Endpoints differ per sandbox; secrets never in Git |
| Custom metadata / custom permissions for toggles | Ship dark, turn on after deploy without another deploy |
| Bulkified Apex | A deploy can be green and still fail the first real batch |
| No environment-specific branches | `if (org.IsSandbox)` is a last resort; config belongs in the target |
</details>
