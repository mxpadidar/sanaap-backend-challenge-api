from enum import StrEnum, auto


class DocStatus(StrEnum):
    ACTIVE = auto()
    MODIFIED = auto()
    DELETED = auto()

    @classmethod
    def choices(cls) -> list[tuple[str, str]]:
        return [(status, status.name.capitalize()) for status in cls]
