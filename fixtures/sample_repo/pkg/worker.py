class Worker:
    def run(self, value: int) -> int:
        return self.normalize(value)

    def normalize(self, value: int) -> int:
        return value + 1
