from annotated_case.worker import Worker


def start(value: int) -> int:
    worker: Worker = Worker()
    return worker.run(value)
