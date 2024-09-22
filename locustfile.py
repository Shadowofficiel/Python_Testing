from locust import HttpUser, between, task

class CompetitionUser(HttpUser):
    wait_time = between(1, 3)
    host = "http://127.0.0.1:5000"  # Utilisation de l'URL correcte pour ton application

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})
