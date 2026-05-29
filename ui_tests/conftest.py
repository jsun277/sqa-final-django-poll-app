"""E2E fixtures: spin up Django dev server against an isolated sqlite DB,
seed a superuser, yield the base URL, kill the server on teardown."""
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from contextlib import closing

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
E2E_DB = REPO_ROOT / "e2e_test.sqlite3"
TEST_USER = "alice"
TEST_PW = "Wonderland123!"


def _free_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _env() -> dict:
    env = os.environ.copy()
    env["DJANGO_DB_PATH"] = str(E2E_DB)
    env["DJANGO_SETTINGS_MODULE"] = "pollme.settings"
    return env


@pytest.fixture(scope="session")
def django_server():
    if E2E_DB.exists():
        E2E_DB.unlink()

    py = sys.executable
    subprocess.run([py, "manage.py", "migrate", "--noinput"],
                   cwd=REPO_ROOT, env=_env(), check=True)
    subprocess.run([py, "manage.py", "shell", "-c",
                    f"from django.contrib.auth.models import User; "
                    f"User.objects.create_superuser('{TEST_USER}', 'a@b.com', '{TEST_PW}')"],
                   cwd=REPO_ROOT, env=_env(), check=True)

    port = _free_port()
    proc = subprocess.Popen(
        [py, "manage.py", "runserver", f"127.0.0.1:{port}", "--noreload"],
        cwd=REPO_ROOT, env=_env(),
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    base_url = f"http://127.0.0.1:{port}"

    # Wait up to 10 s for the server to accept connections.
    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=0.5):
                break
        except OSError:
            time.sleep(0.2)
    else:
        proc.terminate()
        raise RuntimeError(f"Django server failed to start on {base_url}")

    yield base_url

    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
    if E2E_DB.exists():
        E2E_DB.unlink()


@pytest.fixture
def login(page, django_server):
    """Helper: log alice in, leave the browser at the home page."""
    def _do_login():
        page.goto(f"{django_server}/accounts/login/")
        page.fill('input[name="username"]', TEST_USER)
        page.fill('input[name="password"]', TEST_PW)
        page.click('button[type="submit"]')
        page.wait_for_url(f"{django_server}/")
    return _do_login
