# Concept intersection — what appears in both sources

**Question:** which Salesforce concepts appear in both the webpages and the repository.

Distinct from the earlier claim work: this asks whether a concept is *present at all*, not whether the
source is right about it. Presence is a substring question, so keyword matching is adequate here — a page
mentioning "sandbox" covers the concept even if it describes it badly.

**Taxonomy:** 49 concepts, derived from the five pages' own scope (crash-course sections, DevOps training
items, lab topics, user-and-data topics).
**Compared:** live webpages (5 pages, 84,078 chars rendered) vs repo bundles (85 files, 1,661,273 chars).

---

## Result

| Set | Count |
|---|---|
| Appear in **both** | **48** |
| Only in webpages | 0 |
| Only in repo | 1 |
| In neither | 0 |

**The single concept only in the repository: `payload_limits`** — the Metadata API deploy ceilings
(≈39 MB compressed / ≈600 MB uncompressed / 10,000 files).

Verified: the live site contains **zero** occurrences of `39 MB` or `600 MB`. It discusses deploy payloads
13 times — payload compilation, payload dependencies, what happens when a payload references something
missing — but never states a size limit. The concept is present; the *number* is not.

## The concepts in both (48)

```
apex                        soql                        quick_deploy
branching                   soap_api                    rollback
bulkification               soql_limit_100              sandbox_masking
change_control              test_classes                sandbox_types
change_sets                 triggers                    scratch_orgs
ci_cd                       unlocked_packages           security_model
code_coverage               users_profiles_roles        licenses
cpu_time                    validation_rules            data_import
data_model_relationships    visualforce                 duplicate_management
debug_logs                  dml_limit                   design_patterns
deploy_conflicts            field_level_security        flow_automation
devops_tools                git_source_control          governor_limits
heap_size                   heap / cpu / soql limits    integrations
lwc                         managed_packages            metadata_api
named_credentials           navigation_setup_paths      objects_records_fields
permission_sets             process_builder_workflow    record_types
rest_api
```

## What this means

**The webpages are not missing concepts. They are missing depth inside concepts they already have.**

This is the result that ties the whole investigation together, and it is not what a coverage scan would have
predicted:

| Measurement | Result | What it means |
|---|---|---|
| Concept presence | 48 / 49 in both | breadth is complete |
| Depth vs repo (retrieval judge) | repo broader on 10/10 | treatment is thin |
| Contradictions (polarity) | 2, both repo-wrong | the repo's extra depth is not always correct |

So the site's problem is **not** "these topics are absent." Every topic is there. The problem is that each is
treated at ELI5 depth while the release-engineering questions need specifics — which is exactly what the
merged `devops-engineer` page adds (+151 lines), and why it added *values* rather than *topics*.

**Practical consequence for future work:** a coverage-gap scan would have produced almost no actionable list
(1 concept). A depth scan produces the real work. If someone asks "what's missing from the docs", the honest
answer here is "one concept, and a great deal of specificity inside the other 48."

## Two regex false negatives, found and fixed

Worth recording, because both would have produced a wrong answer:

**`dml_limit` initially reported "only in repo."** It is not — the live site says *"10,000 records per DML."*
My pattern was `10,000\s*(rows|DML)`, which requires "10,000 rows" or "10,000 DML" and misses
"10,000 records per DML". Corrected to `10,000\s*(rows|records?|DML)|DML.{0,40}10,000`. The concept is in both.

**`payload_limits` genuinely is repo-only.** Verified by direct search: 0 hits for `39 MB`, 0 for `600 MB`,
while "payload" appears 13 times. This one survived scrutiny.

Both cases argue for the same habit: when a set-difference reports a single item, check that item by hand
before believing it. Here one of two was a regex artefact.

## Files

| File | Role |
|---|---|
| `concepts.py` | presence detection + three-set comparison |
| `taxonomy.json` | 49 concepts with their detection patterns |
| `concepts_final.json` | full per-concept detail (which source has which) |

## Caveat

Presence detection is deliberately shallow. It will report a concept as covered when a source mentions it once
in passing. That is correct for this question — "does the concept appear" — and wrong for any question about
quality. Use `polarity.py` for claims and the retrieval judge for depth.