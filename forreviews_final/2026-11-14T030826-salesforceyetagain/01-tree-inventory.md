# 01 — Inventory of `forreviews/` (main)

Sizes from the GitHub contents API. "Verdict" is about merge value, not quality.

## Bundles (directories)

| # | Bundle | Contents | Size | Verdict |
|---|---|---|---|---|
| B1 | `20261114-020300-salesforceagain-kilo/` | `00-plan`, `00-research-bundle-convention`, `01-jd-crossreference` (17K), `02-limits-and-constraints` (27K), `03-devops-tools-ui` (39K), `04-github-actions-salesforce-cicd` (35K), `05-jd-term-deep-dive` (44K), `06-certifications-curriculum` (15K), `07-system-properties-setup-paths` (20K), `08-cross-bundle-delta`, `sources` (27K), `00-consolidated-review-copy` (**263K**) | ~530K | **PRIMARY.** Best-structured DevOps set. `00-consolidated-review-copy` is a concatenation — index only, never merge as prose |
| B2 | `20261114-023241-salesforceagain-v2/` | limits/governors (33K), metadata dependencies (23K), tools UI (22K), CI/CD (24K), JD term-by-term (32K), certs (17K), INDEX, PLAN, README, sources | ~175K | **SECONDARY.** Same topics as B1 with different framing; useful as a cross-check, not additive |
| B3 | `20261114-020852-salesforcemore/` | `PLAN`, `SALESFORCE_DEVOPS_DEEP_DIVE` (35K), `SALESFORCE_LIMITS_DEEP_DIVE` (18K), `certification-research/`, `salesforce-principles/`, `source-capture/`, `merge-against-pages/MAPPING_MATRIX.md` | ~55K | **HIGH VALUE.** Owns the 12-principle spine and the only per-page mapping matrix. Its `MAPPING_MATRIX` is per-bundle only — this folder supersedes it at tree level |
| B4 | `salesforceagain-v4-2026-11-14-0230/` | `comprehensive-devops-research` (28K), `research-plan`, `README` | ~31K | **PARTIAL DUPLICATE** of B1/B2 with a planning frame. Keep the README's framing only |
| B5 | `2026-11-14T0210Z-salesforceyetagain-v2/` | mirrors the four flat T0210Z files | small | **SUPERSEDED** by flat files of the same stamp |
| B6 | `2026-11-14T023312_salesforcemore-v3/` | not enumerated | — | **UNVERIFIED** — merge agent must list before touching |
| B7 | `2026-11-14T023507_salesforcemore-v2/` | mirrors `2026-11-14T023507_salesforcemore-v2.md` | — | **DUPLICATE** of the flat 200K file |

## Flat files

| File | Size | Verdict |
|---|---|---|
| `2026-11-14T0210Z-…-README.md` | 1.3K | Superseded by this folder's README |
| `2026-11-14T0210Z-…-00_planning-salesforce-principles.md` | 4.6K | **9 anchors** — subset of B3's 12 principles. Keep as the short version |
| `2026-11-14T0210Z-…-01_certifications-curriculum.md` | 6.2K | **Canonical cert summary** (short). B1/B2 `06` are longer variants |
| `2026-11-14T0210Z-…-02_crash-course.md` | 45K | **Canonical crash-course mirror.** Covers all five pages incl. Labs 1–4 and user/data. Value = corrections, not re-merge |
| `2026-11-14T021036_salesforceyetagain-v3.md` | 1.2K | Planning note only |
| `2026-11-14T023241_salesforceagain-v2.md` | 175K | Concatenation of B2 → index only |
| `2026-11-14T023507_salesforcemore-v2.md` | 200K | Concatenation incl. B3 → index only |
| `…-v3_devops-gearset-ui-deep-dive.md` | 18K | **Best Gearset UI detail**; fold into B1 `03` |
| `…-v3_devops-github-cicd-pipeline.md` | 17K | Duplicate of B1 `04`; use for cross-check |
| `…-v3_devops-governor-limits-deep-dive.md` | 21K | Duplicate of B1 `02` |
| `…-v3_devops-metadata-dependencies-deep-dive.md` | 20K | Duplicate of B1 `02` |

## Duplication counts (the merge problem in numbers)

| Topic | Copies | Canonical choice |
|---|---|---|
| Planning principles | 3 (9-anchor flat, B3 12-principle, v4 plan) | **B3 12-principle** |
| Certifications | 4 | **flat 01** + B1 `06` detail |
| Governor/limits | 4 | **B2 `01` (33K)** |
| Metadata dependencies | 3 | **B2 `02`** |
| DevOps tools UI | 3 | **B1 `03` + v3 Gearset** |
| CI/CD | 3 | **B1 `04`** |
| JD term-by-term | 2 | **B1 `05`** |
| Setup paths | 2 | **B1 `07`** |
| Crash course | 2 (flat 02, inside 175K/200K) | **flat 02** |
