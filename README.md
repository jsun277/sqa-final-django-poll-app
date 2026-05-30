# SQA Final Project - Django Poll App

QA work for the open-source Django Poll App:
https://github.com/devmahmud/Django-Poll-App

## Setup

python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
python manage.py migrate

## Run checks

# Q1
pylint polls accounts pollme seeder.py

# Q3
pytest tests/unit -v --cov --cov-report=term --cov-report=html:evidence/q3/htmlcov

# Q7
pytest tests/integration -v

# Q5
playwright install chromium
pytest ui_tests -v

## Performance tests

DJANGO_DB_PATH=$PWD/perf_test.sqlite3 python manage.py migrate --noinput
DJANGO_DB_PATH=$PWD/perf_test.sqlite3 python perf/seed_perf.py
DJANGO_DB_PATH=$PWD/perf_test.sqlite3 python manage.py runserver 127.0.0.1:8765 --noreload


In a second terminal:

cd perf
locust -f locustfile_load.py --headless -H http://127.0.0.1:8765 --html ../evidence/q4/load.html
locust -f locustfile_spike.py --headless -H http://127.0.0.1:8765 --html ../evidence/q4/spike.html

## Evidence map

| Question | Main files |
|---|---|
| Q1 | .pylintrc, evidence/q1/findings.md |
| Q2 | evidence/q2/uat_suite.xlsx, evidence/q2/notes.md |
| Q3 | tests/unit/, evidence/q3/htmlcov/, evidence/q3/notes.md |
| Q4 | perf/, evidence/q4/load.html, evidence/q4/spike.html |
| Q5 | ui_tests/, evidence/q5/run.txt |
| Q6 | evidence/q6/smoke_plan.md |
| Q7 | tests/integration/, evidence/q7/notes.md |
| Q8 | evidence/q8/notes.md |
| Q9 | .github/workflows/ci.yml, evidence/q9/notes.md |

# Generative AI Disclosure

Generative AI was used only to support application-code work and project organization. I used Claude Code and Codex to help identify small application-code fixes, scaffold configuration files, and organize run commands.

The submitted tests, UAT cases, test plans, performance interpretation, smoke test plan, code-smell analysis, screenshots, and final written answers were reviewed, edited, executed, and validated by me.

AI tools used:

| Tool | Used for |
|---|---|
| Claude Code | Helped inspect the Django Poll App source code and identify small application-code fixes for Q1 lint issues. |
| Codex | Helped check consistency between evidence files and written results, prepare concise run instructions, and summarize/write this disclosure. |

No external blog posts, Stack Overflow answers, or peer-written material were copied into the submission.

The original upstream README is preserved in README_upstream.md.
