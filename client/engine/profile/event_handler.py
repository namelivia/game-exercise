import logging
from client.engine.primitives.event_handler import EventHandler
from .events import (
    SetProfileEvent,
    NewProfileEvent,
)
from .commands import (
    ProfileIsSet,
    SetProfile,
)

logger = logging.getLogger(__name__)


class SetProfileEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.set_profile(event.key)
        ProfileIsSet(client_state.profile, client_state.queue, event.key).execute()


class NewProfileEventHandler(EventHandler):
    def handle(self, event, client_state):
        new_profile_key = client_state.new_profile().key
        SetProfile(client_state.profile, client_state.queue, new_profile_key).execute()


handlers_map = {
    SetProfileEvent: SetProfileEventHandler,
    NewProfileEvent: NewProfileEventHandler,
}
