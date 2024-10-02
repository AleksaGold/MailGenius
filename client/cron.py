from client.models import Client


def add_client():
    new_client = Client(last_name="Cron", first_name="Crony", email="cron@example.com")
    new_client.save()
    print("Client added:", new_client)
