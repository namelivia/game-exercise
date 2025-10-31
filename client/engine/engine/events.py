from typing import TYPE_CHECKING

from engine.primitives.event import Event

if TYPE_CHECKING:
    from uuid import UUID


class QuitGameEvent(Event):
    pass
