# Q2 UAT Notes

Suite file: evidence/q2/uat_suite.xlsx

## User stories covered

1. Register a new account.
2. Log in with valid credentials.
3. Reject invalid login credentials.
4. Create a poll with two choices.
5. Search polls by keyword.
6. Sort polls by name, date, or vote count.
7. Vote once on an active poll.
8. Block repeat voting.
9. View poll results.
10. Owner edits poll text or choices.
11. Owner deletes or ends a poll.

## Black-box techniques used

| Technique | Test cases |
|---|---|
| Equivalence Partitioning | valid/invalid registration, valid/invalid login, search match/no-match |
| Boundary Value Analysis | username length, password length, choice text length |
| State Transition | active poll → voted poll → ended poll |
| Decision Table | owner vs non-owner, active vs ended, voted vs not voted |
| Pairwise | sort/search/page combinations |

Manual work left: execute the Excel cases, fill **Actual Result** and **Pass/Fail**, then screenshot the completed sheet.
