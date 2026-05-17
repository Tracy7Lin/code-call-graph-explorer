from service_case.utils.formatting import normalize_payload


class OrderService:
    def __init__(self, client):
        self.client = client

    def process(self, payload):
        cleaned = normalize_payload(payload)
        return self.client.send(cleaned)
