# 03 — Work update: Salesforce research deliverables

The existing index (`forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/research_index.md`) marks four
deliverables **Pending**. They map 1:1 to the four Salesforce guides not yet turned into notes. This folder
completes them from the guide sources on the learning repo `main` branch, with the accuracy corrections from
`02_guide_accuracy_review.md` applied.

## Coverage matrix

| Guide | Source (learning repo `main`) | Existing artifact | Status | This bundle |
|---|---|---|---|---|
| Salesforce Crash Course | `docs/salesforce/crash-course.md` (629 lines) | `forreviews/salesforceyetagain-v4/…/crash_course.md` | Complete (paraphrase) | reviewed — 4 LOW findings (F-07…F-10) |
| DevOps & Release Engineering | `docs/salesforce/devops-engineer.md` (554 lines) | none | **New** | `devops_release_engineering.md` |
| Navigation & Breadcrumbs | `docs/salesforce/navigation-breadcrumbs.md` (207 lines) | none | **New** | `navigation_breadcrumbs.md` |
| Labs & Design | `docs/salesforce/labs-design.md` (353 lines) | none | **New** | `labs_design.md` (corrected) |
| User Management & Data | `docs/salesforce/user-management-data.md` (374 lines) | none | **New** | `user_management_data.md` |

## Files

| File | Contents |
|---|---|
| `devops_release_engineering.md` | The 12 training items, environments, branching, CI/CD, tools, conflict clinic, packages, validation, rollback, banking change control, labs, interview drills. |
| `navigation_breadcrumbs.md` | The Setup tree and every breadcrumb path, grouped by admin/developer task. |
| `labs_design.md` | The four labs with corrected commands, plus design considerations and the corrected system-properties table. |
| `user_management_data.md` | Users, profiles/permission sets, roles/sharing, licenses, import/export, integrity, FLS/encryption, duplicate management, data design, troubleshooting. |
| `corrections_to_existing_notes.md` | Factual fixes to the already-published `certifications.md` and gap list for `crash_course.md`. |

## How to fold these in

These are proposed additions for the merge round. They are kept inside this `forreviews_final/` folder so
they do not collide with the concurrent agent working the same review. The merge round should:

1. Copy the four new notes into `forreviews/salesforceyetagain-v4/2026-11-14T02-11-53Z/` (or the successor
   bundle the merge round chooses).
2. Apply `corrections_to_existing_notes.md` to `certifications.md` and `crash_course.md`.
3. Update `research_index.md` so the four Pending rows read Complete.
4. Apply the `labs-design.md` source fixes (F-01, F-02, F-03, F-04, F-05) in the learning repo, since the
   guide is the published artifact learners actually follow.
