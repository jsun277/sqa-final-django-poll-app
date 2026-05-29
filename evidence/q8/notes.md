# Q8 Code Smells

No code was changed for this question.

| Smell | Location | Why it matters | Proposed improvement |
|---|---|---|---|
| Long Method | accounts/views.py:31-66 | create_user handles form validation, duplicate checks, messages, user creation, and redirects in one block. | Move duplicate checks into UserRegistrationForm.clean(). |
| Duplicated Code | polls/views.py:91-102 and 122-132 | Poll and choice edit views repeat the same POST/form/save/message/redirect pattern. | Extract a small helper for successful form saves. |
| Magic Number | polls/views.py:28 and 46 | Page sizes 6 and 7 are hard-coded with no clear reason. | Replace them with named constants. |

Code excerpts to include in the final document:

- accounts/views.py:31-66 shows the long create_user block.
- polls/views.py:91-102 and 122-132 show repeated form handling.
- polls/views.py:28 and 46 show Paginator(..., 6) and Paginator(..., 7).
