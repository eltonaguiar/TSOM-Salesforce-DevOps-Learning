# Contributing — Research Folder Convention

This repo collects research from **multiple agents and worktrees**. Follow this convention so runs stay unique, reviewable, and mergeable.

---

## 1. Folder naming (required)

Every run lives in its own folder:

```
research/<YYYYMMDD>T<HHMMSS>Z-<worktree-name>/
```

- Timestamp is **UTC**, ISO-8601 basic format, e.g. `20261114T021017Z`.
- `<worktree-name>` is the git worktree/branch slug, e.g. `salesforceagain-v2`.
- Generate it in one command:

```bash
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
DIR="research/${STAMP}-$(basename "$PWD")"
mkdir -p "$DIR"
```

**Why:** uniqueness across agents, chronological ordering, and traceability back to the worktree that produced it.

---

## 2. Required files

| File | Required | Purpose |
|---|---|---|
| `README.md` | Yes | Run manifest: agent, date, scope, confidence, merge destinations, known gaps |
| `PLAN.md` | Yes | Structured approach + the principles the research follows |
| `01-…md`, `02-…md`, … | Yes | The research, numbered in reading order |
| `sources.md` | Yes | Every URL, what it supported, access caveats (403/JS-only, etc.) |

Optional: `diagrams/`, `assets/`, `labs/`.

---

## 3. Content rules

1. **Primary source first.** Quote the requisition or the official doc; do not paraphrase into vagueness.
2. **Label confidence.** Use `[Canonical]`, `[Verify]`, `[Behaviour]` for limits and version-sensitive claims.
3. **Failure-first.** Every concept should state the common failure and the first diagnostic step.
4. **Actionable.** Prefer a Setup path, a CLI command, or a tool location over abstract advice.
5. **Regulated lens.** Name the control/evidence produced (ticket, reviewer, deploy ID, tag, mask confirmation).
6. **No duplication.** Link to the published crash course/breadcrumbs instead of repeating them.
7. **No secrets.** Never include org IDs, tokens, private keys, customer data, or real endpoints.
8. **No invented numbers.** If you cannot verify a limit, say so and link the authoritative page.

---

## 4. Git workflow

- Work on a **branch** (e.g. `research/<worktree>-<stamp>`), not directly on `main`.
- Commit **only files you created** in your run folder (plus any root index edits you were asked to make).
- One commit per logical unit, with a message that names the run folder.
- Open a **pull request**; the merge round reviews and integrates.
- Never force-push, never rewrite history, never delete another run.

```bash
git checkout -b research/salesforceagain-v2-20261114
git add research/20261114T021017Z-salesforceagain-v2 README.md CONTRIBUTING.md
git commit -m "research(salesforceagain-v2): limits, dependencies, tools, CI/CD, JD decoder"
git push -u origin research/salesforceagain-v2-20261114
```

---

## 5. Review checklist for the merge round

- [ ] Folder name matches the convention.
- [ ] `README.md`, `PLAN.md`, `sources.md` present.
- [ ] Every JD line is covered (see `05-jd-term-by-term.md` cross-reference).
- [ ] Time-sensitive claims flagged and re-verified.
- [ ] No secrets or customer data.
- [ ] Anchors on the published page preserved.
- [ ] Duplication with the crash course avoided.
- [ ] Diagrams added where text alone is weak (dependency graph, pipeline).

---

## 6. Status labels

Use one of:

- **Round 1 — research complete**
- **Round 1 — partial (see known gaps)**
- **Round 2 — merged**
- **Superseded by `<folder>`**
