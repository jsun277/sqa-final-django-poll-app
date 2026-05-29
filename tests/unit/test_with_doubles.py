"""Unit tests using test doubles. 4 tests, 4 different double types.

Each test documents:
  - Double type (Meszaros taxonomy)
  - Real dependency replaced
  - Why the replacement is useful
  - How the double isolates the unit under test
"""
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from polls.models import Poll


# ---------------------------------------------------------------------------
# Test 1 — STUB
# ---------------------------------------------------------------------------
# Type:        Stub (canned responses, no behavior verification).
# Replaces:    Django User + reverse relation `user.vote_set` (ORM queryset).
# Why useful:  Real call hits the DB through 3 chained ORM methods. Stub keeps
#              the test in-process, deterministic, no fixtures, no migrations.
# Isolation:   `Poll.user_can_vote` reads ONLY `user.vote_set.all().filter().exists()`.
#              Stubbing that chain isolates the branching logic from the ORM.
def test_user_can_vote_returns_false_when_vote_exists_stub():
    queryset_stub = SimpleNamespace(exists=lambda: True)
    vote_set_stub = SimpleNamespace(
        all=lambda: SimpleNamespace(filter=lambda poll: queryset_stub)
    )
    user_stub = SimpleNamespace(vote_set=vote_set_stub)

    poll = Poll(text="X")
    assert poll.user_can_vote(user_stub) is False


def test_user_can_vote_returns_true_when_no_vote_exists_stub():
    queryset_stub = SimpleNamespace(exists=lambda: False)
    vote_set_stub = SimpleNamespace(
        all=lambda: SimpleNamespace(filter=lambda poll: queryset_stub)
    )
    user_stub = SimpleNamespace(vote_set=vote_set_stub)

    poll = Poll(text="X")
    assert poll.user_can_vote(user_stub) is True


# ---------------------------------------------------------------------------
# Test 2 — MOCK
# ---------------------------------------------------------------------------
# Type:        Mock (verifies the call happened with the right arguments).
# Replaces:    `secrets.choice` (stdlib RNG used to pick alert CSS class).
# Why useful:  RNG output is nondeterministic — without a mock we can only
#              assert "value is in the list", not "function was called correctly".
#              Mock pins both the return value AND verifies the argument list.
# Isolation:   The unit (get_result_dict) is decoupled from the real RNG; we
#              prove it delegates color choice to `secrets.choice` rather than
#              rolling its own (which would be a duplication smell).
@patch("polls.models.secrets.choice", return_value="primary")
def test_get_result_dict_uses_secrets_choice_for_alert_class_mock(mock_choice, db, poll):
    poll.get_result_dict()
    mock_choice.assert_called_with(
        ["primary", "secondary", "success", "danger", "dark", "warning", "info"]
    )


# ---------------------------------------------------------------------------
# Test 3 — FAKE
# ---------------------------------------------------------------------------
# Type:        Fake (working substitute, simpler than real, not prod-ready).
# Replaces:    Poll + Choice ORM relations (choice_set / vote_set managers).
# Why useful:  We want to test the percentage math in `get_result_dict` for the
#              zero-vote edge case. Hitting the DB would force fixture setup
#              and migrations; a fake captures the contract (.choice_set.all(),
#              choice.get_vote_count) in 10 lines and runs in microseconds.
# Isolation:   Replaces the entire persistence layer; the test exercises only
#              the arithmetic branch (no votes → percentage = 0).
class _FakeChoice:
    def __init__(self, text):
        self.choice_text = text

    @property
    def get_vote_count(self):
        return 0


class _FakeChoiceSet:
    def __init__(self, choices):
        self._choices = choices

    def all(self):
        return self._choices


class _FakePoll:
    """Duck-typed Poll: implements only the surface get_result_dict reads."""
    def __init__(self, choices):
        self.choice_set = _FakeChoiceSet(choices)

    @property
    def get_vote_count(self):
        return 0


def test_get_result_dict_zero_votes_returns_zero_percentage_fake(monkeypatch):
    monkeypatch.setattr("polls.models.secrets.choice", lambda lst: "primary")
    fake_poll = _FakePoll([_FakeChoice("A"), _FakeChoice("B")])

    # Invoke the real method against the fake (unbound — duck typing)
    result = Poll.get_result_dict(fake_poll)
    assert [r["percentage"] for r in result] == [0, 0]
    assert [r["text"] for r in result] == ["A", "B"]


# ---------------------------------------------------------------------------
# Test 4 — SPY
# ---------------------------------------------------------------------------
# Type:        Spy (wraps real implementation, records calls).
# Replaces:    `django.contrib.messages.error` — a side-effecting call.
# Why useful:  We want to confirm the duplicate-vote branch in `poll_vote`
#              flashes an error message. Spying preserves real Django messaging
#              behavior while letting us assert call count/args.
# Isolation:   Spy wraps (does not replace) the call, so the view still runs
#              end-to-end but we get observability on the message side effect.
@patch("polls.views.messages.error", wraps=lambda *a, **kw: None)
def test_poll_vote_flashes_error_when_user_already_voted_spy(spy_error, client, user, poll):
    from polls.models import Vote
    Vote.objects.create(user=user, poll=poll, choice=poll.choice_set.first())
    client.force_login(user)

    client.post(f"/polls/{poll.id}/vote/", {"choice": poll.choice_set.first().id})

    assert spy_error.called
    args, _ = spy_error.call_args
    assert "already voted" in args[1].lower()
