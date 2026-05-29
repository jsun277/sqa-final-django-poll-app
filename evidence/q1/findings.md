# Q1 Linter Findings

Linter used: **pylint + pylint-django**. I chose it because it understands Django projects and catches both style issues and real Python logic mistakes.

## Five fixed examples

| # | File | Pylint message | Fix |
|---|---|---|---|
| 1 | polls/views.py:62 | W0125 using-constant-test | Changed if form.is_valid: to if form.is_valid():. This was a real bug because the method object is always truthy. |
| 2 | seeder.py:58 | W0612 unused-variable | Removed c = from Choice(...).save(). |
| 3 | accounts/views.py:15 | R1705 no-else-return | Removed unnecessary else after a return. |
| 4 | polls/models.py:4 | C0411 wrong-import-order | Moved standard-library import secrets above Django imports. |
| 5 | accounts/views.py:6 | W0611 unused-import | Removed unused HttpResponse. |

## Captured output

- Before: evidence/q1/before.txt
- After: evidence/q1/after.txt

Add terminal screenshots of the before/after pylint output in the final document.
