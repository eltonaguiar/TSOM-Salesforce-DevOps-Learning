# 01 — Cross-reference: the review surface

Everything below is evidence-backed from `gh`, `git`, tree listings, and the worktree at `1d9354ab9e2`.
Counts taken 2026-11-14 03:19 UTC.

## 1. Where `modern-venom` sits relative to `main`

`origin/main` tip at review time: `7fe5a8ce94e` ("Scanner data update [2026-11-14 03:08 UTC] [skip ci]").
`main` is a **high-churn automated branch** — the recent commits are bot/scanner commits firing every few
minutes. That matters for review: a branch cut from `main` is stale within the hour.

`modern-venom` is **5 commits ahead of `origin/main`** (merge-base `165879f2174`), and those 5 are the whole
review payload:

| # | sha | Title | Nature |
|---|-----|-------|--------|
| 1 | `df2eadf054c` | Retire the Inception (Mercury) API from every provider registry | code (36 files) |
| 2 | `83787bd97b` | docs: add the dated FREEBUFF chatlog | doc |
| 3 | `2c08a4bb14` | docs: extend the dated chatlog with the review inventory | doc |
| 4 | `4294fd835f` | test: deploy broken mermaid diagram to GH pages | test/CI scaffolding |
| 5 | `1d9354ab9e` | simulation: deploy broken mermaid diagram for swarm audit | test/simulation |

`git diff --stat origin/main...modern-venom` = **41 files, +4254 / −348**. The bulk is
`litellm_config.yaml`, four new `tools/*.py` discovery/audit tools, and `start_litellm_proxy.sh` hardening.

**Cross-reference:** `df2eadf054c` is the commit the FREEBUFF chatlog
(`updates/2026-11-12-FREEBUFF-chatlog-1959UTC.md`) documents as the Mercury retirement on branch
`scrub/inception-mercury-2026-11-12`. The chatlog says "37 files changed vs `main`, in two commits"
(`df2eadf054cb` = 36 files, plus the chatlog itself). On `modern-venom` it is 41 files / 5 commits because
the two mermaid-test commits and the two chatlog commits sit on top. **A reviewer must review the code
commit, not the chatlog's file count.**

## 2. Review artifacts already on `main` (the items under review)

`origin/main` carries exactly one review folder:

```text
forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/
  certifications.md
  crash_course.md
  key_principles.md
  research_index.md
  research_plan.md
```

Its own index marks **four deliverables Pending**:

1. DevOps & Release Engineering notes
2. Navigation & Breadcrumbs notes
3. Labs & Design notes
4. User Management & Data notes

Those map 1:1 to the four Salesforce guides not yet turned into notes. That is the gap `03_work_update/`
closes.

## 3. Remote branches carrying review content

| Branch | Review content |
|---|---|
| `origin/main` | the 5-file `salesforceyetagain-v4` set above |
| `origin/salesforceagain-v3` | 4 DevOps deep-dive files: Gearset UI, GitHub CI/CD pipeline, governor limits, metadata dependencies |
| `origin/samagain-v4` | SAM module reference — unrelated to Salesforce; no review content |

No other remote branch carries `forreviews/` content. `gh-pages` is the deployed-site branch and holds no
review artifacts.

## 4. The two sibling Salesforce repositories

### `eltonaguiar/TSOM-Salesforce-DevOps-Learning`

Separate clone at `/home/eaguiar2015/TSOM-Salesforce-DevOps-Learning`. Its `forreviews/` holds the deeper
bundles:

- `2026-11-14T0210Z-salesforceyetagain-v2-*` — planning anchors, certifications, crash course
- `2026-11-14T023241_salesforceagain-v2/` — 6 numbered files: limits, metadata dependencies, DevOps tool UI
  walkthroughs, GitHub CI/CD, JD term-by-term, certifications
- `2026-11-14T023507_salesforcemore-v2/` — 8 sections: source log, principles, limits/constraints, DevOps
  tools, CI/CD, certifications, term deep-dives, merge map, cross-bundle notes
- `20261114-020852-salesforcemore/` — deep dives plus a `source-capture/` copy of all five guides
- consolidated single-file versions of each

Branches: `main`, `research/salesforceagain-2026-11-14T020300Z`, `research/salesforcemore-v2-2026-11-14T021057Z`,
and three `forreviews/*` split branches.

### `eltonaguiar/ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM`

The published site's source repo. `main` carries
`docs/salesforce/{crash-course, navigation-breadcrumbs, labs-design, user-management-data, devops-engineer}.md`.
Branches: `arlo/theme-and-tsom-labs-2026-11-05`, `direction-a-gaps-sam-guide-2026-11-13`,
`docs/sam-guide-gaps-2026-11-13`, `freebuff-guides-2026-11-05T2135Z`, `hermes-success-pack-2026-11-06`.
**None of the non-main branches touch the Salesforce track**, so `main` is the only source of truth for the
guides.

## 5. Open pull requests — 33 open, all `reviewDecision: ""`

All authored by `eltonaguiar`; **not one has a recorded review decision**. They cluster into three groups:

**A. Recent, plausibly mergeable (Oct–Nov 2026):** #766, #765, #763, #762, #761, #760, #759, #758, #757,
#756, #751, #750, #749, #747, #746, #745, #744, #736, #735

**B. Stale since June–July 2026 (no activity ~4 months):** #667, #666, #665, #657, #600, #595, #581,
#564, #562 — the "edge hunt / money-ready / forward-track" generation, almost certainly behind `main` by
thousands of commits.

**C. Security / CI hygiene (Oct 2026):** #713 backup-verify false failures + issue spam · #711 stale-tag
defects · #701 pick rationale · #700 LLM free-first + secret scrub · #696 Discord webhook rotation

**Cross-reference risk:** #761 (rotated FTP credentials), #700 (secret scrub), and #696 (webhook rotation)
touch the same secret-handling surface as the Mercury-retirement commit's provider-registry changes. If both
land, review them together — the Salesforce lens (secrets never in the repo, Named Credentials over hardcoded
endpoints) applies to both.

## 6. Open issues — 44 open

- **~30 `[backup-verify] Restore check FAILED`** bot issues, one every ~30 min, dating back to 2026-06-15.
  This is the issue spam PR #713 claims to fix. It is real, ongoing, and the single loudest signal in the
  issue list.
- **5 monthly `[Security] Monthly Secret Rotation Reminder`** — Jul/Aug/Sep/Oct/Nov 2026 (#668, #675, #685,
  #695, #764).
- **#748 "Production resolver predates _priceless_close -> exit_price=0.0 flat closes"** — a real
  human-filed data-correctness bug, open since Oct 20. Highest-value non-bot issue.
- **#654 weekly event gap scan — DEGRADED** (scrapers blocked).

## 7. Cross-reference summary (the one-screen version)

- **`main`** = bot-driven, moving every few minutes; any review branch is stale on arrival.
- **`modern-venom`** = 5 commits: 1 real code change (Mercury retirement + litellm hardening + 4 new tools),
  2 chatlog docs, 2 mermaid-test scaffolding commits that should not ship.
- **Salesforce review content lives in three places**: `forreviews/salesforceyetagain-v4/` on `main`,
  `forreviews/*` on the TSOM repo, and the five guide sources on the learning repo. The existing index's
  four Pending items are exactly the four guides not yet turned into notes.
- **33 open PRs** = none reviewed; ~9 stale since June/July; 3 security/CI PRs overlap this branch's
  credential work.
- **44 open issues** = mostly `backup-verify` spam (PR #713 target) + 5 monthly secret-rotation reminders +
  1 real data bug (#748).
