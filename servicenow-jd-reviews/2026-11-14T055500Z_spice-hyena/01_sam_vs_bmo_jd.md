# SAM repo vs the BMO SAM Administrator JD

**Repo:** <https://github.com/eltonaguiar/serviceNow_Learning_sam> @ `0ffb933`
**Size:** 42 markdown files, 188,761 chars
**Reference page:** <https://eltonaguiar.github.io/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/docs/modules/sam/sam-guide/>
**Ground truth:** SubQ decision pass over the full repo, cross-checked term-by-term with direct search

---

## Verdict

| Topic | Verdict | Evidence |
|---|---|---|
| 1. End-to-end SAM flow | **PARTIAL** | entitlement 43, reconciliation 23, normalisation 13 — but **"Discovery Model" appears 0 times** |
| 2. Content library / normalisation | **PARTIAL** | normalisation 13; **"unrecognised software" 0** |
| 3. Entitlements & licence metrics | **PARTIAL** | entitlement 43, core-based 35, per-user 3, per-device 2; **downgrade/upgrade rights 0** |
| 4. Reconciliation results | **PARTIAL** | reconcile 23, over/under-licensed 8, allocation 21; **true-up 0** |
| 5. Removal & reclamation | **MISSING** | **reclamation 0**, unused-licence 1 |
| 6. SaaS Licence Management | **MISSING** | **SaaS 0**; M365 4, Adobe 3 as passing mentions only |
| 7. Publisher packs | **MISSING** | publisher pack 2, Oracle 1, **IBM 0, VMware 0** |
| 8. CMDB & data quality | **PARTIAL** | CMDB 38, IRE 4, data quality 1 |
| 9. Audit readiness | **PARTIAL** | dashboard 35, audit 12; **vendor audit 0** |
| 10. Bank angle | **MISSING** | **CAB 0, segregation 0**; cost 44 |

**6 partial, 4 missing, 0 fully covered.**

The pattern is consistent: the repo explains SAM **concepts** well and the **operational** half poorly. It is a
learning repo (ELI5, concepts, labs, career paths), not a SAM Pro runbook. That is not a defect — but it means
it will not carry you through the BMO interview on its own.

## The most serious gap: "Discovery Model" never appears

The JD's very first requirement is the pipeline: *"discovery or SCCM data goes into Software Installations, gets
normalized into Discovery Models with publisher, product, version and edition, and then reconciles against
entitlements."*

The repo contains `Software Installation` 4 times, `normalisation` 13, `reconciliation` 23, `entitlement` 43 —
and **`Discovery Model` zero times**.

If the interviewer says "walk me through from a Discovery Model to a licence position," the repo gives you no
anchored answer. **This is the single highest-value thing to add.**

## What the repo does well

| Strength | Evidence |
|---|---|
| Entitlement concepts | 43 mentions, across concepts, modules, and Hermes |
| CMDB linkage | 38 mentions; the strongest measured topic |
| Core-based licensing | 35 mentions — Microsoft/Oracle core counting is a JD topic and is present |
| Cost framing | 44 mentions — the "licence risk as cost" angle is there |
| Over/under-licensed | 8 mentions, correctly framed |
| Allocation to users/devices | 21 mentions |
| Dashboards | 35 mentions — relevant to audit-readiness reporting |

## What to add, in priority order

| # | Gap | Why it matters for BMO |
|---|---|---|
| 1 | **Discovery Model** as a named object, with its normalisation status lifecycle | The JD's first topic; currently zero mentions |
| 2 | **Removal / reclamation workflow** — candidates, rules, harvest | A whole JD topic at zero. Bank licence-cost reduction is exactly this |
| 3 | **SaaS Licence Management** — M365/Adobe subscriptions, inactive-user reclamation, integration profiles | Zero on "SaaS"; bank angle is heavy on M365 |
| 4 | **True-up** and the reconciliation→cost→true-up chain | Zero mentions; the JD asks for true-up cost explicitly |
| 5 | **Vendor audit response** — the actual report pack | "audit" 12 but "vendor audit" 0 |
| 6 | **CAB / segregation of duties** | Zero. Explicit JD topic and a bank-specific control |
| 7 | **Publisher pack detail** — IBM, VMware | Oracle 1 mention, IBM/VMware 0 |
| 8 | **Unrecognised software approval** workflow | Zero. JD topic 2 explicitly asks for it |

## The story the JD asks for, and where the repo supports it

The JD says: *"a reconciliation gap you fixed, a cost you saved, and a data-quality problem you solved… the
CMDB one is your strongest story, so lead with it."*

| Story | Repo support |
|---|---|
| CMDB / data-quality problem solved | **Strong** — CMDB 38, IRE 4, data quality present |
| Reconciliation gap fixed | **Moderate** — reconciliation 23, but no worked example of a gap and its fix |
| Cost saved | **Moderate** — cost 44, but no reclamation/true-up mechanics to attach a number to |

So the repo backs the CMDB story — which the JD says to lead with — and is thin on the other two. Add a worked
reclamation example and a true-up example, and all three stories have scaffolding.

## Honest assessment

**Can you interview off this repo alone?** No. It will get you through the conceptual half (what SAM is, how
entitlements and reconciliation work, why CMDB matters) and leave you exposed on the operational half (the
Discovery Model pipeline, reclamation, SaaS, true-up, audit response, CAB).

**Is it worth keeping?** Yes — the concept material and the CMDB/data-quality depth are genuinely useful, and
the absence of a "Discovery Model" section is a specific, cheap fix.