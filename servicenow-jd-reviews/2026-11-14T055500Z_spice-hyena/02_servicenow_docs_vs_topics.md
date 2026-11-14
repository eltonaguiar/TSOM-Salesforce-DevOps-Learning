# The ServiceNow guide pages vs your developer/retail topic list

**Repo:** <https://github.com/eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM>
**Scope:** 31 markdown pages (26 ServiceNow + 5 Salesforce), measured at `5e32e5e`
**Method:** term-frequency matrix per page, then targeted depth checks on the weakest topics

---

## Headline

| Topic from your list | Total mentions | Verdict |
|---|---|---|
| ITSM processes (Incident/Problem/Change/Request, SLAs) | **1,610** | **Strong** |
| Integrations (REST, Import Sets, Transform Maps, MID) | **1,057** | **Strong** |
| Flow Designer / IntegrationHub | **637** | **Good** |
| Delivery (update sets, scoped apps, ATF, upgrades) | **584** | **Good** |
| Client-side scripting | **504** | **Good** |
| Server-side scripting | **388** | **Moderate** |
| Retail angle (portal, self-service, knowledge) | **381** | **Moderate** |
| Security / ACL | **242** | **Moderate** |
| **GlideRecord** | **97** | **Weak** |
| **Service Catalog** | **76** | **Weak** |

**Eight of ten topics are adequately covered. Two are not — and they are two of the most interview-critical.**

## The GlideRecord problem, quantified

GlideRecord is the single most-asked ServiceNow developer skill. It is spread thin: **20 mentions in
`ai/javascript-reference.md`, 14 in `interviews/custom-application-development.md`, 11 in `cmdb-guide.md`** —
and nowhere else above 6. There is no page that teaches GlideRecord.

Method-level coverage across the **entire** guide:

| Method / pattern | Occurrences | Your list asks for it? |
|---|---|---|
| `addQuery` | 53 | implied |
| `getValue` | 45 | implied |
| `next()` | 33 | implied |
| `setLimit` | 17 | — |
| `get(` | 13 | — |
| `orderBy` | 5 | — |
| `GlideAggregate` | **6** | **yes** |
| `setValue` | **3** | implied |
| `addEncodedQuery` | **0** | **yes — "encoded queries"** |
| `setWorkflow(false)` | **0** | **yes — named explicitly** |
| `hasNext` | **0** | — |
| `chooseWindow` | **0** | — |

Three of the things you named — **encoded queries, `setWorkflow(false)`, and GlideAggregate as a real topic** —
are effectively absent. Encoded queries and `setWorkflow(false)` are exactly the two GlideRecord details that
separate "I have used it" from "I know it."

## The Service Catalog problem

76 mentions total, and **30 of them are in a single page** (`itsm-guide.md`). No dedicated catalog page exists.

Your list asks for: *record producers, variables and variable sets, catalog client scripts, fulfilment flows* —
and notes this is *"a common ask for a retail or pharmacy business with store requests."*

What the guide has is catalog content inside the ITSM page (catalog items as a request channel), not catalog
**mechanics**. A retail interviewer asking "how would you build a store-supply request?" needs record producers,
variable sets, and a fulfilment flow — none of which is taught as a topic.

## Where the guide is genuinely strong

| Topic | Best page | Why it works |
|---|---|---|
| **ITSM** | `itsm/itsm-guide.md` — **582** mentions of process terms | Deepest coverage in the repo by an order of magnitude |
| **Integrations** | `cmdb-guide.md` (169), `other-guide.md` (211), `interviews/integrations.md` (104) | REST, Import Sets, Transform Maps all present with volume |
| **Flow Designer** | `cmdb-guide.md` (118), `other-guide.md` (102) | 637 total; flows/subflows/actions covered |
| **Delivery** | `interviews/code-deployment.md` — **92** delivery mentions in one page | Update sets, ATF, scoped apps all there |
| **CMDB** | `cmdb-guide.md` — 177,990 chars, the largest page | Comprehensive; also covers IRE and data quality |
| **Client scripting** | `interviews/custom-application-development.md` (67), `ai/javascript-reference.md` (54) | onLoad/onChange/onSubmit, g_form, g_user all present |

## The AI guide is doing work it should not

`ai/ai-guide.md` carries **126 mentions of ITSM process terms** and **69 of Flow Designer** — more than most
module pages. It is 80K chars and is acting as a general ServiceNow page, not an AI page. That inflates the
coverage numbers for topics it should not be the primary source for, and it means the real ITSM/catalog
coverage is more concentrated than the totals suggest.

## What to add, in priority order

| # | Gap | Suggested home |
|---|---|---|
| 1 | **A GlideRecord page**: queries, `addEncodedQuery`, `setWorkflow(false)`, `GlideAggregate`, performance (no queries in loops) | New `docs/modules/scripting/gliderecord.md` — currently spread across 6 pages with no owner |
| 2 | **A Service Catalog page**: record producers, variable sets, catalog client scripts, fulfilment flows | New `docs/modules/catalog/catalog-guide.md` |
| 3 | **Encoded queries specifically** | Into the GlideRecord page — zero mentions today is a real hole |
| 4 | **`setWorkflow(false)`** | Into the GlideRecord page — a one-paragraph topic that is currently absent |
| 5 | **Retail/scaled self-service** — high ticket volume, portal deflection, automating repetitive requests | Extend `itsm-guide.md` or `csm-guide.md`; currently 381 mentions spread thin with no retail framing |
| 6 | **ACL evaluation order** — table vs field, and the order ACLs are evaluated | `cmdb-guide.md` has 22 ACL mentions; the evaluation-order detail belongs somewhere discoverable |

## Relevancy to the retail angle

The JD's retail point is: *lots of stores and pharmacies → high service-desk volume → portal, self-service,
knowledge, automating repetitive requests.*

The guide covers portal/self-service/knowledge at **381 mentions** but scattered — `csm-guide.md` 45,
`itsm-guide.md` 46, `hrsd-guide.md` 26. There is no page that frames these as a **volume problem with a
deflection strategy**, which is the way a retail interviewer will ask it.

`hrsd-guide.md` scoring 26 on retail-self-service is a hint: employee-centre patterns are the closest thing the
guide has to a store-portal discussion, and it is filed under HR.

## Honest assessment

**Relevant and useful** for 8 of 10 topics — ITSM, integrations, Flow Designer, delivery, client scripting,
CMDB, and the Salesforce track are all genuinely strong.

**Not sufficient** for the two scripting-adjacent questions that tend to decide ServiceNow developer
interviews: GlideRecord depth and Service Catalog mechanics. Both are cheap to fix — two pages — and both are
currently at the bottom of the measured coverage.