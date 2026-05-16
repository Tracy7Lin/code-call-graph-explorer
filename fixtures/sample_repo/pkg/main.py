from pkg.helpers import helper
from pkg.worker import Worker


def start(value: int) -> int:
    worker = Worker()
    return helper(worker.run(value))
