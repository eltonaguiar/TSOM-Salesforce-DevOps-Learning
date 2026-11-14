# Decision record — what the comparison actually concludes

**One SubQ call. 870 input tokens, 0 output tokens. Six decisions, each carrying its measured evidence as
criteria.**

This is the output the whole comparison exists to produce. The analysis files measure; this file decides.

| Decision | Choice | Confidence |
|---|---|---|
| Port the merged pages to the live site | **port the merge** | 0.949 |
| Canonical bundle for `devops-engineer` | *unresolved* | **0.517** |
| Add the Metadata API payload ceilings | **add them** | 0.929 |
| Add the five concepts absent from the site | **add them** | 0.950 |
| Delete the four flat duplicate files | **delete them** | 0.954 |
| Delete the four redundant research branches | **delete them** | 0.964 |

Mean confidence **0.877**.

---

## The five that commit

### Port the merge (0.949)

Evidence supplied: `live_false_assertions: 4`, `merged_false_assertions: 0`, `live_missing_39MB: true`,
`merged_adds_lines: 151`, `live_stale_setup_path: "Setup > Apex Jobs"`.

Re-verified at the full context budget: the merged pages now read **8/8 correct denials, 0 false assertions**
(confidence 0.866–0.961), against 4 false assertions for the live site and 5 for the repo.

The live pages carry four false assertions the merged pages do not, and lack a concept they add. This is the
one decision with unambiguous support.

### Add the payload ceilings (0.929)

Evidence: `site_occurrences_39MB: 0`, `site_occurrences_600MB: 0`, `site_payload_mentions: 13`,
`repo_depth: 0.694`, `site_depth: 0.294`, `verified_against: "meta-deploy.html"`.

The largest measured depth gap of the ten concepts (0.400), and the site discusses deploy payloads 13 times
without ever stating a size. Verified against the primary source.

### Add the five absent concepts (0.950)

Evidence: `absent_from_site: 5`, `absent_from_repo: 0`, `missing_from_both: [heroku, tableau_crm]`,
`role: "commercial-banking release engineering"`.

The five (`mfa`, `source_tracking`, `big_objects`, `mulesoft`, `einstein`) are absent from the site and present
in the repo. The two missing from both are left out deliberately — they are not core to metadata release
engineering.

### Delete the four flat duplicates (0.954)

Evidence: `exact_duplicate_groups: 3`, `near_duplicate_pairs: 4`, `semantic_pairs_ge_060: 1`,
`all_four_are: "salesforceyetagain-v2 folder vs flat twin"`.

Four files, two copies each, one pattern. The semantic check (max 0.675 across 3,570 pairs) confirms these are
the only real duplicates in the corpus.

### Delete the redundant branches (0.964)

Evidence: `branches_ahead: 4`, `unique_content_on_branches: 0`,
`verified_by: "git diff --stat origin/main origin/<branch>"`.

All four are behind `main` with no unique content.

---

## The one that does not resolve

### Which bundle should be canonical for `devops-engineer` — **0.517**

| Candidate | False assertions | Files | Self-documentation |
|---|---|---|---|
| `20261114-020300-salesforceagain-kilo` | 0 | 13 | has a cross-bundle delta file |
| `2026-11-14T023507_salesforcemore-v2` | 24 files | 24 | documents its own corrections |
| the rest | 3 | — | — |

**Both leading candidates score identically on the axis the model was given: zero false assertions.** The
evidence does not separate them, and the model said so at 0.517 — a coin flip.

That is the gate working as designed. Below ~0.6 the measurements do not decide, so the correct action is to
measure on a different axis rather than let the model guess.

**What would separate them** — none of which the current evidence captures:

- **Coverage of the specific concepts the page needs** (the two bundles differ: `salesforcemore-v2` is stronger
  on limits, `salesforceagain-kilo` on structure and JD mapping)
- **Currency** — which is closer to the current CLI and API versions
- **Maintenance** — which is likelier to be updated

Those are three cheap measurements. Until they are taken, the honest state of this decision is *open*, and the
right move is to merge from both rather than crown one.

**Note:** this decision is the one most likely to move once re-run at the full context budget. The two
candidates were separated on a 1.1K-char excerpt; the budget fix already changed two other results materially.

---

## What this demonstrates

The comparison did not end in more analysis. It ended in **six committed decisions and one correctly-flagged
gap**, produced in a single call with no output tokens, where the same evidence always yields the same answer.

The value of the SubQ-native framing is that the decision is **reproducible and auditable**: the evidence is in
the file, the choice follows from it, and the confidence says whether the evidence was sufficient.

A chat model asked "what should we do about these docs?" would have produced a confident paragraph covering all
six, including the one where the evidence is a coin flip. That is the failure this replaces.

## Files

| File | Role |
|---|---|
| `SUBQ_NATIVE_APPROACH.md` | why the framing is decision-first, with the criteria-evidence test |
| `decision_record.json` | the six questions, their evidence, and SubQ's answers |
| `COMPLETENESS_VS_ACCURACY.md` | the accuracy evidence behind "port the merge" |
| `SEMANTIC_VS_LEXICAL.md` | the depth evidence behind the payload and concept decisions |
| `DUPLICATES_AND_OVERLAP.md` | the evidence behind the two delete decisions |