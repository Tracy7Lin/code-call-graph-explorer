from factory_case.factories import make_worker


def start(value: int) -> int:
    worker = make_worker()
    return worker.run(value)
