# Built-in
from typing import Optional


class VisionEvent:
    def __init__(self, eventType: str, data: Optional[any] = None) -> None:
        self.eventType = eventType
        self.data = data
