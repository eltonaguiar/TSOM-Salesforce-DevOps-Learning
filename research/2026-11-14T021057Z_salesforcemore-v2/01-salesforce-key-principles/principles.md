# Salesforce key principles for release engineering

**Merge target:** framing material for the page intro and section 12 (design patterns). Keep each principle short; the value is the release-engineering consequence, not the definition.

## 1. Git is the source of truth; the org is a deploy target

**Principle.** Every metadata change has a commit, a branch, a review, and a tag. Production is a target, not a workspace.

**Release consequence.** If Setup and Git disagree, the pipeline cannot tell which state is intended. Treat the difference as drift: retrieve it, review it, decide which side is correct, and record the decision.

**Anti-pattern.** "I changed it in production, I will copy it to Git later." Later never comes, and the next deploy silently reverts the change.

**Interview line.** "If Setup and Git disagree, that is an incident, not a workflow."

## 2. A deploy is a compile against the target

**Principle.** The Metadata API validates the payload against the target org. It resolves dependencies inside the payload, enforces the target's tests, and fails if the target cannot satisfy a reference.

**Release consequence.** Validate against the org you are about to change. A green deploy to Dev is not evidence for UAT or Prod.

**Anti-pattern.** "It worked in Dev" as a release argument.

**Interview line.** "A deploy is a compile against the target, not a file copy."

## 3. Promote one artifact

**Principle.** Build or validate once, then promote the same commit or package version through the environments. Do not rebuild from a different branch at each stage.

**Release consequence.** The artifact has an id: a commit SHA, a validation job id, a package version `04t...`, and a release tag. The runbook records it.

**Anti-pattern.** Rebuilding the release from a `uat` branch that no longer matches the release branch.

**Interview line.** "One artifact, many targets. The artifact is promoted; the environment is configured."

## 4. Least privilege and segregation of duties

**Principle.** The identity that deploys is not the identity that approves. The integration user has the minimum permissions to deploy; a human approves the production change.

**Release consequence.** The pipeline uses JWT auth with a dedicated integration user. Production has a protected environment with required reviewers. The author is not the approver.

**Anti-pattern.** A shared admin login in a CI secret, or the developer approving their own production deploy.

**Interview line.** "The integration user deploys, a human approves, and they are different identities."

## 5. Environment parity, not environment branches

**Principle.** Environments differ by configuration and data, not by forked code. The same metadata should work in every stage.

**Release consequence.** Put environment-specific values in named credentials, custom metadata, custom settings, or the target's configuration. Do not create a `uat` branch that can never merge.

**Anti-pattern.** `if (org.IsSandbox)` scattered through Apex, or a branch per environment.

**Interview line.** "Configure the target; do not fork the codebase."

## 6. Test against the org you will change

**Principle.** A test proves behaviour in the org where it ran. A Developer sandbox and production are different orgs with different data, features, and limits.

**Release consequence.** The validation that counts is a dry-run against the target. Production requires passing tests and 75% coverage when the payload contains Apex.

**Anti-pattern.** A 75% coverage result in Dev used as the production gate.

**Interview line.** "Validate against the target, not against the branch."

## 7. Bulkify by default

**Principle.** Apex and Flows run on collections, not single records. One SOQL for the collection, one DML for the list, no callouts in a loop.

**Release consequence.** A deploy can be green and the feature can fail at 200 or 10,000 records. Review asks: "What happens on 200 records? What happens on 10,000?"

**Anti-pattern.** SOQL or DML inside a loop.

**Interview line.** "A green unit test is not bulk evidence."

## 8. Make metadata modular

**Principle.** Small, single-purpose metadata merges and deploys better than monoliths. Permission sets per persona, subflows for parallel work, packages for real module boundaries, custom metadata for configuration.

**Release consequence.** Two stories do not collide in one 10,000-line profile or one Flow. The deploy payload is reviewable.

**Anti-pattern.** One `CB_Admin` permission set, one giant Flow, one profile edited by every story.

**Interview line.** "Design so the deploy is boring."

## 9. Design for reversibility

**Principle.** Metadata does not roll back by itself. Reversibility is a forward deploy of the last known-good tag, a previous package version, or a Flow-version activation.

**Release consequence.** Tag every successful production deploy. Keep the previous package version. Write the rollback owner into the runbook. Know that destructive deletes and data scripts are not undone by Git.

**Anti-pattern.** No tag, no previous version, and a verbal "we will figure it out."

**Interview line.** "If you do not have a tag from the last good production deploy, you do not have a rollback."

## 10. Mask before you share

**Principle.** A Full sandbox is a copy of production customer data. It is not safe for broad access until masking has run and access is limited.

**Release consequence.** A refresh is not complete when the copy finishes; it is complete when masking, integration cut-over, and access control are complete. Record who confirmed the mask.

**Anti-pattern.** An unmasked Full sandbox with broad logins; production data pasted into a ticket or a debug log.

**Interview line.** "Refresh is not done until masking and integration cut-over are done."

## 11. Evidence is part of the deploy

**Principle.** A regulated release needs proof: ticket, reviewed diff, approver, validation id, test results, production deploy id, tag, and mask evidence.

**Release consequence.** The pipeline writes the ids somewhere durable. The runbook is filled per release, not reconstructed after an incident.

**Anti-pattern.** "We deployed it and it worked" with no deploy id or approver.

**Interview line.** "The deploy is technical; the audit pack is the job."

## 12. Observability after deploy

**Principle.** A deploy is not done when the API returns success. It is done when the smoke test, the API usage check, and the business check pass.

**Release consequence.** Run a named smoke test, check Setup → Company Information → API Usage, and confirm the user-facing behaviour. Record the result in the runbook.

**Anti-pattern.** Declaring success because the deployment status says "Succeeded" while the Flow version is inactive or the named credential secret is missing.

**Interview line.** "Green deploy is not green feature. I verify activation, assignment, secrets, and a real user."

## How these principles land on the page

- Use principles 1–3 to open the page and justify the pipeline.
- Use principles 4, 11, 12 in the banking change-control section.
- Use principles 5, 8, 10 in the design-patterns and sandbox sections.
- Use principles 6, 7 in the tests/limits sections.
- Use principle 9 in the rollback section.
- Put the one-line interview answers in section 14.
