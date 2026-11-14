# JD ↔ published page cross-reference

| JD requirement | Published page section | Gap this bundle fills |
|---|---|---|
| CI/CD pipelines, Git workflows | §5 CI/CD (stage table) | Full YAML, delta tooling, JWT auth, PR checks, environment protection |
| Multi-environment release (Dev→QA→UAT→Pre-Prod→Prod) | §3 Environments | Sandbox refresh cadence numbers, post-copy hooks, deliverability reset |
| Scheduled / hotfix / emergency deploys | §10 | Speed table + runbook + rollback decision tree |
| Audit, security, compliance | §11 | Audit-pack artifact list mapped to pipeline outputs |
| Metadata lifecycle in Git | §1 | Source vs metadata format, retrieve/commit/dry-run loop |
| Sandbox strategy, create/refresh/masking | §3 | Mask field classes, who signs off, pre-login endpoint checks |
| Conflicts: profiles/permission sets/record types/layouts/flows/apex | §7 | Root cause per conflict + merge-safe pattern |
| DevOps tools (Gearset/Copado/AutoRABIT) | §6 | Click-path walkthroughs with confidence tags |
| **Limits, dependencies, deployment constraints** | §2 + §9 (light) | `04-limits-dependencies-constraints.md` — the requested deep dive |
| Unlocked / managed packages | §8 | 2GP vs org-dependent vs managed decision table |
| Salesforce DX | §1 | Scratch org vs sandbox; source format; `sf` command set |
| Regulated/enterprise (banking) | §11 | OSFI/SoD framing, segregation of duties in the pipeline |
| Certifications (PD1, Advanced Admin, DevOps certs) | Certifications | `06-certifications-curriculum.md` — correct names + study order |

## Corrections to carry into the merge

- The published page says Advanced Admin was renamed **"Platform Administrator II"**. Treat this as
  `vendor-claim` and verify against the current Salesforce credential catalog before publishing. Safest
  public wording: "Advanced Administrator (verify the current credential name on Trailhead)."
- The published page lists "a Salesforce DevOps Engineer cert" — there is **no official Salesforce
  DevOps Engineer certification**. Say so plainly; vendor certs (Gearset/Copado/AutoRABIT) are separate.
- `[Verify]` tags in this bundle are deliberate. A wrong button name is worse than a gap; the merge agent
  should only promote a click-path to prose after confirming it in-tenant or in vendor docs.

## What the role actually owns (framing for the page)

The posting is not "write features." It is "make Salesforce releases fast, safe, and auditable" for a
commercial-banking org.

| You own | You partner on | You do not own alone |
|---|---|---|
| Git history of metadata | Apex, triggers, LWC | Business requirements |
| Pipeline: validate, test, deploy | Flow design | Production data fixes without a ticket |
| Dev/QA/UAT/Pre-Prod/Prod path | QA test evidence | Security exceptions |
| Sandbox create/refresh/mask | Admin config in a story | Approving your own prod change |
| Conflict resolution on deploy | Dependency design | Deciding release scope |
| Runbooks, rollback, audit pack | Platform limits | Bypassing change control because "small" |

ELI5: developers build the furniture. You own the loading dock, the truck, the checklist, and the proof
that the right furniture arrived in the right building without breaking what is already there.
