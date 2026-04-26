from locust import HttpUser, task, between

class ASAAUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.username = "admin"
        self.password = "admin"
        response = self.client.post("/auth/login", data={
            "username": self.username,
            "password": self.password
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None

    @task(3)
    def admin_access(self):
        if self.token:
            self.client.get("/admin/users", headers=self.headers)

    @task(5)
    def analyst_access(self):
        if self.token:
            self.client.get("/analyst/reports", headers=self.headers)

    @task(2)
    def public_data(self):
        if self.token:
            self.client.get("/viewer/public-data", headers=self.headers)
