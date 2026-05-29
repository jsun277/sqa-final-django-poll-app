# Q5 UI Automation Notes

Framework: **Playwright for Python + pytest**.

Command: pytest ui_tests -v

Tests in ui_tests/test_e2e.py:

1. Register a new user and verify redirect to login.
2. Log in and create a poll, then verify it appears in the list.
3. Submit a vote and verify the results page shows the selected choice.
4. Edit poll text and verify the updated text appears.
5. Edit a choice and verify the new choice text appears.

Captured run output: evidence/q5/run.txt.
