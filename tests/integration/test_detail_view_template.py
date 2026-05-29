"""Integration test: poll_detail view <-> template.

Components integrated: the view layer (context dict construction) and the
Django template engine (poll_detail.html rendering).

Failure mode protected against: a regression where the view stops passing the
poll's choices into the template context, or the template stops iterating
choice_set — visible only when the rendered HTML is inspected, invisible to a
view test that only checks status_code.
"""
import pytest


@pytest.mark.integration
@pytest.mark.django_db
def test_detail_page_renders_all_choice_texts(client, poll):
    response = client.get(f"/polls/{poll.id}/")

    assert response.status_code == 200
    html = response.content.decode()
    for choice in poll.choice_set.all():
        assert choice.choice_text in html
    assert poll.text in html
