"""5 end-to-end Playwright tests covering core user interactions.

Each test starts from a fresh page; the session-scoped Django server is shared.
Tests run sequentially; later tests depend on earlier-created data (polls, votes).
"""
import re
import uuid

from playwright.sync_api import Page, expect


# ---------------------------------------------------------------------------
# Test 1 — Registration
# User: visit /accounts/register/, fill form, submit; expect redirect to login.
# ---------------------------------------------------------------------------
def test_register_new_user_redirects_to_login(page: Page, django_server: str):
    username = f"bob_{uuid.uuid4().hex[:6]}"
    page.goto(f"{django_server}/accounts/register/")
    page.fill('input[name="username"]', username)
    page.fill('input[name="email"]', f"{username}@example.com")
    page.fill('input[name="password1"]', "P@ssword999")
    page.fill('input[name="password2"]', "P@ssword999")
    page.click('button[type="submit"]')

    expect(page).to_have_url(re.compile(r"/accounts/login/$"))


# ---------------------------------------------------------------------------
# Test 2 — Login + create poll
# User: log in, navigate to add-poll, submit, expect new poll in list.
# ---------------------------------------------------------------------------
def test_login_then_create_poll_lists_it(page: Page, django_server: str, login):
    login()
    poll_text = f"Cats or dogs? {uuid.uuid4().hex[:4]}"

    page.goto(f"{django_server}/polls/add/")
    page.fill('textarea[name="text"]', poll_text)
    page.fill('input[name="choice1"]', "Cats")
    page.fill('input[name="choice2"]', "Dogs")
    page.click('button[type="submit"]')

    page.goto(f"{django_server}/polls/list/")
    expect(page.locator("body")).to_contain_text(poll_text)


# ---------------------------------------------------------------------------
# Test 3 — Vote + result count increments
# User: open a poll, select choice, submit, expect result page with a count.
# ---------------------------------------------------------------------------
def test_vote_submission_shows_result_page(page: Page, django_server: str, login):
    login()
    poll_text = f"Tabs or spaces? {uuid.uuid4().hex[:4]}"
    page.goto(f"{django_server}/polls/add/")
    page.fill('textarea[name="text"]', poll_text)
    page.fill('input[name="choice1"]', "Tabs")
    page.fill('input[name="choice2"]', "Spaces")
    page.click('button[type="submit"]')

    # Navigate to the new poll's detail page via the list
    page.goto(f"{django_server}/polls/list/")
    page.get_by_text(poll_text).first.click()

    page.locator('input[name="choice"]').first.check()
    page.click('input[type="submit"][value="Vote"]')

    # On the result page, the poll text should be present and at least one vote count visible.
    expect(page.locator("body")).to_contain_text(poll_text)
    expect(page.locator("body")).to_contain_text(re.compile(r"\d+\s*Votes?", re.IGNORECASE))


# ---------------------------------------------------------------------------
# Test 4 — Edit poll text
# User: open edit page for a poll they own, change text, save, expect new text in list.
# ---------------------------------------------------------------------------
def test_owner_can_edit_poll_text(page: Page, django_server: str, login):
    login()
    original = f"Original {uuid.uuid4().hex[:4]}"
    edited = f"Edited {uuid.uuid4().hex[:4]}"

    page.goto(f"{django_server}/polls/add/")
    page.fill('textarea[name="text"]', original)
    page.fill('input[name="choice1"]', "A")
    page.fill('input[name="choice2"]', "B")
    page.click('button[type="submit"]')

    # Get this poll's edit href (scope to the <li> containing the right text).
    page.goto(f"{django_server}/polls/list/")
    href = page.locator(
        f'li:has-text("{original}") a[href*="/polls/edit/"]'
    ).first.get_attribute("href")
    page.goto(f"{django_server}{href}")
    page.fill('textarea[name="text"]', edited)
    page.click('button[type="submit"]')

    page.goto(f"{django_server}/polls/list/")
    expect(page.locator("body")).to_contain_text(edited)


# ---------------------------------------------------------------------------
# Test 5 — Edit a choice on an existing poll
# User: on the poll-edit page, follow the edit link next to a choice;
# rename it; expect new text to appear and old text to be gone.
# ---------------------------------------------------------------------------
def test_owner_can_edit_a_choice(page: Page, django_server: str, login):
    login()
    poll_text = f"EditChoice {uuid.uuid4().hex[:4]}"
    page.goto(f"{django_server}/polls/add/")
    page.fill('textarea[name="text"]', poll_text)
    page.fill('input[name="choice1"]', "OldChoice")
    page.fill('input[name="choice2"]', "OtherChoice")
    page.click('button[type="submit"]')

    page.goto(f"{django_server}/polls/list/")
    edit_href = page.locator(
        f'li:has-text("{poll_text}") a[href*="/polls/edit/"]'
    ).first.get_attribute("href")
    page.goto(f"{django_server}{edit_href}")

    # Pick the edit link in the list item that contains "OldChoice".
    choice_edit_href = page.locator(
        'li:has-text("OldChoice") a[href*="/polls/edit/choice/"]'
    ).first.get_attribute("href")
    page.goto(f"{django_server}{choice_edit_href}")
    page.fill('input[name="choice_text"]', "RenamedChoice")
    page.click('button[type="submit"]')

    expect(page.locator("body")).to_contain_text("RenamedChoice")
    expect(page.locator("body")).not_to_contain_text("OldChoice")
