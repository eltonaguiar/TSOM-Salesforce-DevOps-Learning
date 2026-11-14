# Best-match selection

**The third decision shape:** given a set of options and criteria, return the single option that best matches.
Distinct from Yes/No (binary commitment) and from ranking (order all options).

This resolves the decision left **open at 0.517** in `DECISION_RECORD.md`.

---

## The criteria had to be measured first

At 0.517 the decision was unresolvable because the evidence did not separate the candidates — both leading
bundles had zero false assertions. So I measured the axes that would separate them:

| Bundle | Depth | Files | Self-doc | Currency |
|---|---|---|---|---|
| `20261114-020852-salesforcemore` | **0.638** | 12 | 1 | 18 |
| `2026-11-14T023241_salesforceagain-v2` | 0.634 | 10 | 1 | 19 |
| `20261114-020300-salesforceagain-kilo` | 0.616 | 13 | 1 | **165** |
| `2026-11-14T023507_salesforcemore-v2` | 0.615 | **24** | 1 | 23 |
| `2026-11-14T0210Z-salesforceyetagain-v2` | 0.569 | 4 | 0 | 7 |
| `salesforceagain-v4-2026-11-14-0230` | 0.544 | 3 | 0 | 13 |

- **Depth** — mean semantic match to the page's ten core release-engineering concepts
- **Currency** — count of current CLI / API version references (`@salesforce/cli`, `sf project deploy`, API 5x)
- **Self-doc** — does it record its own corrections
- **Files** — granularity

**The trade-off is now visible:** `salesforcemore` has the highest semantic depth (0.638) but currency of 18.
`salesforceagain-kilo` has marginally lower depth (0.616) and **9× the currency** (165).

## Result

| Options | Criteria | Choice | Confidence | Valid? |
|---|---|---|---|---|
| 6 | 1 | — | 0.649 | **no** — returned a criteria key |
| **6** | **2** | **`salesforceagain-kilo`** | **0.922** | yes |
| 3 (top by depth) | 2 | `salesforceagain-kilo` | 0.866 | yes |
| 2 (top by depth) | 2 | `salesforceagain-v2` | 0.707 | yes |

**Best match: `20261114-020300-salesforceagain-kilo` at 0.922.**

It wins on **currency, decisively** — 165 current-CLI references against 18–23 for the others — and that
outweighs a 0.022 depth deficit against `salesforcemore`. That is a defensible outcome for a release-engineering
page: a bundle that is current but marginally less thorough beats one that is thorough and out of date, because
an out-of-date release procedure is worse than a slightly thin one.

The bottom row is consistent with this: when `kilo` is excluded from the option set, the model picks between the
two depth leaders and chooses `salesforceagain-v2` (currency 19) over `salesforcemore` (18) — again favouring
currency at a near-tie on depth.

## The format instability, documented

**One criterion with six options returned a criteria key, not an option.** The choice string came back as
`20261114-020852-salesforcemore__depth` — one of the criteria labels — at 0.649 confidence.

Two criteria with the same six options returned a clean option at 0.922. So the failure is not simply "too many
options"; it is that **criteria keys compete with option names for probability mass**, and when each option
contributes only one key the collision is worst.

Two consequences for use:

1. **Validate the returned choice against the option list.** It can be a criteria key. In the runs above, 1 of 4
   returned invalid. A caller that does not check will silently mis-handle it.
2. **Supply at least two criteria per option** when there are more than ~3 options. One criterion is not enough
   to keep the option names separable from their evidence.

This is the same underlying artefact as `probabilities` containing an `options` key: the API treats criteria keys
as pseudo-options. It is harmless when it does not win, and silently wrong when it does.

## Resolution of the open decision

`DECISION_RECORD.md` had this as the single unresolved item:

> Which bundle should be canonical for `devops-engineer` — **0.517**

**Resolved:** `20261114-020300-salesforceagain-kilo`, at 0.922, on the criterion of currency.

**But note what this does not settle.** The evidence that separates them is currency and depth — both measured.
What it does not measure is *coverage of the specific concepts the page still needs*, which is the axis most
likely to change the answer if the page's actual gaps are concentrated in areas `salesforcemore` covers better.
That remains a cheap follow-up.

## Files

| File | Role |
|---|---|
| `bestmatch_evidence.json` | the measured criteria per bundle |
| `YES_NO_DECISIONS.md` | the binary decision set |
| `DECISION_RECORD.md` | the multi-option decisions, including the one this resolves |