"""Spike test: 10 users baseline -> jump to 100 -> cool down to 10. 120 s total.

Run:
  locust -f perf/locustfile_spike.py --headless -H http://127.0.0.1:8765 \
         --csv evidence/q4/spike --html evidence/q4/spike.html
"""
from locust_users import PollUser  # noqa: F401

from locust import LoadTestShape


class SpikeShape(LoadTestShape):
    stages = [
        {"duration": 30, "users": 10, "spawn_rate": 5},
        {"duration": 90, "users": 100, "spawn_rate": 50},
        {"duration": 120, "users": 10, "spawn_rate": 50},
    ]

    def tick(self):
        t = self.get_run_time()
        for s in self.stages:
            if t < s["duration"]:
                return s["users"], s["spawn_rate"]
        return None
