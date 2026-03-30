from datetime import datetime

from ddd import Clock


class StubClock(Clock):
    def __init__(self, current_time: datetime) -> None:
        self.__current_time = current_time

    def now(self) -> datetime:
        return self.__current_time