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
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from client.engine.client_state import ClientState


logger = logging.getLogger(__name__)


class SetProfileEventHandler(EventHandler):
    def handle(self, event: "SetProfileEvent", client_state: "ClientState"):
        client_state.set_profile(event.key)
        ProfileIsSet(client_state.profile, client_state.queue, event.key).execute()


class NewProfileEventHandler(EventHandler):
    def handle(self, event: "NewProfileEvent", client_state: "ClientState"):
        new_profile_key = client_state.new_profile().key
        SetProfile(client_state.profile, client_state.queue, new_profile_key).execute()


class GetProfilesEventHandler(EventHandler):
    def handle(self, event: "GetProfilesEvent", client_state: "ClientState"):
        # TODO retrieve profiles from disk
        profiles = self._build_profiles_index(Persistence.list())
        UpdateProfiles(client_state.profile, client_state.queue, profiles).execute()

    def _build_profiles_index(self, profiles):
        # TODO: Excluding gitkeep should happen in the persistence layer, not here
        return [{"name": profile} for profile in profiles if profile != ".gitkeep"]


handlers_map = {
    SetProfileEvent: SetProfileEventHandler,
    NewProfileEvent: NewProfileEventHandler,
    GetProfilesEvent: GetProfilesEventHandler,
}
