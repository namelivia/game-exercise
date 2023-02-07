import logging
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Type

from client.engine.persistence.persistence import Persistence
from client.engine.primitives.event_handler import EventHandler

from .commands import ProfileIsSet, SetProfile, UpdateProfiles
from .events import GetProfilesEvent, NewProfileEvent, SetProfileEvent

if TYPE_CHECKING:
    from client.engine.general_state.client_state import ClientState
    from client.engine.primitives.event import Event


logger = logging.getLogger(__name__)


class SetProfileEventHandler(EventHandler):
    def handle(self, event: "SetProfileEvent", client_state: "ClientState") -> None:
        client_state.set_profile(event.key)
        ProfileIsSet(client_state.profile, client_state.queue, event.key).execute()


class NewProfileEventHandler(EventHandler):
    def handle(self, event: "NewProfileEvent", client_state: "ClientState") -> None:
        new_profile_key = client_state.new_profile().key
        SetProfile(client_state.profile, client_state.queue, new_profile_key).execute()


class GetProfilesEventHandler(EventHandler):
    def handle(self, event: "GetProfilesEvent", client_state: "ClientState") -> None:
        # TODO retrieve profiles from disk
        profiles = self._build_profiles_index(Persistence.list())
        UpdateProfiles(client_state.profile, client_state.queue, profiles).execute()

    def _build_profiles_index(self, profiles: Iterable[Any]) -> List[Dict[str, str]]:
        # TODO: Excluding gitkeep should happen in the persistence layer, not here
        return [{"name": profile} for profile in profiles if profile != ".gitkeep"]


handlers_map: Dict[Type["Event"], Type[EventHandler]] = {
    SetProfileEvent: SetProfileEventHandler,
    NewProfileEvent: NewProfileEventHandler,
    GetProfilesEvent: GetProfilesEventHandler,
}
