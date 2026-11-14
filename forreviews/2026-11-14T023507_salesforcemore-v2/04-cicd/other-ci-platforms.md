# Azure DevOps and GitLab equivalents

**Merge target:** section 5 of the downstream page, as a "same stages, different syntax" subsection. The posting names GitHub Actions, Azure DevOps, and GitLab, so the page should show that the design is vendor-neutral.

## 1. Concept mapping

| Concept | GitHub Actions | Azure DevOps | GitLab CI/CD |
|---|---|---|---|
| Pipeline definition | Workflow YAML | Pipeline YAML | `.gitlab-ci.yml` |
| Trigger | `on:` | `trigger:` / PR policy | `rules:` / `only:` |
| Job runner | `runs-on` | `pool` | `tags` / runners |
| Secret store | Actions secrets / environment secrets | Variable groups / Key Vault | CI/CD variables (protected, masked) |
| Approval gate | Environment required reviewers | Environment approvals and checks | Protected environment + manual job |
| Branch gate | Branch protection + required checks | Branch policy + build validation | Protected branch + MR approvals |
| Artifact | `actions/upload-artifact` | Pipeline artifact | `artifacts:` |
| Status on PR | Checks API | Branch policy status | MR pipeline status |
| Concurrency | `concurrency:` | `lockBehavior` / demands | `resource_group` |

## 2. Azure DevOps sketch

```yaml
trigger:
  branches:
    include: [release/*]

pr:
  branches:
    include: [release/*]

variables:
  - group: salesforce-ci

stages:
  - stage: Validate
    jobs:
      - job: ValidatePR
        pool: { vmImage: ubuntu-latest }
        steps:
          - checkout: self
            fetchDepth: 0
          - task: NodeTool@0
            inputs: { versionSpec: '20.x' }
          - script: npm install --global @salesforce/cli
          - script: |
              printf '%s' "$(SF_JWT_KEY)" > "$(Agent.TempDirectory)/server.key"
              sf org login jwt --client-id "$(SF_CONSUMER_KEY)" \
                --jwt-key-file "$(Agent.TempDirectory)/server.key" \
                --username "$(SF_USERNAME)" \
                --instance-url "$(SF_INSTANCE_URL)" --alias ci
              rm -f "$(Agent.TempDirectory)/server.key"
          - script: |
              npx --yes sfdx-git-delta --to HEAD --from "origin/$(System.PullRequest.TargetBranch)" \
                --output delta --generate-delta --source force-app
          - script: |
              sf project deploy start --manifest delta/package/package.xml \
                --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml \
                --dry-run --test-level RunLocalTests --target-org ci --wait 60

  - stage: DeployProd
    dependsOn: Validate
    condition: succeeded()
    jobs:
      - deployment: DeployProd
        environment: 'salesforce-prod'   # configure approvals/checks
        pool: { vmImage: ubuntu-latest }
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Auth, quick deploy the validated job, smoke test, tag"
```

Azure DevOps approvals live on the **environment** (Pipelines → Environments → Approvals and checks). Branch policies provide the PR validation gate.

## 3. GitLab sketch

```yaml
stages: [validate, deploy]

variables:
  SF_CLI: "@salesforce/cli"

validate:
  stage: validate
  image: node:20
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script:
    - npm install --global $SF_CLI
    - printf '%s' "$SF_JWT_KEY" > server.key
    - sf org login jwt --client-id "$SF_CONSUMER_KEY" --jwt-key-file server.key
        --username "$SF_USERNAME" --instance-url "$SF_INSTANCE_URL" --alias ci
    - rm -f server.key
    - npx --yes sfdx-git-delta --to HEAD --from "origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME"
        --output delta --generate-delta --source force-app
    - sf project deploy start --manifest delta/package/package.xml
        --post-destructive-changes delta/destructiveChanges/destructiveChanges.xml
        --dry-run --test-level RunLocalTests --target-org ci --wait 60
  artifacts:
    when: always
    paths: [delta/, validation.json]

deploy_prod:
  stage: deploy
  image: node:20
  environment:
    name: salesforce-prod
    action: prepare
  rules:
    - if: $CI_COMMIT_BRANCH =~ /^release\//
      when: manual
  script:
    - echo "Auth, quick deploy the validated job, smoke test, tag"
```

GitLab approvals live on **Settings → CI/CD → Protected environments** and merge request approval rules. A manual job is not an approval by itself; pair it with a protected environment.

## 4. Design invariants

These do not change with the vendor:

1. PR validation targets a disposable CI sandbox.
2. The release validation targets the org you will change.
3. Production requires a human approver who is not the author.
4. Secrets are environment-scoped and never in the repo.
5. The artifact is promoted; it is not rebuilt per environment.
6. A tag is created after a successful production deploy.
7. The pipeline serializes deploys per org.

## 5. Interview line

"I do not care which CI product we use. The stages are the same: validate against the target, gate production on a human approval, promote the same artifact, and tag the release. Only the YAML header, the secret store, and the approval UI change."

## 6. What to merge

**Merge:** the concept mapping and the design invariants.

**Optional:** one short Azure DevOps or GitLab sketch, depending on the page's audience. Do not include all three full pipelines; the page will become a CI manual.
