# 06 — Runbook template, rendered against this repo

The guide's §10 runbook template, filled in with **this repo's real surfaces** rather than Salesforce
placeholders. Two versions: the template as it should be used, and a worked example.

The guide's rule is that the template is filled "for every prod promotion". In this repo a "prod promotion"
is: a change to `TORONTOEVENTS_ANTIGRAVITY/index.html`, the `_next/static/chunks/*` bundle, the FTP-deployed
asset set, or a schema migration.

---

## Template

```
Change ticket:            <ticket id, also in the commit subject>
Release tag:              release-<YYYY-MM-DD>          <- the rollback target
Payload:                  <commit sha, and the file list>
Source branch / commit:   <branch>@<sha>
Validation run / result:  <CI run URL> — pass/fail, test count, coverage %
Prod deploy id / time:    <deploy log id, deploy_*.py output, UTC timestamp>
Approver (not author):    <name>
Post-deploy checks:       <one query, one screen, one test>
Rollback tag:             release-<previous>
Rollback owner:           <name>
How we will know it worked: <single observable>
```

The guide's own note on why each field exists:

> "Keep these, every time: Change ticket id in the commit and the pull request · Diff a second person read
> (not the author) · Validation deploy id and prod deploy id · Test run id and coverage number · Named
> approver, different from the person who wrote the change · Release tag · For a Full sandbox refresh:
> refresh time, mask-complete confirmation, who is allowed to log in."

---

## Field-by-field: what it maps to here

| Template field | This repo's source of truth | Currently tracked? |
|---|---|---|
| Change ticket | Commit subject tags — `[SAM-IMPLEMENTATION-GAP-ANALYSIS-2026-11-13]`, `[KILO-20261113-001]` | **Yes**, by convention |
| Release tag | `git tag release-YYYY-MM-DD` | **No.** Verified: `git tag` returns 3 tags, none a release tag — `backup/homepage-pre-collapse-20261013-212754`, `backup/homepage-pre-fab-fix-20261013-211121`, `refuted/vrp-cloud-minimix-2026-06-05`. There is no rollback target |
| Payload | `git diff --name-only <tag>..<tag>` | **No** |
| Source branch / commit | `git rev-parse HEAD` | **Yes**, in commit |
| Validation run | GitHub Actions run URL | **Yes**, but only for paths matching the `ci-tests.yml` filter |
| Prod deploy id | Output of `deploy_*.py` / `deploy_ftps.py` | **No** |
| Approver | GitHub review | **No** — `reviewDecision` is empty on all 20 open PRs |
| Rollback tag | Previous `release-*` tag | **No** |
| Post-deploy checks | Manual | Ad hoc |

---

## Worked example — a real change from this queue

**PR #749** (resolver true exit time) is a good worked example, because it is a real production-affecting
change that is currently waiting to merge.

```
Change ticket:          batch-close root cause (no ticket id in the PR title; the
                        updates/ record is 2026-10-20-batch-close-rootcause-fix.md)
Release tag:            release-2026-11-14            <- would be created at deploy
Payload:                6 files
                          audit_trail/universal_pick_resolver.py      (+55 / -47)
                          tools/check_batch_closes.py               (new)
                          tools/export_closed_picks_full.py         (new)
                          tools/dry_run_reresolve_zero_price.py     (new)
                          tests/test_batch_close_exit_time.py       (new)
                          updates/2026-10-20-batch-close-rootcause-fix.md (new)
Source branch / commit: buffy/batch-close-rootcause @ 3654630b16f
Validation run:         <CI run URL> — currently INHERITED RED (blocker B1),
                        so there is no valid validation evidence yet
Prod deploy id / time:  <pending>
Approver (not author):  <pending — no review recorded>
Post-deploy checks:     python tools/check_batch_closes.py --payload <live>
                        expect: same-minute clusters disperse, exit_price=0.0 count = 0
Rollback tag:           release-<previous>            <- does not exist
Rollback owner:         <pending>
How we will know it worked: 73 MomentumEMA picks no longer share one resolved_at
```

**This example is the argument for the template.** PR #749 is the best-engineered change in the queue —
it has a root-cause writeup, a regression test, an operational gate, and an explicit "what is not verified"
section. And it still cannot fill in half the runbook, because the repo has no tags, no deploy ids, and no
recorded approval. The missing fields are not the author's fault; they are the release-engineering
infrastructure the guide is describing.

---

## Pre-deploy checklist (derived from the guide's §9 and §11)

Before any prod promotion:

- [ ] A tag exists from the last good prod deploy. *If not, stop — you have no rollback.*
- [ ] The payload compiles/tests green in a validation run against the target, not a different environment.
- [ ] The change ticket id is in the commit subject and the PR.
- [ ] A second person has read the diff. `reviewDecision` is not empty.
- [ ] If the payload contains a destructive change (schema `DROP`, file deletion), it is in a separate,
      explicitly reviewed file — not a side effect of "it was not in the folder".
- [ ] If a data script runs, its reverse script exists and was reviewed before the window.
- [ ] The approver is not the author.

## Post-deploy checklist

- [ ] The single observable in "how we will know it worked" is checked, and the result recorded.
- [ ] Deploy id and UTC time written into the runbook.
- [ ] Release tag created and pushed.
- [ ] The `updates/*.md` record is updated with the deploy id and the observable's result.

## Rollback checklist (guide §10)

- [ ] Metadata/config: validate and deploy the previous tag forward. A `git revert` is not a rollback.
- [ ] Bad Flow with the previous version still in the org: activate the previous version, *then* redeploy
      the last good tag so Git matches the org.
- [ ] Destructive delete already ran: recreate the metadata from Git. Records are gone; data restore is a
      separate ticketed path.
- [ ] Data script already ran: run the reviewed reverse script.

## What this template deliberately does not do

It does not try to be a Salesforce runbook. There are no sandboxes, no change sets, no deployment settings
here. It borrows the **structure** — ticket, diff, validation id, deploy id, approver, tag, observable,
rollback — because that structure is medium-independent, which is the guide's own point:

> "The metadata tool changes. The control does not."