"""Pure unit tests on form validation — no test doubles needed."""
from accounts.forms import UserRegistrationForm


def _payload(**overrides):
    base = {
        "username": "validuser",
        "email": "a@b.com",
        "password1": "secret123",
        "password2": "secret123",
    }
    base.update(overrides)
    return base


def test_registration_form_accepts_valid_data():
    form = UserRegistrationForm(data=_payload())
    assert form.is_valid()


def test_registration_form_rejects_short_username_bva():
    # username min_length=5; 4 chars is the just-invalid boundary
    form = UserRegistrationForm(data=_payload(username="abcd"))
    assert not form.is_valid()
    assert "username" in form.errors
