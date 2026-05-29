# Q4 Performance Notes

Tool: **Locust**.

Endpoints tested: poll list, poll detail, vote submission, and login.

## Load test

| Setting | Value |
|---|---|
| Script | perf/locustfile_load.py |
| Shape | 50 users, 5/sec spawn, 90 seconds |
| Result | 3,976 requests, 0 failures |
| Throughput | ~44.0 req/sec |
| Response time | avg 11 ms, p95 22 ms, p99 130 ms |
| Report | evidence/q4/load.html |

Interpretation: normal load was healthy. First fix priority is still login cost, because login POST was much slower than poll reads.

## Spike test

| Setting | Value |
|---|---|
| Script | perf/locustfile_spike.py |
| Shape | 10 users → 200 users spike → 10 users |
| Result | 6,104 requests, 57 failures |
| Error rate | 0.93% |
| Throughput | ~50.7 req/sec |
| Response time | avg 27 ms, p95 91 ms, p99 470 ms |
| Report | evidence/q4/spike.html |

Interpretation: the app starts to hurt during the login spike. I would first reduce login pressure in tests, move heavier auth work behind realistic user sessions, and use a production WSGI server instead of Django runserver.
