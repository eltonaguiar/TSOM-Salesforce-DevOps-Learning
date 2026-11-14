# Feedback

Written 2026-11-14T03:12Z from worktree `chill-egg`, after reading `origin/main` of both repos and the five live Salesforce pages.

## On the review corpus

The corpus did the job it was asked to do, then kept doing it. Nine bundles and two open PRs describe one requisition and one page. The later bundles (`023507` salesforcemore-v2, `023241` salesforceagain-v2, `023312` salesforcemore-v3) are the ones with primary-source citations. The earlier captures and the v4 long file are superseded.

Best single bundle if a fact is missing from the live page: `forreviews/2026-11-14T023507_salesforcemore-v2/`. Use it for the deploy ceiling, the one-at-a-time queue, the fifth test level, and the vendor-name corrections. Do not use its `07-merge/content-gaps.md` as a merge checklist. That file was written against an earlier page. Sections 3.8 through 3.13 are already published.

Best bundle for a vendor menu, if someone insists on a click-path offline: `forreviews/20261114-023241-salesforceagain-v2/03-devops-tools-ui-walkthroughs.md`, then the kilo bundle if that file is thin. Do not promote either onto the public page without a fresh vendor-doc check. The `023507` cross-bundle note already says the menus disagree if both are pasted.

`[Verify]` tags in the v3 bundle are the right habit. A wrong button name is worse than a gap. Keep that rule.

## On the published track

The DevOps page is the strongest of the five. It already sounds like the role: Git as source of truth, sandbox types, hotfix cut from `main`, validate then quick deploy, permission sets over profiles, mask a Full copy, author is not the approver. Research that repeats those sections is noise.

The crash course is the right ELI5 front door and the wrong place to leave uncorrected limit rows. The DevOps page tells the reader to trust that governor section before signing off an Apex story. The scheduled-job row and the mass-email row are not safe to trust.

The labs page imported a ServiceNow habit. `org.wideSharing.default` and `setup.locked` are not Salesforce settings. A reader who searches Setup for those keys will think they failed. That is the highest-priority fix in the track, ahead of any new DevOps chapter.

The breadcrumbs page and the users/data page agree with the DevOps conflict clinic. Leave them.

## On process

- Close DevOps-learning PRs #1 and #2, or retitle them as “already on main.” Merging them creates a second copy under `research/`.
- Do not commit this `forreviews_final/` folder onto the local branch `forreviews-split/salesforcemore-v2-2026-11-14T023507Z`. That branch is 7 commits behind `origin/main`.
- Do not treat `findtorontoevents` worktrees `salesforceagain` and `salesforceyetagain` as inputs. Wrong repo.
- One more agent writing another full limits chapter will not improve the page. The open work is the correction list in `03-corrections.md`.

## What I did not verify this pass

- The exact bytes in the Metadata API `deploy()` ceiling. Cited via the `023507` bundle, not re-fetched.
- Whether `RunRelevantTests` is still Beta on API 66. Confirm with CLI `--help` on the edit date.
- The quick-deploy window length. Confirm on Salesforce Help before writing a number.
- Each Trailhead URL in the crash course. Not clicked.
- Scotiabank requisition 276046 still being open. The pages and the bundles both use it. The job posting was not re-fetched.
