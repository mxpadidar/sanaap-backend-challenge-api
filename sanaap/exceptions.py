class BaseExc(Exception):
    def __init__(self, msg: str, *args) -> None:
        self.detail = msg or self.detail
        super().__init__(self.detail, *args)


class ConflictExc(BaseExc): ...
