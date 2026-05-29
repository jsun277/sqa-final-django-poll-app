"""Seed a small dataset for the perf DB: superuser 'alice' + 6 polls."""
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollme.settings")

import django  # noqa: E402
django.setup()

from django.contrib.auth.models import User  # noqa: E402
from polls.models import Poll, Choice  # noqa: E402

USERNAME = "alice"
PASSWORD = "Wonderland123!"

if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, "alice@example.com", PASSWORD)
    print(f"Created superuser {USERNAME}")
else:
    print(f"Superuser {USERNAME} already exists")

alice = User.objects.get(username=USERNAME)
for i in range(6):
    text = f"Perf poll #{i + 1}: which option?"
    poll, created = Poll.objects.get_or_create(owner=alice, text=text)
    if created:
        Choice.objects.create(poll=poll, choice_text=f"Option A {i}")
        Choice.objects.create(poll=poll, choice_text=f"Option B {i}")
print(f"Polls in DB: {Poll.objects.count()}")
