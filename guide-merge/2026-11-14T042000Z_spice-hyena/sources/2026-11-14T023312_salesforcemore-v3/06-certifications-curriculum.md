# Certifications & curriculum

> Credential names and domain weights change. Treat everything here as `vendor-claim` until verified
> against the live Trailhead credential page at merge time.

## Credential mapping

| Credential | Why it maps to this JD | Notes |
|---|---|---|
| **Platform Developer I (PD1)** | Apex, triggers, tests, platform model you deploy | The JD names it. Primary technical credential. |
| **Platform App Builder** | Objects, Flow, security — metadata you move weekly | Strong secondary. |
| **Advanced Administrator** | Security model, change/environment topics | JD names it. **Verify current credential name** on Trailhead before publishing (published page claims a rename to "Platform Administrator II" — `vendor-claim`). |
| **Development Lifecycle and Deployment Architect** | Environments, release management, CI/CD, governance — the *actual* DevOps architect credential | Best long-term fit for this role; not named in the JD but directly on-point. |
| **Integration Architect** | Named Credentials, callouts, integration patterns across environments | Useful for the integration side of releases. |
| **Vendor certs (Gearset/Copado/AutoRABIT)** | Shows hands-on tool time | Not a substitute for PD1; vendor-specific. |

## Corrections to make in the published page

- **There is no official Salesforce "DevOps Engineer" certification.** State that plainly. The closest
  official credential is *Development Lifecycle and Deployment Architect*; vendor certs are separate.
- Do not print the "Platform Administrator II" rename as fact without a Trailhead citation.
- Do not print domain weights from memory. Pull them from the current exam guide at merge.

## Study order for this role

1. Crash-course fundamentals (objects, security, Flow, Apex, governor limits).
2. This track's labs (retrieve/dry-run, profile conflict, failing validation, runbook, sandbox checklist).
3. PD1 exam objectives.
4. Platform App Builder / Advanced Admin overlap (security model, change management, environments).
5. Development Lifecycle and Deployment Architect (long-term).

## Curriculum gaps worth adding to the track

- A lab on **quick-deploy invalidation** (change something after validation, watch it expire).
- A lab on the **Master-Detail two-step** deploy.
- A lab on **JWT auth + connected app** for CI, including secret rotation.
- A module on **audit pack assembly** from pipeline outputs (ticket, PR, job ids, tag).
