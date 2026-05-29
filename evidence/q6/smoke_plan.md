# Q6 Smoke Test Plan

## Objective

Smoke passes when the build can install, migrate, start, authenticate users, create a poll, vote, show results, and run the fast automated gates without failure.

## Scope

In scope: startup, migrations, registration/login, poll creation, vote submission, result display, owner edit, and automated lint/unit/integration/UI smoke checks.

Out of scope: full browser matrix, long soak tests, deep accessibility review, and exhaustive negative UAT cases.

## Approach

Hybrid. CI runs automated smoke checks; a tester may do one quick manual browser pass before release.

## Smoke cases

| ID | Steps | Expected result |
|---|---|---|
| ST-01 | Install dependencies and run migrations. | Setup succeeds. |
| ST-02 | Start Django server and open home page. | HTTP 200. |
| ST-03 | Register a user. | User is redirected to login. |
| ST-04 | Log in. | Poll list is reachable. |
| ST-05 | Create a poll with two choices. | Poll appears in list. |
| ST-06 | Vote once. | Results page shows the vote. |
| ST-07 | Edit poll text as owner. | Updated text is shown. |
| ST-08 | Run lint/unit/integration/UI smoke commands. | All commands exit 0. |

## Deliverables

Terminal logs, screenshots for manual checks, CI result, and failed-step notes if smoke fails.

## Environment

Local or GitHub Actions runner, Python 3.12, SQLite test database, Playwright Chromium.

## Entry and exit criteria

Schedule: run on each pull request and once before final submission.

Entry: dependencies install, migrations run, and server starts.

Exit: all smoke cases pass. Any failed critical path blocks deeper testing.

## Risks and contingency

If smoke fails, stop the release, keep the failing artifact, fix the blocking issue, and rerun smoke before continuing.
