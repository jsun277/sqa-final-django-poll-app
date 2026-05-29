"""Shared fixtures for unit + integration tests."""
import pytest
from django.contrib.auth.models import User

from polls.models import Poll, Choice


@pytest.fixture
def user(db):
    return User.objects.create_user(username="alice", password="pw12345")


@pytest.fixture
def other_user(db):
    return User.objects.create_user(username="bob", password="pw12345")


@pytest.fixture
def poll(db, user):
    p = Poll.objects.create(owner=user, text="Favorite color?")
    Choice.objects.create(poll=p, choice_text="Red")
    Choice.objects.create(poll=p, choice_text="Blue")
    return p
