"""Pure unit tests on model methods — no test doubles needed."""
import pytest

from polls.models import Poll, Choice, Vote


@pytest.mark.django_db
def test_poll_str_returns_text(user):
    p = Poll(owner=user, text="Tabs or spaces?")
    assert str(p) == "Tabs or spaces?"


@pytest.mark.django_db
def test_choice_str_truncates_long_poll_and_choice_text(user):
    poll = Poll.objects.create(owner=user, text="A" * 50)
    choice = Choice.objects.create(poll=poll, choice_text="B" * 50)
    label = str(choice)
    # __str__ truncates poll.text to 25 and choice_text to 25 with " - " between
    assert label == ("A" * 25) + " - " + ("B" * 25)


@pytest.mark.django_db
def test_get_result_dict_calculates_percentage_for_voted_choice(user):
    poll = Poll.objects.create(owner=user, text="Best editor?")
    vim = Choice.objects.create(poll=poll, choice_text="Vim")
    emacs = Choice.objects.create(poll=poll, choice_text="Emacs")
    Vote.objects.create(user=user, poll=poll, choice=vim)

    results = {item["text"]: item["percentage"] for item in poll.get_result_dict()}

    assert results["Vim"] == 100
    assert results["Emacs"] == 0


@pytest.mark.django_db
def test_vote_str_combines_poll_choice_and_username(user):
    poll = Poll.objects.create(owner=user, text="A" * 30)
    choice = Choice.objects.create(poll=poll, choice_text="B" * 30)
    vote = Vote.objects.create(user=user, poll=poll, choice=choice)

    assert str(vote) == ("A" * 15) + " - " + ("B" * 15) + f" - {user.username}"
