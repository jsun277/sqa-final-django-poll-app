# Q3 Unit Test Notes

Command:

pytest tests/unit -v --cov --cov-report=term --cov-report=html:evidence/q3/htmlcov

## Unit tests added

| File | Tests |
|---|---|
| `tests/unit/test_models_pure.py` | `Poll.__str__`, `Choice.__str__` truncation |
| `tests/unit/test_forms_pure.py` | valid registration form, short username boundary |
| `tests/unit/test_with_doubles.py` | 4 isolated tests using doubles |

## Test doubles

| Test | Double | Replaces | Why |
|---|---|---|---|
| `test_user_can_vote_returns_false_when_vote_exists_stub` | Stub | user vote query chain | Makes vote history deterministic without creating a real user. |
| `test_get_result_dict_uses_secrets_choice_for_alert_class_mock` | Mock | `secrets.choice` | Removes randomness and checks the call. |
| `test_get_result_dict_zero_votes_returns_zero_percentage_fake` | Fake | choice manager/queryset | Tests percentage logic without database setup. |
| `test_poll_vote_flashes_error_when_user_already_voted_spy` | Spy | `messages.error` | Confirms the error path without depending on rendered messages. |

Coverage summary: overall **50%**, `polls/models.py` **100%**. HTML report: `evidence/q3/htmlcov/index.html`.
