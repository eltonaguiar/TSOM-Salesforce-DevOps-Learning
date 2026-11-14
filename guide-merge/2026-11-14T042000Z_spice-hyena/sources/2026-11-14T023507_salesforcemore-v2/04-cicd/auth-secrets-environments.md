# Authentication, secrets, environments, and approvals

**Merge target:** sections 5.1 and 11 of the downstream page. This file is the "how the pipeline proves who is allowed to do what" research.

## 1. Authentication: JWT bearer flow

The standard CI pattern is the OAuth 2.0 JWT bearer flow:

1. Create a Connected App (or External Client App, depending on the org's release).
2. Enable OAuth settings and **Use digital signatures**.
3. Upload the public certificate.
4. Grant the `api` scope (and the scopes the integration needs).
5. Create a dedicated integration user with a least-privilege deploy permission set.
6. Pre-authorize the Connected App for that user (for example, "Admin approved users are pre-authorized" plus a permission set).
7. Generate an RSA key pair. Store the private key in the CI secret store. Upload the certificate to the Connected App.
8. In CI, run `sf org login jwt` with the consumer key, username, private key, and instance URL.

```bash
sf org login jwt \
  --client-id "$SF_CONSUMER_KEY" \
  --jwt-key-file "$RUNNER_TEMP/server.key" \
  --username "$SF_USERNAME" \
  --instance-url "$SF_INSTANCE_URL" \
  --alias target
```

The runner writes the key to a temporary file and deletes it after login. The key is never committed and is never printed.

## 2. The integration user

| Property | Rule |
|---|---|
| Identity | Dedicated, not a human's admin login |
| Permissions | Least privilege: API Enabled plus the deploy permissions the pipeline needs (often Modify All Data for Metadata API deploys; confirm the bank's approved set) |
| Password | Not used for JWT; the certificate is the credential |
| Rotation | The certificate/key pair has an owner and a rotation date |
| Monitoring | The user's API usage and login history are reviewed |
| Scope | One user per environment (or a tightly controlled shared CI identity with environment isolation) |
| Approval | The user cannot approve changes; approval is a human action |

## 3. Secrets

| Secret | Scope | What it is | Rotation |
|---|---|---|---|
| `SF_CONSUMER_KEY` | Repo or environment | Connected App consumer key | When the app is rotated |
| `SF_USERNAME` | Environment | Integration username | When the user changes |
| `SF_INSTANCE_URL` | Environment | `https://login.salesforce.com` or `https://test.salesforce.com` | Rarely |
| `SF_JWT_KEY` | Environment | PEM private key | On a schedule and on suspected exposure |
| `SF_CLIENT_SECRET` | Do not use with JWT | Not needed for the JWT bearer flow | — |

**Rules:**
- Production secrets are environment-scoped, not repository-wide.
- Development/QA secrets do not grant production access.
- Do not echo secrets. Mask them in logs.
- Rotate on a schedule and immediately after any suspected exposure.
- Do not put secrets in a pull request, an issue, a screenshot, or a debug log.

## 4. GitHub Environments and approvals

**Settings → Environments → `prod`:**

| Control | Setting | Why |
|---|---|---|
| Required reviewers | Named release managers | A human approves the production deploy |
| Prevent self-review | Enabled if available | The author is not the approver |
| Deployment branches | Only the release branch or a tag | A feature branch cannot deploy to prod |
| Environment secrets | Prod-only `SF_*` values | The QA runner cannot read prod credentials |
| Wait timer | Optional | Adds a pause after approval for a final check |

The `environment:` key in the workflow is what makes the approval gate real:

```yaml
jobs:
  deploy:
    environment: ${{ inputs.target || 'qa' }}
```

For production, the job pauses before it runs until the required reviewer approves. That is the structural segregation of duties.

## 5. Branch protection

**Settings → Branches → Branch protection rules** for `main` and `release/**`:

- Require a pull request before merging.
- Require at least one approval (two for production-bound branches if the bank requires it).
- Dismiss stale approvals when new commits are pushed.
- Require status checks to pass, including the CI validation job.
- Require conversation resolution.
- Restrict who can push.
- Include administrators, if the bank's policy allows.
- Add `CODEOWNERS` for `force-app/**`, `manifest/**`, and `.github/workflows/**`.

## 6. Segregation of duties

| Action | Who |
|---|---|
| Write the Apex or Flow | Developer |
| Review the diff | A second person, not the author |
| Run the validation | Pipeline / integration user |
| Approve the production deploy | Named release manager, not the author |
| Execute the deploy | Pipeline / integration user |
| Verify the business result | QA or business owner |
| Retain the evidence | Release engineer |

If the same person can author, approve, and deploy, the control is cultural, not structural. The pipeline should make it impossible.

## 7. Common authentication failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `invalid_grant` / `user hasn't approved this consumer` | The Connected App is not pre-authorized for the integration user | Pre-authorize the app or assign the permission set |
| `invalid_client_id` | Wrong consumer key for the environment | Use the environment-scoped secret |
| `invalid_grant` / `expired access/refresh token` | Wrong instance URL or user | Check `SF_INSTANCE_URL` and `SF_USERNAME` |
| `INVALID_SESSION_ID` | The key/cert pair does not match | Re-upload the certificate, rotate the key |
| Login works, deploy fails with permission error | The integration user lacks a deploy permission | Assign the approved deploy permission set |
| Callout works in Dev, fails in CI | Named credential secret/cert missing in the target | Configure per-org secrets and certificates |

## 8. What to merge

**Merge:** the JWT flow, the integration-user table, the secrets table, the environment/approval table, the branch-protection list, and the segregation-of-duties table.

**Compress:** the failure table if the page is long; keep the first four rows.

**Do not merge:** a specific permission-set name, consumer key, org id, or certificate. None is included, and none should be.
