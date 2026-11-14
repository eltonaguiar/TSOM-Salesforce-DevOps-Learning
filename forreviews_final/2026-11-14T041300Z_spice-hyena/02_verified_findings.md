# 02 — Verified findings

Every row was checked against a primary source in this session. Where I could not verify, I say so.

## 1. The heap conflation — root cause, not just a wrong number

**Status: confirmed.**

The crash course publishes heap as `6 MB sync / 12 MB async` in three places, and five bundles repeat it.

The official governor-limits table has two separate rows:

| Limit | Sync | Async |
|---|---|---|
| Total heap size | 10 MB | 25 MB |
| Maximum size of callout request or response (HTTP request or Web services call) | 6 MB | 12 MB |

The crash course's numbers are the **callout** row, applied to the **heap** row. The number is real; the row
is wrong. That is why it reproduced so faithfully across five independent agents — each copied a
plausible-looking pair from the page that was supposed to be authoritative.

**Secondary defect in the same sentence.** `crash-course.md:434` says async heap "doubles to 12 MB". Even on
its own wrong premise it is not doubling: 6 → 12 is 2×, but the real figures are 10 → 25 MB, which is 2.5×.
So the sentence carries a second error that survives the first fix if you only swap the numbers.

**Correction for the page:**

| Line | Current | Correct |
|---|---|---|
| 345 | `\| Heap size \| 6 MB (sync) / 12 MB (async) \|` | `\| Heap size \| 10 MB (sync) / 25 MB (async) \|` |
| 425 | `### 3. Heap Size — 6 MB Synchronous / 12 MB Asynchronous` | `### 3. Heap Size — 10 MB Synchronous / 25 MB Asynchronous` |
| 434 | `…where the heap limit doubles to 12 MB.` | `…where the heap limit rises to 25 MB and CPU to 60,000 ms.` |

**And add a row** so the 6/12 figures are not orphaned — they belong to callouts:

```
| Max callout request or response size | 6 MB (sync) / 12 MB (async), counts toward heap |
```

**Source:** `https://developer.salesforce.com/docs/platform/apex-dev/references/apex-dev/apex-gov-limits.html`

## 2. The 1% coverage rule — does not exist

**Status: confirmed absent.**

Official text, `apex_code_coverage_intro.htm`:

> "To deploy Apex or package it for the Salesforce AppExchange, unit tests must cover at least **75%** of your
> Apex code, and those tests must pass."

No per-class or per-trigger 1% floor appears. Seven sites across three bundles state one:

| File:line | Claim |
|---|---|
| `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:222` | "ApexTrigger — Requires at least 1% test coverage on the trigger itself" |
| `2026-11-14_salesforceagain-v3_devops-metadata-dependencies-deep-dive.md:225` | "at least 1% per trigger, 75% org-wide" |
| `2026-11-14_salesforceagain-v3_devops-github-cicd-pipeline.md:241` | "Trigger coverage: 1% minimum per trigger" |
| `20261114-020852-salesforcemore/SALESFORCE_LIMITS_DEEP_DIVE.md:84` | "75% org-wide … 1% per class minimum" |
| `20261114-020852-salesforcemore/SALESFORCE_LIMITS_DEEP_DIVE.md:295` | "each class ≥ 1%" |
| `20261114-020852-salesforcemore/salesforce-principles/KEY_PRINCIPLES.md:103` | "each Apex class needs ≥1% coverage" |
| `2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:69` | "Every trigger needs some coverage `[Verify the 1% trigger rule]`" |

The last one is the model to copy: it states the rule it is unsure about and flags it.

**What is actually true, and worth publishing instead:** an Apex class or trigger with **zero** coverage
contributes nothing to the 75% and, more importantly, the payload fails if *the org's* coverage is under 75%.
There is no per-item threshold. Writing "1%" implies a documented floor where none exists — and a team that
believes it will write a single trivial test per trigger and assume the box is ticked.

**Correction:** replace every "1% per class/trigger" with "75% org-wide; each class and trigger needs
meaningful coverage, and there is no per-item percentage threshold".

## 3. Deploy payload ceiling — out by 10×

**Status: confirmed wrong in two bundles.**

| File:line | Claim | Correct |
|---|---|---|
| `2026-11-14_salesforceagain-v3_devops-governor-limits-deep-dive.md:184` | "Total deploy zip size — 400 MB (recommended)" | ≈39 MB compressed |
| `2026-11-14T023312_salesforcemore-v3/04-limits-dependencies-constraints.md:66` | "Max compressed payload ~400 MB `[Verify current byte cap]`" | ≈39 MB compressed |
| `salesforceagain-v4/comprehensive-devops-research.md:109` | "Package.xml max size — 10 MB" | ≈39 MB compressed |

Correct in `2026-11-14T023507_salesforcemore-v2`, which also records its own earlier 400 MB error in
`08-cross-bundle-notes.md:21` — the only bundle that documents a self-correction.

## 4. Deprecated CLI install with a suppressed failure

**Status: confirmed.**

`20261114-020852-salesforcemore/SALESFORCE_DEVOPS_DEEP_DIVE.md:599`:

```bash
npm install -g sfdx-cli || true  # prefer official sf installer in practice
```

Two defects: `sfdx-cli` is the deprecated predecessor of `@salesforce/cli`; and `|| true` suppresses the
failure, so a broken install proceeds silently. Correct form, from
`20261114-020300-salesforceagain-kilo/04-github-actions-salesforce-cicd.md:179`:

```bash
npm install -g @salesforce/cli@<pinned>
```

## 5. Non-existent CLI commands and flags

**Status: partially verified.** I confirmed these do not appear in the CLI command inventory used by the
peer's review; I did not execute the CLI myself.

| File:line | Claim | Problem |
|---|---|---|
| `salesforceagain-v4/comprehensive-devops-research.md:278` | `sf project deploy start --validated-deploy-request-id <id>` | Not a flag. Quick deploy is `sf project deploy quick --job-id <id>` |
| `2026-11-14T023507_salesforcemore-v2.md:713, 987, 988, 1003` | `sf org list limits` | Not a command. Use `sf limits api display` — and it reports **API request** limits, not storage |
| `2026-11-14T023507_salesforcemore-v2.md:988` | `sf org list limits` for a Storage row | Same command, and it does not report storage at all |

The `2026-11-14T023507_salesforcemore-v2.md:713` occurrence hedges ("confirm the command in your CLI
version"), which is again the right instinct applied inconsistently.

## 6. Deprecated Setup path, self-contradicting

**Status: confirmed.**

`crash-course.md:84-85`:

```
| Debug Logs         | Setup > Debug Logs                        |
| System Log / Apex Logs | Setup > Monitor > Logs > Debug Logs   |
```

Line 84 is right, line 85 is deprecated, and they sit adjacent. `navigation-breadcrumbs.md` uses
`Setup > Debug Logs` in both places it appears. One-line fix.

## 7. Claim I checked and believe is correct — disputing the peer

**Status: I disagree with the peer's D21/D32.**

The peer records "No official Salesforce DevOps cert" as a defect in two bundles. I do not think it is one.

The published guide says:

> "A Salesforce 'DevOps Engineer' cert — There is not an official one to list as if it existed. Copado,
> Gearset, and AutoRABIT offer their own certificates. Those show tool time. They do not replace PD1."

The bundles claim there is no credential *named* "DevOps Engineer". That is narrower and true. The existence
of a "Development Lifecycle and Deployment Architect" credential does not falsify it.

**Where the peer is right:** if a bundle says "there is no Salesforce credential relevant to DevOps", that
would be wrong. Check the exact wording before changing it.

**My position:** keep the bundles' claim, add the architect credential as a distinct related item, and verify
it against the official credential page before it enters a curriculum. I did not verify it here and am not
asserting it.

## 8. Things I could not verify in this session

| Claim | Why not |
|---|---|
| Gearset / Copado / AutoRABIT click paths | Vendor UIs; the guide itself says these stay at category level |
| Exam weight percentages | No cited exam guide. Publishing invented weights is the error the peer caught twice |
| `RunRelevantTests` API version gate (claimed 66.0+) | Not in the CLI messages I read; peer says drop it |
| Metadata API intra-payload ordering claim | Would need a live deploy to test |
| Whether a Full sandbox masking checklist matches Salesforce Data Mask's current UI | Product UI, not doc-verifiable here |

Recording these as unverified is the point. A defect register that asserts everything is not more useful than
one that marks its edges.