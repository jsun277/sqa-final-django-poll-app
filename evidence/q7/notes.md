# Q7 Integration Test Notes

Command: pytest tests/integration -v

| Test | Components integrated | Failure mode protected |
|---|---|---|
| test_vote_view_db.py | URL routing, authenticated client, vote view, ORM, SQLite test DB | Vote POST could redirect but fail to create a Vote row or increment the selected choice. |
| test_detail_view_template.py | URL routing, detail view, ORM query, template rendering | Detail page could return 200 but fail to render the choices needed for voting. |

Add a screenshot showing both tests passing.
