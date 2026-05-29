"""Load test: 50 users sustained for ~60 s (after 30 s ramp).

Run:
  locust -f perf/locustfile_load.py --headless -H http://127.0.0.1:8765 \
         --csv evidence/q4/load --html evidence/q4/load.html
"""
from locust_users import PollUser  # noqa: F401  (registered with Locust)

from locust import LoadTestShape


class LoadShape(LoadTestShape):
    stages = [
        {"duration": 30, "users": 50, "spawn_rate": 5},
        {"duration": 90, "users": 50, "spawn_rate": 5},
    ]

    def tick(self):
        t = self.get_run_time()
        for s in self.stages:
            if t < s["duration"]:
                return s["users"], s["spawn_rate"]
        return None
