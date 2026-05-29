"""Shared user class for Q4 load and spike tests."""
import random

from locust import HttpUser, task, between

USERNAME = "alice"
PASSWORD = "Wonderland123!"


class PollUser(HttpUser):
    wait_time = between(0.5, 2.0)

    def on_start(self):
        self.client.get("/accounts/login/")
        csrf = self.client.cookies.get("csrftoken", "")
        self.client.post(
            "/accounts/login/",
            data={"username": USERNAME, "password": PASSWORD,
                  "csrfmiddlewaretoken": csrf},
            headers={"Referer": f"{self.host}/accounts/login/"},
        )
        list_resp = self.client.get("/polls/list/")
        ids = []
        for token in list_resp.text.split('href="/polls/')[1:]:
            head = token.split("/")[0]
            if head.isdigit():
                ids.append(int(head))
        self.poll_ids = list(set(ids)) or [1, 2, 3, 4, 5, 6]

    @task(5)
    def list_polls(self):
        self.client.get("/polls/list/", name="/polls/list/")

    @task(3)
    def poll_detail(self):
        pid = random.choice(self.poll_ids)
        self.client.get(f"/polls/{pid}/", name="/polls/[id]/")

    @task(1)
    def vote_attempt(self):
        pid = random.choice(self.poll_ids)
        self.client.get(f"/polls/{pid}/")
        csrf = self.client.cookies.get("csrftoken", "")
        self.client.post(
            f"/polls/{pid}/vote/",
            data={"choice": "1", "csrfmiddlewaretoken": csrf},
            headers={"Referer": f"{self.host}/polls/{pid}/"},
            name="/polls/[id]/vote/",
        )
