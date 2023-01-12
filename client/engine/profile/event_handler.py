import logging
from client.engine.primitives.event_handler import EventHandler
from .events import (
    SetProfileEvent,
    NewProfileEvent,
    GetProfilesEvent,
)
from .commands import (
    ProfileIsSet,
    SetProfile,
    UpdateProfiles,
)
from client.engine.persistence.persistence import Persistence

logger = logging.getLogger(__name__)


class SetProfileEventHandler(EventHandler):
    def handle(self, event, client_state):
        client_state.set_profile(event.key)
        ProfileIsSet(client_state.profile, client_state.queue, event.key).execute()


class NewProfileEventHandler(EventHandler):
    def handle(self, event, client_state):
        new_profile_key = client_state.new_profile().key
        SetProfile(client_state.profile, client_state.queue, new_profile_key).execute()


class GetProfilesEventHandler(EventHandler):
    def handle(self, event, client_state):
        # TODO retrieve profiles from disk
        profiles = self._build_profiles_index(Persistence.list())
        UpdateProfiles(client_state.profile, client_state.queue, profiles).execute()

    def _build_profiles_index(self, profiles):
        return [{"name": profile} for profile in profiles if profile != ".gitkeep"]


handlers_map = {
    SetProfileEvent: SetProfileEventHandler,
    NewProfileEvent: NewProfileEventHandler,
    GetProfilesEvent: GetProfilesEventHandler,
}
