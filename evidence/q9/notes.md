# Q9 CI/CD Notes

Workflow file: .github/workflows/ci.yml

Runs on:

- push to main
- pull request

Pipeline gates:

1. Install Python and dependencies.
2. Run Django migrations/checks.
3. Run pylint.
4. Run unit tests with coverage.
5. Run integration tests.
6. Run a short Locust performance smoke test.
7. Run Playwright UI tests.

Screenshots still needed:

- One successful GitHub Actions run.
- One intentionally failing run, such as an unused import that fails pylint.
