"""Integration test: poll_vote view <-> database.

Components integrated: HTTP request handling (Django view + URL routing) and
the ORM persistence layer (Vote model writing to SQLite).

Failure mode protected against: a regression where the view returns 200 / a
success template but silently fails to persist the Vote — for example, after
refactoring the form-handling branch or breaking the FK relation. Mocking the
DB would hide this entire class of bug, which is the point of an integration
test.
"""
import pytest

from polls.models import Vote


@pytest.mark.integration
@pytest.mark.django_db
def test_post_vote_creates_row_and_increments_choice_count(client, user, poll):
    chosen = poll.choice_set.first()
    initial_count = chosen.get_vote_count
    client.force_login(user)

    response = client.post(f"/polls/{poll.id}/vote/", {"choice": chosen.id})

    assert response.status_code == 200
    assert Vote.objects.filter(user=user, poll=poll, choice=chosen).exists()
    chosen.refresh_from_db()
    assert chosen.get_vote_count == initial_count + 1
