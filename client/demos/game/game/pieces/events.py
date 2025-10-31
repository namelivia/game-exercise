from typing import TYPE_CHECKING

from engine.primitives.event import Event

if TYPE_CHECKING:
    from uuid import UUID

"""
Events contain an operation and the data needed in order to perform
the operation. Will be put on a queue and when handler will execute
that operation.
"""


class PlaceASymbolRequestEvent(Event):
    def __init__(self, event_id: "UUID", position: int):
        super().__init__()
        self.event_id = event_id
        self.position = position
