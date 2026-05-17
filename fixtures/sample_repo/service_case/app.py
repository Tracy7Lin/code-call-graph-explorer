import service_case.services.orders as order_services
from service_case.clients.api import ApiClient


def run_job(payload):
    client = ApiClient()
    service = order_services.OrderService(client)
    return service.process(payload)
